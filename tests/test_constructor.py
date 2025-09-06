import allure
import pytest
from src.data import URLs
from pages.constructor_page import ConstructorPage


@allure.feature("Основной функционал")
class TestConstructor:

    @allure.title("Переход на конструктор со страниц не требующих авторизации")
    @pytest.mark.parametrize("start_url", [URLs.ORDER_FEED, URLs.LOGIN])
    def test_navigate_to_constructor_from_unprotected_pages(self, driver, start_url):
        constructor_page = ConstructorPage(driver, start_url)
        constructor_page.click_constructor_link()
        assert constructor_page.wait_for_url_to_be(URLs.CONSTRUCTOR)
        assert constructor_page.get_current_url() == URLs.CONSTRUCTOR

    @allure.title("Переход на конструктор со страницы профиля")
    def test_navigate_to_constructor_from_profile_page(self, driver, logged_in_user):
        constructor_page = ConstructorPage(driver, URLs.PROFILE)
        constructor_page.wait_for_constructor_ready()
        constructor_page.click_constructor_link()
        assert constructor_page.wait_for_url_to_be(URLs.CONSTRUCTOR)
        assert constructor_page.get_current_url() == URLs.CONSTRUCTOR

    @allure.title("Переход в ленту заказов")
    def test_navigate_to_order_feed(self, driver):
        constructor_page = ConstructorPage(driver, URLs.CONSTRUCTOR)
        constructor_page.click_order_feed_link()
        assert constructor_page.wait_for_url_to_be(URLs.ORDER_FEED)
        assert constructor_page.get_current_url() == URLs.ORDER_FEED

    @allure.title("Открытие модального окна с деталями ингредиента")
    def test_open_ingredient_modal(self, driver):
        constructor_page = ConstructorPage(driver, URLs.CONSTRUCTOR)
        constructor_page.click_ingredient()
        assert constructor_page.is_modal_visible()

    @allure.title("Закрытие модального окна с деталями ингредиента")
    def test_close_ingredient_modal(self, driver):
        constructor_page = ConstructorPage(driver, URLs.CONSTRUCTOR)
        constructor_page.click_ingredient()
        assert constructor_page.is_modal_visible()
        constructor_page.close_constructor_modal()
        assert not constructor_page.is_modal_visible()

    @allure.title("Добавление ингредиента в конструктор")
    def test_add_ingredient_to_constructor(self, driver):
        constructor_page = ConstructorPage(driver, URLs.CONSTRUCTOR)
        constructor_page.wait_for_constructor_ready()

        success = constructor_page.add_bun_to_constructor()
        assert success, "Не удалось добавить ингредиент"

        counter = constructor_page.get_bun_counter()
        assert counter == 2, f"Ожидался счетчик 2, получен {counter}"

    @allure.title("Оформление заказа авторизованным пользователем")
    def test_make_order_authenticated(self, driver, logged_in_user):
        constructor_page = ConstructorPage(driver, URLs.CONSTRUCTOR)

        previous_order_number = constructor_page.make_order()
        order_number = constructor_page.wait_for_real_order_number()

        assert int(order_number) > int(previous_order_number)

        constructor_page.close_constructor_modal()