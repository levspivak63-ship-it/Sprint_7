import pytest
import requests
import allure
from helper import CourierHelper
from config import BASE_URL
from data import TestData


@pytest.fixture
@allure.title("Фикстура для создания курьера и последующего удаления")
def create_courier():
    with allure.step("Создание курьера"):
        courier_data = CourierHelper.register_new_courier()
        login_response = CourierHelper.login_courier(courier_data["login"], courier_data["password"])
        courier_id = login_response.json()['id']
    
        yield courier_data
    
    with allure.step("Удаление курьера"):
        CourierHelper.delete_courier(courier_id)


@pytest.fixture
@allure.title("Фикстура для создания заказа перед тестом и его удаления после")
def create_order():
    with allure.step("Создание заказа"):
        order_data = TestData.get_order_data()
        response = requests.post(f'{BASE_URL}/orders', json=order_data)
        track = response.json()['track']
    
    yield track
    
    with allure.step("Отмена заказа"):
        requests.put(f'{BASE_URL}/orders/cancel', params={'track': track})