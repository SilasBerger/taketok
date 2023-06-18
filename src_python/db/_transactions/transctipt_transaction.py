from src_python.db._transactions.transaction import Transaction
from src_python.db.database import Database


class TranscriptTransaction(Transaction):

    def __init__(self, db: Database):
        super().__init__(db)

    def insert_transcript(self, transcript, video_id):
        self._db.execute("update video set transcript = ? where id = ?", (transcript, video_id))
        return self
