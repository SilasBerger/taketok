from src.db._transactions.transaction import Transaction
from src.db.database import Database
from src.util.helpers import tuples_equal


class VideoMetadataTransaction(Transaction):

    def __init__(self, db: Database):
        super().__init__(db)

    def save_author_if_not_exists(self, author_id: str):
        self._db.execute("insert or ignore into author (id) values (?)", (author_id,))

    def update_author_info_if_changed(self, author_id, unique_id, nickname, signature, current_date_iso):
        latest_entry_for_author = self._db.fetch_one("""
                select unique_id, nickname, signature
                from author_info
                where author_id = ?
                order by date desc limit 1
            """, (author_id,))

        possible_update = (unique_id, nickname, signature)
        if tuples_equal(latest_entry_for_author, possible_update):
            return

        self._db.execute("""
                insert into author_info (author_id, unique_id, nickname, signature, date) 
                values (?, ?, ?, ?, ?)
            """, (author_id, unique_id, nickname, signature, current_date_iso))

    def save_video_metadata(self, video_metadata):
        self._db.execute("""
                insert into video (id, resolved_url, download_date_iso, description, upload_date_iso, author_id) 
                values (:id, :resolved_url, :download_date_iso, :description, :upload_date_iso, :author_id)
            """, video_metadata)

    def _insert_hashtag_if_not_exists(self, hashtag):
        self._db.execute("insert or ignore into hashtag (name) values (?)", (hashtag,))
        return self._db.fetch_one("select id from hashtag where name = ?", (hashtag,))[0]

    def _insert_video_hashtag_associations(self, video_id, hashtag_ids):
        for hashtag_id in hashtag_ids:
            insert_statement = "insert or ignore into video_hashtag_rel (video_id, hashtag_id) values (?, ?)"
            self._db.execute(insert_statement, (video_id, hashtag_id))

    def insert_hashtags(self, video_id, hashtags):
        hashtag_ids = [self._insert_hashtag_if_not_exists(hashtag) for hashtag in hashtags]
        self._insert_video_hashtag_associations(video_id, hashtag_ids)

    def _insert_challenge_if_not_exists(self, challenge):
        return

    def insert_challenges(self, video_id, challenges):
        for challenge in challenges:
            challenge_id = challenge["id"]
            self._db.execute("insert or ignore into challenge (id, title, description) values (?, ?, ?)", (
                challenge_id,
                challenge["title"],
                challenge["description"]
            ))
            self._db.execute("insert or ignore into video_challenge_rel (video_id, challenge_id) values (?, ?)", (
                video_id,
                challenge_id
            ))

    def mark_source_url_as_processed(self, source_url):
        self._db.execute("update source_urls set processed = true where url = ?", (source_url,))
