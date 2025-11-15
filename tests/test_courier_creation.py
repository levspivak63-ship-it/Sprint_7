import pytest
import requests
import allure
from config import BASE_URL
from data import TestData
from helper import CourierHelper


@allure.feature("Тесты для ручки создания курьера")
class TestCourierCreation:
        
    @allure.title("Проверка создания курьера с передачей валидных данных во все поля")
    def test_create_courier_success(self):
        
        with allure.step("Подготовка тестовых данных курьера"):
            courier_data = TestData.get_courier_data()
        
        with allure.step("Передача данных во все поля для создания курьера с валидными данными"):
            response = requests.post(f'{BASE_URL}/courier', data=courier_data)
        
        with allure.step("Проверка кода и текста ответа 'ok': True об успешном создании учетной записи"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}
        
        with allure.step("Очистка тестовых данных"):
            login_response = CourierHelper.login_courier(courier_data["login"], courier_data["password"])
            courier_id = login_response.json()['id']
            delete_response = CourierHelper.delete_courier(courier_id)
            assert delete_response.status_code == 200

    @allure.title("Проверка возможности создания курьера без поля firstName")
    def test_create_courier_without_firstname_success(self):
    
        with allure.step("Подготовка данных без поля firstName"):
            payload = {
                "login": TestData.generate_random_string(10),
                "password": TestData.generate_random_string(10)
            }
    
        with allure.step("Передача данных для авторизации курьера без поля firstName"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
    
        with allure.step("Проверка кода и текста ответа 'ok': True об успешном создании учетной записи"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}
        
        with allure.step("Очистка тестовых данных"):
            login_response = CourierHelper.login_courier(payload["login"], payload["password"])
            courier_id = login_response.json()['id']
            delete_response = CourierHelper.delete_courier(courier_id)
            assert delete_response.status_code == 200

    @allure.title("Проверка невозможности создания двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self):
        
        with allure.step("Создание первого курьера"):
            first_courier_data = TestData.get_courier_data()
            first_response = requests.post(f'{BASE_URL}/courier', data=first_courier_data)
            assert first_response.status_code == 201
            assert first_response.json() == {"ok": True}
        
            login_response = CourierHelper.login_courier(first_courier_data["login"], first_courier_data["password"])
            courier_id = login_response.json()['id']
        
        with allure.step("Cоздание второго курьера с данными первого курьера"):
            second_response = requests.post(f'{BASE_URL}/courier', data={
                "login": first_courier_data["login"],
                "password": first_courier_data["password"],
                "firstName": first_courier_data["firstName"]
            })
        
        with allure.step("Проверка кода ошибки"):
            assert second_response.status_code == 409
                    
        with allure.step("Очистка тестовых данных"):
            delete_response = CourierHelper.delete_courier(courier_id)
            assert delete_response.status_code == 200
            
    @allure.title("Проверка невозможности создания курьера без поля login")
    def test_create_courier_without_login_fails(self):
        
        with allure.step("Подготовка данных без поля login"):
            payload = {
                "password": TestData.generate_random_string(10),
                "firstName": TestData.generate_random_string(10),
            }
        
        with allure.step("Передача данных для авторизации курьера без поля login"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
        
        with allure.step("Проверка кода ошибки"):
            assert response.status_code == 400
            
    @allure.title("Проверка невозможности создания курьера без поля password")
    def test_create_courier_without_password_fails(self):
        
        with allure.step("Подготовка данных без поля password"):
            payload = {
                "login": TestData.generate_random_string(10),
                "firstName": TestData.generate_random_string(10),
            }
        
        with allure.step("Передача данных для авторизации курьера без поля password"):
            response = requests.post(f'{BASE_URL}/courier', data=payload)
        
        with allure.step("Проверка кода ошибки"):
            assert response.status_code == 400
           
               
    @allure.title("Проверка невозможности создания курьера с уже существующим логином")
    def test_create_courier_with_existing_login_fails(self):
                
        with allure.step("Создание первого курьера"):
            first_courier_data = TestData.get_courier_data()
            first_response = requests.post(f'{BASE_URL}/courier', data=first_courier_data)
            assert first_response.status_code == 201
            assert first_response.json() == {"ok": True}
        
            login_response = CourierHelper.login_courier(
                first_courier_data["login"], 
                first_courier_data["password"]
            )
            courier_id = login_response.json()['id']

        with allure.step("Создание второго курьера с тем же логином, но другими именем и паролем"):
            second_courier_data = {
                "login": first_courier_data["login"], 
                "password": TestData.generate_random_string(10),  
                "firstName": TestData.generate_random_string(8)   
            }
            second_response = requests.post(f'{BASE_URL}/courier', data=second_courier_data)
        
        with allure.step("Проверка кода ошибки"):
            assert second_response.status_code == 409
                    
        with allure.step("Очистка тестовых данных - удаление первого курьера"):
            delete_response = CourierHelper.delete_courier(courier_id)
            assert delete_response.status_code == 200
           