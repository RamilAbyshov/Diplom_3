import allure
from src.data import URLs, Timeouts
from pages.order_feed_page import OrderFeedPage


@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("Переход на страницу ленты заказов")
    def test_navigate_to_order_feed(self, driver):
        order_feed_page = OrderFeedPage(driver, URLs.CONSTRUCTOR)
        order_feed_page.navigate_from_constructor()
        assert order_feed_page.wait_for_url_to_be(URLs.ORDER_FEED)
        assert order_feed_page.get_current_url() == URLs.ORDER_FEED

    @allure.title("Открытие модального окна с деталями заказа")
    def test_open_order_details_modal(self, driver, logged_in_user):
        order_feed_page = OrderFeedPage(driver, URLs.CONSTRUCTOR)
        real_order_number = order_feed_page.wait_for_order_from_constructor()

        assert order_feed_page.click_order_by_number(real_order_number), "Не удалось кликнуть на заказ"
        assert order_feed_page.is_order_modal_visible(Timeouts.MODAL_TIMEOUT), "Модальное окно не открылось"

        order_feed_page.close_order_modal()

    @allure.title("Заказы пользователя из раздела «История заказов» отображаются на странице «Лента заказов»")
    def test_user_orders_from_history_in_feed(self, driver, logged_in_user):
        order_feed_page = OrderFeedPage(driver, URLs.CONSTRUCTOR)
        real_order_number = order_feed_page.wait_for_order_from_constructor()

        assert order_feed_page.wait_for_order_in_feed(real_order_number, Timeouts.ORDER_TIMEOUT), \
            f"Заказ {real_order_number} не отображается в ленте заказов"

    @allure.title("Номер заказа появляется в разделе В работе")
    def test_order_in_progress_section(self, driver, logged_in_user):
        order_feed_page = OrderFeedPage(driver, URLs.CONSTRUCTOR)
        real_order_number = order_feed_page.wait_for_order_from_constructor()

        assert order_feed_page.wait_for_order_in_progress(real_order_number, Timeouts.ORDER_TIMEOUT), \
            f"Заказ {real_order_number} не появился в разделе 'В работе'"

    @allure.title("Счетчики заказов увеличиваются при новом заказе")
    def test_counters_increase_on_new_order(self, driver, logged_in_user):
        order_feed_page = OrderFeedPage(driver, URLs.ORDER_FEED)
        order_feed_page.wait_for_page_load()

        initial_total = order_feed_page.get_orders_done_total()

        # Создаем новый заказ через конструктор
        order_feed_page.navigate_to(URLs.CONSTRUCTOR)
        real_order_number = order_feed_page.wait_for_order_from_constructor()

        new_total = order_feed_page.get_orders_done_total()
        assert new_total > initial_total, \
            f"Счетчик не увеличился: было {initial_total}, стало {new_total}"