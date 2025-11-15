import requests
import allure
from config import BASE_URL
from helper import CourierHelper
from data import TestData


@allure.feature("Тесты для ручки логина курьера")
class TestCourierLogin:
    """Тесты для ручки логина курьера"""
    
    @allure.title("Проверка успешной авторизации курьера")
    def test_login_courier_success(self):
       
        with allure.step("Создание тестового курьера"):
            courier_data = CourierHelper.register_new_courier()
        
        with allure.step("Передача данных для авторизации курьера"):
            login_response = CourierHelper.login_courier(courier_data["login"], courier_data["password"])
            courier_id = login_response.json()['id']
        
        with allure.step("Проверка кода и текста ответа при успешной авторизации"):
            assert login_response.status_code == 200
            assert login_response.json() == {"id": courier_id}
        
        with allure.step("Очистка тестовых данных"):
            delete_response = CourierHelper.delete_courier(courier_id)
            assert delete_response.status_code == 200
            
    @allure.title("Проверка невозможности авторизации без логина")
    def test_login_without_login_fails(self):
       
        with allure.step("Передача данных для авторизации курьера без логина"):
            password = TestData.generate_random_string(10)
            response = CourierHelper.login_courier("", password)
        
        with allure.step("Проверка кода ошибки"):
            assert response.status_code == 400
            
    @allure.title("Проверка невозможности авторизации без пароля")
    def test_login_without_password_fails(self):
       
        with allure.step("Передача данных для авторизации курьера без пароля"):
            login = TestData.generate_random_string(10)
            response = CourierHelper.login_courier(login, "")
        
        with allure.step("Проверка кода ошибки"):
            assert response.status_code == 400
            
    @allure.title("Проверка невозможности авторизации с неправильным паролем")
    def test_login_with_wrong_password_fails(self):
        
        with allure.step("Создание тестового курьера"):
            courier_data = CourierHelper.register_new_courier()
        
        with allure.step("Передача данных для авторизации курьера с неправильным паролем"):
            login_response = CourierHelper.login_courier(courier_data["login"], "wrong_password")
        
        with allure.step("Проверка кода ошибки"):
            assert login_response.status_code == 404
                 
        
    @allure.title("Проверка невозможности авторизации с неправильным логином")
    def test_login_with_wrong_login_fails(self):
        
        with allure.step("Создание тестового курьера"):
            courier_data = CourierHelper.register_new_courier()
        
        with allure.step("Передача данных для авторизации курьера с неправильным логином"):
            login_response = CourierHelper.login_courier("wrong_login", courier_data["password"])
        
        with allure.step("Проверка кода ошибки"):
            assert login_response.status_code == 404
                    
        
    @allure.title("Проверка невозможности авторизации при отсутствии поля login в запросе")
    def test_login_with_missing_login_field_fails(self):
        
        with allure.step("Передача данных для авторизации курьера без поля login"):
            payload = {"password": TestData.generate_random_string(10)}
            response = requests.post(f'{BASE_URL}/courier/login', data=payload)
        
        with allure.step("Проверка кода ошибки"):
            assert response.status_code == 400
            
    @allure.title("Проверка невозможности авторизации при отсутствии поля password в запросе")
    def test_login_with_missing_password_field_fails(self):
        
        with allure.step("Передача данных для авторизации курьера без поля password"):
            payload = {"login": TestData.generate_random_string(10)}
            response = requests.post(f'{BASE_URL}/courier/login', data=payload)
        
        with allure.step("Проверка кода ошибки"):
            assert response.status_code == 400
            
    @allure.title("Проверка невозможности авторизации при пустом теле запроса")
    def test_login_with_empty_body_fails(self):
        
        with allure.step("Передача данных для авторизации курьера с пустым запросом"):
            response = requests.post(f'{BASE_URL}/courier/login', data={})
        
        with allure.step("Проверка кода ошибки"):
            assert response.status_code == 400
            
    @allure.title("Проверка невозможности авторизации несуществующего пользователя")
    def test_login_nonexistent_user_fails(self):
       
        with allure.step("Передача данных для авторизации курьера с несуществующими данными"):
            response = CourierHelper.login_courier("99999999", "99999999")
        
        with allure.step("Проверка кода ошибки"):
            assert response.status_code == 404
            