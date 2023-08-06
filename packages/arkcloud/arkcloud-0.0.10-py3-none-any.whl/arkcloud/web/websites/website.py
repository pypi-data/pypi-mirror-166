from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse
from arkcloud.web import Driver
from collections import defaultdict


class Website:
    WEBSITES = defaultdict(dict)
    __INDEX = 0

    def __init__(self, url: str, remote=False, dark_mode=False, x=None, y=None, width=None, height=None, profile=None, **kwargs):
        self.__id: int = Website.__INDEX
        Website.__INDEX += 1
        self.__kwargs = kwargs
        arguments = {
            'remote_options': remote,
            'dark_mode_options': dark_mode,
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'profile_options': profile,
            **kwargs}
        self._driver = Driver.new(**arguments)
        if "about_blank" in self._driver.tabs:
            self._driver.switch_tab("about_blank")
            self.get(url)
        else:
            self._driver.new_tab(url=url)

    def bind(self):
        if self._driver:
            return self._driver.bind()

    def domain(self):
        if self._driver:
            return self._driver.domain()

    def url(self):
        if self._driver and self._driver.bind():
            return self.bind().current_url

    def focus(self):
        if self._driver:
            self._driver.switch_tab(self._driver.domain())

    def reload(self):
        if self._driver and self._driver.bind():
            self.focus()
            self.bind().refresh()

    def back(self):
        if self._driver and self._driver.bind():
            self.bind().back()

    def forward(self):
        if self._driver and self._driver.bind():
            self.bind().forward()

    def vertical_scroll(self, amount: int):
        if self._driver and self._driver.bind():
            action = ActionChains(self.bind())
            action.scroll_by_amount(amount, 0).perform()

    def horizontal_scroll(self, amount: int):
        if self._driver and self.bind():
            action = ActionChains(self.bind())
            action.scroll_by_amount(0, amount).perform()

    def captcha(self, timeout=30):
        if not self._driver:
            return False
        while self._driver.execute_script("return document.readyState;") != 'complete':
            self._driver.pause(0.3)
        handle = self.bind().current_window_handle
        try:
            for frame in self._driver.elements('iframe'):
                url = urlparse(frame.get_attribute('src'))
                if 'captcha' in url.netloc:
                    if 'geo' in url.netloc:
                        frame.wait_until_disappear(timeout=timeout)
                    else:
                        self._driver.switch_to(frame)
                        self._driver.element('div', id='checkbox', **{'aria-checked': 'true'}, timeout=timeout)
                        self.bind().switch_to.window(handle)
                    return True
            return False
        except TimeoutException as e:
            self.bind().switch_to.window(handle)
            e.msg = f"\n[CAPTCHA TIMEOUT]: Captcha challenge was not completed within {timeout} seconds."
            raise e

    def get(self, url):
        if self.bind():
            self._driver.get(url)
        return self

    def close(self):
        if self._driver:
            self._driver.close_tab()
        self._driver = None

    def __str__(self):
        s = f"""<Website>\n"""
        for i, (name, value) in enumerate(self.__kwargs.items()):
            s += f"\t[{i}]  {name} = {value}\n"
        s += "</Website>\n"
        return s

    def __repr__(self):
        args = ','.join([f"{k}={repr(v)}" for k, v in self.__kwargs.items()])
        return f"<Website({args})>"


if __name__ == "__main__":
    window = {'width': 800, 'height': 800, 'x': -1000, 'y': 10}
    web = Website("https://www.google.com", dark_mode=True, **window)
    print(web)
    print(repr(web))
    print(web.domain())
    web.close()

