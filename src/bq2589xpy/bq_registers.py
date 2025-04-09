from enum import Flag, auto

from bq2589xpy.register import BitField, Register


class Reset(Flag):
    SOFTWARE = auto()
    WATCHDOG = auto()
    REG_RST = auto()
    NOT_SPECIFIED = auto()


class BitType(Flag):
    READ = auto()
    WRITE = auto()


READ_WRITE = BitType.READ | BitType.WRITE


class BqBitField(BitField):
    def __init__(
        self,
        width=1,
        default=None,
        bit_type: BitType = READ_WRITE,
        reset: Reset = Reset.NOT_SPECIFIED,
    ):
        self.bit_type = bit_type
        self.reset = reset
        super().__init__(width, default)


class BqRegister(Register):
    def __init__(self, value=0):
        self._check_size()
        super().__init__(value)

    @classmethod
    def _check_size(cls):
        assert cls.size == 8

    def address(self):
        cls_name = type(self).__name__
        return int(cls_name[-2:], base=16)


class REG00(BqRegister):
    IINLIM = BqBitField(width=6, default=0b0001000, bit_type=READ_WRITE, reset=Reset.REG_RST)
    """Input Current Limit
    Offset: 100mA
    Range: 100mA (000000) – 3.25A (111111)
    Default:0001000 (500mA)
    (Actual input current limit is the lower of I2C or ILIM pin)
    IINLIM bits are changed automaticallly after input source
    type detection is completed
    USB Host SDP w/ OTG=Hi (USB500) = 500mA
    USB Host SDP w/ OTG=Lo (USB100) = 500mA
    USB CDP = 1.5A
    USB DCP = 3.25A
    Adjustable High Voltage (MaxCharge) DCP = 1.5A
    Unknown Adapter = 500mA
    Non-Standard Adapter = 1A/2A/2.1A/2.4A

        TODO MAPPING: 
            IINLIM[5] -> 1600mA
            IINLIM[4] -> 800mA
            IINLIM[3] -> 400mA
            IINLIM[2] -> 200mA
            IINLIM[1] -> 100mA
            IINLIM[0] -> 50mA"""

    EN_ILIM = BqBitField(width=1, default=1, bit_type=READ_WRITE, reset=Reset.REG_RST | Reset.WATCHDOG)
    """Enable ILIM Pin
    0 – Disable
    1 – Enable (default: Enable ILIM pin (1))"""

    EN_HIZ = BqBitField(width=1, default=0, bit_type=READ_WRITE, reset=Reset.REG_RST | Reset.WATCHDOG)
    """Enable HIZ Mode
    0 – Disable (default)
    1 – Enable"""


class REG02(BqRegister):
    AUTO_DPDM_EN = BqBitField(width=1, default=1, bit_type=READ_WRITE, reset=Reset.REG_RST)
    """Automatic D+/D- Detection Enable
    0 –Disable D+/D- or PSEL detection when VBUS is plugged-in
    1 –Enable D+/D- or PEL detection when VBUS is plugged-in (default)
    """

    FORCE_DPDM = BqBitField(width=1, default=0, bit_type=READ_WRITE, reset=Reset.REG_RST | Reset.WATCHDOG)
    """Force D+/D- Detection
    0 – Not in D+/D- or PSEL detection (default)
    1 – Force D+/D- detection
    """

    MAXC_EN = BqBitField(width=1, default=1, bit_type=READ_WRITE, reset=Reset.REG_RST)
    """MaxCharge Adapter Enable
    0 – Disable MaxCharge handshake
    1 – Enable MaxCharge handshake (default)
    """

    HVDCP_EN = BqBitField(width=1, default=1, bit_type=READ_WRITE, reset=Reset.REG_RST)
    """High Voltage DCP Enable
    0 – Disable HVDCP handshake
    1 – Enable HVDCP handshake (default)
    """

    ICO_EN = BqBitField(width=1, default=1, bit_type=READ_WRITE, reset=Reset.REG_RST)
    """Input Current Optimizer (ICO) Enable
    0 – Disable ICO Algorithm
    1 – Enable ICO Algorithm (default)
    """

    BOOST_FREQ = BqBitField(width=1, default=1, bit_type=READ_WRITE, reset=Reset.REG_RST | Reset.WATCHDOG)
    """Boost Mode Frequency Selection
    0 – 1.5MHz
    1 – 500KHz (default)
    Note: Write to this bit is ignored when OTG_CONFIG is enabled
    """

    CONV_RATE = BqBitField(width=1, default=0, bit_type=READ_WRITE, reset=Reset.REG_RST | Reset.WATCHDOG)
    """ADC Conversion Rate Selection
    0 – One shot ADC conversion (default)
    1 – Start 1s Continuous Conversion
    """

    CONV_START = BqBitField(width=1, default=0, bit_type=READ_WRITE, reset=Reset.REG_RST | Reset.WATCHDOG)
    """ADC Conversion Start Control
    0 – ADC conversion not active (default).
    1 – Start ADC Conversion
    This bit is read-only when CONV_RATE = 1. The bit stays high during
    ADC conversion and during input source detection.
    """


