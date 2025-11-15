import requests
import allure
from config import BASE_URL
from helper import CourierHelper
from data import TestData


@allure.feature("DEBUG: Тесты для ручки принятия заказа")
class TestDebugAcceptOrder:
        
    @allure.title("DEBUG: Проверка успешного принятия заказа курьером")
    def test_debug_accept_order_success(self):
        
        print("\n" + "="*50)
        print("DEBUG ЗАПУСК: Принятие заказа")
        print("="*50)
        
        with allure.step("Создание курьера"):
            courier_data = CourierHelper.register_new_courier()
            login_response = CourierHelper.login_courier(courier_data["login"], courier_data["password"])
            courier_id = login_response.json()['id']
            print(f"✓ Создан курьер ID: {courier_id}")
            print(f"  Логин: {courier_data['login']}")
            print(f"  Пароль: {courier_data['password']}")
    
        with allure.step("Создание заказа"):
            order_data = TestData.get_order_data()
            print(f"Данные заказа: {order_data}")
            order_response = requests.post(f'{BASE_URL}/orders', json=order_data)
            assert order_response.status_code == 201, f"Ошибка создания заказа: {order_response.text}"
            order_track = order_response.json()['track']
            print(f"✓ Создан заказ с track: {order_track}")
        
        with allure.step("Получение ID заказа по номеру"):
            get_order_response = requests.get(f'{BASE_URL}/orders/track', params={'t': order_track})
            assert get_order_response.status_code == 200, f"Ошибка получения заказа: {get_order_response.text}"
            order_info = get_order_response.json()['order']
            actual_order_id = order_info['id']
            order_status = order_info['status']
            print(f"✓ Заказ ID: {actual_order_id}")
            print(f"  Статус: {order_status} (тип: {type(order_status)})")
            print(f"  cancelled: {order_info['cancelled']}")
            print(f"  finished: {order_info['finished']}")
            print(f"  inDelivery: {order_info['inDelivery']}")
        
        with allure.step("Проверка, что заказ доступен для принятия"):
            # API возвращает статус как число 0 вместо строки "OPEN"
            assert order_status == 0, f"Заказ должен быть в статусе 0 (OPEN), но имеет статус: {order_status}"
            assert order_info['cancelled'] == False, "Заказ отменен"
            assert order_info['finished'] == False, "Заказ завершен"
            assert order_info['inDelivery'] == False, "Заказ уже в доставке"
            print("✓ Заказ в статусе 0 (OPEN) - готов к принятию")
    
        with allure.step("Отправка запроса на принятие заказа курьером"):
            print(f"📤 Отправка запроса принятия заказа:")
            print(f"  URL: PUT {BASE_URL}/orders/accept/{actual_order_id}")
            print(f"  Параметры: courierId={courier_id}")
            
            accept_response = requests.put(
                f'{BASE_URL}/orders/accept/{actual_order_id}', 
                params={"courierId": courier_id}
            )
            
            print(f"📥 Ответ принятия заказа:")
            print(f"  Status Code: {accept_response.status_code}")
            print(f"  Response Body: {accept_response.text}")
        
        with allure.step("Анализ результата"):
            if accept_response.status_code == 200:
                response_data = accept_response.json()
                print("🎉 УСПЕХ: Заказ принят (200 OK)")
                print(f"  Response: {response_data}")
                assert response_data == {"ok": True}, f"Неожиданный ответ: {response_data}"
                
            elif accept_response.status_code == 409:
                error_data = accept_response.json()
                print("❌ ОШИБКА: 409 Conflict")
                print(f"  Сообщение ошибки: {error_data}")
                
                # Диагностика: проверяем статус заказа после ошибки
                print("\n🔍 Диагностика после 409 ошибки:")
                get_order_response_after = requests.get(f'{BASE_URL}/orders/track', params={'t': order_track})
                if get_order_response_after.status_code == 200:
                    order_after = get_order_response_after.json()['order']
                    print(f"  Статус заказа: {order_after['status']}")
                    print(f"  cancelled: {order_after['cancelled']}")
                    print(f"  finished: {order_after['finished']}")
                    print(f"  inDelivery: {order_after['inDelivery']}")
                    
                    # Проверяем, не принял ли заказ другой курьер
                    if order_after['inDelivery'] == True:
                        print("  💡 Заказ уже в доставке (принят другим курьером?)")
                    elif order_after['cancelled'] == True:
                        print("  💡 Заказ отменен")
                    elif order_after['finished'] == True:
                        print("  💡 Заказ завершен")
                        
            else:
                print(f"❌ НЕОЖИДАННЫЙ СТАТУС: {accept_response.status_code}")
                print(f"  Полный ответ: {accept_response.text}")
        
        with allure.step("Очистка тестовых данных"):
            print("\n🧹 Очистка тестовых данных...")
            
            # Отмена заказа
            cancel_response = requests.put(f'{BASE_URL}/orders/cancel', params={'track': order_track})
            print(f"  Отмена заказа: {cancel_response.status_code}")
            if cancel_response.status_code == 200:
                print(f"  ✓ Заказ отменен: {cancel_response.json()}")
            else:
                print(f"  ✗ Ошибка отмены заказа: {cancel_response.text}")
                       
            # Удаление курьера
            delete_response = CourierHelper.delete_courier(courier_id)
            print(f"  Удаление курьера: {delete_response.status_code}")
            if delete_response.status_code == 200:
                print(f"  ✓ Курьер удален: {delete_response.json()}")
            else:
                print(f"  ✗ Ошибка удаления курьера: {delete_response.text}")
                
            print("✓ Очистка завершена")
        
        print("\n" + "="*50)
        print("DEBUG ЗАВЕРШЕН")
        print("="*50)


# Дополнительный тест для проверки статусов заказов
@allure.feature("DEBUG: Тесты статусов заказов")
class TestDebugOrderStatus:
    
    @allure.title("DEBUG: Проверка статусов заказов")
    def test_debug_order_statuses(self):
        """Тест для понимания каких статусов бывают у заказов"""
        
        print("\n" + "="*50)
        print("DEBUG: Анализ статусов заказов")
        print("="*50)
        
        # Создаем несколько заказов и смотрим их статусы
        for i in range(2):
            print(f"\n--- Заказ #{i+1} ---")
            order_data = TestData.get_order_data()
            order_response = requests.post(f'{BASE_URL}/orders', json=order_data)
            
            if order_response.status_code == 201:
                order_track = order_response.json()['track']
                get_response = requests.get(f'{BASE_URL}/orders/track', params={'t': order_track})
                
                if get_response.status_code == 200:
                    order_info = get_response.json()['order']
                    print(f"Статус: {order_info['status']}")
                    print(f"cancelled: {order_info['cancelled']}")
                    print(f"finished: {order_info['finished']}")
                    print(f"inDelivery: {order_info['inDelivery']}")
                    
                    # Отменяем заказ
                    requests.put(f'{BASE_URL}/orders/cancel', params={'track': order_track})