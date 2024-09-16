import smbus
import time


class PinMode:
    INPUT = 0
    OUTPUT = 1


class Pin:
    bus_number = 1

    def __init__(self, address, pin_number):
        print(f"Инициализация Pin: {self.bus_number}, 0x{address:X}, {pin_number}")
        self.bus = smbus.SMBus(self.bus_number)
        self.address = address
        self.pin_number = pin_number
        self.mode = PinMode.INPUT
        self.state = 0xFF  # Initial state with all pins high (assuming active low)
        self._write_state(self.state)

    def _write_state(self, state):
        print(f"Запись состояния 0x{state:X} в адрес 0x{self.address:X}")
        self.bus.write_byte(self.address, state)

    def _read_state(self):
        state = self.bus.read_byte(self.address)
        print(f"Чтение состояния 0x{state:X} с адреса 0x{self.address:X}")
        return state

    def set_mode(self, mode):
        self.mode = mode
        if mode == PinMode.OUTPUT:
            self.state &= ~(1 << self.pin_number)  # Set pin to low (active)
            print(f"Установка режима OUTPUT для пина {self.pin_number}")
        else:
            self.state |= (1 << self.pin_number)  # Set pin to high (inactive)
            print(f"Установка режима INPUT для пина {self.pin_number}")
        self._write_state(self.state)

    def write(self, value):
        if self.mode != PinMode.OUTPUT:
            raise ValueError("Cannot write to pin not set as output")
        print(f"Запись значения {value} на пин {self.pin_number}")
        if value:
            self.state |= (1 << self.pin_number)
        else:
            self.state &= ~(1 << self.pin_number)
        self._write_state(self.state)

    def read(self):
        if self.mode != PinMode.INPUT:
            raise ValueError("Cannot read from pin not set as input")
        state = self._read_state()
        pin_value = (state & (1 << self.pin_number)) == 0
        print(f"Чтение значения с пина {self.pin_number}: {pin_value}")
        return pin_value

    def clear(self):
        print(f"Очистка состояния пина {self.pin_number}")
        if self.mode == PinMode.OUTPUT:
            self.write(0)
        else:
            self.state |= (1 << self.pin_number)
            self._write_state(self.state)

    def wait_for_press(self, timeout=None):
        print(f"Ожидание нажатия кнопки на пине {self.pin_number}")
        start_time = time.time()
        while True:
            state = self.read()
            print(state)
            if state:
                print(f"Кнопка на пине {self.pin_number} нажата")
                return True
            if timeout and (time.time() - start_time) > timeout:
                print(f"Время ожидания нажатия кнопки на пине {self.pin_number} истекло")
                return False
            time.sleep(0.01)  # Debounce delay
