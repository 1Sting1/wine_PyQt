import requests
import time


class TerminalRegistration:
    """ Описание класса """

    def __init__(self):
        """Attributes:
            self.ath (str): Путь к файлу.
            self.link (str): Ссылка для регистрации.
            self.__info (dict): Информация о терминале.
        """
        self.link = "http://51.250.89.99/terminal/register-terminal"
        self.__info = {}
        self.__register_terminal()

    def __register_terminal(self):
        """
        Регистрирует новый терминал.

        Returns:
            tuple: Кортеж с ID и именем зарегистрированного терминала.
        """
        serial = self.__get_serial_number()

        while True:
            response = requests.post(self.link, json={"serial": serial})
            if response.status_code == 200:
                self.__info = {'id': response.json()['terminal_id'],
                               'serial': serial,
                               'token': response.json()['token']}
                break
            else:
                time.sleep(1)

    @staticmethod
    def __get_serial_number():
        """ Описание функции """
        serial_number = None
        try:
            # Открываем файл /proc/cpuinfo
            with open('/proc/cpuinfo', 'r') as file:
                # Читаем все содержимое файла
                cpuinfo = file.read()
                # Находим индекс начала строки с серийным номером
                start_index = cpuinfo.find('Serial')
                if start_index != -1:
                    # Находим конец строки с серийным номером
                    end_index = cpuinfo.find('\n', start_index)
                    # Извлекаем строку с серийным номером и убираем лишние пробелы
                    serial_number = cpuinfo[start_index:end_index].split(':')[1].strip()
        except FileNotFoundError:
            print("Файл /proc/cpuinfo не найден.")
        return serial_number

    @property
    def terminal_id(self):
        """ Описание функции """
        return self.__info['id']

    @property
    def token(self):
        """ Описание функции """
        return self.__info['token']
