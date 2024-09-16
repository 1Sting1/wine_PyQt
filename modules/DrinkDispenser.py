from storage.Storage import Storage
from modules.Pin import Pin, PinMode
import time


class DrinkDispenser:

    def __init__(self, slot_number: int, volume: float):
        self.storage = Storage()

        pump_address, pump_pin_number = self.storage.dispander_pin(slot_number)
        pump_pin = Pin(pump_address, pump_pin_number)
        pump_pin.set_mode(PinMode.OUTPUT)
        time.sleep(volume)
        pump_pin.set_mode(PinMode.INPUT)
