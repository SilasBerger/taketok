import sys

from src.db.dao import Dao
from src.data_importer import DataImporter
from src.db.database import Database
from src.util.config import read_config
from src.util.path_utils import sqlite_file


def get_config_name():
    return sys.argv[1] if len(sys.argv) > 1 else 'default'


def main():
    config_name = get_config_name()
    config = read_config(config_name)
    database = Database.connect(sqlite_file(config.name))
    dao = Dao(database)
    video_importer = DataImporter(dao, config)
    video_importer.import_all_new_links()


if __name__ == '__main__':
    main()
    