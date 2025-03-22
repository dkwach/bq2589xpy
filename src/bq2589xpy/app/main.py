import collections
import inspect
import re
from functools import lru_cache

from flask import Flask, jsonify, render_template, request

from bq2589xpy.driver import Bq25895Driver, create
from bq2589xpy.register import Register

app = Flask(__name__)
driver = create()


# set FLASK_APP=bq2589xpy/app/main.py
# python -m flask run


@lru_cache
def get_bit_filed_doc(reg: Register, bit_field_name: str):
    source = inspect.getsource(reg)
    doc = re.search(rf'{bit_field_name}.*?"""(.*?)"""', source, re.DOTALL)
    return doc.group(1).replace("\n", "<br>") if doc else ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registers")
def registers():
    registers = collections.OrderedDict()
    for reg_name in dir(Bq25895Driver):
        if reg_name.startswith("REG"):
            reg = getattr(Bq25895Driver, reg_name)
            reg_instance = driver.read(reg())
            bit_fields = collections.OrderedDict()
            for bit_name in reg._fields_:
                bit_field = getattr(reg_instance, bit_name)
                bit_fields[bit_name] = {
                    "value": bit_field,
                    "doc": get_bit_filed_doc(reg, bit_name),
                    "size": getattr(reg, bit_name).width,
                }
            registers[reg_name] = {
                "address": reg_instance.address(),
                "value": reg_instance.value,
                "doc": reg.__doc__,
                "bit_fields": bit_fields,
            }

    return render_template("registers.html", registers=registers)


@app.route("/update_register", methods=["POST"])
def update_register():
    reg_name = request.form["register"]
    value = int(request.form["value"], 2)
    reg = getattr(Bq25895Driver, reg_name)
    reg_instance = reg()
    reg_instance.value = value
    driver.write(reg_instance)
    return jsonify({"status": "success", "message": f"Register {reg_name} updated successfully."})


@app.route("/update_bit_field", methods=["POST"])
def update_bit_field():
    reg_name = request.form["register"]
    bit_field_name = request.form["bit_field"]
    value = int(request.form["value"], 2)
    reg = getattr(Bq25895Driver, reg_name)
    reg_instance = driver.read(reg())
    setattr(reg_instance, bit_field_name, value)
    driver.write(reg_instance)
    return jsonify(
        {"status": "success", "message": f"Bit field {bit_field_name} in register {reg_name} updated successfully."}
    )


if __name__ == "__main__":
    app.run(debug=True)
