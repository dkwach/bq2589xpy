import random

from .i2c_backend import I2C


class MockI2C(I2C):
    def read_byte(self, device_address: int, offset: int) -> int:
        super().read_byte(device_address, offset)
        return random.randint(0, 8)
