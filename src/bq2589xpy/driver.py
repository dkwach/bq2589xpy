from bq2589xpy.communication.i2c_backend import I2C
from bq2589xpy.register import Register


class Driver:
    def __init__(self, i2c: I2C, device_address: int):
        self._i2c = i2c
        self._device_address = device_address

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    def read(self, r: Register) -> Register:
        r.value = self._i2c.read_byte(self._device_address, r.address())
        return r

    def write(self, r: Register) -> None:
        self._i2c.write_byte(self._device_address, r.address(), r.value)
