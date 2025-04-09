import logging
import threading
import time

from bq2589xpy import bq_registers
from bq2589xpy.communication.thread_safe_i2c import ThreadSafeI2C
from bq2589xpy.driver import Driver

logger = logging.getLogger(__name__)


class Bq25895Driver(Driver):
    REG00 = bq_registers.REG00()
    # REG01 = bq_registers.REG01()
    REG02 = bq_registers.REG02()
    REG03 = bq_registers.REG03()
    REG04 = bq_registers.REG04()
    # REG05 = bq_registers.REG05()
    # REG06 = bq_registers.REG06()
    # REG07 = bq_registers.REG07()
    # REG08 = bq_registers.REG08()
    # REG09 = bq_registers.REG09()
    # REG0A = bq_registers.REG0A()
    REG0B = bq_registers.REG0B()
    REG0C = bq_registers.REG0C()
    # REG0D = bq_registers.REG0D()
    REG0E = bq_registers.REG0E()
    REG0F = bq_registers.REG0F()
    REG10 = bq_registers.REG10()
    REG11 = bq_registers.REG11()
    REG12 = bq_registers.REG12()
    # REG13 = bq_registers.REG13()
    REG14 = bq_registers.REG14()

    def read_faults(self) -> bq_registers.REG0C:
        return self.read(bq_registers.REG0C())

    def read_current_limit(self) -> bq_registers.REG00:
        return self.read(bq_registers.REG00())

    def read_status(self) -> bq_registers.REG0B:
        return self.read(bq_registers.REG0B())

    def read_bat_adc(self) -> bq_registers.REG0E:
        return self.read(bq_registers.REG0E())

    def trigger_adc_conversion(self):
        reg02: bq_registers.REG02 = self.read(bq_registers.REG02())
        reg02.CONV_START = 1
        self.write(reg02)

    def configure_otg(self, enable=True):
        reg03: bq_registers.REG03 = self.read(bq_registers.REG03())
        if bool(reg03.OTG_CONFIG) != enable:
            reg03.OTG_CONFIG = enable
            self.write(reg03)

    def reset_watchdog(self):
        reg03: bq_registers.REG03 = self.read(bq_registers.REG03())
        reg03.WD_RST = 1
        self.write(reg03)

    def reset_watchdog_periodically(self):
        while True:
            logger.info("Reset watchdog")
            self.reset_watchdog()
            time.sleep(20)


def create(backend: str = "") -> Bq25895Driver:
    if backend == "smbus":
        from bq2589xpy.communication import smbus

        i2c_backend = smbus.SMbusI2C()
    else:
        from bq2589xpy.communication import mock

        i2c_backend = mock.MockI2C()

    thread_safe_i2c = ThreadSafeI2C(i2c_backend)  # Wrap the I2C backend with the thread-safe decorator
    d = Bq25895Driver(thread_safe_i2c)
    threading.Thread(target=d.reset_watchdog_periodically, daemon=True).start()
    return d
