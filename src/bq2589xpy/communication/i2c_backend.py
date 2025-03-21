import logging

logger = logging.getLogger(__name__)


class I2C:
    def write_byte(self, device_address: int, offset: int, value: int):
        logger.info("Writing to device %s at offset %s value %s", device_address, offset, value)

    def read_byte(self, device_address: int, offset: int) -> int:
        logger.info("Reading from device %s at offset %s", device_address, offset)
