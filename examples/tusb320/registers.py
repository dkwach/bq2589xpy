from enum import Flag, auto

from driver_composer.register import BitField, Register


class ACCESS(Flag):
    READ = auto()
    WRITE = auto()
    SET = auto()
    CLEAR = auto()
    UPDATE = auto()
    NO_ACCESS = auto()


READ_WRITE = ACCESS.READ | ACCESS.WRITE


class TUsbBitField(BitField):
    def __init__(
        self,
        width=1,
        default=None,
        access: ACCESS = READ_WRITE,
    ):
        self.access = access
        super().__init__(width, default)


class TUsbRegister(Register):
    def __init__(self, value=0):
        self._check_size()
        super().__init__(value)

    @classmethod
    def _check_size(cls):
        assert cls.size == 8

    def address(self):
        cls_name = type(self).__name__
        return int(cls_name[-2:], base=16)


class REG08(TUsbRegister):
    ACTIVE_CABLE_DETECTION = TUsbBitField(width=1, default=None, access=ACCESS.READ | ACCESS.UPDATE)
    """This flag indicates that an active cable has been plugged
    into the Type-C connector. When this field is set, an active
    cable is detected."""

    ACCESSORY_CONNECTED = TUsbBitField(width=3, default=0, access=ACCESS.READ | ACCESS.UPDATE)
    """These bits are read by the application to determine if an
    accessory was attached.
    000 – No accessory attached (default)
    001 – Reserved
    010 – Reserved
    011 – Reserved
    100 – Audio accessory
    101 – Audio charged thru accessory
    110 – Debug accessory
    111 – Reserved"""

    CURRENT_MODE_DETECT = TUsbBitField(width=2, default=0, access=ACCESS.READ | ACCESS.UPDATE)
    """These bits are set when an UFP determines the Type-C
    Current mode.
    00 – Default (value at start up)
    01 – Medium
    10 – Charge through accessory – 500 mA
    11 – High"""

    CURRENT_MODE_ADVERTISE = TUsbBitField(width=2, default=0, access=READ_WRITE)
    """These bits are programmed by the application to raise the
    current advertisement from default.
    00 – Default (500 mA / 900 mA) initial value at startup
    01 – Medium (1.5 A)
    10 – High (3 A)
    11 – Reserved"""


class REG09(TUsbRegister):
    RESERVED_0 = TUsbBitField(width=1, default=None, access=ACCESS.READ)
    """Reserved"""

    DRP_DUTY_CYCLE = TUsbBitField(width=2, default=0, access=READ_WRITE)
    """Percentage of time that a DRP advertises DFP during tDRP
    00 – 30% (default)
    01 – 40%
    10 – 50%
    11 – 60%
    """

    RESERVED_1 = TUsbBitField(width=1, default=None, access=ACCESS.READ)
    """Reserved"""

    INTERRUPT_STATUS = TUsbBitField(width=1, default=None, access=ACCESS.READ | ACCESS.CLEAR | ACCESS.UPDATE)
    """The INT pin is pulled low whenever a CSR changes. When
    a CSR change has occurred this bit should be held at 1 until
    the application clears it.
    0 – Clear
    1 – Interrupt (When INT_N is pulled low, this bit will be 1.
    This bit is 1 whenever any CSR are changed)
    Note: SW must make sure the INTERRUPT_STATUS has
    been cleared to zero. Rewrites to this register are needed
    for the INT_N to be correctly asserted for all interrupt
    events."""

    CABLE_DIR = TUsbBitField(width=1, default=1, access=ACCESS.READ | ACCESS.UPDATE)
    """Cable orientation. The application can read these bits for
    cable orientation information.
    0 – CC1
    1 – CC2 (default)"""

    ATTACHED_STATE = TUsbBitField(width=2, default=0, access=ACCESS.READ | ACCESS.UPDATE)
    """This is an additional method to communicate attach other
    than the ID pin. These bits can be read by the application to
    determine what was attached.
    00 – Not attached (default)
    01 – Attached.SRC (DFP)
    10 – Attached.SNK (UFP)
    11 – Attached to an accessory"""


class REG0A(TUsbRegister):
    RESERVED = TUsbBitField(width=3, default=None, access=ACCESS.READ)
    """Reserved"""

    I2C_SOFT_RESET = TUsbBitField(width=1, default=None, access=ACCESS.READ | ACCESS.SET | ACCESS.UPDATE)
    """This resets the digital logic. The bit is self-clearing. A write
    of 1 starts the reset. The following registers maybe affected
    after setting this bit:
    CURRENT_MODE_DETECT
    ACTIVE_CABLE_DETECTION
    ACCESSORY_CONNECTED
    ATTACHED_STATE
    CABLE_DIR"""

    MODE_SELECT = TUsbBitField(width=2, default=0, access=READ_WRITE)
    """This register can be written to set the TUSB320 device
    mode operation. The ADDR pin must be set to I2C
    mode. If the default is maintained, the TUSB320 device
    operates according to the PORT pin levels and modes.
    The MODE_SELECT can only be changed when in the
    unattached state.
    00 – Maintain mode according to PORT pin selection
    (default)
    01 – UFP mode (unattached.SNK)
    10 – DFP mode (unattached.SRC)
    11 – DRP mode (start from unattached.SNK)"""

    DEBOUNCE = TUsbBitField(width=2, default=0, access=READ_WRITE)
    """The nominal amount of time the TUSB320 device
    debounces the voltages on the CC pins.
    00 – 133 ms (default)
    01 – 116 ms
    10 – 151 ms
    11 – 168 ms"""


if __name__ == "__main__":
    r08 = REG08()
    r09 = REG09()
    r0A = REG0A()
