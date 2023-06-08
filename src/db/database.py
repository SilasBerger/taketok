import os
import sqlite3


class Database:

    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection
        self._cursor = self._connection.cursor()

    @staticmethod
    def connect(sqlite_file: os.path):
        # TODO: Ensure file exists (create blank if needed)
        conn = sqlite3.connect(str(sqlite_file))
        # TODO: Ensure correct schema.
        return Database(conn)

    def fetch_one(self, statement, bindings=()):
        self._cursor.execute(statement, bindings)
        return self._cursor.fetchone()

    def fetch_all(self, statement, bindings=()):
        self._cursor.execute(statement, bindings)
        return self._cursor.fetchall()

    def write(self, statement, bindings=()):
        self._cursor.execute(statement, bindings)
        self._connection.commit()
        return self._cursor.lastrowid
