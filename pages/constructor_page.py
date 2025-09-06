from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from locators.constructor_locators import ConstructorLocators
from pages.base_page import BasePage
from src.data import Timeouts


class ConstructorPage(BasePage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)

    def get_ingredient_counter(self, ingredient_locator):
        try:
            ingredient = WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.visibility_of_element_located(ingredient_locator)
            )
            counter_element = ingredient.find_element(*ConstructorLocators.INGREDIENT_COUNTER)
            counter_text = counter_element.text.strip()
            return int(counter_text) if counter_text.isdigit() else 0
        except Exception:
            return 0

    def is_constructor_empty(self):
        try:
            constructor_elements = self.driver.find_elements(*ConstructorLocators.CONSTRUCTOR_ELEMENT)
            empty_message = self.driver.find_elements(*ConstructorLocators.EMPTY_CONSTRUCTOR_MESSAGE)
            return len(constructor_elements) == 0 or len(empty_message) > 0
        except:
            return False

    def get_order_status(self):
        try:
            WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.visibility_of_element_located(ConstructorLocators.ORDER_STATUS_COOKING)
            )
            return "Готовится"
        except:
            try:
                status_text = self.driver.find_element(*ConstructorLocators.ORDER_STATUS_TEXT).text
                return status_text
            except:
                return "Неизвестен"

    def get_order_price(self):
        price_element = self.driver.find_element(*ConstructorLocators.ORDER_PRICE)
        return int(price_element.text) if price_element.text.isdigit() else 0

    def get_order_timestamp(self):
        time_element = self.driver.find_element(*ConstructorLocators.ORDER_TIMESTAMP)
        return time_element.text

    def wait_for_constructor_ready(self, timeout=Timeouts.ELEMENT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(ConstructorLocators.PAGE_TITLE)
            )
            return self
        except TimeoutException:
            return self

    def wait_for_page_loaded(self, timeout=Timeouts.PAGE_TIMEOUT):
        self.wait_for_document_ready(timeout)
        return self

    def drag_ingredient_to_constructor(self, ingredient_locator, target_locator):
        try:
            ingredient = WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(ingredient_locator)
            )
            target = WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(target_locator)
            )

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

    def click_constructor_link(self):
        self.safe_click(ConstructorLocators.CONSTRUCTOR_LINK)
        self.wait_for_page_loaded()
        return self

    def click_order_feed_link(self):
        self.safe_click(ConstructorLocators.ORDER_FEED_LINK)
        self.wait_for_page_loaded()
        return self

    def click_profile_link(self):
        self.safe_click(ConstructorLocators.PROFILE_LINK)
        self.wait_for_page_loaded()
        return self

    def click_ingredient(self):
        ingredient = WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
            EC.element_to_be_clickable(ConstructorLocators.INGREDIENT_BUN)
        )
        self.driver.execute_script("arguments[0].click();", ingredient)
        return self

    def get_order_number(self, timeout=Timeouts.MODAL_TIMEOUT):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(ConstructorLocators.ORDER_NUMBER)
        )
        return element.text

    def close_constructor_modal(self):
        try:
            WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.visibility_of_element_located(ConstructorLocators.MODAL)
            )

            close_button = WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(ConstructorLocators.MODAL_CLOSE)
            )

            self.driver.execute_script("arguments[0].click();", close_button)

            WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.invisibility_of_element_located(ConstructorLocators.MODAL)
            )
            return self

        except Exception:
            try:
                action = ActionChains(self.driver)
                action.send_keys(Keys.ESCAPE).perform()
                return self
            except Exception:
                try:
                    overlay = self.driver.find_element(*ConstructorLocators.MODAL_OVERLAY)
                    overlay.click()
                    return self
                except:
                    self.driver.refresh()
                    self.wait_for_constructor_ready()
                    return self

    def is_modal_visible(self):
        return super().is_modal_visible(ConstructorLocators.MODAL)

    def make_order(self):
        try:
            self.wait_for_constructor_ready()

            success = self.drag_ingredient_to_constructor(
                ConstructorLocators.INGREDIENT_BUN,
                ConstructorLocators.CONSTRUCTOR_TOP
            )

            if not success:
                return None

            order_button = WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(ConstructorLocators.ORDER_BUTTON)
            )

            self.driver.execute_script("arguments[0].click();", order_button)

            WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.visibility_of_element_located(ConstructorLocators.MODAL)
            )

            return self.get_order_number()

        except Exception as e:
            print(f"Ошибка при оформлении заказа: {e}")
            return None

    def wait_for_real_order_number(self, timeout=Timeouts.ORDER_TIMEOUT):
        initial_number = self.get_order_number_text()

        try:
            try:
                initial_num = int(initial_number)
            except ValueError:
                initial_num = 0

            WebDriverWait(self.driver, timeout).until(
                lambda driver: self._is_order_number_increased(initial_num)
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


    def get_order_number_text(self):
        return WebDriverWait(self.driver, Timeouts.ELEMENT_TIMEOUT).until(
                EC.visibility_of_element_located(ConstructorLocators.ORDER_NUMBER)
            ).text

    def add_bun_to_constructor(self):
        return self.drag_ingredient_to_constructor(
            ConstructorLocators.INGREDIENT_BUN,
            ConstructorLocators.CONSTRUCTOR_TOP
        )

    def get_bun_counter(self):
        return self.get_ingredient_counter(ConstructorLocators.INGREDIENT_BUN)

    def add_sauce_to_constructor(self):
        return self.drag_ingredient_to_constructor(
            ConstructorLocators.INGREDIENT_SAUCE,
            ConstructorLocators.CONSTRUCTOR_MAIN
        )

    def add_main_to_constructor(self):
        return self.drag_ingredient_to_constructor(
            ConstructorLocators.INGREDIENT_MAIN,
            ConstructorLocators.CONSTRUCTOR_MAIN
        )