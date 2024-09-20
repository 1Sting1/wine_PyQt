import smbus
import time
from modules.Pin import Pin, PinMode


class PumpPin:
    bus_number = 1

    def __init__(self, address, pin_number):

        self.bus = smbus.SMBus(self.bus_number)
        self.address = address
        self.pin_number = pin_number
        self.state = 0xFF  # Initial state with all pins high (assuming active low)
        self._write_state_pump(self.state)
        self.pin = Pin(self.address, self.pin_number)


    def _write_state_pump(self, state):
        print(f"Запись состояния 0x{state:X} в адрес 0x{self.address:X}")
        self.bus.write_byte(self.address, state)


    def write(self, value):
        if self.pin.mode != PinMode.OUTPUT:
            raise ValueError("Cannot write to pin not set as output")
        print(f"Запись значения {value} на пин {self.pin_number}")
        if value:
            self.state |= (1 << self.pin_number)
        else:
            self.state &= ~(1 << self.pin_number)
        self._write_state_pump(self.state)
