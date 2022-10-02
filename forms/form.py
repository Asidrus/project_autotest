from webdriver import *


class BaseForm(WebDriver):

    def __init__(self, driver):
        self.__dict__.update(driver.__dict__)