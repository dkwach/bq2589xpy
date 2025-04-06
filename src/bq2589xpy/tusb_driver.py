from bq2589xpy import tusb320
from bq2589xpy.communication.thread_safe_i2c import ThreadSafeI2C
from bq2589xpy.driver import Driver


class TUsbDriver(Driver):
    REG08 = tusb320.REG08()
    REG09 = tusb320.REG09()
    REG0A = tusb320.REG0A()

    def __init__(self, i2c, device_address=106):
        super().__init__(i2c, device_address)


def create(backend: str = "") -> Driver:
    if backend == "smbus":
        from bq2589xpy.communication import smbus

        i2c_backend = smbus.SMbusI2C()
    else:
        from bq2589xpy.communication import mock

        i2c_backend = mock.MockI2C()

    thread_safe_i2c = ThreadSafeI2C(i2c_backend)  # Wrap the I2C backend with the thread-safe decorator
    d = TUsbDriver(thread_safe_i2c)
    return d
