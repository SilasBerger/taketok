import requests

from src_python.db.database import Database
from src_python.db.transactions import video_metadata_transaction, download_state_transaction, transcript_transaction
from src_python.db.views import fetch_non_processed_source_urls
from src_python.util.config import Config


class VideoImporter:

    def __init__(self, db: Database, config: Config):
        self._db = db
        self._video_out_dir = config.video_output_dir
        self._whisper_model = config.whisper_model

    def _import_video_metadata(self, source_url: str, transaction):
        response = requests.post('http://127.0.0.1:5000/import-from-source-url', json={
            "source_url": source_url,
            "video_output_dir": str(self._video_out_dir)
        })

        if response.status_code != 200:
            return None

        response_body = response.json()
        video = response_body['video']
        video_id = video['id']
        author = response_body['author']
        author_id = author['id']

        transaction.save_author_if_not_exists(author_id)
        transaction.update_author_info_if_changed(
            author_id,
            author['unique_id'],
            author['nickname'],
            author['signature'],
            author['date'],
        )

        transaction.save_video_metadata({
            "id": video_id,
            "resolved_url": video['resolved_url'],
            "download_date_iso": video['download_date_iso'],
            "description": video['description'],
            "upload_date_iso": video['upload_date_iso'],
            "author_id": author_id
        })

        transaction.insert_hashtags(video_id, video['hashtags'])
        transaction.insert_challenges(video_id, video['challenges'])
        transaction.mark_source_url_as_processed(source_url)

        return video_id

    def _import_transcript(self, video_id):
        response = requests.post('http://127.0.0.1:5000/transcribe', json={
            "video_id": video_id,
            "video_output_dir": str(self._video_out_dir),
            "whisper_model": self._whisper_model
        })

        if response.status_code != 200:
            return

        transcript = response.json()['transcript']
        transcript_transaction(self._db).insert_transcript(video_id, transcript).commit()

    def _import_video(self, source_url: str):
        metadata_transaction = video_metadata_transaction(self._db)
        video_id = self._import_video_metadata(source_url, metadata_transaction)

        if video_id is None:
            metadata_transaction.rollback()
            download_state_transaction(self._db).mark_source_as_failed(source_url).commit()
            print('Failed to import video with source URL %s' % source_url)
            return

        metadata_transaction.commit()
        self._import_transcript(video_id)

    def _import_all(self, new_links: [str]):
        for index, source_url in enumerate(new_links):
            print('\nImporting video %s/%s (URL: %s)' % (index + 1, len(new_links), source_url))
            self._import_video(source_url)

    def import_all_new_links(self):
        new_links = fetch_non_processed_source_urls(self._db)
        self._import_all(new_links)
