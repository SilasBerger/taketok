from pathlib import Path


def as_path(string):
    return Path(string)


def taketok_home():
    return Path.home() / '.taketokrc'


def config_file(config_name):
    return taketok_home() / ('%s.config.json' % config_name)


def gcp_credentials_file(config_name):
    return taketok_home() / ('%s.gcp-credentials.json' % config_name)


def gcp_token_file(config_name):
    return taketok_home() / ('%s.gcp-token.json' % config_name)