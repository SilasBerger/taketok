import json

from src_python.util.path_utils import as_path, config_file


def read_config(config_name):
    with open(config_file(config_name)) as fp:
        return Config(config_name, json.load(fp))


class Config:

    def __init__(self, name, config):
        self.name = name
        self.video_output_dir = as_path(config['videoOutputDir'])  # TODO: Maybe create if not exists?
        self.whisper_model = config['whisperModel']
