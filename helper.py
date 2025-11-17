# helper.py

import requests
import allure
import random
import string
from config import BASE_URL


class DataGenerator:
    
    @staticmethod
    def generate_random_string(length):
        """Генерирует строку, состоящую только из букв нижнего регистра"""
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    def get_courier_data():
        """Генерирует случайные данные для регистрации курьера"""
        return {
            "login": DataGenerator.generate_random_string(10),
            "password": DataGenerator.generate_random_string(10),
            "firstName": DataGenerator.generate_random_string(10)
        }


class CourierHelper:
    
    @staticmethod
    @allure.step("Создание курьера")
    def create_courier(courier_data):
        response = requests.post(f'{BASE_URL}/courier', data=courier_data)
        return response

    @staticmethod
    @allure.step("Регистрация нового курьера и возврат данных")
    def register_new_courier_and_return_login_password():
        """Регистрирует нового курьера и возвращает список [логин, пароль, имя]"""
        courier_data = DataGenerator.get_courier_data()
        response = CourierHelper.create_courier(courier_data)

        if response.status_code == 201:
            return [courier_data["login"], courier_data["password"], courier_data["firstName"]]
        return []
    
    @staticmethod
    @allure.step("Авторизация курьера")
    def login_courier(login, password):
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{BASE_URL}/courier/login', data=payload)
        return response
    
    @staticmethod
    @allure.step("Удаление курьера")
    def delete_courier(courier_id):
        response = requests.delete(f'{BASE_URL}/courier/{courier_id}')
        return response
