import sys

from src_python.db.database import Database
from src_python.util.path_utils import taketok_home, sqlite_file


def get_config_name():
    return sys.argv[1] if len(sys.argv) > 1 else 'default'


def main():
    config_name = get_config_name()
    database = Database.connect(sqlite_file(config_name), create_if_not_exists=True)
    source_links_file_path = taketok_home() / (config_name + ".source-links.txt")
    with open(source_links_file_path) as links_file:
        lines = links_file.readlines()
        for line in lines:
            database.execute("insert or ignore into source_urls (url) values (?)", (line.strip(),))
        database.commit()


if __name__ == "__main__":
    main()
