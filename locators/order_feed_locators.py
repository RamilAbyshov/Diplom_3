from selenium.webdriver.common.by import By
from locators.common_locators import CommonLocators


class OrderFeedLocators(CommonLocators):
    PAGE_TITLE = (By.XPATH, "//h1[text()='Лента заказов']")
    ORDER_LIST = (By.XPATH, "//div[contains(@class, 'OrderFeed_orderList__')]")
    ORDER_ITEMS = (By.XPATH, "//div[contains(@class, 'OrderHistory_listItem__')]")
    ORDER_LINKS = (By.XPATH, "//a[contains(@class, 'OrderHistory_link__')]")

    # Статистика заказов
    ORDERS_DONE_TODAY = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    ORDERS_DONE_TOTAL = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")

    # Раздел "В работе"
    ORDERS_IN_PROGRESS_SECTION = (By.XPATH, "//p[text()='В работе:']/following-sibling::ul[1]")
    ORDERS_IN_PROGRESS_NUMBERS = (By.XPATH,
                                  "//ul[contains(@class, 'OrderFeed_orderListReady__')]//li[contains(@class, 'text_type_digits-default')]")

    # Модальное окно заказа
    ORDER_MODAL = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened__')]")
    ORDER_MODAL_NUMBER = (By.XPATH, "//p[@class='text text_type_digits-default mb-10 mt-5']")

    # Альтернативные локаторы
    ORDER_MODAL_ALTERNATIVE = (By.XPATH, "//div[contains(@class, 'Modal_modal__container__')]")
    ORDER_MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay__')]")

    # Для поиска заказов по номеру
    ORDER_BY_NUMBER = (By.XPATH, "//*[contains(text(), '{}')]")

    # Номера в модальном окне (альтернативные варианты)
    ORDER_MODAL_NUMBER_ALT1 = (By.XPATH, "//p[contains(@class, 'text_type_digits-default') and contains(text(), '#')]")
    ORDER_MODAL_NUMBER_ALT2 = (By.XPATH,
                               "//div[contains(@class, 'Modal_orderBox__')]//p[contains(@class, 'digits-default')]")
    ORDER_MODAL_NUMBER_ALT3 = (By.XPATH, "//p[contains(text(), '#')]")
    ORDER_MODAL_NUMBER_ALT4 = (By.CSS_SELECTOR, "p.text_type_digits-default")