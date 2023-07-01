import datetime
import traceback

from src_python.db.database import Database
from src_python.db.transactions import video_metadata_transaction, download_state_transaction, transcript_transaction
from src_python.db.views import fetch_non_processed_source_urls
from src_python.tiktok.tiktok import resolve_video_id, tiktok_download, resolve_video_url_if_shortened
from src_python.transcribe.transcribe import VideoTranscriber
from src_python.util.config import Config


class VideoImporter:

    def __init__(self, db: Database, config: Config):
        self._db = db
        self._video_out_dir = config.video_output_dir
        self._transcriber = VideoTranscriber(config)

    def _save_video(self, video_bytes, video_id):
        filename = self._video_out_dir / ('%s.mp4' % video_id)
        with open(filename, 'wb') as video_outfile:
            video_outfile.write(video_bytes)

    @staticmethod
    def _extract_hashtags(info):
        return [hashtag['hashtagName'] for hashtag in info['textExtra']] if 'textExtra' in info else []

    @staticmethod
    def _extract_challenges(info):
        return [{
            "id": challenge["id"],
            "title": challenge["title"],
            "description": challenge["desc"],
        } for challenge in info["challenges"]] if "challenges" in info else []

    def _import_transcript_if_exists(self, video_id):
        try:
            transcript = self._transcriber.transcribe(video_id)
            if transcript is not None:
                transcript_transaction(self._db).insert_transcript(transcript, video_id).commit()
        except Exception as e:
            print("Failed to transcribe video with ID %s:" % video_id)
            print(e)

    def _import_video_metadata(self, source_url: str, transaction):
        current_date_iso = datetime.datetime.now().isoformat()  # TODO: Use UTC date
        resolved_url = resolve_video_url_if_shortened(source_url)
        video_id = resolve_video_id(resolved_url)

        tiktok_result = tiktok_download(video_id)
        self._save_video(tiktok_result.bytes, video_id)
        info = tiktok_result.info['itemInfo']['itemStruct']
        author = info['author']
        author_id = author['id']

        transaction.save_author_if_not_exists(author['id'])
        transaction.update_author_info_if_changed(
            author_id,
            author['uniqueId'],
            author['nickname'],
            author['signature'],
            current_date_iso,
        )

        transaction.save_video_metadata({
            "id": video_id,
            "resolved_url": resolved_url,
            "download_date_iso": current_date_iso,
            "description": info['desc'],
            "upload_date_iso": datetime.datetime.utcfromtimestamp(info['createTime']).isoformat(),  # TODO: Factor out.
            "author_id": author_id
        })

        transaction.insert_hashtags(video_id, self._extract_hashtags(info))
        transaction.insert_challenges(video_id, self._extract_challenges(info))
        transaction.mark_source_url_as_processed(source_url)

        return video_id

    def _import_video(self, source_url: str):
        metadata_transaction = video_metadata_transaction(self._db)
        try:
            video_id = self._import_video_metadata(source_url, metadata_transaction)
            metadata_transaction.commit()
        except Exception:
            metadata_transaction.rollback()
            download_state_transaction(self._db).mark_source_as_failed(source_url, traceback.format_exc()).commit()
            print('Failed to import video with source URL %s' % source_url)
            return

        self._import_transcript_if_exists(video_id)

    def _import_all(self, new_links: [str]):
        for index, source_url in enumerate(new_links):
            print('\nImporting video %s/%s (URL: %s)' % (index + 1, len(new_links), source_url))
            self._import_video(source_url)

    def import_all_new_links(self):
        new_links = fetch_non_processed_source_urls(self._db)
        self._import_all(new_links)
