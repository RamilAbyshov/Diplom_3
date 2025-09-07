import pytest
from src.data import URLs
from utils.browser_factory import BrowserFactory
from src.helpers import create_test_user, delete_test_user
from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store_true", default=False)


@pytest.fixture
def browser_name(request):
    return request.config.getoption("--browser")


@pytest.fixture
def headless(request):
    return request.config.getoption("--headless")


@pytest.fixture
def driver(browser_name, headless):
    driver = BrowserFactory.get_driver(browser_name, headless)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def test_user():
    user_data = create_test_user()
    try:
        yield user_data
    finally:
        delete_test_user(user_data)


@pytest.fixture
def logged_in_user(driver, test_user):
    login_page = LoginPage(driver, URLs.LOGIN)
    login_page.login(test_user["email"], test_user["password"])
    login_page.wait_for_login_success()
    yield test_user