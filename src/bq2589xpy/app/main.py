import collections
import inspect
import re
import threading
import time
from functools import lru_cache

from flask import Flask, jsonify, render_template, request

from bq2589xpy.driver import create
from bq2589xpy.register import Register

app = Flask(__name__)
driver = create()

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


def get_registers(update: bool = False):
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
                    "has_changed": value_history.check_history(f"{reg_name}{bit_name}", bit_field),
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
    doc = re.search(rf'{bit_field_name}.*?"""(.*?)"""', source, re.DOTALL)
    return doc.group(1).replace("\n", "<br>") if doc else ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registers")
def registers():
    return render_template("registers.html", registers=get_registers(update=False))


@app.route("/read_registers")
def read_registers():
    return render_template("registers.html", registers=get_registers(update=True))


@app.route("/update_register", methods=["POST"])
def update_register():
    reg_name = request.form["register"]
    value = int(request.form["value"], 2)
    reg_instance = getattr(driver, reg_name)
    reg_instance.value = value
    driver.write(reg_instance)
    return jsonify({"status": "success", "message": f"Register {reg_name} updated successfully."})


@app.route("/update_bit_field", methods=["POST"])
def update_bit_field():
    reg_name = request.form["register"]
    bit_field_name = request.form["bit_field"]
    value = int(request.form["value"], 2)
    reg_instance = getattr(driver, reg_name)
    setattr(reg_instance, bit_field_name, value)
    driver.write(reg_instance)
    return jsonify(
        {"status": "success", "message": f"Bit field {bit_field_name} in register {reg_name} updated successfully."}
    )


def reset_watchdog_periodically():
    while True:
        driver.reset_watchdog()
        time.sleep(20)


# Start the background thread
threading.Thread(target=reset_watchdog_periodically, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)
