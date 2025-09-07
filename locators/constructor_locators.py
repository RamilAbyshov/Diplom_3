from selenium.webdriver.common.by import By
from locators.common_locators import CommonLocators


class ConstructorLocators(CommonLocators):
    # Ингредиенты

    INGREDIENT_BUN = (By.XPATH, "//a[.//p[text()='Флюоресцентная булка R2-D3']]")
    INGREDIENT_SAUCE = (By.XPATH, "//section[h2[text()='Соусы']]//a[contains(@class, 'BurgerIngredient_ingredient__')][1]")
    INGREDIENT_MAIN = (By.XPATH, "//section[h2[text()='Начинки']]//a[contains(@class, 'BurgerIngredient_ingredient__')][1]")

    # Конструктор
    CONSTRUCTOR_TOP = (By.XPATH, "//div[contains(@class, 'constructor-element_pos_top')]")
    CONSTRUCTOR_BOTTOM = (By.XPATH, "//div[contains(@class, 'constructor-element_pos_bottom')]")
    CONSTRUCTOR_MAIN = (By.XPATH, "//div[contains(@class, 'BurgerConstructor_items__')]")
    CONSTRUCTOR_ELEMENT = (By.XPATH, "//div[contains(@class, 'constructor-element__text')]")
    EMPTY_CONSTRUCTOR_MESSAGE = (By.XPATH, "//*[contains(text(), 'Перетяните булочку сюда') or contains(text(), 'Конструктор пуст')]")
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay__')]")

    # Кнопка оформления заказа
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")

    # Заголовок
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Соберите бургер')]")

    # Соусы (конкретные)
    INGREDIENT_SAUCE_SPICY_X = (By.XPATH, "//a[.//p[text()='Соус Spicy-X']]")
    INGREDIENT_SAUCE_1 = (By.XPATH, "//section[h2[text()='Соусы']]//a[contains(@class, 'BurgerIngredient_ingredient__')][1]")
    INGREDIENT_SAUCE_2 = (By.XPATH, "//section[h2[text()='Соусы']]//a[contains(@class, 'BurgerIngredient_ingredient__')][2]")

    # Начинки
    INGREDIENT_MAIN_1 = (By.XPATH, "//section[h2[text()='Начинки']]//a[contains(@class, 'BurgerIngredient_ingredient__')][1]")
    INGREDIENT_MAIN_2 = (By.XPATH, "//section[h2[text()='Начинки']]//a[contains(@class, 'BurgerIngredient_ingredient__')][2]")

    # Номер заказа в модальном окне
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'digits-large')]")

    # Счётчик ингредиента
    INGREDIENT_COUNTER = (By.XPATH, ".//p[contains(@class, 'counter_counter__num__3nue1')]")

    # Статус заказа
    ORDER_STATUS_COOKING = (By.XPATH, "//p[contains(text(), 'Ваш заказ начали готовить')]")
    ORDER_STATUS_TEXT = (By.XPATH, "//p[contains(@style, 'color: rgb(0, 204, 204)')]")

    # Цена заказа
    ORDER_PRICE = (By.XPATH, "//div[contains(@class, 'Modal_priceContainer__')]//p[contains(@class, 'digits-default')]")

    # Время заказа
    ORDER_TIMESTAMP = (By.XPATH, "//p[contains(text(), 'Сегодня, в') or contains(text(), 'Вчера, в')]")