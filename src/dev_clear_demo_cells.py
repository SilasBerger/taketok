from src.spreadsheet.google_sheets import GoogleSheet
from src.util.config import read_config


def main():
    google_sheet = GoogleSheet(read_config('default'))

    google_sheet.clear_range('C20:L20')
    google_sheet.clear_range('C22:L23')


if __name__ == '__main__':
    main()
    