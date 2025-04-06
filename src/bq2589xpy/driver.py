from bq2589xpy.communication.i2c_backend import I2C
from bq2589xpy.communication.thread_safe_i2c import ThreadSafeI2C
from bq2589xpy.register import Register


class Driver:
    def __init__(self, i2c: I2C, device_address: int = 0x6A):
        self._i2c = i2c
        self._device_address = device_address

    def read(self, r: Register) -> Register:
        r.value = self._i2c.read_byte(self._device_address, r.address())
        return r

    def write(self, r: Register) -> None:
        self._i2c.write_byte(self._device_address, r.address(), r.value)


def create(backend: str = "") -> Driver:
    from bq2589xpy.bq_driver import Bq25895Driver

    if backend == "smbus":
        from bq2589xpy.communication import smbus

        i2c_backend = smbus.SMbusI2C()
    else:
        from bq2589xpy.communication import mock

        i2c_backend = mock.MockI2C()

    thread_safe_i2c = ThreadSafeI2C(i2c_backend)  # Wrap the I2C backend with the thread-safe decorator
    d = Bq25895Driver(thread_safe_i2c)
    return d
