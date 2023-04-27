import math

from src.spreadsheet.spreadsheet import Spreadsheet, TableRow
from src.tiktok.tiktok import resolve_video_id, tiktok_download
from src.util.config import Config


class DataImporter:

    def __init__(self, spreadsheet: Spreadsheet, config: Config):
        self._sheet = spreadsheet
        self._video_out_dir = config.video_output_dir
        self._import_chunk_size = config.import_chunk_size

    def _save_video(self, video_bytes, video_id):
        filename = self._video_out_dir / ('%s.mp4' % video_id)
        with open(filename, 'wb') as video_outfile:
            video_outfile.write(video_bytes)

    @staticmethod
    def _extract_hashtags(info):
        return ",".join([hashtag['hashtagName'] for hashtag in info['textExtra']]) if 'textExtra' in info else ''

    @staticmethod
    def _extract_suggested_words(info):
        return ",".join(info['suggestedWords']) if 'suggestedWords' in info else ''

    @staticmethod
    def _map_meta_data(info):
        info = info['itemInfo']['itemStruct']
        author = info['author']

        return [
            info['id'],
            info['desc'],
            DataImporter._extract_hashtags(info),
            DataImporter._extract_suggested_words(info),
            author['id'],
            author['uniqueId'],
            author['nickname'],
            author['signature']
        ]

    def _save_video_and_fetch_meta_data(self, video_url):
        video_id = resolve_video_id(video_url)
        tiktok_result = tiktok_download(video_id)
        self._save_video(tiktok_result.bytes, video_id)
        return DataImporter._map_meta_data(tiktok_result.info)

    def _split_into_import_chunks(self, rows: list[TableRow]):
        num_rows = len(rows)
        num_chunks = math.ceil(num_rows / self._import_chunk_size)
        print('Found %s rows to import, importing in %s chunks of %s' % (num_rows, num_chunks, self._import_chunk_size))
        chunks = []
        for chunk_nr in range(num_chunks):
            start_index = chunk_nr * self._import_chunk_size
            end_index = min(start_index + self._import_chunk_size, num_rows)
            chunks.append(rows[start_index:end_index])
        return chunks

    def _import_chunk(self, chunk):
        rows_to_update = []
        for index, row in enumerate(chunk):
            try:
                print('Importing line %s' % (index + 1))
                meta_data = self._save_video_and_fetch_meta_data(row.data[0])
                # TODO: Magic constant for status / magic order.
                rows_to_update.append(TableRow(row.index, ['OK', ''] + meta_data))
            except Exception as e:
                # TODO: Magic status / magic order.
                rows_to_update.append(TableRow(row.index, ['FAILED', str(e)]))

        print('Fetched all data, updating spreadsheet')
        self._sheet.save_imported_video_data(rows_to_update)

    def import_all_new_urls(self):
        # TODO: Magic numbers (URL / status col indices).
        new_rows = [row for row in self._sheet.read_url_and_status() if not row.data[1]]
        chunks = self._split_into_import_chunks(new_rows)
        for index, chunk in enumerate(chunks):
            print('\nImporting chunk %s/%s' % (index + 1, len(chunks)))
            try:
                self._import_chunk(chunk)
            except Exception as e:
                print('Chunk failed:')
                print(e)
