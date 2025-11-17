# test_order_list.py

import pytest
import requests
import allure
from config import BASE_URL


@allure.feature("Тесты для ручки получения списка заказов")
class TestOrderList:
        
    @allure.title("Проверка получения списка заказов")
    def test_get_orders_list(self):
       
        with allure.step("Отправка запроса на получение списка заказов"):
            response = requests.get(f'{BASE_URL}/orders')
    
        with allure.step("Проверка кода и возврата списка заказов в теле ответа"):
            assert response.status_code == 200
            data = response.json()
            
            assert 'orders' in data
            assert type(data['orders']) is list
           
        