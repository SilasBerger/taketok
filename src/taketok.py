import sys

from src.spreadsheet.spreadsheet import Spreadsheet
from src.spreadsheet.google_sheets import GoogleSheet
from src.data_importer import DataImporter
from src.transcribe.transcribe import VideoTranscriber
from src.util.config import read_config


def get_config_name():
    return sys.argv[1] if len(sys.argv) > 1 else 'default'


def transcribe():
    config = read_config('default')
    # video_id = '7206107080787266862'
    video_id = '7221168281086938394'
    transcriber = VideoTranscriber(config)
    print(transcriber.transcribe(video_id))


def main():
    config_name = get_config_name()
    config = read_config(config_name)
    google_sheet = GoogleSheet(config)
    spreadsheet = Spreadsheet(google_sheet, config)
    video_importer = DataImporter(spreadsheet, config)
    video_importer.import_all_new_urls()


if __name__ == '__main__':
    transcribe()
    