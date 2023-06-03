from googleapiclient.discovery import build
from gcp_commons.auth import GcpAuthHandler

from src.util.config import Config
from src.util.path_utils import gcp_token_file


def cell(col, row):
    return '%s%s' % (col, row)


def cell_range(start, end, tab=None):
    if tab is not None:
        return '%s!%s:%s' % (tab, start, end)
    return '%s:%s' % (start, end)


class GoogleSheet:

    def __init__(self, config: Config):
        self._spreadsheet_id = config.google_sheet.id
        self._auth = GcpAuthHandler(gcp_token_file(config.name), gcp_token_file(config.name))

    def _connect_to_sheet(self):
        service = build('sheets', 'v4', credentials=self._auth.load_credentials())
        return service.spreadsheets()

    def _values(self):
        return self._connect_to_sheet().values()

    def read_range(self, read_range):
        result = self._values().get(spreadsheetId=self._spreadsheet_id, range=read_range).execute()
        return result.get('values', [])

    def write_range(self, update_range, data):
        self._values().update(
            spreadsheetId=self._spreadsheet_id,
            range=update_range,
            body={'values': data},
            valueInputOption='RAW'
        ).execute()

    def clear_range(self, range_to_clear):
        self._values().clear(spreadsheetId=self._spreadsheet_id, range=range_to_clear).execute()