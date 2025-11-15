import requests
import random
import string
import allure
from config import BASE_URL


class TestData:
    
    @staticmethod
    def generate_random_string(length):
        """Генерирует строку, состоящую только из букв нижнего регистра"""
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    def register_new_courier_and_return_login_password():
        """ Регистрирует нового курьера и возвращает список [логин, пароль, имя]"""
        login_pass = []

        # генерируем логин, пароль и имя курьера
        login = TestData.generate_random_string(10)
        password = TestData.generate_random_string(10)
        first_name = TestData.generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post(f'{BASE_URL}/courier', data=payload)

        # если регистрация прошла успешно (код ответа 201), добавляем в список имя, логин и пароль курьера
        if response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)
            
        # возвращаем список
        return login_pass
    
    @staticmethod
    def get_order_data(color=None):
        return {
            "firstName": "Иван",
            "lastName": "Васильев", 
            "address": "Проспект Мира, 1",
            "metroStation": "4",
            "phone": "+7 999 123 45 67",
            "rentTime": 5,
            "deliveryDate": "2025-11-11",
            "comment": "Привет",
            "color": color if color is not None else [] 
        }
    
    @staticmethod
    def get_courier_data():
        """Генерирует случайные данные для регистрации курьера"""
        return {
            "login": TestData.generate_random_string(10),
            "password": TestData.generate_random_string(10),
            "firstName": TestData.generate_random_string(10)
        }