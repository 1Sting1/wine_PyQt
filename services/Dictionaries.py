class Dictionaries:
    """ Описание класса """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Dictionaries, cls).__new__(cls)
        return cls.instance

    """Время"""

    @property
    def datetime_current_with_days_mounts_years(self):
        """
        Время: День, месяц, год
        """
        return "d:%m:%Y"

    @property
    def datetime_current_with_hours_minutes_seconds(self):
        """
        Время: Часы, минуты, секунды
        """
        return "%H:%M:%S"

    @property
    def datetime_current_with_hours_minutes_microseconds(self):
        """
        Время: Часы, минуты, секунды и миллисекунды
        """
        return "%H:%M:%S.%f"

    @property
    def datetime_current_with_days_mounts_years_hours_minutes_microseconds(self):
        """
        Время вместе с датой: День, месяц, год, часы, минуты, секунды, миллисекунды
        """
        return "%d.%m.%Y %H:%M:%S.%f"

    """Для всех классов"""

    @property
    def order_id_for_all_class(self):
        """
        Запись id операции в учёт(Log)
        """
        return "order_id"

    @property
    def volume_for_all_class(self):
        """
        Запись: Какой обЪём был налит клиенту(Log)
        """
        return "volume"

    """Словари для RFIDReader"""

    @property
    def access_granted_for_class_rfidreader(self):
        """
        Проверяет разрешен ли доступ (запрашивая данные у сервера)
        """
        return "access_granted"

    @property
    def rfid_no_for_class_rfidreader(self):
        """
        Если доступ не разрешён: rfid no
        """
        return "rfid no"

    @property
    def number_of_bottle_for_all_class(self):
        """
        Запись номера бутылки в учёт(Log)
        """
        return "number_of_bottle"

    """Словари для Registration"""

    @property
    def id_for_class_registration(self):
        """
        Возвращает id устройства на сервере из json файла для последующего применения
        """
        return "id"

    @property
    def name_for_class_registration(self):
        """
        Возвращает название устройства на сервере из json файла для последующего применения
        """
        return "name"

    @property
    def terminal_for_class_registration(self):
        """
        Поле terminal (массив), внутри него расположены поля: id и name
        """
        return "terminal"

    @property
    def terminal_id_for_class_registration(self):
        """
        Объединение terminal и id
        """
        return "terminal_id"

    @property
    def terminal_name_for_class_regitration(self):
        """
        Объединение terminal и name
        """
        return "terminal_name"

    @property
    def bottle_id_for_all_class(self):
        """
        Наименование бутылки которая использовалась для налива
        """
        return "bottle_id"
