from locators.recovery_locators import RecoveryLocators
from pages.base_page import BasePage


class RecoveryPage(BasePage):
    def go_to_recovery(self):
        self.click(RecoveryLocators.RECOVERY_LINK)

    def type_email(self, email):
        self.type(RecoveryLocators.EMAIL_FIELD, email)

    def submit_recovery(self):
        self.click(RecoveryLocators.RECOVERY_BUTTON)

    def get_password_field_visible(self):
        return self.is_visible(RecoveryLocators.PASSWORD_FIELD_VISIBLE)

    def click_show_password(self):
        self.click(RecoveryLocators.SHOW_PASSWORD_ICON)

    def is_password_field_active(self):
        field = self.get_password_field_visible()
        active_element = self.driver.switch_to.active_element
        return field == active_element