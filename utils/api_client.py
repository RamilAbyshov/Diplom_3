import requests
import allure
from src.data import URLs


class UserAPI:
    @staticmethod
    @allure.step("Регистрация пользователя")
    def register(email, password, name):
        payload = {"email": email, "password": password, "name": name}
        return requests.post(URLs.API_REGISTER, json=payload)

    @staticmethod
    @allure.step("Логин пользователя")
    def login(email, password):
        payload = {"email": email, "password": password}
        return requests.post(URLs.API_LOGIN, json=payload)

    @staticmethod
    @allure.step("Обновление данных пользователя")
    def update(access_token, data):
        headers = {"Authorization": access_token}
        return requests.patch(URLs.API_USER, headers=headers, json=data)

    @staticmethod
    @allure.step("Удаление пользователя")
    def delete(access_token):
        headers = {"Authorization": access_token}
        return requests.delete(URLs.API_DELETE, headers=headers)


class OrderAPI:
    @staticmethod
    @allure.step("Создание заказа")
    def create(access_token, ingredients):
        headers = {"Authorization": access_token} if access_token else {}
        payload = {"ingredients": ingredients}
        return requests.post(f"{URLs.API_BASE}/orders", headers=headers, json=payload)

    @staticmethod
    @allure.step("Получение заказов пользователя")
    def get_user_orders(access_token):
        headers = {"Authorization": access_token} if access_token else {}
        return requests.get(f"{URLs.API_BASE}/orders", headers=headers)

    @staticmethod
    @allure.step("Получение id ингредиентов")
    def get_ingredient_ids():
        response = requests.get(f"{URLs.API_BASE}/ingredients")
        response.raise_for_status()
        return [item["_id"] for item in response.json()["data"]]