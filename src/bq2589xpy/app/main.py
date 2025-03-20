import collections
import inspect
import re
from functools import lru_cache

from flask import Flask, render_template

from bq2589xpy.driver import Bq25895Driver, create
from bq2589xpy.register import Register

app = Flask(__name__)
driver = create()


@lru_cache
def get_bit_filed_doc(reg: Register, bit_field_name: str):
    source = inspect.getsource(reg)
    doc = re.search(rf'{bit_field_name}.*?"""(.*?)"""', source, re.DOTALL)
    return doc.group(1).replace("\n", "<br>") if doc else ""


@app.route("/")
def index():
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

    return render_template("template.html", registers=registers)


if __name__ == "__main__":
    app.run(debug=True)
