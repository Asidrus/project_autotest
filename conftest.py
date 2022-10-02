import allure
import pytest
import aiohttp
import asyncio

from allure_commons.types import AttachmentType

from model import Mode
from webdriver import *


# @pytest
# def mode(request, meta)


@pytest.fixture(scope="session")
def session():
    session = aiohttp.ClientSession()
    yield session
    loop = asyncio.get_event_loop()
    loop.run_until_complete(session.close())


@pytest.fixture(scope="session")
def driver() -> WebDriver:
    driver = WebDriver(**webdriver_data)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(autouse=True, scope="session")
def app(mode, driver):
    session = aiohttp.ClientSession()
    yield {"mode": mode, "session": session, "driver": driver}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(session.close())


@pytest.fixture(scope="function")
def screenshot_on_failure(request, app):
    if app.get('mode') == Mode.UI and (request.node.rep_setup.failed or request.node.rep_call.failed):
        finalizer = lambda: allure.attach(app["driver"].get_screenshot_as_png(), attachment_type=AttachmentType.PNG)
        request.addfinalizer(finalizer)
