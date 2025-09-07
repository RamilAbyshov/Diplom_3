from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from locators.constructor_locators import ConstructorLocators
from pages.base_page import BasePage
from src.data import Timeouts
import allure


class ConstructorPage(BasePage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)

    @allure.step("Получение счетчика ингредиента")
    def get_ingredient_counter(self, ingredient_locator):
        try:
            ingredient = self.wait_for_visibility(ingredient_locator)
            counter_element = ingredient.find_element(*ConstructorLocators.INGREDIENT_COUNTER)
            counter_text = counter_element.text.strip()
            return int(counter_text) if counter_text.isdigit() else 0
        except Exception:
            return 0

    @allure.step("Ожидание готовности конструктора")
    def wait_for_constructor_ready(self, timeout=Timeouts.ELEMENT_TIMEOUT):
        try:
            self.wait_for_visibility(ConstructorLocators.PAGE_TITLE, timeout)
            return self
        except TimeoutException:
            return self

    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_loaded(self, timeout=Timeouts.PAGE_TIMEOUT):
        self.wait_for_document_ready(timeout)
        return self

    @allure.step("Перетаскивание ингредиента в конструктор")
    def drag_ingredient_to_constructor(self, ingredient_locator, target_locator):
        try:
            ingredient = self.wait_for_visibility(ingredient_locator)
            target = self.wait_for_visibility(target_locator)

            js_script = """
            function simulateDragDrop(sourceNode, destinationNode) {
                var EVENT_TYPES = {
                    DRAG_END: 'dragend',
                    DRAG_START: 'dragstart',
                    DROP: 'drop',
                    DRAG_OVER: 'dragover',
                    DRAG_ENTER: 'dragenter',
                    DRAG_LEAVE: 'dragleave',
                    DRAG_EXIT: 'dragexit'
                }

                function createEvent(type) {
                    var event = new CustomEvent("CustomEvent")
                    event.initCustomEvent(type, true, true, null)
                    event.dataTransfer = {
                        data: {},
                        setData: function(type, val) {
                            this.data[type] = val
                        },
                        getData: function(type) {
                            return this.data[type]
                        }
                    }
                    return event
                }

                function dispatchEvent(node, type, event) {
                    if (node.dispatchEvent) {
                        return node.dispatchEvent(event)
                    }
                    if (node.fireEvent) {
                        return node.fireEvent("on" + type, event)
                    }
                }

                var event = createEvent(EVENT_TYPES.DRAG_START)
                dispatchEvent(sourceNode, EVENT_TYPES.DRAG_START, event)

                var dropEvent = createEvent(EVENT_TYPES.DROP)
                dropEvent.dataTransfer = event.dataTransfer
                dispatchEvent(destinationNode, EVENT_TYPES.DROP, dropEvent)

                var dragEndEvent = createEvent(EVENT_TYPES.DRAG_END)
                dragEndEvent.dataTransfer = event.dataTransfer
                dispatchEvent(sourceNode, EVENT_TYPES.DRAG_END, dragEndEvent)
            }

            simulateDragDrop(arguments[0], arguments[1]);
            """

            self.driver.execute_script(js_script, ingredient, target)
            return True

        except Exception as e:
            print(f"JS drag and drop error: {e}")
            return False

    @allure.step("Клик по ссылке конструктора")
    def click_constructor_link(self):
        self.safe_click(ConstructorLocators.CONSTRUCTOR_LINK)
        self.wait_for_page_loaded()
        return self

    @allure.step("Клик по ссылке ленты заказов")
    def click_order_feed_link(self):
        self.safe_click(ConstructorLocators.ORDER_FEED_LINK)
        self.wait_for_page_loaded()
        return self

    @allure.step("Клик по ингредиенту")
    def click_ingredient(self):
        ingredient = self.wait_for_visibility(ConstructorLocators.INGREDIENT_BUN)
        self.driver.execute_script("arguments[0].click();", ingredient)
        return self

    @allure.step("Получение номера заказа")
    def get_order_number(self, timeout=Timeouts.MODAL_TIMEOUT):
        element = self.wait_for_visibility(ConstructorLocators.ORDER_NUMBER, timeout)
        return element.text

    @allure.step("Закрытие модального окна конструктора")
    def close_constructor_modal(self):
        try:
            self.wait_for_visibility_with_timeout(ConstructorLocators.MODAL)
            close_button = self.wait_for_element_with_timeout(ConstructorLocators.MODAL_CLOSE)
            self.driver.execute_script("arguments[0].click();", close_button)

            self.wait_for_invisibility(ConstructorLocators.MODAL, Timeouts.ELEMENT_TIMEOUT)
            return self
        except Exception:
            try:
                action = ActionChains(self.driver)
                action.send_keys(Keys.ESCAPE).perform()
                return self
            except Exception:
                try:
                    overlay = self.find_element(ConstructorLocators.MODAL_OVERLAY)
                    overlay.click()
                    return self
                except:
                    self.driver.refresh()
                    self.wait_for_constructor_ready()
                    return self

    @allure.step("Проверка видимости модального окна")
    def is_modal_visible(self):
        try:
            element = self.wait_for_visibility_custom(ConstructorLocators.MODAL, timeout=Timeouts.MODAL_TIMEOUT)
            return element is not None
        except TimeoutException:
            return False

    @allure.step("Оформление заказа")
    def make_order(self):
        try:
            self.wait_for_constructor_ready()
            success = self.drag_ingredient_to_constructor(
                ConstructorLocators.INGREDIENT_BUN,
                ConstructorLocators.CONSTRUCTOR_TOP
            )
            if not success:
                return None
            order_button = self.wait_for_visibility(ConstructorLocators.ORDER_BUTTON)
            self.driver.execute_script("arguments[0].click();", order_button)
            self.wait_for_visibility(ConstructorLocators.MODAL)
            return self.get_order_number()

        except Exception as e:
            print(f"Ошибка при оформлении заказа: {e}")
            return None

    @allure.step("Ожидание реального номера заказа")
    def wait_for_real_order_number(self, timeout=Timeouts.ORDER_TIMEOUT):
        initial_number = self.get_order_number_text()
        try:
            initial_num = int(initial_number)
            self.wait_for_condition_with_timeout(
                lambda driver: self._is_order_number_increased(initial_num),
                timeout
            )
            return self.get_order_number_text()
        except TimeoutException:
            return self.get_order_number_text()

    def _is_order_number_increased(self, initial_num):
        current_number_text = self.get_order_number_text()
        try:
            current_num = int(current_number_text)
            return current_num > initial_num
        except ValueError:
            return False

    @allure.step("Получение текста номера заказа")
    def get_order_number_text(self):
        return self.wait_for_visibility(ConstructorLocators.ORDER_NUMBER).text

    @allure.step("Добавление булки в конструктор")
    def add_bun_to_constructor(self):
        return self.drag_ingredient_to_constructor(
            ConstructorLocators.INGREDIENT_BUN,
            ConstructorLocators.CONSTRUCTOR_TOP
        )

    @allure.step("Получение счетчика булки")
    def get_bun_counter(self):
        return self.get_ingredient_counter(ConstructorLocators.INGREDIENT_BUN)