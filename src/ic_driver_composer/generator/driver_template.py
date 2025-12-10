TEMPLATE = '''
from ic_driver_composer.driver import Driver
from ic_driver_composer.register import BitField, Register

{% if data is defined %}{% set registers = data.registers %}{% set driver_name = data.name %}{% elif model is defined %}{% set registers = model.registers %}{% set driver_name = model.name %}{% else %}{% set registers = [] %}{% set driver_name = 'Driver' %}{% endif %}

{% for reg in registers %}class {{ reg.name }}(Register):
{% for field in reg.fields | sort(attribute="bit_offset") %}    {{ field.name }} = BitField(width={{ field.bit_width }}, default={{ field.default }})
    """
    {{ field.description | wordwrap() | indent() | default('No description provided.') }}
    """
{% endfor %}
{% endfor %}

class {{ driver_name }}(Driver):
{% for reg in registers %}    {{ reg.name }} = {{ reg.name }}()
{% endfor %}

    def __init__(self, i2c, device_address=0):
        super().__init__(i2c, device_address)
'''
