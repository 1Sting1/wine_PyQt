from storage.Storage import Storage
from modules.Pin import Pin, PinMode
from modules.DrinkDispenser import DrinkDispenser

class ButtonReader:
    """Класс для чтения состояния кнопок и управления процессом"""

    def __init__(self, slot_number: int):
        self.storage = Storage()
        self.__run = True

        led_address, led_pin = self.storage.led_pin(slot_number)
        button_address, button_pin = self.storage.button_pin(slot_number)

        self.led_pin = Pin(led_address, led_pin)
        self.led_pin.set_mode(PinMode.OUTPUT)

        self.button_pin = Pin(button_address, button_pin)
        self.button_pin.set_mode(PinMode.INPUT)
        self.button_pin.wait_for_press()
        #self.led_pin.set_mode(PinMode.INPUT)