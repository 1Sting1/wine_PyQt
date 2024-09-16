from pirc522 import RFID
from services.Dictionaries import Dictionaries
import requests
import signal
import sys
import datetime


class RFIDReader:
    """Описание класса"""

    def __init__(self):
        self.run = True
        self.rdr = RFID()
        self.util = self.rdr.util()
        self.util.debug = True
        self.dictionaries = Dictionaries()

        signal.signal(signal.SIGINT, self.clean)

    """ Функция для корректного завершения чтения """


    def clean(self, signum=None, frame=None):
        self.run = False
        self.rdr.cleanup()
        sys.exit()

    @staticmethod
    def reformat_uid(uid):
        """ Преобразуем UID из списка в строку """
        result = ""
        for number in uid:
            result += str(number)
        return result

    @staticmethod
    def send_to_server(uid) -> dict:
        server_url = f"http://51.250.89.99/rfid/validate/{uid}"
        response = requests.get(server_url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "broken"}
#         return {'access_granted': "granted", 'limit': "1:00"}

    def start_reading(self):
        """ Основная функция для считывания меток """
        while self.run:
            self.rdr.wait_for_tag()

            """ Применяем встроеную функцию в библиотеку для отправки запроса """
            (error, data) = self.rdr.request()
            if not error:
               print("\nDetected: " + format(data, "02x"))

            """ Избегаем колизии """
            (error, uid) = self.rdr.anticoll()

            """ Если нет ошибок, то выполняем программу далее """
            if not error and uid is not None:
                """ Форматируем UID """
                uid = self.reformat_uid(uid)
                print("UID: " + uid)

                """Отправляем UID метки на сервер """
                response = self.send_to_server(uid)
                response["rfid_code"] = uid
                """ Если доступ разрешен """
                return response
                
