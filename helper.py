import requests
import allure
from config import BASE_URL
from data import TestData


class CourierHelper:
    
    @staticmethod
    @allure.step("Регистрация нового курьера и возврат данных")
    def register_new_courier():
        
        courier_data = TestData.get_courier_data()
        
        response = requests.post(f'{BASE_URL}/courier', data=courier_data)
        
        if response.status_code == 201:
            return {
                "login": courier_data["login"],
                "password": courier_data["password"],
                "firstName": courier_data["firstName"]
            }
        return None
    
    @staticmethod
    @allure.step("Авторизация курьера")
    def login_courier(login, password):
       
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{BASE_URL}/courier/login', data=payload)
        return response
    
    @staticmethod
    @allure.step("Удаление курьера")
    def delete_courier(courier_id):
       
        response = requests.delete(f'{BASE_URL}/courier/{courier_id}')
        return response
    