from src_python.db.database import Database


def fetch_non_processed_source_urls(db: Database):
    return [line[0] for line in db.fetch_all("select url from source_url where source_url.processed = false")]