class REG03(BqRegister):
    Reserved = BqBitField(width=1, default=1, bit_type=READ_WRITE, reset=Reset.REG_RST | Reset.WATCHDOG)
    """Reserved (default = 0)"""

    SYS_MIN = BqBitField(width=3, default=0b101, bit_type=READ_WRITE, reset=Reset.REG_RST)
    """Minimum System Voltage Limit
    Offset: 3.0V
    Range 3.0V-3.7V
    Default: 3.5V (101)

            TODO MAPPING: 
            SYS_MIN[2] -> 0.4V
            SYS_MIN[1] -> 0.2V
            SYS_MIN[0] -> 0.1V"""

    CHG_CONFIG = BqBitField(width=1, default=1, bit_type=READ_WRITE, reset=Reset.REG_RST | Reset.WATCHDOG)
    """Charge Enable Configuration
    0 - Charge Disable
    1- Charge Enable (default)"""

    OTG_CONFIG = BqBitField(width=1, default=1, bit_type=READ_WRITE, reset=Reset.REG_RST | Reset.WATCHDOG)
    """Boost (OTG) Mode Configuration
    0 – OTG Disable
    1 – OTG Enable (default)"""

    WD_RST = BqBitField(width=1, default=0, bit_type=READ_WRITE, reset=Reset.REG_RST)
    """I2C Watchdog Timer Reset
    0 – Normal (default)
    1 – Reset (Back to 0 after timer reset)"""

    BAT_LOADEN = BqBitField(width=1, default=0, bit_type=READ_WRITE, reset=Reset.REG_RST | Reset.WATCHDOG)
    """Battery Load (IBATLOAD) Enable
    0 – Disabled (default)
    1 – Enabled"""


class REG04(BqRegister):
    ICHG = BqBitField(width=7, default=0b0100000, bit_type=READ_WRITE, reset=Reset.SOFTWARE | Reset.WATCHDOG)
    """Fast Charge Current Limit
    Offset: 0mARange: 0mA (0000000) – 5056mA (1001111)
    Default: 2048mA (0100000)
    Note:
    ICHG=000000 (0mA) disables charge
    ICHG > 1001111 (5056mA) is clamped to register value 1001111 (5056mA)"""

    EN_PUMPX = BqBitField(width=1, default=0, bit_type=READ_WRITE, reset=Reset.SOFTWARE | Reset.WATCHDOG)
    """Current pulse control Enable
    0 - Disable Current pulse control (default)
    1- Enable Current pulse control (PUMPX_UP and PUMPX_DN)"""


