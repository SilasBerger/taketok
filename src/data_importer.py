import datetime

from src.db.dao import Dao
from src.tiktok.tiktok import resolve_video_id, tiktok_download, resolve_video_url_if_shortened
from src.transcribe.transcribe import VideoTranscriber
from src.util.config import Config


class DataImporter:

    def __init__(self, dao: Dao, config: Config):
        self._dao = dao
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
        } for challenge in info["challenges"]]

    def _import_video(self, source_url: str):
        current_date_iso = datetime.datetime.now().isoformat()
        resolved_url = resolve_video_url_if_shortened(source_url)
        video_id = resolve_video_id(resolved_url)

        tiktok_result = tiktok_download(video_id)
        # self._save_video(tiktok_result.bytes, video_id) TODO: Activate
        info = tiktok_result.info['itemInfo']['itemStruct']
        author = info['author']

        author_rowid = self._dao.save_author_if_not_exists(author['id'])
        self._dao.update_author_info_if_changed(
            author_rowid,
            author['id'],
            author['uniqueId'],
            author['nickname'],
            author['signature'],
            current_date_iso,
        )

        video_rowid = self._dao.save_video_metadata(source_url, {
            "resolved_url": resolved_url,
            "download_status": 'OK',
            "video_id": video_id,
            "download_date_iso": current_date_iso,
            "description": info['desc'],
            "upload_date_iso": datetime.datetime.utcfromtimestamp(info['createTime']).isoformat(),
            "author_rowid": author_rowid
        })

        self._dao.insert_hashtags(video_rowid, self._extract_hashtags(info))
        self._dao.insert_challenges(video_rowid, self._extract_challenges(info))

        # TODO: Factor out into separate step, don't mark as failed.
        transcript = self._transcriber.transcribe(video_id)
        self._dao.insert_transcript(video_rowid, transcript)

    def _import_all(self, new_links: [str]):
        for index, source_url in enumerate(new_links):
            print('Importing link %s (URL: %s)' % (index + 1, source_url))
            try:
                self._import_video(source_url)
            except Exception as e:
                self._dao.mark_source_url_as_failed(source_url)
                print('Failed to import video with source URL %s:' % source_url)
                print(e)

    def import_all_new_links(self):
        new_links = self._dao.get_links_without_download_status()
        self._import_all(new_links)
