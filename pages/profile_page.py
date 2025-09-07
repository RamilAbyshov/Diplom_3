from selenium.common import TimeoutException
from pages.base_page import BasePage
from locators.profile_locators import ProfileLocators
from locators.common_locators import CommonLocators
from src.data import Timeouts, URLs
import allure


class ProfilePage(BasePage):
    @allure.step("Переход в профиль")
    def navigate_to_profile(self):
        self.click(CommonLocators.PROFILE_LINK)
        self.wait_for_profile_page()
        return self

    @allure.step("Переход в профиль без авторизации")
    def navigate_to_profile_unauthenticated(self):
        self.click(CommonLocators.PROFILE_LINK)
        return self

    @allure.step("Выход из аккаунта")
    def click_logout(self):
        self.click(ProfileLocators.LOGOUT_BUTTON)
        return self

    @allure.step("Ожидание загрузки страницы профиля")
    def wait_for_profile_page(self, timeout=Timeouts.ELEMENT_TIMEOUT):
        try:
            self.wait_for_url_contains(URLs.PROFILE, timeout)
            self.wait_for_visibility_custom(ProfileLocators.PROFILE_NAV, timeout)
            self.wait_for_document_ready(timeout)
            return self
        except TimeoutException:
            raise TimeoutException("Страница профиля не загрузилась")