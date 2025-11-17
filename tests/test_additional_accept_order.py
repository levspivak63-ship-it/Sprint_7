# test_additional_accept_order.py

import requests
import allure
from config import BASE_URL
from helper import CourierHelper
from data import TestData


@allure.feature("Тесты для ручки принятия заказа")
class TestAcceptOrder:
        
    @allure.title("Проверка успешного принятия заказа курьером")
    def test_accept_order_success(self):
        
        with allure.step("Создание курьера"):
            courier_data = CourierHelper.register_new_courier_and_return_login_password()
            courier_dict = {
                "login": courier_data[0],
                "password": courier_data[1],
                "firstName": courier_data[2]
            }
            login_response = CourierHelper.login_courier(courier_dict["login"], courier_dict["password"])
            courier_id = login_response.json()['id']
        
        with allure.step("Создание заказа"):
            order_data = TestData.get_order_data([''])
            order_response = requests.post(f'{BASE_URL}/orders', json=order_data)
            assert order_response.status_code == 201
            order_track = order_response.json()['track']
        
        with allure.step("Получение ID заказа по номеру"):
            get_order_response = requests.get(f'{BASE_URL}/orders/track', params={'t': order_track})
            assert get_order_response.status_code == 200
            actual_order_id = get_order_response.json()['order']['id']
        
        with allure.step("Отправка запроса на принятие заказа курьером"):
            accept_response = requests.put(
                f'{BASE_URL}/orders/accept/{actual_order_id}', 
                params={"courierId": courier_id}
            )
        
        with allure.step("Проверка ответа"):
            assert accept_response.status_code == 200
            assert accept_response.json() == {"ok": True}
        
        with allure.step("Очистка тестовых данных"):
            requests.put(f'{BASE_URL}/orders/cancel', params={'track': order_track})
            CourierHelper.delete_courier(courier_id)
            
    @allure.title("Проверка ошибки при принятии заказа без ID курьера")
    def test_accept_order_without_courier_id_fails(self):
        
        with allure.step("Отправка запроса на принятие заказа без ID курьера"):
            response = requests.put(f'{BASE_URL}/orders/accept/1', params={})
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 400
            assert response.json() == {"message": "Недостаточно данных для поиска"}
            
    @allure.title("Проверка ошибки при принятии заказа с несуществующим ID курьера")
    def test_accept_order_with_wrong_courier_id_fails(self):
       
        with allure.step("Отправка запроса на принятие заказа с несуществующим ID курьера"):
            response = requests.put(f'{BASE_URL}/orders/accept/1', params={"courierId": 999999})
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 404
            assert response.json() == {"message": "Курьера с таким id не существует"}
            
    @allure.title("Проверка ошибки при принятии заказа с несуществующим ID заказа")
    def test_accept_order_with_wrong_order_id_fails(self):
        
        with allure.step("Создание курьера"):
            courier_data = CourierHelper.register_new_courier_and_return_login_password()
            courier_dict = {
                "login": courier_data[0],
                "password": courier_data[1],
                "firstName": courier_data[2]
            }
            login_response = CourierHelper.login_courier(courier_dict["login"], courier_dict["password"])
            courier_id = login_response.json()['id']
        
        with allure.step("Отправка запроса на принятие заказа с несуществующим id заказа"):
            response = requests.put(f'{BASE_URL}/orders/accept/999999', params={"courierId": courier_id})
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 404
            assert response.json() == {"message": "Заказа с таким id не существует"}
                    
        with allure.step("Удаление курьера"):
            CourierHelper.delete_courier(courier_id)