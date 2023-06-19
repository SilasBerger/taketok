from src_python.db._transactions.download_state_transaction import DownloadStateTransaction
from src_python.db._transactions.transaction import Transaction
from src_python.db._transactions.transctipt_transaction import TranscriptTransaction
from src_python.db._transactions.video_metadata_transaction import VideoMetadataTransaction
from src_python.db.database import Database


class TransactionHandler:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TransactionHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._current_transaction = None

    def set_transaction(self, transaction: Transaction):
        if self._current_transaction is not None:
            raise "Invalid state: cannot set transaction while another transaction is pending"
        self._current_transaction = transaction

    def commit(self):
        if self._current_transaction is None:
            raise "No transaction pending"
        self._current_transaction.commit()
        self._current_transaction = None

    def rollback(self):
        if self._current_transaction is None:
            raise "No transaction pending"
        self._current_transaction.rollback()
        self._current_transaction = None


def _register_transaction(transaction):
    TransactionHandler().set_transaction(transaction)
    return transaction


def video_metadata_transaction(db: Database) -> VideoMetadataTransaction:
    return _register_transaction(VideoMetadataTransaction(db))


def download_state_transaction(db: Database) -> DownloadStateTransaction:
    return _register_transaction(DownloadStateTransaction(db))


def transcript_transaction(db: Database) -> TranscriptTransaction:
    return _register_transaction(TranscriptTransaction(db))