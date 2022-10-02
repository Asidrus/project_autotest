from selenium.webdriver.remote.webelement import WebElement as _webelement_
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException

from time import time, sleep

from .config import *

from .waiting import waiting


class WebElement(_webelement_):

    def __init__(self, webelement: _webelement_):
        self.__dict__.update(webelement.__dict__)

    def find_elements(self, by=By.XPATH, value=None, timeout=TIMEOUT, steptime=STEPTIME, check=False) -> list[
        _webelement_]:
        start = time()
        last_error = None
        while time() - start < timeout:
            try:
                elements = super().find_elements(by, value)
                if not elements:
                    raise NoSuchElementException(f'For selector {by=} and {value=} couldn`t find any element')
                sleep(SLEEP_AFTER)
                return [WebElement(element) for element in elements]
            except NoSuchElementException as e:
                last_error = e
                sleep(steptime)
        if check:
            return [None]
        else:
            raise last_error

    def find_element(self, by=By.XPATH, value=None, timeout=TIMEOUT, steptime=STEPTIME, check=False) -> _webelement_:
        return self.find_elements(by, value, timeout, steptime, check)[0]

    def find_elements_by_xpath(self, xpath: str, timeout=TIMEOUT, steptime=STEPTIME, check=False) -> list[_webelement_]:
        return self.find_elements(By.XPATH, xpath, timeout, steptime, check)

    def find_element_by_xpath(self, xpath: str, timeout=TIMEOUT, steptime=STEPTIME, check=False) -> _webelement_:
        return self.find_element(By.XPATH, xpath, timeout, steptime, check)

    @waiting()
    def click(self, **kwargs):
        super().click()

    @waiting()
    def send_keys(self, *value, step=0, clear=True, **kwargs) -> None:
        value = "".join(value)
        if clear:
            self.clear()
            sleep(SLEEP_AFTER)
        if step == 0:
            super().send_keys(value)
        else:
            for sym in value:
                super().send_keys(sym)
                sleep(step)
        sleep(SLEEP_AFTER)
