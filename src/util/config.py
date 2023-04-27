import json

from src.util.path_utils import as_path, config_file


def read_config(config_name):
    with open(config_file(config_name)) as fp:
        return Config(config_name, json.load(fp))


class GoogleSheetConfig:

    def __init__(self, config):
        self.id = config['id']
        self.video_data_tab = config['videoDataTab']


class Config:

    def __init__(self, name, config):
        self.name = name
        self.video_output_dir = as_path(config['videoOutputDir'])
        self.import_chunk_size = config['importChunkSize']
        self.google_sheet = GoogleSheetConfig(config['googleSheet'])
        self.whisper_model = config['whisperModel']
