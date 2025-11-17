# data.py
class TestData:
        
    @staticmethod
    def get_order_data(color):
        return {
            "firstName": "Naruto2",  
            "lastName": "Uchiha",    
            "address": "Konoha, 142 apt.",
            "metroStation": "4",       
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color  
        }
    