from ..form import *


class OrderModal(BaseForm):

    def send(self, address: str, phone: str):
        self.address.send_keys(address)
        self.phone.send_keys(phone)
        self.btn_order.click()
        return self

    def close_modal(self) -> None:
        xpath = "//button[@class='btn-close']"
        self.find_element_by_xpath(xpath).click()

    @property
    def address(self) -> WebElement:
        xpath = "//input[@name='address']"
        return self.find_element_by_xpath(xpath)

    @property
    def phone(self) -> WebElement:
        xpath = "//input[@name='phone']"
        return self.find_element_by_xpath(xpath)

    @property
    def btn_order(self) -> WebElement:
        xpath = "//button[@id='request']"
        return self.find_element_by_xpath(xpath)
