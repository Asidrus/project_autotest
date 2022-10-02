from webdriver import *
from forms import *


def main():
    driver = WebDriver(**webdriver_data)
    driver.maximize_window()
    form = OrderForm(driver)
    form.get("http://localhost:8000/order")
    id = form.new(pizza="Pepperoni", address="лубянка", phone="81234567890")
    print(id)


if __name__ == "__main__":
    main()
