from selenium import webdriver
from arkcloud.web.driver.chrome import Options, Service


class Chrome:
    def __init__(self, **kwargs):
        service = Service()
        options = Options(**kwargs)
        self._driver = webdriver.Chrome(service=service.bind(), options=options.bind())
        self._kwargs = kwargs

    def bind(self):
        return self._driver

    def destroy(self):
        self._driver.quit()
        self._driver = None
        self._kwargs = None

    def exists(self):
        return self._driver is not None

    def __repr__(self):
        args = ', '.join([f"{k}={repr(v)}" for k, v in self._kwargs.items()])
        return f"""<Chrome({args})>"""
