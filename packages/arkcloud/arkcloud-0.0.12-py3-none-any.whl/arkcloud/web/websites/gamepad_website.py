from arkcloud.web.websites.website import Website
from arkcloud.gamepad import XboxController


class GamepadWebsite(Website):
    URL = "https://gamepad-tester.com/"

    def __init__(self, **kwargs):
        super().__init__(self.URL, **kwargs)
        self.controller = XboxController()
        self._driver.pause(2)

    @classmethod
    def controller_listener(cls, driver, controller):
        driver.execute_script(controller.js_update(), controller.encode())

    def connect_controller(self):
        self._driver.execute_script(self.controller.js_connect())
        self.controller.on_change(self.controller_listener, self._driver, self.controller)

    def disconnect_controller(self):
        self.focus()
        self._driver.execute_script(self.controller.js_disconnect())

    def disable_controller(self):
        self._driver.execute_script(self.controller.js_disconnect())
        self.controller.remove_on_change(self.controller_listener)

    def press_face_buttons(self):
        self.focus()
        self.controller.press_buttons('a', 'b', 'x', 'y')

    def release_face_buttons(self):
        self.focus()
        self.controller.release_buttons('a', 'b', 'x', 'y')

    def press_shoulder_buttons(self):
        self.focus()
        self.controller.press_buttons('left_trigger', 'left_bumper', 'right_trigger', 'right_bumper')

    def release_shoulder_buttons(self):
        self.focus()
        self.controller.release_buttons('left_trigger', 'left_bumper', 'right_trigger', 'right_bumper')

    def press_dpad_buttons(self):
        self.focus()
        self.controller.press_buttons('up', 'down', 'left', 'right')

    def release_dpad_buttons(self):
        self.focus()
        self.controller.release_buttons('up', 'down', 'left', 'right')

    def pause(self, seconds: int):
        self._driver.pause(seconds)


if __name__ == "__main__":
    web = GamepadWebsite()
    web.connect_controller()
    web.press_face_buttons()
    web.pause(3)
    web.release_face_buttons()
    web.close()
