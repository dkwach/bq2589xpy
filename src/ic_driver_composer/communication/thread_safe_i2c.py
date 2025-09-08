import threading

from .i2c_backend import I2C


class ThreadSafeI2C:
    def __init__(self, i2c: I2C):
        self._i2c = i2c
        self._lock = threading.Lock()

    def write_byte(self, device_address: int, offset: int, value: int):
        with self._lock:
            self._i2c.write_byte(device_address, offset, value)

    def read_byte(self, device_address: int, offset: int) -> int:
        with self._lock:
            return self._i2c.read_byte(device_address, offset)
