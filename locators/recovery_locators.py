from selenium.webdriver.common.by import By


class RecoveryLocators:
    RECOVERY_LINK = (By.CSS_SELECTOR, "a[href*='forgot-password']")
    EMAIL_FIELD = (By.CSS_SELECTOR, "input[type='text']")
    RECOVERY_BUTTON = (By.CSS_SELECTOR, "button[class*='button_button']")

    PASSWORD_FIELD_HIDDEN = (By.CSS_SELECTOR, "input.input__textfield[type='password']")
    PASSWORD_FIELD_VISIBLE = (By.CSS_SELECTOR, "input.input__textfield[type='text']")

    SHOW_PASSWORD_ICON = (By.CSS_SELECTOR, ".input__icon-action")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[class*='button_button']")