# Driver Composer

Driver Composer is a simple package designed to help you quickly prototype with I2C-controlled devices when no existing I2C driver is available. It provides utilities for:

- Writing your own driver by defining register classes based on the device datasheet, with minimal metadata.
- A register monitor: a simple Flask app to monitor and write registers in connected devices, controlled via environment variables.
- A generator: an agent that can read a device datasheet and generate a driver for you.

---

## Platform Compatibility

- **Linux-based systems**: e.g., Raspberry Pi.
- **MicroPython compatibility**: Work in progress (WIP).

---

## Core Functionality

The core of Driver Composer provides utilities to define bit fields, registers, and drivers. Check the `tusb320` example to understand the minimal requirements for defining a working driver.

The implementation is based on Python descriptors and a small metadata class to ensure the order of bit field declarations reflects the register layout (from the least significant bit at the top of the register class definition).

---

## Register Monitor

The register monitor is a small Flask app that provides a web interface to monitor and write registers. It is controlled via environment variables.

### Installation

Install the package with the `ui` option:

```
pip install .[ui]
```

### Running the Monitor

Run the Flask app with the following command:

```
python -m flask --app driver_composer.register_monitor.main --env-file examples/.env.ui.example run
```

Refer to `examples/.env.example` for environment variable configuration.

---

## Driver Generator

The generator is an agent that can create a driver for you by analyzing the path or URL of a device datasheet.

> **⚠ CAUTION**
> AI agents can produce incorrect or misleading output. Any generated driver must be reviewed and thoroughly tested before use. Using an unverified driver may lead to malfunctions, data loss, or device damage.

> **⚠ CAUTION**
> By default, the input file will be sent to an LLM (e.g., OpenAI). Be mindful of the data you share and review the model provider's data processing and retention policies.

### Installation

Install the package with the `ai` option:

```
pip install .[ai]
```

### Configuration

Set your OpenAI API key and model before usage. You can use `examples/.env.ai.example` as a reference or modify `llm.py` to use a different model.

### Usage

> **⚠ CAUTION**
> Running the LLM can consume a significant number of tokens. Use it cautiously.

Run the generator with the following command:

```
python -m driver_composer.generator --datasheet-path path_to_local_pdf_or_url_with_pdf
```

---

## Examples

Refer to the `examples` directory for sample `.env` files and usage scenarios.
