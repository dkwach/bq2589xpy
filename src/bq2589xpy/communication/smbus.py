import smbus2 as smbus

from .i2c_backend import I2C


class SMbusI2C(I2C):
    BUS_NUMBER = 1

    def __init__(self, bus_number: int | None = None):
        self._bus = smbus.SMBus(bus_number or self.BUS_NUMBER)
        super().__init__()

    def write_byte(self, device_address: int, offset: int, value: int):
        return self._bus.write_byte_data(device_address, offset, value)

    def read_byte(self, device_address: int, offset: int) -> int:
        return self._bus.read_byte_data(device_address, offset)
