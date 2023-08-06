import arkcloud.web.websites as websites
from arkcloud.web import Website
import os
from pathlib import Path
from arklibrary import Ini


def get_xbox_controller_configuration():
    path = Path.cwd() / Path('config.ini')
    config = Ini(path)
    if 'XBOX' in config and 'controller_configuration' in config['XBOX']:
        return config['XBOX']['controller_configuration']


class XboxControllerExtension(Website):
    URL = "chrome-extension://nmfedkijhhigaikbadoijiolmjjgoimd/popup.html"
    PRESET = os.path.dirname(websites.__file__) / Path('xbox_controller_preset.json')

    def __init__(self, **kwargs):
        arguments = {
            'xbox_controller_options': True,
            'remote': False,
            **kwargs
        }
        super().__init__(self.URL, **arguments)
        self.focus()
        self._add_preset('xbox_controller')
        button = self._button_import()
        button.click()
        self._send_file()
        self._mouse_keyboard(enabled=True)
        self._use()

    def _mouse_keyboard(self, enabled=False, timeout=2):
        self.focus()
        try:
            if enabled:
                self._driver.element(tag='button', title='Disable mouse and keyboard', timeout=timeout).click()
            else:
                self._driver.element(tag='button', title='Enable mouse and keyboard', timeout=timeout).click()
        except Exception:
            pass


    def _use(self, timeout=2):
        self.focus()
        try:
            button_use = self._driver.element(tag='button', class_contains='ms-Button ms-Button--primary root-194', timeout=timeout)
            button_use.click()
        except Exception:
            pass


    def _add_preset(self, name: str, timeout=2):
        self.focus()
        if not self._driver.elements(tag='input', placeholder='New preset name', timeout=timeout):
            button_add = self._driver.element(tag='button', id='new-config-btn', timeout=timeout)
            button_add.click()
        input_name = self._driver.element(tag='input', placeholder='New preset name', timeout=timeout)
        input_name.send_buttons(*(['BACKSPACE'] * 20))
        input_name.send_keys(name)

    def _button_import(self, timeout=2):
        self.focus()
        if self._driver.elements(text='Import File', timeout=timeout):
            child = self._driver.element(text='Import File', timeout=timeout)
            parent = child.parent
            while parent != child and parent.tag != 'button':
                child = parent
                parent = child.parent
            if parent.tag == 'button':
                return parent

    def _send_file(self, timeout=2):
        self.focus()
        if self._driver.elements(tag='input', type='file', id='import-json-input', timeout=timeout):
            input_file = self._driver.element(tag='input', type='file', id='import-json-input', timeout=10)
            self._driver.pause(2)
            input_file.send_keys(str(self.PRESET))
            self._driver.pause(3)
            self._driver.accept_alert()
            self._driver.pause(1)


