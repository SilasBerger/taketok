from src.db.database import Database
from src.util.path_utils import taketok_home, sqlite_file


def main():
    database = Database.connect(sqlite_file("default"), create_if_not_exists=True)
    source_links_file_path = taketok_home() / "source-links.txt"
    with open(source_links_file_path) as links_file:
        lines = links_file.readlines()
        for line in lines:
            database.write_and_commit("insert or ignore into video (source_url) values (?)", (line.strip(),))


if __name__ == "__main__":
    main()
