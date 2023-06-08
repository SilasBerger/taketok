import os
import sqlite3
from pathlib import Path

from src.util.path_utils import db_scripts_dir


class Database:

    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection
        self._cursor = self._connection.cursor()

    @staticmethod
    def create(sqlite_file: Path):
        if sqlite_file.exists():
            raise "Cannot create database because it already exists: %s" % sqlite_file
        sqlite_file.touch()
        conn = sqlite3.connect(str(sqlite_file))
        cursor = conn.cursor()
        with open(db_scripts_dir() / "create_schema.sql") as script_file:
            script = script_file.read()
            cursor.executescript(script)
        conn.close()

    @staticmethod
    def connect(sqlite_file: Path, create_if_not_exists=False):
        if not sqlite_file.exists():
            if create_if_not_exists:
                Database.create(sqlite_file)
            else:
                raise "SQLite file does not exist: %s" % sqlite_file
        conn = sqlite3.connect(str(sqlite_file))
        instance = Database(conn)
        instance._sanity_check(sqlite_file)
        return instance

    def _sanity_check(self, sqlite_file):
        try:
            if len(self.fetch_one("select schema_version from taketok_schema")) >= 1:
                return
        except Exception:
            pass
        raise "Unexpected schema; this is likely not a taketok database file: %s" % sqlite_file

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
