import aiohttp
import requests
from pydantic import BaseModel
from enum import Enum
from bs4 import BeautifulSoup

from config import WEBSITE_URL

from session.session import waiting, waiting_sync, step
from .mode import Mode
from forms import OrderForm


class OrderStatus(Enum):
    cooking = "cooking"
    onTheWay = "on the way"
    delivered = "delivered"


class Order(BaseModel):
    id: int
    status: OrderStatus
    address: str
    phone: str
    pizza: str

    @staticmethod
    # @step("Создание нового заказа", "Заказ создан")
    async def new(address="default address", phone='81234567890', pizza="Pepperoni", **kwargs):
        if kwargs.get("mode") == Mode.UI:
            id, status = OrderForm(kwargs["driver"]).new(address=address, phone=phone, pizza=pizza)
        else:
            session = kwargs["session"] if kwargs.get("session") else aiohttp.ClientSession()
            async with session.get(WEBSITE_URL+"/order") as response:
                token = response.cookies.get("csrftoken").value
                text = await response.text()
                soup = BeautifulSoup(text, "lxml")
                tag = soup.find("input", attrs={"name": "csrfmiddlewaretoken"})
                middle_token = tag.get("value")
            async with session.post(WEBSITE_URL+"/order/buy", cookies={"csrftoken": token},
                                    data={
                                        "csrfmiddlewaretoken": middle_token,
                                        "address": address,
                                        "phone": phone,
                                        "pizza": pizza,
                                    }) as response:
                body = await response.json()
                assert response.status == 200
                id = body["orderID"]
                status = body["status"]
            if not kwargs.get("session"):
                await session.close()

        assert status == "cooking", "Incorrect status of order"
        assert type(id) is int, "Incorrect type orderID in order"
        return Order(id=id, status=OrderStatus[status], address=address, phone=phone, pizza=pizza)

    async def update_status(self, new_status: OrderStatus, **kwargs) -> None:
        session = kwargs["session"] if kwargs.get("session") else aiohttp.ClientSession()
        async with session.post(WEBSITE_URL+"/order/updateStatus",
                                data={"orderID": self.id, "status": new_status}) as response:
            assert response.status == 200
        self.status = new_status
        await self.get_status(**kwargs)
        if not kwargs.get("session"):
            await session.close()

    @waiting()
    async def get_status(self, *args, **kwargs):
        if kwargs.get("mode") == Mode.UI:
            status = OrderForm(kwargs["driver"]).get_status(self.id)
        else:
            session = kwargs["session"] if kwargs.get("session") else aiohttp.ClientSession()
            async with session.get(WEBSITE_URL + f"/order/getStatus?orderID={self.id}") as response:
                body = await response.json()
            status = body["status"]
            if not kwargs.get("session"):
                await session.close()
        assert self.status == OrderStatus(status)

    # sync methods

    @staticmethod
    def new_sync(address="default address", phone='81234567890', pizza="Pepperoni", **kwargs):
        if kwargs.get("mode") == Mode.UI:
            id, status = OrderForm(kwargs["driver"]).new(address=address, phone=phone, pizza=pizza)
        else:
            session = kwargs["session"] if kwargs.get("session") else requests.session()
            response = session.get(WEBSITE_URL + "/order")
            token = response.cookies.get("csrftoken").value
            soup = BeautifulSoup(response.text, "lxml")
            tag = soup.find("input", attrs={"name": "csrfmiddlewaretoken"})
            middle_token = tag.get("value")
            response = session.post(WEBSITE_URL + "/order/buy", cookies={"csrftoken": token},
                         data={
                             "csrfmiddlewaretoken": middle_token,
                             "address": address,
                             "phone": phone,
                             "pizza": pizza,
                         })
            assert response.status_code == 200
            json = response.json()
            id = json["orderID"]
            status = json["status"]
            if not kwargs.get("session"):
                session.close()

        assert status == "cooking", "Incorrect status of order"
        assert type(id) is int, "Incorrect type orderID in order"
        return Order(id=id, status=OrderStatus[status], address=address, phone=phone, pizza=pizza)

    def update_status_sync(self, new_status: OrderStatus, **kwargs) -> None:
        session = kwargs["session"] if kwargs.get("session") else requests.session()
        response = session.post(WEBSITE_URL+"/order/updateStatus", data={"orderID": self.id, "status": new_status})
        assert response.status_code == 200
        self.status = new_status
        self.get_status_sync(**kwargs)
        if not kwargs.get("session"):
            session.close()

    @waiting_sync()
    def get_status_sync(self, *args, **kwargs):
        if kwargs.get("mode") == Mode.UI:
            status = OrderForm(kwargs["driver"]).get_status(self.id)
        else:
            session = kwargs["session"] if kwargs.get("session") else requests.session()
            response = session.get(WEBSITE_URL + f"/order/getStatus?orderID={self.id}")
            json = response.json()
            status = json["status"]
            if not kwargs.get("session"):
                session.close()
        assert self.status == OrderStatus(status)


async def main():
    order = await Order.new()
    await order.update_status(OrderStatus.onTheWay)


if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
