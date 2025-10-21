from enum import Flag, auto

from ic_driver_composer.register import BitField, RegXX


class ACCESS(Flag):
    READ = auto()
    WRITE = auto()


READ_WRITE = ACCESS.READ | ACCESS.WRITE


class Mp2722Field(BitField):
    def __init__(
        self,
        width=1,
        default=None,
        access: ACCESS = READ_WRITE,
        is_OTP=False,
        is_watchdog_reset=False,
        is_interrupt=False,
    ):
        self.access = access
        self.is_watchdog_reset = is_watchdog_reset
        self.is_OTP = is_OTP
        self.is_interrupt = is_interrupt
        super().__init__(width, default)


class REG13(RegXX):
    CHG_FAULT = Mp2722Field(width=2, default=None, access=ACCESS.READ, is_interrupt=True)
    """
    00: Normal
    01: Input OVP
    10: The charge timer has expired
    11: Battery OVP
    """

    BOOST_FAULT = Mp2722Field(width=3, default=None, access=ACCESS.READ, is_interrupt=True)
    """
    000: Normal
    001: An IN overload or short (latch-off) has occurred
    010: Boost over-voltage protection (OVP) (not latch) has occurred
    011: Boost over-temperature protection (latch-off) has occurred
    100: The boost has stopped due to BATT_LOW (latch-off)
    """

    CHG_STAT = Mp2722Field(width=3, default=0, access=ACCESS.READ)
    """
    000: Not charging
    001: Trickle charge
    010: Pre-charge
    011: Fast charge
    100: Constant-voltage charge
    101: Charging is done
    """
