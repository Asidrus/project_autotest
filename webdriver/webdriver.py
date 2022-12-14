from time import time, sleep

from selenium import webdriver
from selenium.webdriver import Chrome, Firefox, ChromeOptions, FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from .webelement import WebElement
from .config import *
from config import *


window_size = (1920, 1080)

""" choose type of webdriver class """
options = None
command_executor = None
if BROWSER == "Chrome":
    _webdriver_ = webdriver.Chrome
    options = webdriver.ChromeOptions()
elif BROWSER == "Firefox":
    _webdriver_ = webdriver.Firefox
    options = webdriver.FirefoxOptions()
elif BROWSER == "Edge":
    _webdriver_ = webdriver.Edge
    options = webdriver.EdgeOptions()
else:
    raise Exception(f'Browser type "{BROWSER}" doesn`t exist. Use "Chrome" or "Firefox"')
if REMOTE:
    _webdriver_ = webdriver.Remote
    command_executor = f"http://{WEBDRIVER_IP}:{WEBDRIVER_PORT}/wd/hub"

""" make options"""
options.add_argument(f"window-size={window_size[0]}x{window_size[1]}")
# options.capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}  # Включить логи
if not INTERACTIVE_MODE:
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--width={window_size[0]}")
    options.add_argument(f"--height={window_size[1]}")

"prepare kwargs for initial driver"
webdriver_data = {
    "options": options,
    "desired_capabilities": options.capabilities,
    "command_executor": command_executor,
    "executable_path": WEBDRIVER_PATH,
}


class WebDriver(_webdriver_):

    def __init__(self, options: [ChromeOptions, FirefoxOptions],
                 desired_capabilities,
                 command_executor: [str, None] = None,
                 executable_path: str = None):
        if command_executor:
            super().__init__(options=options, desired_capabilities=desired_capabilities,
                             command_executor=command_executor)
        elif executable_path:
            super().__init__(executable_path, options=options, desired_capabilities=desired_capabilities)
        else:
            super().__init__(options=options, desired_capabilities=desired_capabilities)

    def find_elements(self, by=By.XPATH, value=None, timeout=TIMEOUT, steptime=STEPTIME, check=False) -> list[WebElement]:
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

    def find_element(self, by=By.XPATH, value=None, timeout=TIMEOUT, steptime=STEPTIME, check=False) -> WebElement:
        return self.find_elements(by, value, timeout, steptime, check)[0]

    def find_elements_by_xpath(self, xpath: str, timeout=TIMEOUT, steptime=STEPTIME, check=False) -> list[WebElement]:
        return self.find_elements(By.XPATH, xpath, timeout, steptime, check)

    def find_element_by_xpath(self, xpath: str, timeout=TIMEOUT, steptime=STEPTIME, check=False) -> WebElement:
        return self.find_element(By.XPATH, xpath, timeout, steptime, check)
