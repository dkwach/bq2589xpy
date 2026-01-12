# Driver Composer
Simple package to qucly start prototyping with i2c controlled device when there is no existing
i2c driver. It is providing utilities to:
* write your own driver just by defining registers classes by coping description and some minimal set
of metadata from i2c device datasheet.
* register monitor - simple flask app, which monitor and write registers in connected devices controlled by env variables.
* generator - simple agent, which can read device datasheet and generate driver for you.

# Platform
 * linux based - raspberry pi
 * micropython comatiblityy - WIP

# core
 It is providing all utilities to define bit fields, registers and driver.
 Look at tusb320 example to see what you have to do define to get working driver.

 Implementation is based on python descriptors and small metadata class to make order of bit field declaration meaningful -
 order should reflect register layout (from less meaningful bit at top of register class definition)

# monitor

Small Flask app to monitor/write drivers in web interface controlled by env variables.
See examples/.env.example as reference

Install with ui option
```
pip install .[ui]
```

Run
```
python -m flask --app driver_composer.register_monitor.main -e examples/.env.ui.example run
```


# generator
Graph/agent which can generate driver for you just by providing path or url to device datasheet

> [!CAUTION]
> AI agents can hallucinate (produce incorrect or misleading output). For that reason, any generated driver must be reviewed and thoroughly
> tested before use. Using a driver without proper verification is at your own risk and may lead to malfunctions, data loss, or damage to your > device.

> [!CAUTION]
> In default configuration input file, will be send to llm (openAI), please keep in mind what you are sending and check how model provider
is processing and keeping sent data.


Install with ai option
```
pip install .[ai]
```

Set your openAI key and set model before usage
You can use `examples/.env.ai.example` as reference
or change llm.py to use different model


Usage

> [!CAUTION]
> This llm run can be token consuming so be careful.


```
python -m driver_composer.generator --datasheet-path path_to_local_pdf_or_url_with_pdf```
