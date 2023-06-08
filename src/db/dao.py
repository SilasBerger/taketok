import os
import sqlite3

from src.util.helpers import tuples_equal


class Dao:

    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection
        self._cursor = self._connection.cursor()

    @staticmethod
    def create(sqlite_file: os.path):
        # TODO: Ensure file exists (create blank if needed)
        conn = sqlite3.connect(str(sqlite_file))
        # TODO: Ensure correct schema.
        return Dao(conn)

    def get_links_without_download_status(self):
        self._cursor.execute("select source_url from video where download_status is null")
        return [line[0] for line in self._cursor.fetchall()]

    def _set_download_status(self, source_url: str, status: str):
        self._cursor.execute("update video set download_status = ? where source_url = ?", (status, source_url))
        self._connection.commit()

    def mark_source_url_as_failed(self, source_url):
        self._set_download_status(source_url, "FAILED")

    def save_author_if_not_exists(self, author_id):
        self._cursor.execute("select ROWID from author where author_id = ?", (author_id,))
        existing_author = self._cursor.fetchone()

        if existing_author:
            return existing_author[0]

        self._cursor.execute("insert into author (author_id) values (?)", (author_id,))
        self._connection.commit()
        return self._cursor.lastrowid

    # TODO: Accept dict instead of individual params
    def update_author_info_if_changed(self, author_rowid, id, unique_id, nickname, signature, current_date_iso):
        self._cursor.execute("""
            select id, unique_id, nickname, signature
            from author_data
            where ROWID = ?
            order by date desc limit 1
        """, (author_rowid,))
        latest_entry = self._cursor.fetchone()

        new_data = (id, unique_id, nickname, signature)
        if tuples_equal(latest_entry, new_data):
            return

        self._cursor.execute("""
            insert into author_data (author_rowid, id, unique_id, nickname, signature, date) 
            values (?, ?, ?, ?, ?, ?) 
        """, (author_rowid, id, unique_id, nickname, signature, current_date_iso))
        self._connection.commit()

    def save_video_metadata(self, source_url, resolved_url, download_status, video_id, current_date_iso, description, upload_date_iso,
                            author_rowid):
        self._cursor.execute("select ROWID from video where source_url = ?", (source_url,))
        rowid = self._cursor.fetchone()[0]

        self._cursor.execute("""
            update video
            set
                resolved_url = ?,
                download_status = ?,
                video_id = ?,
                download_date_iso = ?,
                description = ?,
                upload_date_iso = ?,
                author_rowid = ?
            where ROWID = ?
        """, (
            resolved_url,
            download_status,
            video_id,
            current_date_iso,
            description,
            upload_date_iso,
            author_rowid,
            rowid
        ))
        self._connection.commit()

        return rowid

    def _insert_hashtag_if_not_exists(self, hashtag):
        self._cursor.execute("select ROWID from hashtag where hashtag = ?", (hashtag,))
        result = self._cursor.fetchone()
        if result is not None:
            return result[0]

        self._cursor.execute("insert into hashtag (hashtag) values (?)", (hashtag,))
        self._connection.commit()
        return self._cursor.lastrowid

    def _insert_video_hashtag_associations(self, video_rowid, hashtag_rowids):
        self._cursor.execute("select hashtag_rowid from video_hashtag_rel where video_rowid = ?", (video_rowid,))
        associated_hashtag_rowids = [row[0] for row in self._cursor.fetchall()]
        hashtag_rowids_to_associate = [rowid for rowid in hashtag_rowids if rowid not in associated_hashtag_rowids]

        for hashtag_rowid in hashtag_rowids_to_associate:
            self._cursor.execute("""
                insert into video_hashtag_rel (video_rowid, hashtag_rowid)
                values (?, ?)
            """, (video_rowid, hashtag_rowid))
            self._connection.commit()

    def insert_hashtags(self, video_rowid, hashtags):
        hashtag_rowids = [self._insert_hashtag_if_not_exists(hashtag) for hashtag in hashtags]
        self._insert_video_hashtag_associations(video_rowid, hashtag_rowids)

    def _insert_challenge_if_not_exists(self, challenge):
        self._cursor.execute("select ROWID from challenge where id = ?", (challenge["id"],))
        result = self._cursor.fetchone()
        if result is not None:
            return result[0]

        self._cursor.execute("insert into challenge (id, title, description) values (?, ?, ?)", (
            challenge["id"],
            challenge["title"],
            challenge["description"]
        ))
        self._connection.commit()
        return self._cursor.lastrowid

    def insert_challenges(self, video_rowid, challenges):
        for challenge in challenges:
            challenge_rowid = self._insert_challenge_if_not_exists(challenge)
            self._cursor.execute("""
                insert into video_challenge_rel (video_rowid, challenge_rowid)
                values (?, ?) 
            """, (video_rowid, challenge_rowid))
            self._connection.commit()

    def insert_transcript(self, video_rowid, transcript):
        self._cursor.execute("update video set transcript = ? where ROWID = ?", (transcript, video_rowid))
        self._connection.commit()
