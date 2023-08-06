from arkcloud.web.websites.website import Website, Driver
from arkcloud.ai import OCR
import os
from arkcloud.gamepad import XboxController
from arkcloud.lib import get_email, get_password, get_admin_password
from arkcloud.lib import get_server_name, countdown


def controller_listener(driver: Driver, controller: XboxController):
    driver.execute_script(controller.js_update(), controller.encode())


class ArkWebsite(Website):
    LOGIN_URL = "https://login.live.com/login.srf"
    LOGOUT_URL = "https://login.live.com/logout.srf?ru=https%3A%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-signout"
    GAME_URL = "https://www.xbox.com/en-US/play/games/ark-ultimate-survivor-edition/9N5JRWWGMS1R"

    RESOLVE_INDEX = 0

    def __init__(self, **kwargs):
        super().__init__(self.LOGIN_URL, **kwargs)
        self.controller = XboxController()
        self.controller.on_change(controller_listener, self._driver, self.controller)

    def connect_controller(self):
        self.disconnect_controller()
        self._driver.execute_script(self.controller.js_connect())

    def disconnect_controller(self):
        self._driver.execute_script(self.controller.js_disconnect())

    def lobby(self):
        print("Navigating to lobby")
        super().focus()
        self._driver.get(ArkWebsite.GAME_URL, timeout=10)
        countdown(5, 'Waiting for lobby to finish loading')

    def login(self, email: str = None, password: str = None, timeout=0):
        email = email or get_email() or os.getenv('XBOX_EMAIL')
        password = password or get_password() or os.getenv('XBOX_PASSWORD')
        if not email or not password:
            raise Exception("An Xbox email and password must be provided")
        print("Logging in")
        self.focus()
        self._driver.get(self.LOGIN_URL)
        self.login_username(email=email)
        self.login_password(password=password)

        try:
            input_last_4 = self._driver.element(tag='input', type='tel')
            input_last_4.send_keys('6187')
            button_phone_verification = self._driver.element(tag='input', type='submit', id='iSelectProofAction')
            button_phone_verification.click()
            #security_input = self._driver.element(tag='input', type='tel', id='iOttText')
            #security_input.send_keys(input("Enter the security code sent to your phone: "))
            #button_next = self._driver.element(tag='input', type='submit', id='iVerifyCodeAction')
            #button_next.click()
        except Exception:
            pass

        try:
            button_terms = self._driver.element(tag='input', type='submit', timeout=timeout)
            button_terms.click()
        except Exception:
            pass
        try:
            dont_show_again = self._driver.element(tag='input', name='DontShowAgain', timeout=timeout)
            dont_show_again.click()
            yes = self._driver.element(tag='input', type='submit')
            yes.click()
        except Exception:
            pass
        print("Logged in")

    def login_username(self, email: str):
        timeout = 3
        self.focus()
        try:
            input_email = self._driver.element(tag='input', type='email', timeout=timeout)
            input_email.send_keys(email)
            button_next = self._driver.element(tag='input', type='submit')
            button_next.click()
        except Exception:
            # Already logged in
            return
        try:
            self._driver.element(tag='div', id='usernameError', timeout=timeout)
            raise ConnectionRefusedError
        except ConnectionRefusedError:
            self.close()
            raise ConnectionRefusedError("Invalid username")
        except Exception:
            pass

    def login_password(self, password: str):
        timeout = 3
        self.focus()
        try:
            input_password = self._driver.element(tag='input', type='password', timeout=timeout)
            input_password.send_keys(password)
            button_sign_in = self._driver.element(tag='input', type='submit')
            button_sign_in.click()
        except Exception:
            return  # already logged in
        try:
            self._driver.element(tag='div', id='passwordError', timeout=timeout)
            raise ConnectionRefusedError
        except ConnectionRefusedError:
            self.close()
            raise ConnectionRefusedError("Invalid password")
        except Exception:
            pass

    def reboot(self):
        print("Starting reboot")
        self.login()
        self.press_play()
        self.wait_for_loading()
        if not self.is_in_game():
            self.intro_menu_start()
            self.join_ark_server_list()
            self.join_server()
        if self.is_character_creation():
            self.create_character()
        if self.is_respawning():
            self.respawn()
        self.enable_admin()

    def press_play(self, timeout=2, count=0, failed=False):
        if count > 5:
            print("Failed to press play 5 times")
            self._driver.save_png(f"./cache/error_press_play_{count}")
            if failed:
                raise Exception("Unable to press play")
            self.press_play(failed=True)
        long_timeout = timeout + 10
        self.focus()
        self.lobby()
        try:
            print("Pressing Sign in if it exists")
            button_sign_in = self._driver.element(tag='a', text='Sign in', timeout=timeout)
            button_sign_in.parent().click()
            countdown(long_timeout, message='Pausing for any loading')
        except Exception as e:
            print(f"Couldn't find the sign in button: {e}")

        try:
            print("Pressing play")
            button_play = self._driver.element(tag='button', text='Play', timeout=long_timeout)
            button_play.parent().click()
            self.continue_anyway(timeout=timeout)
            print("Pressed play succeeded")
        except Exception as e:
            print(f"Couldn't find the play button: {e}")
            print("Retrying the lobby...")
            self.press_play(timeout=timeout, count=count + 1, failed=failed)

    def wait_for_loading(self, timeout=10):
        self.resolve_disconnections()
        try:
            loading = self._driver.element(tag='div', class_starts_with='RocketAnimation-module__container___', timeout=timeout)
            print("Game is loading...")
            loading.wait_until_disappear(timeout=300)
        except Exception:
            print("Could not catch the loading screen")
        self.resolve_disconnections()
        try:
            self._driver.element(tag='div', class_starts_with='InProgressScreen-module__container___', timeout=timeout)
            print("Game has started")
            self.connect_controller()
            print("Controller connected")
            countdown(45, message='Waiting 45 seconds for starting screen to clear')
            print("Loaded onto the start screen")
            return True
        except Exception:
            print("Could not get to the game loading screen")
            return False

    def intro_menu_start(self, exceeded=0):
        self.focus()
        self.resolve_disconnections()
        if exceeded > 10:
            print("Some went wrong when trying for intro menu start")
            self.save_screenshot('./cache/error_intro_menu_start.png')
        if not self.is_intro_menu():
            self.dashboard_reset()
            self.press_play()
            self.wait_for_loading()
            self.intro_menu_start(exceeded=exceeded+1)
        else:
            print("Pressing start from the intro menu")
            self.send_buttons('a', spread=2)

    def join_ark_server_list(self):
        self.resolve_disconnections()
        self.focus()
        if not self.is_main_menu():
            print("Currently not in the main menu")
            self.send_buttons('b', 'b', 'b', spread=2)
            print("Retrying the start menu")
            self.intro_menu_start()
            self.join_ark_server_list()
        else:
            self.send_buttons(*(['UP'] * 7), spread=0.5)
            print("Opening server list")
            self.send_buttons('a', spread=2)
            countdown(30, 'Waiting for server list to load')

    def join_server(self, server_name: str = None, timeout=3):
        self.resolve_disconnections()
        self.focus()
        server_name = server_name or get_server_name()
        if not server_name:
            raise Exception("Server name must be provided")
        if not self.is_server_list():
            self.join_ark_server_list()
            self.join_server(server_name=server_name, timeout=timeout)
        else:
            print(f"Moving to search field")
            self.send_buttons('LEFT', hold=10)
            self.send_buttons('UP', hold=10)
            self.send_buttons('a')
            print(f"Searching searching server: {server_name}")
            self.input_dialog(server_name, timeout=timeout)
            print("Selecting first search result")
            self.send_buttons('DOWN', 'a', 'START', spread=3)
            print(f"Joining server: {server_name}")
            countdown(60, message='Waiting 60 seconds for game to load')
            if self.is_server_list():
                raise Exception(f"Server {server_name} was not found")
            print("Finished joining server")

    def save_screenshot(self, path):
        try:
            self._driver.element(tag='div', id='root').click()
            self._driver.save_png(path)
        except Exception:
            pass

    def ocr(self, retries=0):
        self.focus()
        image_bytes = self._driver.png_bytes()
        data = OCR(image_bytes=image_bytes)
        if retries < 10 and (data.text == '' or data.all_failed()):
            return self.ocr(retries=retries + 1)
        return data

    def respawn(self):
        if not self.is_respawning():
            print("Could not detect respawning")
            return False
        print("Attempting to respawn")
        self.send_buttons(*(['left'] * 5), spread=0.2)
        self.send_buttons(*(['down'] * 20), spread=0.2)
        self.send_buttons(*(['RIGHT'] * 5), spread=0.2)
        self.send_buttons(*(['down'] * 20), spread=0.2)
        self.send_buttons('left', spread=0.2)
        self.send_buttons('a')
        self._driver.pause(2)
        if self.is_respawning():
            return self.respawn()
        else:
            print("Finished respawning")
            return True

    def create_character(self):
        if not self.is_character_creation():
            print("Could not detect character creation")
            return False
        self.send_buttons(*(['b'] * 6), spread=0.2)
        print("Attempting to create character")
        self.send_buttons(*(['LEFT'] * 6), spread=0.2)
        self.send_buttons(*(['UP'] * 20), spread=0.2)
        self.send_buttons(*(['DOWN'] * 20), spread=0.2)
        self.send_buttons(*(['RIGHT'] * 6), spread=0.2)
        self.send_buttons('a', spread=1)
        self._driver.pause(2)
        if self.is_character_creation():
            self.send_buttons(*(['LEFT'] * 6), spread=0.2)
            self.send_buttons(*(['UP'] * 20), spread=0.2)
            self.send_buttons(*(['DOWN'] * 20), spread=0.2)
            self.send_buttons(*(['RIGHT'] * 6), spread=0.2)
            self.send_buttons('UP', 'UP', 'a', 'a', spread=1)
            self._driver.pause(2)
        if self.is_character_creation():
            return self.create_character()
        else:
            print("Finished creating character")
            return True

    def menu_reset(self, timeout=2):
        print("Trying to go to main menu")
        self.send_buttons('b', 'b', spread=1)
        self.send_buttons('START')
        countdown(2, 'Waiting for menu to appear')
        if self.is_options_menu():
            self.send_buttons('UP', hold=5)
            self.send_buttons('DOWN', 'DOWN', 'DOWN', spread=2)
            self.send_buttons('a')
            self._driver.pause(2)
            self.send_buttons('b', spread=1)
        if self.resolve_disconnections() or not self.is_intro_menu():
            print("Was unable to resolve or get to the intro menu, trying again...")
            self.send_buttons('START')
            self.send_buttons('UP', hold=5)
            self.send_buttons('DOWN', 'DOWN', spread=2)
            self.send_buttons('a')
            self._driver.pause(2)
            self.send_buttons('b', spread=1)
            self.menu_reset(timeout=timeout)
        print("Menu reset has finished")

    def dashboard_reset(self, timeout=2):
        if self._driver.url() == 'https://www.xbox.com/en-US/play' or self._driver.url() != "https://www.xbox.com/en-US/play/launch/ark-ultimate-survivor-edition/9N5JRWWGMS1R":
            print("Dashboard reset has finished")
            return
        print("Trying to go to main menu")
        self.send_buttons('b', 'b', spread=1)
        self.send_buttons('START')
        countdown(2, 'Waiting for menu to appear')
        if self.is_options_menu():
            self.send_buttons('UP', hold=5)
            self.send_buttons('DOWN', 'DOWN', 'DOWN', spread=2)
            self.send_buttons('a')
            self.send_buttons('b', spread=1)
        if not self.is_intro_menu():
            print("Was unable to resolve or get to the intro menu, trying again...")
            self.send_buttons('START')
            self.send_buttons('UP', hold=5)
            self.send_buttons('DOWN', 'DOWN', spread=2)
            self.send_buttons('a')
            self.send_buttons('b', spread=1)
            self.dashboard_reset(timeout=timeout)
            return
        print("Menu reset has finished")
        print("Trying to exit from xbox")
        self.send_buttons('HOME', spread=1)
        self.send_buttons('DOWN', hold=5)
        self.send_buttons('a', spread=1)
        self.continue_anyway(timeout=timeout)
        try:
            print("Trying to close the survey")
            self._driver.element(tag='button', **{'aria-label': 'Close'}).click()
        except Exception:
            pass
        if self._driver.url() != 'https://www.xbox.com/en-US/play':
            print("Was unable to get to the home page")
            self.dashboard_reset(timeout=timeout)
            return
        print("Dashboard reset has finished")

    def logout(self, timeout=2):
        self.focus()
        self.menu_reset(timeout=timeout)
        self.dashboard_reset(timeout=timeout)
        self._driver.get(self.LOGOUT_URL)
        self._driver.execute_script(self.controller.js_disconnect())
        countdown(3, 'Waiting for browser to finish loading')
        print("Logged out")

    def container_text(self):
        try:
            container = self._driver.element(tag='div', **{'data-id': 'ui-container'})
            return container.text
        except Exception:
            return ''

    def continue_anyway(self, timeout=2):
        self.focus()
        try:
            button = self._driver.element(tag='button', text='Continue anyway', timeout=timeout)
            button.hover()
            button.click()
            button.wait_until_disappear(timeout=timeout)
        except Exception:
            pass
        try:
            button = self._driver.element(tag='button', text='Refresh page', timeout=timeout)
            button.hover()
            button.click()
            button.wait_until_disappear(timeout=timeout)
        except Exception:
            pass
        try:
            button = self._driver.element(tag='button', text='Quit game', timeout=timeout)
            button.hover()
            button.click()
            button.wait_until_disappear(timeout=timeout)
        except Exception:
            pass
        try:
            button = self._driver.element(tag='button', class_starts_with="PopupScreen-module__button___")
            button.hover()
            button.click()
            button.wait_until_disappear(timeout=timeout)
        except Exception:
            pass

    def input_dialog(self, text: str, timeout=2):
        try:
            self.continue_anyway(timeout=timeout)
            input_request = self._driver.element(tag='input', type='default', class_starts_with='Input-module__input___', timeout=timeout)
            while input_request.value():
                input_request.clear()
                input_request = self._driver.element(tag='input', type='default', class_starts_with='Input-module__input___', timeout=timeout)
            input_request.send_keys(text)
            button_submit = self._driver.element(tag='button', class_starts_with='Keyboard-module__actionButton___', timeout=timeout)
            button_submit.click()
            self.continue_anyway(timeout=timeout)
            self._driver.pause(1)
            print("Sending to input dialog was successful")
            return True
        except Exception:
            print("Unable to find input dialogue")
            return False

    def enable_admin(self, password: str = None, timeout=1):
        print("Enabling admin")
        admin_password = password or get_admin_password()
        self.cmd(admin_password, timeout=timeout)
        commands = '|'.join([
            'cheat GCM', 'cheat Ghost', 'cheat God', 'cheat Fly', 'cheat tp blue'])
        self.cmd(commands, timeout=timeout)

    def cmd(self, command: str, timeout=3):
        print("Sending command")
        self.focus()
        if self.disconnected():
            self.resolve_disconnections()
        self.send_buttons('START')
        countdown(2, 'Waiting 2 seconds for menu to appear')
        if not self.is_options_menu():
            self.send_buttons('b')
            self.cmd(command, timeout=timeout)
        else:
            self.send_multi_buttons(['x', 'y', 'LEFT_BUMPER', 'RIGHT_BUMPER'])
            self.send_buttons('UP', hold=1)
            self.send_buttons('a')
            if not self.input_dialog(command, timeout=timeout):
                print("Unable to send commands from input_dialog.")
                return
            self.send_buttons('RIGHT', hold=2)
            self.send_buttons('a', spread=0.2)
            self.send_buttons('START', spread=0.2)
            countdown(2, 'Waiting 2 seconds for menu to disappear')
            print(f"Command sent: {command}")

    def disconnected(self) -> bool:
        errors = []
        errors += self._driver.elements(tag='h1', class_starts_with='PureErrorPage')
        errors += self._driver.elements(tag='div', class_name_starts_with='ReconnectScreen - module__title___')
        errors += self._driver.elements(tag='button', class_starts_with="PopupScreen-module__button___")
        if self._driver.url() != "https://www.xbox.com/en-US/play/launch/ark-ultimate-survivor-edition/9N5JRWWGMS1R":
            errors += [self._driver.url()]
        return len(errors) > 0

    def resolve_disconnections(self, timeout=10) -> bool:
        print("Checking for any disconnection popups... ", end='')
        result = False
        if self.disconnected():
            print("Disconnected... trying to resolve")
            result = True
            self._driver.save_png(f'./cache/errors_resolve_{ArkWebsite.RESOLVE_INDEX}.png')
            ArkWebsite.RESOLVE_INDEX += 1
            self.continue_anyway(timeout=timeout)
            if self.disconnected():
                raise Exception("Unable to resolve an error: './cache/errors_resolve.png'")
            self.wait_for_loading()
        elif self._driver.url() != "https://www.xbox.com/en-US/play/launch/ark-ultimate-survivor-edition/9N5JRWWGMS1R":
            print("Current url is invalid. Rebooting.")
            self.reboot()
        else:
            print("All good, no disconnections")
        return result

    def send_buttons(self, *keys, hold=0.1, spread: float = 0):
        for key in keys:
            self.controller[key].press()
            self._driver.pause(hold)
            self.controller[key].release()
            self._driver.pause(spread)

    def send_multi_buttons(self, keys: list[str], hold=0.1, spread=0):
        for key in keys:
            self.controller[key].press()
        self._driver.pause(hold)
        for key in keys:
            self.controller[key].release()
        self._driver.pause(spread)

    def disable_mouse(self, timeout=0):
        self.focus()
        try:
            if not self._driver.elements(tag='div', id='click-to-enable-mouse-xmc', timeout=timeout):
                self._driver.send_button("ESCAPE")
            control = self._driver.element(tag='div', id='click-to-enable-mouse-xmc', timeout=timeout)
            attributes = control.attributes
            if 'class' in attributes and 'minimized' not in attributes['class']:
                self._driver.element(tag='div', class_name='minimize-btn', timeout=timeout).click()
        except Exception:
            pass

    def is_intro_menu(self):
        ocr = self.ocr()
        return ocr.is_intro_menu()

    def is_main_menu(self):
        ocr = self.ocr()
        return ocr.is_main_menu()

    def is_server_list(self):
        ocr = self.ocr()
        return ocr.is_server_list()

    def is_character_creation(self):
        ocr = self.ocr()
        return ocr.is_character_creation()

    def is_respawning(self):
        ocr = self.ocr()
        return ocr.is_respawning()

    def is_options_menu(self):
        ocr = self.ocr()
        return ocr.is_options_menu()

    def is_in_game(self):
        ocr = self.ocr()
        return ocr.is_in_game()

    def is_(self):
        ocr = self.ocr()
        return ocr.is_in_game()

    def focus(self):
        try:
            self._driver.element(tag='div', id='root').click()
        except Exception:
            pass

    def quit(self):
        self.dashboard_reset()
        self.close()