class REG0B(BqRegister):
    VSYS_STAT = BqBitField(width=1, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """VSYS Regulation Status
    0 – Not in VSYSMIN regulation (BAT > VSYSMIN)
    1 – In VSYSMIN regulation (BAT < VSYSMIN)"""

    SDP_STAT = BqBitField(width=1, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """USB Input Status
    0 – USB100 input is detected
    1 – USB500 input is detected
    Note: This bit always read 1 when VBUS_STAT is not 001"""

    PG_STAT = BqBitField(width=1, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Power Good Status
    0 – Not Power Good
    1 – Power Good"""

    CHRG_STAT = BqBitField(width=2, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Charging Status
    00 – Not Charging
    01 – Pre-charge ( < VBATLOWV)
    10 – Fast Charging
    11 – Charge Termination Done"""

    VBUS_STAT = BqBitField(width=3, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """BUS Status register
    BQ25895
    000: No Input 001: USB Host SDP
    010: USB CDP (1.5A)
    011: USB DCP (3.25A)
    100: Adjustable High Voltage DCP (MaxCharge) (1.5A)
    101: Unknown Adapter (500mA)
    110: Non-Standard Adapter (1A/2A/2.1A/2.4A)
    111: OTG
    Note: Software current limit is reported in IINLIM register"""


class REG0C(BqRegister):
    NTC_FAULT = BqBitField(width=3, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """NTC Fault Status
    Buck Mode:
    000 – Normal
    001 – TS Cold
    010 – TS Hot
    Boost Mode:
    000 – Normal
    101 – TS Cold
    110 – TS Hot"""

    BAT_FAULT = BqBitField(width=1, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Battery Fault Status
    0 – Normal
    1 – BATOVP (VBAT > VBATOVP)"""

    CHRG_FAULT = BqBitField(width=2, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Charge Fault Status
    00 – Normal
    01 – Input fault (VBUS > VACOV or VBAT < VBUS < VVBUSMIN(typical
    3.8V) )
    10 - Thermal shutdown
    11 – Charge Safety Timer Expiration"""

    BOOST_FAULT = BqBitField(width=1, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Boost Mode Fault Status
    0 – Normal
    1 – VBUS overloaded in OTG, or VBUS OVP, or battery is too low in
    boost mode"""

    WATCHDOG_FAULT = BqBitField(width=1, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Watchdog Fault Status
    Status 0 – Normal
    1- Watchdog timer expiration"""


class REG0E(BqRegister):
    BATV = BqBitField(width=7, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """ADC conversion of Battery Voltage (VBAT)
    Offset: 2.304V
    Range: 2.304V (0000000) – 4.848V (1111111)
    Default: 2.304V (0000000)
    TODO MAPPING: 
        BATV[6] -> 1280mV
        BATV[5] -> 640mV
        BATV[4] -> 320mV
        BATV[3] -> 160mV
        BATV[2] -> 80mV
        BATV[1] -> 40mV
        BATV[0] -> 20mV"""

    THERM_STAT = BqBitField(width=1, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Thermal Regulation Status
    0 – Normal
    1 – In Thermal Regulation"""


class REG0F(BqRegister):
    SYSV = BqBitField(width=7, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """ADDC conversion of System Voltage (VSYS)
    Offset: 2.304V
    Range: 2.304V (0000000) – 4.848V (1111111)
    Default: 2.304V (0000000)
    TODO MAPPING: 
        SYSV[6] -> 1280mV
        SYSV[5] -> 640mV
        SYSV[4] -> 320mV
        SYSV[3] -> 160mV
        SYSV[2] -> 80mV
        SYSV[1] -> 40mV
        SYSV[0] -> 20mV"""

    Reserved = BqBitField(width=1, default=0, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Reserved: Always reads 0
    """


class REG11(BqRegister):
    VBUSV = BqBitField(width=7, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """ADC conversion of VBUS voltage (VBUS)
    Offset: 2.6V
    Range 2.6V (0000000) – 15.3V (1111111)
    Default: 2.6V (0000000)
    TODO MAPPING: 
        VBUSV[6] -> 6400mV
        VBUSV[5] -> 3200mV
        VBUSV[4] -> 1600mV
        VBUSV[3] -> 800mV
        VBUSV[2] -> 400mV
        VBUSV[1] -> 200mV
        VBUSV[0] -> 100mV"""

    VBUS_GD = BqBitField(width=1, default=0, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """VBUS Good Status
    0 – Not VBUS attached
    1 – VBUS Attached
    """


class REG12(BqRegister):
    ICHGR = BqBitField(width=7, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """ADC conversion of Charge Current (IBAT) when VBAT >
    VBATSHORT
    Offset: 0mA
    Range 0mA (0000000) – 6350mA (1111111)
    Default: 0mA (0000000)
    Note:
    This register returns 0000000 for VBAT < VBATSHORT
    TODO MAPPING: 
        ICHGR[6] -> 3200mA
        ICHGR[5] -> 1600mA
        ICHGR[4] -> 800mA
        ICHGR[3] -> 400mA
        ICHGR[2] -> 200mA
        ICHGR[1] -> 100mA
        ICHGR[0] -> 50mA"""

    Unused = BqBitField(width=1, default=0, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Always reads 0"""


class REG14(BqRegister):
    DEV_REV = BqBitField(width=2, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Device Revision: 01"""

    TS_PROFILE = BqBitField(width=1, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Temperature Profile
    0 – Cold/Hot (default)"""

    PN = BqBitField(width=3, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Device Configuration
    111: BQ25895"""

    ICO_OPTIMIZED = BqBitField(width=1, default=None, bit_type=BitType.READ, reset=Reset.NOT_SPECIFIED)
    """Input Current Optimizer (ICO) Status
    0 – Optimization is in progress
    1 – Maximum Input Current Detected"""

    REG_RST = BqBitField(width=1, default=0, bit_type=READ_WRITE, reset=Reset.NOT_SPECIFIED)
    """Register Reset
    0 – Keep current register setting (default)
    1 – Reset to default register value and reset safety timer
    Note:
    Reset to 0 after register reset is completed"""


if __name__ == "__main__":
    r00 = REG00()
    r02 = REG02()
    r03 = REG03()
    r0B = REG0B()
    r0C = REG0C()
    r0E = REG0E()
    r0F = REG0F()
    r11 = REG11()
    r12 = REG12()
    r12.address()

    print(r02)
    r02.CONV_START = 1
    print(r02)
