from faker import Faker
from utils.api_client import UserAPI

fake = Faker('ru_RU')

def create_test_user():

    user_data = {
        "email": fake.email(),
        "password": fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
        "name": fake.first_name()
    }

    response = UserAPI.register(user_data["email"], user_data["password"], user_data["name"])

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
        UserAPI.delete(user_data["accessToken"])