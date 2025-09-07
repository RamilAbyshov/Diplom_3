import allure
from src.data import URLs
from pages.recovery_page import RecoveryPage


@allure.feature("Восстановление пароля")
class TestPasswordRecovery:

    @allure.title("Переход на страницу восстановления пароля")
    def test_navigate_to_recovery_page(self, driver):
        recovery_page = RecoveryPage(driver, URLs.LOGIN)
        recovery_page.go_to_recovery()
        recovery_page.wait_for_url_to_be(URLs.FORGOT_PASSWORD)
        assert recovery_page.get_current_url() == URLs.FORGOT_PASSWORD

    @allure.title("Ввод почты и восстановление пароля")
    def test_recovery_with_email(self, driver, test_user):
        recovery_page = RecoveryPage(driver, URLs.FORGOT_PASSWORD)
        recovery_page.type_email(test_user["email"])
        recovery_page.submit_recovery()
        recovery_page.wait_for_url_to_be(URLs.RESET_PASSWORD)
        assert recovery_page.get_current_url() == URLs.RESET_PASSWORD

    @allure.title("Клик по иконке показать/скрыть пароль делает поле активным")
    def test_password_visibility_toggle(self, driver, test_user):
        recovery_page = RecoveryPage(driver, URLs.FORGOT_PASSWORD)
        recovery_page.type_email(test_user["email"])
        recovery_page.submit_recovery()
        recovery_page.wait_for_url_to_be(URLs.RESET_PASSWORD)
        recovery_page.click_show_password()
        assert recovery_page.is_password_field_active()