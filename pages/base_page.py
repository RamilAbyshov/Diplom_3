from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from src.data import Timeouts


class BasePage:
    def __init__(self, driver, url=None):
        self.driver = driver
        if url:
            self.driver.get(url)
            self.wait_for_document_ready()

    def click(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

        WebDriverWait(self.driver, timeout).until(
            lambda d: element.is_displayed() and element.is_enabled()
        )

        try:
            element.click()
        except:
            # Если обычный клик не работает, используется JavaScript
            self.driver.execute_script("arguments[0].click();", element)

        return self

    def safe_click(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def type(self, locator, text, timeout=Timeouts.ELEMENT_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)
        return self

    def is_visible(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def get_current_url(self):
        return self.driver.current_url

    def wait_for_url_contains(self, url_part, timeout=Timeouts.PAGE_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(url_part)
        )
        return self

    def wait_for_url_to_be(self, url, timeout=Timeouts.PAGE_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.url_to_be(url)
        )
        return self

    def wait_for_document_ready(self, timeout=Timeouts.PAGE_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return self

    def refresh_page(self):
        self.driver.refresh()
        self.wait_for_document_ready()
        return self

    def navigate_to(self, url):
        self.driver.get(url)
        self.wait_for_document_ready()
        return self

    def close_modal(self, close_locator, modal_locator):
        try:
            close_button = WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.element_to_be_clickable(close_locator)
            )
            self.driver.execute_script("arguments[0].click();", close_button)

            WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.invisibility_of_element_located(modal_locator)
            )
            return True
        except Exception:
            return False

    def is_modal_visible(self, modal_locator):
        try:
            return self.is_visible(modal_locator, timeout=Timeouts.ELEMENT_TIMEOUT)
        except TimeoutException:
            return False