from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from locators.order_feed_locators import OrderFeedLocators
from pages.base_page import BasePage
from src.data import URLs, Timeouts
import allure


class OrderFeedPage(BasePage):
    def __init__(self, driver, url=URLs.ORDER_FEED):
        super().__init__(driver, url)

    @allure.step("Поиск заказа по номеру")
    def find_order_by_any_format(self, order_number):
        formats_to_try = [f"#{order_number}", f"#0{order_number}", f"0{order_number}", order_number]

        for number_format in formats_to_try:
            try:
                order_locator = (OrderFeedLocators.ORDER_BY_NUMBER[0],
                                 OrderFeedLocators.ORDER_BY_NUMBER[1].format(number_format))

                order_element = self.wait_for_visibility_with_timeout(order_locator, timeout=Timeouts.ELEMENT_TIMEOUT)

                if order_element.is_displayed():
                    return order_element
            except:
                continue
        return None

    @allure.step("Клик по заказу по номеру")
    def click_order_by_number(self, order_number):
        try:
            order_element = self.find_order_by_any_format(order_number)
            if not order_element:
                return False

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", order_element)
            self.wait_for_element_clickable(order_element)
            self.driver.execute_script("arguments[0].click();", order_element)
            self.wait_for_visibility_with_timeout(OrderFeedLocators.ORDER_MODAL)

            return True

        except Exception as e:
            print(f"Error clicking order {order_number}: {e}")
            return False

    @allure.step("Проверка видимости модального окна заказа")
    def is_order_modal_visible(self, timeout=Timeouts.MODAL_TIMEOUT):
        locators_to_try = [
            OrderFeedLocators.ORDER_MODAL,
            OrderFeedLocators.ORDER_MODAL_ALTERNATIVE,
            OrderFeedLocators.ORDER_MODAL_OVERLAY
        ]

        for locator in locators_to_try:
            try:
                element = self.wait_for_visibility_with_timeout(locator, timeout=timeout / len(locators_to_try))
                if element.is_displayed():
                    return True
            except:
                continue
        return False

    @allure.step("Навигация из конструктора")
    def navigate_from_constructor(self):
        from pages.constructor_page import ConstructorPage
        constructor_page = ConstructorPage(self.driver, URLs.CONSTRUCTOR)
        constructor_page.wait_for_constructor_ready()
        constructor_page.click_order_feed_link()
        self.wait_for_page_load()
        return self

    @allure.step("Ожидание заказа из конструктора")
    def wait_for_order_from_constructor(self, timeout=Timeouts.ORDER_TIMEOUT):
        from pages.constructor_page import ConstructorPage
        constructor_page = ConstructorPage(self.driver, URLs.CONSTRUCTOR)
        order_number = constructor_page.make_order()
        real_order_number = constructor_page.wait_for_real_order_number()
        constructor_page.close_constructor_modal()
        self.navigate_to(URLs.ORDER_FEED)
        self.wait_for_page_load()
        assert self.wait_for_order_in_feed(real_order_number, timeout), f"Заказ {real_order_number} не появился в ленте"
        return real_order_number

    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_load(self, timeout=Timeouts.ELEMENT_TIMEOUT):
        self.wait_for_visibility(OrderFeedLocators.PAGE_TITLE, timeout)
        return self


    @allure.step("Ожидание заказа в ленте")
    def wait_for_order_in_feed(self, order_number, timeout=Timeouts.ORDER_TIMEOUT):
        try:
            self.wait_for_custom_condition(
                lambda driver: self.find_order_by_any_format(order_number) is not None,
                timeout
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидание заказа в разделе 'В работе'")
    def wait_for_order_in_progress(self, order_number, timeout=Timeouts.ORDER_TIMEOUT):
        expected_formats = [f"0{order_number}", str(order_number)]
        try:
            self.wait_for_custom_condition(
                lambda driver: any(format in number for number in self.get_orders_in_progress_numbers()
                                   for format in expected_formats),
                timeout
            )
            return True
        except TimeoutException:
            return False


    @allure.step("Получение номеров заказов в работе")
    def get_orders_in_progress_numbers(self):
        try:
            number_elements = self.find_elements(OrderFeedLocators.ORDERS_IN_PROGRESS_NUMBERS)
            return [element.text.strip() for element in number_elements if element.is_displayed() and element.text.strip()]
        except Exception:
            return []


    @allure.step("Получение общего количества выполненных заказов")
    def get_orders_done_total(self):
        try:
            elements = self.find_elements(OrderFeedLocators.ORDERS_DONE_TOTAL)
            if elements:
                return int(elements[0].text) if elements[0].text.isdigit() else 0
            return 0
        except:
            return 0

    @allure.step("Закрытие модального окна заказа")
    def close_order_modal(self):
        try:
            from selenium.webdriver.common.keys import Keys
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            return True
        except:
            return False