from pathlib import Path


def as_path(string):
    return Path(string)


def taketok_home():
    return Path.home() / 'taketok'


def config_dir():
    return taketok_home() / 'config'


def tmp_dir():
    tmp_dir_path = taketok_home() / 'tmp'
    if not tmp_dir_path.exists():
        tmp_dir_path.mkdir()
    return tmp_dir_path


def config_file(config_name):
    return config_dir() / ('%s.config.json' % config_name)


def gcp_credentials_file(config_name):
    return config_dir() / ('%s.gcp-credentials.json' % config_name)


def gcp_token_file(config_name):
    return tmp_dir() / ('%s.gcp-token.json' % config_name)