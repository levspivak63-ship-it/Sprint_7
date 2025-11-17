# conftest.py

import pytest
import allure
from helper import CourierHelper, DataGenerator  


@pytest.fixture
@allure.title("Фикстура для создания курьера и последующего удаления")
def create_courier():
    with allure.step("Создание курьера"):
        courier_data = {
            "login": DataGenerator.generate_random_string(10),
            "password": DataGenerator.generate_random_string(10),
            "firstName": DataGenerator.generate_random_string(10)
        }
        
        # Создаем курьера в системе
        create_response = CourierHelper.create_courier(courier_data)
        login_response = CourierHelper.login_courier(courier_data["login"], courier_data["password"])
        courier_id = login_response.json()['id']
    
    # Возвращаем данные и ID в виде словаря
    result = {
        "data": courier_data,
        "id": courier_id,
        "create_response": create_response
    }
    
    yield result
    
    with allure.step("Удаление курьера"):
        CourierHelper.delete_courier(courier_id)