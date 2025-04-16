import collections
import inspect
import re
from functools import lru_cache

from flask import Flask, jsonify, render_template, request

from bq2589xpy.driver_builder import create
from bq2589xpy.register import Register

app = Flask(__name__)
drivers = create()

# todo: consider to rewrite the following code to use Quart instead of Flask
# to make code more async-friendly, or consider to migrate to microdot
# to have support for micropython

# set FLASK_APP=bq2589xpy/app/main.py
# python -m flask run


class ValueHistory:
    def __init__(self):
        self.previous_values = {}

    def check_history(self, key: str = None, value: str = None):
        previous = self.previous_values.get(key)
        is_changed = previous is not None and previous != value
        self.previous_values[key] = value
        return is_changed


value_history = ValueHistory()


def get_registers(driver, update: bool = False):
    registers = collections.OrderedDict()
    for reg_name in dir(driver):
        if reg_name.startswith("REG"):
            reg_instance = getattr(driver, reg_name)
            if update:
                driver.read(reg_instance)

            reg = type(reg_instance)
            bit_fields = collections.OrderedDict()

            for bit_name in reg._fields_:
                bit_field = getattr(reg_instance, bit_name)
                bit_fields[bit_name] = {
                    "value": bit_field,
                    "doc": get_bit_filed_doc(reg_instance, bit_name),
                    "size": getattr(reg, bit_name).width,
                    "has_changed": value_history.check_history(f"{driver.name()}{reg_name}{bit_name}", bit_field),
                }

            registers[reg_name] = {
                "address": reg_instance.address(),
                "value": reg_instance.value,
                "doc": reg.__doc__,
                "bit_fields": bit_fields,
                "has_changed": value_history.check_history(reg_name, reg_instance.value),
            }

    return registers


@lru_cache
def get_bit_filed_doc(reg: Register, bit_field_name: str):
    source = inspect.getsource(type(reg))
    doc = re.search(rf'{bit_field_name} =.*?"""(.*?)"""', source, re.DOTALL)
    return doc.group(1).replace("\n", "<br>") if doc else ""


@app.route("/drivers")
def list_drivers():
    return jsonify({"drivers": [driver.name() for driver in drivers]})


def get_driver(driver_name: str):
    for driver in drivers:
        if driver.name() == driver_name:
            return driver
    return None


@app.route("/")
def index():
    return render_template("index.html", drivers=[driver.name() for driver in drivers])


@app.route("/registers")
def registers():
    driver_name = request.args.get("driver")
    driver = get_driver(driver_name)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404
    return render_template("registers.html", registers=get_registers(driver, update=False))


@app.route("/read_registers")
def read_registers():
    driver_name = request.args.get("driver")
    driver = get_driver(driver_name)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404
    return render_template("registers.html", registers=get_registers(driver, update=True))


@app.route("/update_register", methods=["POST"])
def update_register():
    driver_name = request.form["driver"]
    driver = get_driver(driver_name)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404
    reg_name = request.form["register"]
    value = int(request.form["value"], 2)
    reg_instance = getattr(driver, reg_name)
    reg_instance.value = value
    driver.write(reg_instance)
    return jsonify({"status": "success", "message": f"Register {reg_name} updated successfully."})


@app.route("/update_bit_field", methods=["POST"])
def update_bit_field():
    driver_name = request.form["driver"]
    driver = get_driver(driver_name)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404
    reg_name = request.form["register"]
    bit_field_name = request.form["bit_field"]
    value = int(request.form["value"], 2)
    reg_instance = getattr(driver, reg_name)
    setattr(reg_instance, bit_field_name, value)
    driver.write(reg_instance)
    return jsonify(
        {"status": "success", "message": f"Bit field {bit_field_name} in register {reg_name} updated successfully."}
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
