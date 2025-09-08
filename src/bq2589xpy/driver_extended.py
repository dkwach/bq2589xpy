import logging
import time

from bq2589xpy import driver, registers

logger = logging.getLogger(__name__)


def run_in_thread(fun, args=()):
    """Run a function in a separate thread with micropython support."""
    try:
        import threading

        t = threading.Thread(target=fun, args=args, daemon=True)
        t.start()
    except ImportError:
        import _thread

        _thread.start_new_thread(fun, args)


class Bq25895ExtendedDriver(driver.Bq25895Driver):
    def __init__(self, i2c, device_address=0x6A, run_watchdog=True):
        super().__init__(i2c, device_address)

        if run_watchdog:
            run_in_thread(self.reset_watchdog_periodically)

    def read_faults(self) -> registers.REG0C:
        return self.read(registers.REG0C())

    def read_current_limit(self) -> registers.REG00:
        return self.read(registers.REG00())

    def read_status(self) -> registers.REG0B:
        return self.read(registers.REG0B())

    def read_bat_adc(self) -> registers.REG0E:
        return self.read(registers.REG0E())

    def trigger_adc_conversion(self):
        reg02: registers.REG02 = self.read(registers.REG02())
        reg02.CONV_START = 1
        self.write(reg02)

    def configure_otg(self, enable=True):
        reg03: registers.REG03 = self.read(registers.REG03())
        if bool(reg03.OTG_CONFIG) != enable:
            reg03.OTG_CONFIG = enable
            self.write(reg03)

    def reset_watchdog(self):
        reg03: registers.REG03 = self.read(registers.REG03())
        reg03.WD_RST = 1
        self.write(reg03)

    def reset_watchdog_periodically(self):
        while True:
            logger.info("Reset watchdog")
            self.reset_watchdog()
            time.sleep(20)
