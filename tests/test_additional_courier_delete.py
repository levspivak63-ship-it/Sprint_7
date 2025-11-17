# test_additional_courier_delete.py

import pytest
import requests
import allure
from config import BASE_URL
from helper import CourierHelper


@allure.feature("Тесты для ручки удаления курьера")
class TestCourierDelete:
        
    @allure.title("Проверка успешного удаления курьера")
    def test_delete_courier_success(self):
        
        with allure.step("Создание курьера"):
            courier_data = CourierHelper.register_new_courier_and_return_login_password()
            courier_dict = {
                "login": courier_data[0],
                "password": courier_data[1],
                "firstName": courier_data[2]
            }
            login_response = CourierHelper.login_courier(courier_dict["login"], courier_dict["password"])
            courier_id = login_response.json()['id']
        
        with allure.step("Отправка запроса на удаление курьера"):
            delete_response = CourierHelper.delete_courier(courier_id)
        
        with allure.step("Проверка ответа"):
            assert delete_response.status_code == 200
            assert delete_response.json() == {"ok": True}
        
    @allure.title("Проверка ошибки при удалении курьера без ID")
    def test_delete_courier_without_id_fails(self):
        
        with allure.step("Отправка запроса на удаление курьера без ID"):
            response = requests.delete(f'{BASE_URL}/courier/')
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 400
            assert response.json() == {"message": "Недостаточно данных для удаления курьера"}
            
    @allure.title("Проверка ошибки при удалении курьера с несуществующим id")
    def test_delete_nonexistent_courier_fails(self):
        
        with allure.step("Отправка запроса на удаление курьера с несуществующим id"):
            response = CourierHelper.delete_courier(999999)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 404
            assert response.json() == {"message": "Курьера с таким id нет"}