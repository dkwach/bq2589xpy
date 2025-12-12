from driver_composer.driver import Driver

from . import registers


class Bq25895Driver(Driver):
    REG00 = registers.REG00()
    # REG01 = bq_registers.REG01()
    REG02 = registers.REG02()
    REG03 = registers.REG03()
    REG04 = registers.REG04()
    # REG05 = bq_registers.REG05()
    # REG06 = bq_registers.REG06()
    # REG07 = bq_registers.REG07()
    # REG08 = bq_registers.REG08()
    # REG09 = bq_registers.REG09()
    # REG0A = bq_registers.REG0A()
    REG0B = registers.REG0B()
    REG0C = registers.REG0C()
    # REG0D = bq_registers.REG0D()
    REG0E = registers.REG0E()
    REG0F = registers.REG0F()
    REG10 = registers.REG10()
    REG11 = registers.REG11()
    REG12 = registers.REG12()
    # REG13 = bq_registers.REG13()
    REG14 = registers.REG14()

    def __init__(self, i2c, device_address: int = 0x6A):
        super().__init__(i2c, device_address)
