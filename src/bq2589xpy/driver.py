import threading

from . import bq_registers
from .communication.i2c_backend import I2C


class Driver:
    def __init__(self, i2c: I2C, device_address: int = 0x6A):
        self._i2c = i2c
        self._device_address = device_address
        self._lock = threading.Lock()

    def read(self, r: bq_registers.BqRegister) -> bq_registers.BqRegister:
        with self._lock:
            r.value = self._i2c.read_byte(self._device_address, r.address())
        return r

    def write(self, r: bq_registers.BqRegister) -> None:
        with self._lock:
            self._i2c.write_byte(self._device_address, r.address(), r.value)


class Bq25895Driver(Driver):
    REG00 = bq_registers.REG00()
    # REG01 = bq_registers.REG01
    REG02 = bq_registers.REG02()
    REG03 = bq_registers.REG03()
    REG04 = bq_registers.REG04()
    # REG05 = bq_registers.REG05
    # REG06 = bq_registers.REG06
    # REG07 = bq_registers.REG07
    # REG08 = bq_registers.REG08
    # REG09 = bq_registers.REG09
    # REG0A = bq_registers.REG0A
    REG0B = bq_registers.REG0B()
    REG0C = bq_registers.REG0C()
    # REG0D = bq_registers.REG0D
    REG0E = bq_registers.REG0E()
    REG0F = bq_registers.REG0F()
    # REG10 = bq_registers.REG10
    REG11 = bq_registers.REG11()
    REG12 = bq_registers.REG12()
    # REG13 = bq_registers.REG13
    # REG14 = bq_registers.REG14

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


def create(backend: str = "") -> Bq25895Driver:
    if backend == "smbus":
        from bq2589xpy.communication import smbus

        i2c_backend = smbus.SMbusI2C()
    else:
        from bq2589xpy.communication import mock

        i2c_backend = mock.MockI2C()

    d = Bq25895Driver(i2c_backend)
    return d
