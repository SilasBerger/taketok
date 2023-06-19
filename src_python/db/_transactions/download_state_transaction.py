from src_python.db._transactions.transaction import Transaction
from src_python.db.database import Database


class DownloadStateTransaction(Transaction):

    def __init__(self, db: Database):
        super().__init__(db)

    def mark_source_as_failed(self, source_url: str, failure_reason: str):
        self._db.execute("""
            update source_urls
            set processed = true, failure_reason = ?
            where url = ?
        """, (failure_reason, source_url))
        return self
