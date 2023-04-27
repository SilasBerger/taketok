from src.spreadsheet.google_sheets import GoogleSheet
from src.util.config import Config


class TableRow:

    def __init__(self, index, data):
        self.index = index
        self.data = data


class Spreadsheet:
    
    def __init__(self, google_sheet: GoogleSheet, config: Config):
        self._gs = google_sheet
        self._video_data_tab = config.google_sheet.video_data_tab

    @staticmethod
    def _pad_row(row, width):
        padded_row = []
        for i in range(0, width):
            padded_row.append(row[i] if len(row) > i else None)
        return padded_row

    @staticmethod
    def _map_to_rows(rows, start_row_index, row_width):
        return [TableRow(index + start_row_index, Spreadsheet._pad_row(row, row_width)) for index, row in enumerate(rows)]

    def read_url_and_status(self) -> list[TableRow]:
        # TODO: Magic numbers (range, start row, row width).
        read_range = '%s!B3:C' % self._video_data_tab
        return Spreadsheet._map_to_rows(self._gs.read_range(read_range), start_row_index=3, row_width=2)

    @staticmethod
    def _create_update_chunks(rows_to_update: list[TableRow]):
        chunks = []
        last_row_index = -1
        for row in rows_to_update:
            if row.index != last_row_index + 1:
                chunks.append({'start_row': row.index, 'data': []})
            chunks[-1]['data'].append(row.data)
            last_row_index = row.index
        return chunks

    def _update_range(self, rows_to_update: list[TableRow], tab, start_col_index, end_col_index):
        update_chunks = self._create_update_chunks(rows_to_update)
        for chunk in update_chunks:
            start_row = chunk['start_row']
            data = chunk['data']
            end_row = start_row + len(data)
            update_range = '%s!%s%s:%s%s' % (tab, start_col_index, start_row, end_col_index, end_row)
            self._gs.write_range(update_range, data)

    def save_imported_video_data(self, rows_to_update: list[TableRow]):
        # TODO: Magic col indices.
        self._update_range(rows_to_update, self._video_data_tab, start_col_index='C', end_col_index='L')
