import sys

from src_python.old_data_importer import DataImporter
from src_python.db.database import Database
from src_python.util.config import read_config
from src_python.util.path_utils import sqlite_file


def get_config_name():
    return sys.argv[1] if len(sys.argv) > 1 else 'default'


def main():
    config_name = get_config_name()
    config = read_config(config_name)
    database = Database.connect(sqlite_file(config.name), create_if_not_exists=True)
    video_importer = DataImporter(database, config)
    video_importer.import_all_new_links()


if __name__ == '__main__':
    main()
    