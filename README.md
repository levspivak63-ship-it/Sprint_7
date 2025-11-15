Проект автоматизации тестирования API учебного сервиса Яндекс Самокат: https://qa-scooter.praktikum-services.ru/. 
URL документации: https://qa-scooter.praktikum-services.ru/docs/#api.
Проект включает автоматизацию тестовых сценариев с использованием Selenium.
Для подготовки тестов использован Microsoft VS Code


В проекте испоьзованы технологии:
requests==2.31.0
pytest==7.4.0
allure-pytest==2.13.0
pytest-html==3.2.0

Структура проекта: 
Sprint_7/
│
├── tests/                           
│   ├── test_courier_creation.py
│   ├── test_courier_login.py
│   ├── test_order_creation.py
│   ├── test_order_list.py
│   ├── test_additional_courier_delete.py
│   ├── test_additional_get_order_track.py
│   └── test_additional_accept_order.py
│
├── helper.py                        
├── data.py                          
├── config.py                        
│
├── allure-report/                   
├── requirements.txt
├── README.md
└── conftest.py

Разработаны в соответствии с заданием тестовые сценарии:
1. Для ручки Courier - Создание курьера
2. Для ручки Courier - Логин курьера в системе
3. Для ручки Orders - Создание заказа
4. Для ручки Orders - Получение списка заказов:
5. Дополнительные тесты для ручки Orders - Принять заказ
6. Дополнительные тесты для ручки Courier - Удаление курьера
7. Дополнительные тесты для ручки Orders - Получить заказ по его номеру

Тестирование проводилось в окружении Google Chrome версии 142.0.7444.135
Результаты тестирования: из 30 тестов 27 - успешные (passed), 3 не успешные (failed). 
Тесты выявили:
1. Для ручки Courier - Удаление курьера: несоответствующий код ответа при запросе на удаление без id: 404 вместо 400
2. Для ручки Courier - Логин курьера в системе: при авторизации курьера без поля password и при пустом теле запроса возникает ошибка 504 вместо ожидаемой 400

Результаты тестирования представлены в приложенном allure-report





# Sprint_7
