from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from src.data import Timeouts
import allure


class BasePage:
    def __init__(self, driver, url=None):
        self.driver = driver
        if url:
            self.driver.get(url)
            self.wait_for_document_ready()

    @allure.step("Клик по элементу")
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
            self.driver.execute_script("arguments[0].click();", element)
        return self

    @allure.step("Безопасный клик")
    def safe_click(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        self.driver.execute_script("arguments[0].click();", element)
        return self

    @allure.step("Ввод текста")
    def type(self, locator, text, timeout=Timeouts.ELEMENT_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)
        return self

    @allure.step("Проверка видимости элемента")
    def is_visible(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Получение текущего URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Ожидание URL содержащего часть")
    def wait_for_url_contains(self, url_part, timeout=Timeouts.PAGE_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(url_part)
        )
        return self

    @allure.step("Ожидание конкретного URL")
    def wait_for_url_to_be(self, url, timeout=Timeouts.PAGE_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.url_to_be(url)
        )
        return self

    @allure.step("Ожидание готовности документа")
    def wait_for_document_ready(self, timeout=Timeouts.PAGE_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return self

    @allure.step("Обновление страницы")
    def refresh_page(self):
        self.driver.refresh()
        self.wait_for_document_ready()
        return self

    @allure.step("Переход по URL")
    def navigate_to(self, url):
        self.driver.get(url)
        self.wait_for_document_ready()
        return self

    @allure.step("Закрытие модального окна")
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

    @allure.step("Проверка видимости модального окна")
    def is_modal_visible(self, modal_locator):
        try:
            return self.is_visible(modal_locator, timeout=Timeouts.ELEMENT_TIMEOUT)
        except TimeoutException:
            return False

    @allure.step("Поиск элемента")
    def find_element(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Поиск всех элементов")
    def find_elements(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    @allure.step("Ожидание видимости элемента")
    def wait_for_visibility(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Получение текста элемента")
    def get_text(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        element = self.wait_for_visibility(locator, timeout)
        return element.text.strip()

    @allure.step("Проверка отображения элемента")
    def is_element_displayed(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        try:
            element = self.wait_for_visibility(locator, timeout)
            return element.is_displayed()
        except:
            return False

    @allure.step("Ожидание видимости всех элементов")
    def wait_for_visibility_all(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

    @allure.step("Ожидание элемента (оригинальная логика)")
    def wait_for_element_original(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Ожидание видимости элемента (оригинальная логика)")
    def wait_for_visibility_original(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Поиск элементов (оригинальная логика)")
    def find_elements_original(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    @allure.step("Ожидание элемента с кастомными условиями")
    def wait_for_element_custom(self, condition, timeout=Timeouts.ELEMENT_TIMEOUT, *args):
        return WebDriverWait(self.driver, timeout).until(condition(*args))

    @allure.step("Ожидание видимости элемента по локатору")
    def wait_for_visibility_custom(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Ожидание наличия элемента по локатору")
    def wait_for_presence_custom(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Ожидание видимости всех элементов по локатору")
    def wait_for_visibility_all_custom(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

    @allure.step("Ожидание кастомного условия")
    def wait_for_custom_condition(self, condition, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(condition)

    @allure.step("Ожидание элемента по локатору с кастомным таймаутом")
    def wait_for_element_with_timeout(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Ожидание видимости элемента по локатору с кастомным таймаутом")
    def wait_for_visibility_with_timeout(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Ожидание кликабельности элемента")
    def wait_for_element_clickable(self, element, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(element)
        )

    @allure.step("Ожидание условия с кастомным таймаутом")
    def wait_for_condition_with_timeout(self, condition, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(condition)

    @allure.step("Ожидание невидимости элемента по локатору")
    def wait_for_invisibility(self, locator, timeout=Timeouts.ELEMENT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )