from ic_driver_composer.driver import Driver
from mp2722 import registers


class Mp2722(Driver):
    REG13 = registers.REG13

    def __init__(self, i2c, device_address=0x3F):
        super().__init__(i2c, device_address)
