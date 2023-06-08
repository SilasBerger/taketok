import os
from pathlib import Path


def as_path(string):
    return Path(string)


def _ensure_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True)
    return path


def taketok_home():
    return Path.home() / 'taketok'


def config_dir():
    return taketok_home() / 'config'


def tmp_dir():
    return _ensure_dir(taketok_home() / 'tmp')


def config_file(config_name):
    return config_dir() / ('%s.config.json' % config_name)


def _sqlite_db_dir():
    return _ensure_dir(taketok_home() / 'data')


def sqlite_file(config_name):
    return _sqlite_db_dir() / ('%s.sqlite' % config_name)


def db_scripts_dir():
    return Path().resolve().parent / "db"