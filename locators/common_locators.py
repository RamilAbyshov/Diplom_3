from selenium.webdriver.common.by import By


class CommonLocators:
    PROFILE_LINK = (By.XPATH, "//a[contains(@href, 'account')]")
    CONSTRUCTOR_LINK = (By.XPATH, "//a[.//p[contains(text(), 'Конструктор')]]")
    ORDER_FEED_LINK = (By.XPATH, "//a[.//p[contains(text(), 'Лента Заказов')]]")

    MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__')]")
    MODAL_CLOSE = (By.XPATH, "//div[contains(@class, 'Modal_modal__')]//button")