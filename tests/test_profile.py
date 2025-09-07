import allure
from src.data import URLs
from pages.profile_page import ProfilePage


@allure.feature("Личный кабинет")
class TestProfile:

    @allure.title("Переход в личный кабинет без авторизации")
    def test_navigate_to_profile_unauthenticated(self, driver):
        profile_page = ProfilePage(driver, URLs.CONSTRUCTOR)
        profile_page.navigate_to_profile_unauthenticated()
        assert profile_page.wait_for_url_to_be(URLs.LOGIN)
        assert profile_page.get_current_url() == URLs.LOGIN

    @allure.title("Переход в личный кабинет после авторизации")
    def test_navigate_to_profile_authenticated(self, driver, logged_in_user):
        profile_page = ProfilePage(driver, URLs.CONSTRUCTOR)
        profile_page.navigate_to_profile()
        assert profile_page.wait_for_url_to_be(URLs.PROFILE)
        assert profile_page.get_current_url() == URLs.PROFILE

    @allure.title("Выход из аккаунта")
    def test_logout(self, driver, logged_in_user):
        profile_page = ProfilePage(driver, URLs.CONSTRUCTOR)
        profile_page.navigate_to_profile()
        profile_page.wait_for_profile_page()

        profile_page.click_logout()
        assert profile_page.wait_for_url_to_be(URLs.LOGIN)
        assert profile_page.get_current_url() == URLs.LOGIN