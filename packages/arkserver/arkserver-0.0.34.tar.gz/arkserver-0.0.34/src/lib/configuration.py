from arklibrary import Ini
from pathlib import Path
import lib
import os


def get_root():
    return Path(os.path.dirname(lib.__file__)).parent


def get_cwd():
    return Path.cwd()


def get_root_name():
    root = get_root() / Path('config.ini')
    config = Ini(root) if root.exists() else None
    return None if not config else config['SERVER']['name']


def get_root_host():
    root = get_root() / Path('config.ini')
    config = Ini(root) if root.exists() else None
    return None if not config else config['SERVER']['host']


def get_root_port():
    root = get_root() / Path('config.ini')
    config = Ini(root) if root.exists() else None
    return None if not config else config['SERVER']['port']


def get_cwd_name():
    cwd = get_cwd() / Path('config.ini')
    config = Ini(cwd) if cwd.exists() else None
    return None if not config else config['SERVER']['name']


def get_cwd_host():
    cwd = get_cwd() / Path('config.ini')
    config = Ini(cwd) if cwd.exists() else None
    return None if not config else config['SERVER']['host']


def get_cwd_port():
    cwd = get_cwd() / Path('config.ini')
    config = Ini(cwd) if cwd.exists() else None
    return None if not config else config['SERVER']['port']


def get_name():
    return get_cwd_name() or get_root_name()


def get_host():
    return get_cwd_host() or get_root_host()


def get_port():
    return get_cwd_port() or get_root_port()


