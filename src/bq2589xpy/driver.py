from . import bq_registers
from .communication.i2c import I2C


class Bq25895Driver:
    def __init__(self, device_address: int, i2c: I2C):
        self._i2c = i2c
        self._device_address = device_address

    def read(self, r: bq_registers.BqRegister) -> bq_registers.BqRegister:
        r.value = self._i2c.read_byte(self._device_address, r.address)
        return r

    def write(self, r: bq_registers.BqRegister) -> None:
        self._i2c.write_byte(self._device_address, r.address)

    def read_faults(self) -> bq_registers.REG0C:
        return self.read(bq_registers.REG0C())

    def read_current_limit(self) -> bq_registers.REG00:
        return self.read(bq_registers.REG00())

    def read_status(self) -> bq_registers.REG0B:
        return self.read(bq_registers.REG0B())

    def trigger_adc_conversion(self):
        raise NotImplementedError

    def configure_otg(self, enable=True):
        reg03: bq_registers.REG03 = self.read(bq_registers.REG03())
        if bool(reg03.OTG_CONFIG) != enable:
            reg03.OTG_CONFIG = enable
            self.write(reg03)

    def reset_watchdog(self):
        reg03: bq_registers.REG03 = self.read(bq_registers.REG03())
        reg03.WD_RST = 1
        self.write(reg03)
