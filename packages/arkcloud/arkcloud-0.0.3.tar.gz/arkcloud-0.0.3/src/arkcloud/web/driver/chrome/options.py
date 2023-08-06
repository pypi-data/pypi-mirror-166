from arkcloud import web
from selenium.webdriver.chrome.options import Options as ChromeOptions
from pathlib import Path
import os
from collections import defaultdict


class Options:

    DIR_PATH = Path(os.path.dirname(web.__file__)) / Path("driver/chrome/extensions")
    XBOX_CONTROLLER_EXTENSION = DIR_PATH / Path("XboxCloudController.crx")
    DARK_READER_EXTENSION = DIR_PATH / Path("Dark-Reader.crx")

    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.options = ChromeOptions()
        keys = defaultdict(lambda: None)
        keys.update(kwargs)
        self.width = keys['width']
        self.height = keys['height']
        self.x = keys['x']
        self.y = keys['y']
        self.profile = keys['profile_options']
        self.extensions = []
        self.arguments = []

        self.__params(**kwargs)

    def __params(self, **kwargs):
        if 'remote_options' in kwargs and kwargs['remote_options']:
            self.as_remote()
        if 'dark_mode_options' in kwargs and kwargs['dark_mode_options']:
            self.add_dark_mode()
        if 'xbox_controller_extension' in kwargs and kwargs['xbox_controller_extension']:
            self.add_xbox_controller()
        if 'extensions' in kwargs and isinstance(kwargs['extensions'], list):
            for extension in kwargs['extensions']:
                self.add_extension(extension)
        if 'width' in kwargs and 'height' in kwargs:
            self.set_window_size(width=kwargs['width'], height=kwargs['height'])
        if 'x' in kwargs or 'y' in kwargs:
            self.set_window_position(x=kwargs['x'] or 0, y=kwargs['y'] or 0)
        if 'profile_options' in kwargs and kwargs['profile_options']:
            self.add_profile(kwargs['profile_options'])

    def as_remote(self):
        if "remote" not in self.arguments:
            # self.options.add_argument(f"--no-startup-window")
            self.options.add_argument('--disable-extensions')
            self.options.add_argument('--headless')
            self.options.add_argument('--disable-gpu')
            self.options.add_argument('--no-sandbox')
            self.options.add_argument('--disable-dev-shm-usage')
            self.arguments.append("remote")

    def set_window_size(self, width: int = None, height: int = None):
        if width and height and width > 0 and height > 0:
            self.width = width
            self.height = height

    def set_window_position(self, x: int = None, y: int = None):
        self.x = x
        self.y = y

    def add_extension(self, path: str = None, name: str = None):
        if not path:
            raise FileNotFoundError(f"Extension path must be provided if adding an extension")
        path = Path(path)
        if path.exists() and path.suffix.lower() == '.crx':
            self.options.add_extension(str(path))
            if name:
                self.extensions.append(name)
            else:
                self.extensions.append(path.stem)
        if not path.exists():
            print(f"Warning: {name or path.stem} extension doesn't exist in {path}")
        if path.suffix.lower() != '.crx':
            print(f"Warning: {name or path.stem} extension must be a .crx file in {path}")

    def add_xbox_controller(self):
        if not self.XBOX_CONTROLLER_EXTENSION.exists():
            print("Warning: xbox controller extension doesn't exist")
        elif "Xbox Controller Extension" not in self.extensions:
            self.options.add_extension(str(self.XBOX_CONTROLLER_EXTENSION))
            self.extensions.append("Xbox Controller Extension")

    def add_dark_mode(self):
        if "Dark Mode" not in self.extensions and self.DARK_READER_EXTENSION.exists():
            self.options.add_extension(str(self.DARK_READER_EXTENSION))
            self.extensions.append("Dark Mode")
        if not self.DARK_READER_EXTENSION.exists():
            print("Warning: dark mode extension doesn't exist")

    def add_profile(self, profile_number: int):
        user_data = Path(os.getenv('LOCALAPPDATA')) / Path('Google/Chrome Dev/User Data')
        self.options.add_argument(f"--user-data-dir={user_data}")
        self.options.add_argument(f"--profile-directory=Profile {profile_number}")

    def bind(self):
        if isinstance(self.width, int) and isinstance(self.height, int):
            self.options.add_argument(f"--window-size={self.width},{self.height}")
            if isinstance(self.x, int) and isinstance(self.height, int):
                self.options.add_argument(f"--window-position={self.x},{self.y}")
        return self.options

    def __repr__(self):
        args = [f"{k}={repr(v)}" for k, v in self.__dict__.items()]
        param = ', '.join(args)
        s = f"<Options({param})>"
        if not self.options.arguments and not self.extensions:
            return s
        if self.options.arguments:
            s += "\t<arguments>"
            for arg in self.options.arguments:
                s += f"\t\t{arg}"
            s += "\t</arguments>"
        if len(self.extensions) > 0:
            s += "\t<extensions>"
            for arg in self.extensions:
                s += f"\t\t{arg}"
            s += "\t</extensions>"
        s += "</Options>"
