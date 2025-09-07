class URLs:
    BASE = "https://stellarburgers.nomoreparties.site"
    LOGIN = f"{BASE}/login"
    REGISTER = f"{BASE}/register"
    FORGOT_PASSWORD = f"{BASE}/forgot-password"
    RESET_PASSWORD = f"{BASE}/reset-password"
    PROFILE = f"{BASE}/account/profile"
    ORDER_HISTORY = f"{BASE}/account/order-history"
    CONSTRUCTOR = f"{BASE}/"
    ORDER_FEED = f"{BASE}/feed"
    API_BASE = f"{BASE}/api"
    API_REGISTER = f"{API_BASE}/auth/register"
    API_LOGIN = f"{API_BASE}/auth/login"
    API_USER = f"{API_BASE}/auth/user"
    API_DELETE = f"{API_BASE}/auth/user"

class Timeouts:
    ELEMENT_TIMEOUT = 15
    PAGE_TIMEOUT = 20
    MODAL_TIMEOUT = 10
    ORDER_TIMEOUT = 60
    URL_TIMEOUT = 15
