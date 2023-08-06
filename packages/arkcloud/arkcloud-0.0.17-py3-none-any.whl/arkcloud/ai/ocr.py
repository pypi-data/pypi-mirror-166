from PIL.Image import open as open_image
import pytesseract
import io
from pathlib import Path
import re
import numpy as np
import cv2

best_constants = ['COLOR_RGB2YUV_I420', 'COLOR_RGB2YUV_IYUV', 'COLOR_RGB2YUV_YV12', 'COLOR_RGBA2YUV_I420', 'COLOR_RGBA2YUV_IYUV', 'COLOR_RGBA2YUV_YV12', '_OUTPUT_ARRAY_DEPTH_MASK_ALL']


def ocr_from_bytes(image_data: bytes):
    image = open_image(io.BytesIO(image_data))
    return pytesseract.image_to_string(image)


def ocr_from_file(image_path: str or Path):
    """
    Download the Tesseract-OCR and save the executable path in the environment paths
    'C:\Program Files\Tesseract-OCR\tesseract.exe'
    :param image_path: path to the image
    :return: str, the text from an image
    """
    image = open_image(image_path)
    return pytesseract.image_to_string(image)


def image_from_bytes(image_bytes: bytes):
    arr = np.asarray(bytearray(image_bytes), dtype='uint8')
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    width = len(image[0]) if len(image[0]) % 2 == 0 else len(image[0]) - 1
    height = len(image) if len(image) % 2 == 0 else len(image) - 1
    cropped_image = image[:height, :width]
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2YUV_I420)
    rgb_image = cv2.cvtColor(gray_image, cv2.IMREAD_COLOR)
    return cv2.imencode('.png', rgb_image)[1].tobytes()


def image_from_file(file: str or Path):
    with open(file, 'rb') as r:
        image_bytes = r.read()
        return image_from_bytes(image_bytes)


class OCR:
    def __init__(self, image_path=None, image_bytes=None):
        self.image = None
        self.text = ''
        if image_path:
            self.image = image_from_file(image_path)
            self.text = ocr_from_bytes(self.image).lower()
        elif image_bytes:
            self.image = image_from_bytes(image_bytes)
            self.text = ocr_from_bytes(self.image).lower()

    def is_intro_menu(self):
        values = ['start', 'not signed in', 'switch', 'profile']
        return any([value in self.text for value in values]) or len(self.text.replace("\n", '')) < 30

    def is_main_menu(self):
        values = ['join ark', 'ark news', 'host\\local', 'options', 'game modes', 'survivetheark.com']
        return any([value in self.text for value in values])

    def is_server_list(self):
        count = 0
        for text in self.text.split('\n'):
            if re.match(r'^\[[a-zA-Z0-9]+].*$', text):
                count += 1
        values = ['session', 'name filter', 'map', 'game mode',
                  'sort by', 'auto', 'favorite', 'password',
                  'auto favorite', 'show password', 'protected']
        return count > 1 or any([value in self.text for value in values])

    def is_character_creation(self):
        values = ['skin color', 'hair color', 'upper face size', 'head height', 'male', 'female', 'survivor name']
        return any([value in self.text for value in values])

    def is_respawning(self):
        values = ['bed', 'filter', 'spawn', 'region', 'respawn', 'random', 'location']
        if self.is_character_creation() or self.is_server_list():
            return False
        if re.match('respawn.*random.*location', self.text):
            return True
        return any([value in self.text for value in values])

    def is_options_menu(self):
        values = ['resume', 'options', 'exit to', 'main menu', 'game guide',
                  'invite', 'friends', 'server', 'ping', 'server', 'name',
                  'survivors', 'connected']
        return any([value in self.text for value in values])

    def is_in_game_options_cleared(self):
        values = ['level-up', 'available', 'access inventory', 'to apply', 'gameservergurus']
        return any([value in self.text for value in values])

    def is_in_game(self):
        if self.is_intro_menu() or self.is_main_menu():
            return False
        return any([
            self.is_in_game_options_cleared(),
            self.is_options_menu(),
            self.is_character_creation(),
            self.is_respawning()
        ])

    def all_failed(self):
        return not any([
            self.is_options_menu(),
            self.is_intro_menu(),
            self.is_main_menu(),
            self.is_server_list(),
            self.is_respawning(),
            self.is_character_creation(),
            self.is_in_game_options_cleared()
        ])


def test_booleans():
    file_names = ['intro_menu.png', 'main_menu.png', 'server_list.png',
                  'create_new_character_after_respawning.png', 'create_new_character_from_initialize.png', 'respawn.png']
    for file in file_names:
        path = './ai/menus/' + file
        print(file, ':')
        ocr = OCR(path)
        print("\tis_intro_menu:", ocr.is_intro_menu())
        print("\tis_main_menu:", ocr.is_main_menu())
        print("\tis_server_list:", ocr.is_server_list())
        print("\tis_character_creation:", ocr.is_character_creation())
        print("\tis_respawning:", ocr.is_respawning())


if __name__ == '__main__':
    test_booleans()

