# test_courier_creation.py

import pytest
import requests
import allure
from config import BASE_URL
from helper import DataGenerator, CourierHelper


@allure.feature("Тесты для ручки создания курьера")
class TestCourierCreation:
        
    @allure.title("Проверка создания курьера с передачей валидных данных во все поля")
    def test_create_courier_success(self, create_courier):
        courier = create_courier
    
        with allure.step("Проверка успешного создания курьера"):
        
            assert courier["create_response"].status_code == 201
            assert courier["create_response"].json() == {"ok": True}

    @allure.title("Проверка возможности создания курьера без поля firstName")
    def test_create_courier_without_firstname_success(self):
    
        with allure.step("Подготовка данных без поля firstName"):
            payload = {
                "login": DataGenerator.generate_random_string(10),
                "password": DataGenerator.generate_random_string(10)
            }
    
        with allure.step("Передача данных для создания курьера без поля firstName"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
    
        with allure.step("Проверка кода и текста ответа 'ok': True об успешном создании учетной записи"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}
        
        with allure.step("Очистка тестовых данных"):
            login_response = CourierHelper.login_courier(payload["login"], payload["password"])
            courier_id = login_response.json()['id']
            CourierHelper.delete_courier(courier_id)

    @allure.title("Проверка невозможности создания двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, create_courier):
        courier = create_courier
        
        with allure.step("Создание второго курьера с данными первого курьера"):
            second_response = requests.post(f'{BASE_URL}/courier', data=courier["data"])
        
        with allure.step("Проверка ответа"):
            assert second_response.status_code == 409
            assert second_response.json() == {"message": "Этот логин уже используется"}
            
    @allure.title("Проверка невозможности создания курьера без поля login")
    def test_create_courier_without_login_fails(self):
        
        with allure.step("Подготовка данных без поля login"):
            payload = {
                "password": DataGenerator.generate_random_string(10),
                "firstName": DataGenerator.generate_random_string(10),
            }
        
        with allure.step("Передача данных для создания курьера без поля login"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 400
            assert response.json() == {"message": "Недостаточно данных для создания учетной записи"}
            
    @allure.title("Проверка невозможности создания курьера без поля password")
    def test_create_courier_without_password_fails(self):
        
        with allure.step("Подготовка данных без поля password"):
            payload = {
                "login": DataGenerator.generate_random_string(10),
                "firstName": DataGenerator.generate_random_string(10),
            }
        
        with allure.step("Передача данных для создания курьера без поля password"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 400
            assert response.json() == {"message": "Недостаточно данных для создания учетной записи"}
           
    @allure.title("Проверка невозможности создания курьера с уже существующим логином")
    def test_create_courier_with_existing_login_fails(self, create_courier):
        courier = create_courier

        with allure.step("Создание второго курьера с тем же логином, но другими именем и паролем"):
            second_courier_data = {
                "login": courier["data"]["login"], 
                "password": DataGenerator.generate_random_string(10),  
                "firstName": DataGenerator.generate_random_string(8)   
            }
            second_response = requests.post(f'{BASE_URL}/courier', data=second_courier_data)
        
        with allure.step("Проверка ответа"):
            assert second_response.status_code == 409
            assert second_response.json() == {"message": "Этот логин уже используется"}