from storage.Storage import Storage
from modules.Pin import PinMode
from modules.DispanserPin import PumpPin
from modules.LedPin import LedPin
import time


class DrinkDispenser:

    def __init__(self, slot_number: int, volume: float):
        self.storage = Storage()

        pump_address, pump_pin_number = self.storage.dispander_pin(slot_number)

        self.pump_pin = PumpPin(pump_address, pump_pin_number)
        self.pump_pin.pin.set_mode(PinMode.OUTPUT)
        self.pump_pin.write(0x00)

        time.sleep(volume)

        self.pump_pin.write(0xFF)

        bottle_led_adress, bottle_led_pin = self.storage.bottle_led(slot_number)
        self.bottle_led = LedPin(bottle_led_adress, bottle_led_pin)
        self.bottle_led.write(0x00)

