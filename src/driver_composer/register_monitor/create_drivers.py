import importlib
import os

from driver_composer.communication.safe_i2c import ThreadSafeI2C


def create(backend: str = "", drivers_list: list[str] = None) -> tuple:
    backend = backend or os.environ.get("I2C_BACKEND")
    if backend == "smbus":
        from driver_composer.communication import smbus

        i2c_backend = smbus.SMbusI2C()
    else:
        from driver_composer.communication import mock

        i2c_backend = mock.MockI2C()

    thread_safe_i2c = ThreadSafeI2C(i2c_backend)

    drivers = []
    for driver_path in drivers_list if drivers_list else _get_drivers_module_paths():
        module_path, class_name = driver_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        driver_cls = getattr(module, class_name)
        drivers.append(driver_cls(thread_safe_i2c))

    return tuple(drivers)


def _get_drivers_module_paths():
    drivers_env = os.environ.get("DRIVERS", "")
    return [d.strip() for d in drivers_env.split(",") if d.strip()]
