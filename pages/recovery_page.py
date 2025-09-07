from locators.recovery_locators import RecoveryLocators
from pages.base_page import BasePage
import allure


class RecoveryPage(BasePage):
    @allure.step("Переход к восстановлению пароля")
    def go_to_recovery(self):
        self.click(RecoveryLocators.RECOVERY_LINK)

    @allure.step("Ввод email")
    def type_email(self, email):
        self.type(RecoveryLocators.EMAIL_FIELD, email)

    @allure.step("Отправка восстановления")
    def submit_recovery(self):
        self.click(RecoveryLocators.RECOVERY_BUTTON)

    @allure.step("Получение видимого поля пароля")
    def get_password_field_visible(self):
        return self.is_visible(RecoveryLocators.PASSWORD_FIELD_VISIBLE)

    @allure.step("Клик показать пароль")
    def click_show_password(self):
        self.click(RecoveryLocators.SHOW_PASSWORD_ICON)

    @allure.step("Проверка активности поля пароля")
    def is_password_field_active(self):
        field = self.get_password_field_visible()
        active_element = self.driver.switch_to.active_element
        return field == active_element