from pathlib import Path
from arklibrary import Ini
import os
from arkcloud import lib


def root_directory():
    return Path(os.path.dirname(lib.__file__)).parent


def cwd_directory():
    return Path.cwd()


def get_config_path():
    return cwd_directory() / Path('config.ini')


def get_selenium_url():
    path = get_config_path()
    config = Ini(path)
    if 'BROWSER' in config and 'selenium_url' in config['BROWSER']:
        return config['BROWSER']['selenium_url'] or os.getenv('SELENIUM_URL')


def get_server_name():
    path = get_config_path()
    config = Ini(path)
    if 'ADMIN' in config and 'server_name' in config['ADMIN']:
        return config['ADMIN']['server_name']


def get_admin_password():
    path = get_config_path()
    config = Ini(path)
    if 'ADMIN' in config and 'password' in config['ADMIN']:
        return config['ADMIN']['password']

def get_map():
    path = get_config_path()
    config = Ini(path)
    if 'ADMIN' in config and 'map' in config['ADMIN']:
        return config['ADMIN']['map']


def get_email():
    path = get_config_path()
    config = Ini(path)
    if 'XBOX' in config and 'email' in config['XBOX']:
        return config['XBOX']['email']


def get_password():
    path = get_config_path()
    config = Ini(path)
    if 'XBOX' in config and 'password' in config['XBOX']:
        return config['XBOX']['password']


def get_width():
    path = get_config_path()
    config = Ini(path)
    if 'BROWSER' in config and 'width' in config['BROWSER']:
        return int(config['BROWSER']['width'])


def get_height():
    path = get_config_path()
    config = Ini(path)
    if 'BROWSER' in config and 'height' in config['BROWSER']:
        return int(config['BROWSER']['height'])


def get_x():
    path = get_config_path()
    config = Ini(path)
    if 'BROWSER' in config and 'x' in config['BROWSER']:
        return int(config['BROWSER']['x'])


def get_y():
    path = get_config_path()
    config = Ini(path)
    if 'BROWSER' in config and 'y' in config['BROWSER']:
        return int(config['BROWSER']['y'])


def get_remote():
    path = get_config_path()
    config = Ini(path)
    if 'BROWSER' in config and 'remote' in config['BROWSER']:
        return config['BROWSER']['remote']


def get_dark_mode():
    path = get_config_path()
    config = Ini(path)
    if 'BROWSER' in config and 'dark_mode' in config['BROWSER']:
        return config['BROWSER']['dark_mode']


def get_profile():
    path = get_config_path()
    config = Ini(path)
    if 'BROWSER' in config and 'profile' in config['BROWSER']:
        return config['BROWSER']['profile']
