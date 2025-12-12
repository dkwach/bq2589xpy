from driver_composer.driver import Driver

from . import registers


class TUsbDriver(Driver):
    REG08 = registers.REG08()
    REG09 = registers.REG09()
    REG0A = registers.REG0A()

    def __init__(self, i2c, device_address=106):
        super().__init__(i2c, device_address)
