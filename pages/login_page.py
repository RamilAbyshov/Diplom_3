from pages.base_page import BasePage
from locators.login_locators import LoginLocators
from src.data import URLs
import allure


class LoginPage(BasePage):
    @allure.step("Ввод email")
    def enter_email(self, email):
        self.type(LoginLocators.EMAIL_FIELD, email)
        return self

    @allure.step("Ввод пароля")
    def enter_password(self, password):
        self.type(LoginLocators.PASSWORD_FIELD, password)
        return self

    @allure.step("Клик кнопки логина")
    def click_login(self):
        self.click(LoginLocators.LOGIN_BUTTON)
        return self

    @allure.step("Выполнение логина")
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        self.wait_for_url_contains("/")
        return self

    @allure.step("Ожидание успешного логина")
    def wait_for_login_success(self):
        self.wait_for_url_to_be(URLs.CONSTRUCTOR)
        self.wait_for_document_ready()
        return self