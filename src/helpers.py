import requests
from faker import Faker

from pages.base_page import BasePage
from src.data import URLs

fake = Faker('ru_RU')

def random_email():
    return fake.email()

def random_password(length=10):
    return fake.password(length=length, special_chars=True, digits=True, upper_case=True, lower_case=True)

def random_name():
    return fake.first_name()

def random_user_data():
    return {
        "email": random_email(),
        "password": random_password(),
        "name": random_name()
    }

def register_user(email, password, name):
    payload = {"email": email, "password": password, "name": name}
    return requests.post(f"{URLs.API_BASE}/auth/register", json=payload)

def login_user(email, password):
    payload = {"email": email, "password": password}
    return requests.post(f"{URLs.API_BASE}/auth/login", json=payload)

def delete_user(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    return requests.delete(f"{URLs.API_BASE}/auth/user", headers=headers)

def create_test_user():
    import time
    timestamp = int(time.time() * 1000)

    user_data = {
        "email": f"test{timestamp}@example.com",
        "password": f"Pass{timestamp}$",
        "name": f"User{timestamp}"
    }

    response = register_user(user_data["email"], user_data["password"], user_data["name"])

    if response.status_code == 200:
        access_token = response.json().get("accessToken")
        return {
            "email": user_data["email"],
            "password": user_data["password"],
            "name": user_data["name"],
            "accessToken": access_token
        }
    else:
        raise Exception(f"Failed to create user: {response.text}")

def delete_test_user(user_data):
    if user_data.get("accessToken"):
        delete_user(user_data["accessToken"])

