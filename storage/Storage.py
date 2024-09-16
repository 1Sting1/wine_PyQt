
class Storage:

    """В данный момент I2C под номером 0x22 не существует,
     в дальнейшем планируется использовать её для кнопок
     и подсветки (сборки из четырёх бутылок)"""
        
        
    """ Пины подсветки кнопок """
    __button_Pin_led = {0: (0x20, 4), 1: (0x20, 5), 2: (0x20, 6), 3: (0x20, 7),
                        4: (0x22, 4), 5: (0x22, 5), 6: (0x22, 6), 7: (0x22, 7)}

    __led_bottle = {0: (0x23, 0), 1: (0x23, 1), 2: (0x23, 2), 3: (0x23, 3),
                    4: (0x23, 4), 5: (0x22, 3), 6: (0x23, 6), 7: (0x23, 7)}
    """ Пины для взимодействия с сигналом кнопок """
    __button_Pin = {0: (0x20, 0), 1: (0x20, 1), 2: (0x20, 2), 3: (0x20, 3),
                    4: (0x22, 0), 5: (0x22, 1), 6: (0x22, 2), 7: (0x22, 3)}

    """ Пины для управления насосами (диспенсером) """
    __pump_Pin = {0: (0x21, 0), 1: (0x21, 1), 2: (0x21, 2), 3: (0x21, 3),
                  4: (0x21, 4), 5: (0x21, 5), 6: (0x21, 6), 7: (0x21, 7)}

    # Программа не учитывает нажатие на кнопку.
    # Настроить выборку значения для wait_for_button_press
    # доработать отчищение пинов и вообщем всей программы после завершениия
    
    """ Пин для замены бутылки (Для кнопки) """
    __button_for_replacement = 36 #Настроить нормальные пины

    """ Пин для замены бутылки (Для подсветки кнопки) """
    __button_led_for_replacement = 34 #Настроить нормальные пины

    """ Результат работы программы """
    result_of_program = False

    """!!!Реализовать подгрузку имен вин с файла!!!"""
    __names_of_vine = {1: "1 Vine", 2: "2 Vine", 3: "3 Vine", 4: "4 Vine"}

    """Ссылка на сервер"""
    __server_url = "http://51.250.89.99"

    """Ссылка на сервер для замены бутылки в аппарате"""
    __server_url_for_replace_bottle= ""

    """Путь к файлу с логами основного цикла программы"""
    __path_to_log_file = "technical_information/log.json"

    """Путь к файлу с регистрационной информацией о терминале"""
    __path_to_tech_file = "technical_information/terminal_info.json"

    """Путь к файлу с логами времени работы всей программы"""
    __path_to_system_file = "technical_information/system_info.json"

    """Путь к временному хранилищу данных при обрыве связи с сервером"""
    __path_to_swap_file = "technical_information/swap.json"

    """Ссылка для регистрации терминала"""
    __link_for_registration = "http://51.250.89.99/terminal/register-terminal"

    """Ссылка для контроля состояния сервера в сети"""
    __link_for_session_control = "https://wine.mag.tc"

    """Ссылка для проверки rfid меток"""
    __link_for_rfid = "http://rfid/validate/{rfid_code}"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance
    
    #     def __init__(self):
    # #         self.clean()
    #         self.setup()
    # def clean(self):
    #     self.__clean_pins(list(self.__pump_Pin.values()))
    #     self.__clean_pins(list(self.__button_Pin.values()))
    #     self.__clean_pins(list(self.__button_Pin_led.values()))
    #     self.__clean_pins(list(self.__led_bottle.values()))
    #
    # def __clean_pins(self, lst: list):
    #     for element in lst:
    #         element.clear()

    # def setup(self):
    #     self.__setup_pins(list(self.__pump_Pin.values()), "output")
    #     self.__setup_pins(list(self.__button_Pin.values()), "input")
    #     self.__setup_pins(list(self.__button_Pin_led.values()), "output")
    #     self.__setup_pins(list(self.__led_bottle.values()), "output")
    # def __setup_pins(self, lst: list, status: str) -> None:
    #     for element in lst:
    #         element.set_mode(status)

    @property
    def get_log_file_path(self) -> str:
        """
        Возвращаем путь к файлу с логами
        """
        return self.__path_to_log_file

    @property
    def get_swap_file_path(self) -> str:
        """
        Возвращаем путь к файлу swap'a
        """
        return self.__path_to_swap_file
    
    @property
    def get_system_log_file_path(self):
        """
        Возвращаем путь к файлу с логами циклов перезапуска программы
        """
        return self.__path_to_system_file

    @property
    def get_link_for_registration(self) -> str:
        """
        Возвращаем ссылку на api регистрации в с системе
        """
        return self.__link_for_registration

    @property
    def get_link_for_session_control(self) -> str:
        """
        Возвращаем ссылку на api регистрации в с системе
        """
        return self.__link_for_session_control

    @property
    def get_tech_file_path(self) -> str:
        """
        Возвращаем путь к файлу с технической информацией
        """
        return self.__path_to_tech_file

    def dispander_pin(self, number_of_bottle: int):
        """
        Возвращаем номер пина нужного нам насоса
        """
        return self.__pump_Pin.get(number_of_bottle)

    def led_pin(self, number_of_button: int):
        """
        ID нужного нам пина подстветки по номеру кнопки (по раскладке BOARD)
        """
        return self.__button_Pin_led.get(number_of_button)

    def button_pin(self, number_of_button: int):
        """
        ID пина по номеру кнопки
        """
        return self.__button_Pin.get(number_of_button)

    @property
    def button_for_replacement(self):
        """
        ID пина кнопки для замены бутылки
        """
        return self.__button_for_replacement

    @property
    def button_led_for_replacement(self):
        """
        ID пина подсветки кнопки для замены бутылки
        """
        return self.__button_led_for_replacement

    @property
    def result(self) -> bool:
        """
        Резултат работы одного цикла программы
        """
        return self.result_of_program

    @result.setter
    def result(self, value: bool):
        """
        Изменение промежуточного результата
        """
        self.result_of_program = value

    def get_vine_name(self, bottle_number) -> str:
        """
        Получение наименования вина для формирования модели чека
        """
        return self.__names_of_vine.get(bottle_number)

    @property
    def server_url(self) -> str:
        """
        Получение ссылки на сервер
        """
        return self.__server_url

    @property
    def rfid_url(self) -> str:
        """
        Получение ссылки на сервер проверки rfid
        """
        return self.__link_for_rfid

    @property
    def server_url_for_replace_bottle (self) -> str:
        """
        Получение ссылку для замены бутылки в аппарате
        """
        return self.__server_url_for_replace_bottle

    @server_url_for_replace_bottle.setter
    def server_url_for_replace_bottle(self, value):
        """
        Формируем ссылку для конкретного аппарата
        """
        self.__server_url_for_replace_bottle = ""