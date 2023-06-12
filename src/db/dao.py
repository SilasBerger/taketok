from src.db.database import Database
from src.util.helpers import tuples_equal


class Dao:

    # TODO: Cleanup. Group everything related to the single-transaction metadata import, for clarity.

    def __init__(self, db: Database):
        self._db = db

    def get_links_without_download_status(self):
        return [line[0] for line in self._db.fetch_all("select source_url from video where download_status is null")]

    def _set_download_status(self, source_url: str, status: str):
        self._db.write_transactional("update video set download_status = ? where source_url = ?", (status, source_url))

    def mark_source_url_as_failed(self, source_url):
        self._set_download_status(source_url, "FAILED")

    def save_author_if_not_exists(self, author_id):
        existing_author = self._db.fetch_one("select ROWID from author where author_id = ?", (author_id,))
        if existing_author:
            return existing_author[0]
        return self._db.write_transactional("insert into author (author_id) values (?)", (author_id,))

    def update_author_info_if_changed(self, author_rowid, id, unique_id, nickname, signature, current_date_iso):
        latest_entry = self._db.fetch_one("""
            select id, unique_id, nickname, signature
            from author_data
            where ROWID = ?
            order by date desc limit 1
        """, (author_rowid,))

        new_data = (id, unique_id, nickname, signature)
        if tuples_equal(latest_entry, new_data):
            return

        self._db.write_transactional("""
            insert into author_data (author_rowid, id, unique_id, nickname, signature, date) 
            values (?, ?, ?, ?, ?, ?) 
        """, (author_rowid, id, unique_id, nickname, signature, current_date_iso))

    def save_video_metadata(self, source_url, video_metadata):
        rowid = self._db.fetch_one("select ROWID from video where source_url = ?", (source_url,))[0]
        self._db.write_transactional("""
            update video
            set
                resolved_url = :resolved_url,
                download_status = :download_status,
                video_id = :video_id,
                download_date_iso = :download_date_iso,
                description = :description,
                upload_date_iso = :upload_date_iso,
                author_rowid = :author_rowid
            where ROWID = :rowid
        """, {**video_metadata, "rowid": rowid})

        return rowid

    def _insert_hashtag_if_not_exists(self, hashtag):
        result = self._db.fetch_one("select ROWID from hashtag where hashtag = ?", (hashtag,))
        if result is not None:
            return result[0]
        return self._db.write_transactional("insert into hashtag (hashtag) values (?)", (hashtag,))

    def _insert_video_hashtag_associations(self, video_rowid, hashtag_rowids):
        select_statement = "select hashtag_rowid from video_hashtag_rel where video_rowid = ?"
        associated_hashtag_rowids = [row[0] for row in self._db.fetch_all(select_statement, (video_rowid,))]
        hashtag_rowids_to_associate = [rowid for rowid in hashtag_rowids if rowid not in associated_hashtag_rowids]

        for hashtag_rowid in hashtag_rowids_to_associate:
            insert_statement = "insert into video_hashtag_rel (video_rowid, hashtag_rowid) values (?, ?)"
            self._db.write_transactional(insert_statement, (video_rowid, hashtag_rowid))

    def insert_hashtags(self, video_rowid, hashtags):
        hashtag_rowids = [self._insert_hashtag_if_not_exists(hashtag) for hashtag in hashtags]
        self._insert_video_hashtag_associations(video_rowid, hashtag_rowids)

    def _insert_challenge_if_not_exists(self, challenge):
        result = self._db.fetch_one("select ROWID from challenge where id = ?", (challenge["id"],))
        if result is not None:
            return result[0]

        return self._db.write_transactional("insert into challenge (id, title, description) values (?, ?, ?)", (
            challenge["id"],
            challenge["title"],
            challenge["description"]
        ))

    def insert_challenges(self, video_rowid, challenges):
        for challenge in challenges:
            challenge_rowid = self._insert_challenge_if_not_exists(challenge)
            self._db.write_transactional("""
                insert into video_challenge_rel (video_rowid, challenge_rowid)
                values (?, ?) 
            """, (video_rowid, challenge_rowid))

    def insert_transcript(self, video_rowid, transcript):
        self._db.write_and_commit("update video set transcript = ? where ROWID = ?", (transcript, video_rowid))

    def commit(self):
        self._db.commit()

    def rollback(self):
        self._db.rollback()
