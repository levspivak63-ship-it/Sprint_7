import requests
import allure
from config import BASE_URL
from data import TestData


@allure.feature("Дополнительные тесты для ручки получения заказа по треку")
class TestGetOrdersTrack:

    @allure.title("Проверка успешного получения заказа по трекинговому номеру")
    def test_get_order_by_track_success(self):
        
        with allure.step("Создание заказа"):
            original_order_data = TestData.get_order_data()
            order_response = requests.post(f'{BASE_URL}/orders', json=original_order_data)
            assert order_response.status_code == 201
            order_track = order_response.json()['track']
        
        with allure.step("Отправка запроса на получение заказа по номеру"):
            response = requests.get(f'{BASE_URL}/orders/track', params={'t': order_track})
        
        with allure.step("Проверка кода и текста ответа"):
            assert response.status_code == 200
            data = response.json()
            assert 'order' in data
            
            received_order = data['order']
            
            # Проверяем соответствие переданных при формировании заказа данных, возвращаемым в объекте заказа
            assert received_order['firstName'] == original_order_data['firstName']
            assert received_order['lastName'] == original_order_data['lastName']
            assert received_order['address'] == original_order_data['address']
            assert received_order['metroStation'] == original_order_data['metroStation']
            assert received_order['phone'] == original_order_data['phone']
            assert received_order['rentTime'] == original_order_data['rentTime']
            assert received_order['comment'] == original_order_data['comment']
            assert received_order['color'] == original_order_data['color']
            assert received_order['track'] == order_track
        
        with allure.step("Отмена созданного заказа с проверкой"):
            cancel_response = requests.put(f'{BASE_URL}/orders/cancel', params={'track': order_track})
            assert cancel_response.status_code == 200
            
    @allure.title("Проверка ошибки при получении заказа без номера трека")
    def test_get_order_without_track_fails(self):
        
        with allure.step("Отправка запроса на получение заказа без номера трека"):
            response = requests.get(f'{BASE_URL}/orders/track')
        
        with allure.step("Проверка кода ошибки"):
            assert response.status_code == 400
            
    @allure.title("Проверка ошибки при получении заказа с несуществующим номером трека")
    def test_get_order_with_nonexistent_track_fails(self):
        
        with allure.step("Отправка запроса на получение заказа с несуществующим номером трека"):
            response = requests.get(f'{BASE_URL}/orders/track', params={'t': 999999})
        
        with allure.step("Проверка кода ошибки"):
            assert response.status_code == 404
            