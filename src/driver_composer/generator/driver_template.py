TEMPLATE = '''
from driver_composer.driver import Driver
from driver_composer.register import BitField, Register

{% for reg in model.registers %}class {{ reg.name }}(Register):
{% for field in reg.fields | sort(attribute="bit_offset") %}    {{ field.name }} = BitField(width={{ field.bit_width }}, default={{ field.default }})
    """
    {{ field.description | wordwrap() | indent() | default('No description provided.') }}
    """
{% endfor %}
{% endfor %}

class {{ model.driver_name }}(Driver):
{% for reg in model.registers %}    {{ reg.name }} = {{ reg.name }}()
{% endfor %}

    def __init__(self, i2c, device_address={{ model.i2c_address }}):
        super().__init__(i2c, device_address)
'''
