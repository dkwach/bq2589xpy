import threading

from bq2589xpy.bq_driver import Bq25895Driver
from bq2589xpy.communication.thread_safe_i2c import ThreadSafeI2C
from bq2589xpy.driver import Driver
from bq2589xpy.tusb_driver import TUsbDriver


def create(backend: str = "") -> tuple[Driver]:
    if backend == "smbus":
        from bq2589xpy.communication import smbus

        i2c_backend = smbus.SMbusI2C()
    else:
        from bq2589xpy.communication import mock

        i2c_backend = mock.MockI2C()

    thread_safe_i2c = ThreadSafeI2C(i2c_backend)  # Wrap the I2C backend with the thread-safe decorator

    bq = Bq25895Driver(thread_safe_i2c)
    tusb = TUsbDriver(thread_safe_i2c)

    threading.Thread(target=bq.reset_watchdog_periodically, daemon=True).start()
    return bq, tusb
