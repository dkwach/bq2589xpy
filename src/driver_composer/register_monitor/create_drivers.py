import importlib
import os

from driver_composer.communication.i2c import I2C
from driver_composer.communication.safe_i2c import ThreadSafeI2C


def create(backend: str = "", drivers_list: list[str] = None) -> tuple:
    i2c_backend = _get_backend(backend)

    return tuple(_get_drivers(drivers_list, ThreadSafeI2C(i2c_backend)))


def _get_backend(backend: str):
    backend = backend or os.environ.get("I2C_BACKEND")
    if backend == "smbus":
        from driver_composer.communication import smbus

        return smbus.SMbusI2C()
    if backend == "mock":
        from driver_composer.communication import mock

        return mock.MockI2C()

    raise ValueError(f"Unknown I2C backend: {backend}")


def _get_drivers(i2c: I2C, drivers_list: list[str] = None):
    drivers = []
    for driver_path in drivers_list or _get_drivers_module_paths():
        module_path, class_name = driver_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        driver_cls = getattr(module, class_name)
        drivers.append(driver_cls(i2c))
    return drivers


def _get_drivers_module_paths():
    drivers_env = os.environ.get("DRIVERS", "")
    return [d.strip() for d in drivers_env.split(",") if d.strip()]
