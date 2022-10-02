import asyncio

import pytest
from model import *


def pytest_generate_tests(metafunc):
    metafunc.parametrize("mode", [
        Mode.REST,
        Mode.UI
    ], indirect=False, scope="session")


@pytest.mark.asyncio
async def test_status_cooking(app):
    order = await Order.new(**app)
    await order.get_status(**app)


@pytest.mark.asyncio
@pytest.mark.parametrize("status, app", [(OrderStatus.onTheWay, None), (OrderStatus.delivered, None)], indirect=["app"])
async def test_change_status(status, app: dict):
    order = await Order.new(**(app | {"mode": Mode.REST}))
    await order.update_status(new_status=status, **app)

