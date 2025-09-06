from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage
from locators.profile_locators import ProfileLocators
from locators.common_locators import CommonLocators
from selenium.webdriver.support import expected_conditions as EC
from src.data import Timeouts


class ProfilePage(BasePage):

    def navigate_to_profile(self):
        self.click(CommonLocators.PROFILE_LINK)
        self.wait_for_profile_page()
        return self

    def navigate_to_profile_unauthenticated(self):
        self.click(CommonLocators.PROFILE_LINK)
        return self

    def click_order_history(self):
        self.click(ProfileLocators.ORDER_HISTORY_LINK)
        return self

    def click_logout(self):
        self.click(ProfileLocators.LOGOUT_BUTTON)
        return self

    def get_order_numbers_from_history(self, timeout=Timeouts.ELEMENT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(ProfileLocators.ORDER_HISTORY_LIST)
            )

            order_number_elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(ProfileLocators.ORDER_TEXT_BOX)
            )

            order_numbers = []
            for element in order_number_elements:
                if element.is_displayed() and element.text.strip():
                    number_text = element.text.strip().replace('#', '')
                    if number_text.isdigit() and len(number_text) >= 6:
                        order_numbers.append(number_text)
            return order_numbers

        except Exception:
            return []

    def wait_for_profile_page(self, timeout=Timeouts.ELEMENT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains("/account/profile")
            )

            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(ProfileLocators.PROFILE_NAV)
            )

            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return self

        except TimeoutException:
            raise TimeoutException("Страница профиля не загрузилась")