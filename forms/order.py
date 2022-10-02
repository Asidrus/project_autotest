from .form import *
from .objects import *
import re
from webdriver.waiting import waiting as wait
from config import WEBSITE_URL


class OrderForm(BaseForm):

    def __init__(self, driver):
        super().__init__(driver)
        self.get(WEBSITE_URL+"/order")

    def new(self, **kwargs):
        self.btn_choose_by_pizza_name(kwargs["pizza"]).click()
        OrderModal(self).send(kwargs["address"], kwargs["phone"]).close_modal()
        return self.id(), self.status()

    def btn_choose_by_pizza_name(self, name: str) -> WebElement:
        xpath = f"//button[@data-pizza='{name}']"
        return self.find_element_by_xpath(xpath)

    @wait()
    def id(self) -> int:
        xpath = "//p[@id='order-number']"
        element = self.find_element_by_xpath(xpath, timeout=.5)
        id_str = "".join(re.findall(r"[(0-9)]*", element.text))
        if not id_str:
            raise Exception("ID is None")
        else:
            return int(id_str)

    @wait()
    def status(self) -> str:
        xpath = "//p[@id='order-status']"
        element = self.find_element_by_xpath(xpath)
        return element.text.split(": ")[-1]

    def get_status(self, order_id: int):
        self.delete_all_cookies()
        self.add_cookie({"name": "orderID", "value": str(order_id)})
        self.refresh()
        return self.status()


