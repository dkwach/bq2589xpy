import random

from .i2c import I2C


class MockI2C(I2C):
    def _read_byte(self, device_address: int, offset: int) -> int:
        return random.randint(0, 255)

    def _write_byte(self, device_address: int, offset: int, value: int):
        pass
