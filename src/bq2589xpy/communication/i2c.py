class I2C:
    def write_byte(self, device_address: int, offset: int, value: int):
        raise NotImplementedError

    def read_byte(self, device_address: int, offset: int) -> int:
        raise NotImplementedError
