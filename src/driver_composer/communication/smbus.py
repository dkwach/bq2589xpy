import smbus2 as smbus

from .i2c import I2C


class SMbusI2C(I2C):
    BUS_NUMBER = 1

    def __init__(self, bus_number: int | None = None):
        super().__init__()
        self._bus = smbus.SMBus(bus_number or self.BUS_NUMBER)

    def _write_byte(self, device_address: int, offset: int, value: int):
        return self._bus.write_byte_data(device_address, offset, value)

    def _read_byte(self, device_address: int, offset: int) -> int:
        return self._bus.read_byte_data(device_address, offset)
