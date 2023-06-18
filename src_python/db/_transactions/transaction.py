from src_python.db.database import Database


class Transaction:

    def __init__(self, db: Database):
        self._db = db

    def commit(self):
        self._db.commit()

    def rollback(self):
        self._db.rollback()