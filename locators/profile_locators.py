from selenium.webdriver.common.by import By


class ProfileLocators:
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(@href, 'order-history')]")
    ORDER_HISTORY_ITEMS = (By.XPATH, "//li[contains(@class, 'OrderHistory_listItem__')]")
    ORDER_HISTORY_LIST = (By.XPATH, "//ul[contains(@class, 'OrderHistory_list__')]")

    ORDER_NUMBER_IN_HISTORY = (By.XPATH,
                               ".//p[contains(@class, 'text_type_digits-default') and not(ancestor::div[contains(@class, 'OrderHistory_textContainer__')])]")
    ORDER_PRICE_IN_HISTORY = (By.XPATH,
                              ".//div[contains(@class, 'OrderHistory_textContainer__')]//p[contains(@class, 'text_type_digits-default')]")

    ORDER_NUMBER_STRICT = (By.XPATH,
                           ".//p[@class='text text_type_digits-default' and not(contains(., '₮')) and not(contains(., '₽'))]")

    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")
    PROFILE_TAB = (By.XPATH, "//a[contains(@class, 'Account_link') and contains(text(), 'Профиль')]")

    # Навигация профиля
    PROFILE_NAV = (By.XPATH, "//nav[contains(@class, 'Account_nav__')]")

    # Текстовые боксы
    ORDER_TEXT_BOX = (By.XPATH,
                      "//div[contains(@class, 'OrderHistory_textBox__')]//p[contains(@class, 'text_type_digits-default')]")