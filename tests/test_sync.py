import pytest

from model import *


def pytest_generate_tests(metafunc):
    metafunc.parametrize("mode", [
        Mode.REST,
        Mode.UI
    ], indirect=False, scope="session")


def test_status_cooking(app):
    order = Order.new_sync(**app)
    order.get_status_sync(**app)


@pytest.mark.parametrize("status, app", [(OrderStatus.onTheWay, None), (OrderStatus.delivered, None)], indirect=["app"])
def test_change_status(status, app: dict):
    order = Order.new_sync(**(app | {"mode": Mode.REST}))
    order.update_status_sync(new_status=status, **app)