if __name__ == "__main__":
    server_name = get_server_name()
    if not server_name:
        raise Exception("Server name must be provided")
    options = {'dark_mode': True, 'profile_options': 9}
    window = {'width': 800, 'height': 800, 'x': -1000, 'y': 10}
    timeout = 2
    ark = None

    try:
        ark = ArkWebsite(**window, **options)
        ark.reboot()

        while True:
            print("""
                [1] Teleport to blue ob
                [2] Teleport to green ob
                [3] Teleport to red ob
                [4] Enter command
                [5] Enable admin
                [7] Main menu
                [8] Join Server
                [9] Reboot
                [0] Quit Game
            Select from any of the following above:
            """)
            value = input()
            if value == '1':
                ark.cmd('cheat tp blue')
            elif value == '2':
                ark.cmd('cheat tp green')
            elif value == '3':
                ark.cmd('cheat tp red')
            elif value == '4':
                ark.cmd(input("Enter the command: "))
            elif value == '5':
                ark.enable_admin()
            elif value == '7':
                ark.menu_reset()
            elif value == '8':
                ark.join_server()
            elif value == '9':
                ark.reboot()
            elif value == '0':
                ark.dashboard_reset()
            elif value == 'q' or value.lower() == 'quit':
                ark.quit()
                break
        Driver.destroy_all()
    except Exception as e:
        if ark:
            ark.quit()
        Driver.destroy_all()
        raise e
