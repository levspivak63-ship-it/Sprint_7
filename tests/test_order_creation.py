import pytest
import requests
import allure
from config import BASE_URL
from data import TestData


@allure.feature("Параметризированный тест для ручки создания заказа")
class TestOrderCreation:
       
    @pytest.mark.parametrize('color, test_description', [
        (["BLACK"], "Создание заказа с черным цветом"),
        (["GREY"], "Создание заказа с серым цветом"),
        (["BLACK", "GREY"], "Создание заказа с обоими цветами"),
        ([], "Создание заказа без указания цвета")
    ])
    def test_create_order_with_different_colors(self, color, test_description):
       
        payload = TestData.get_order_data(color)
            
        with allure.step(f"Создание заказа: {test_description}"):
            response = requests.post(f'{BASE_URL}/orders', json=payload)
            
        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 201
            response_data = response.json()
            assert 'track' in response.json()
            
        with allure.step("Отмена созданного заказа"):
            cancel_response = requests.put(f'{BASE_URL}/orders/cancel', params={'track': response_data['track']})
           
            