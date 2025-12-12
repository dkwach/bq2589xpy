import logging
import pathlib

import typer
from pydantic import BaseModel, Field

from .driver_model import DriverModel
from .llm import llm
from .utils import render_template


class Template(BaseModel):
    """Represents the generated Jinja2 template"""

    generated_template: str = Field(
        description="The generated Jinja2 template for the IC python driver"
    )


prompt = """
Create a Jinja2 template for generating an IC python driver.,
Data, which will be filled in template will be fallowing Pydantic model:\n\n,
{model_content}

Order of registers and fields inside registers matters.
Look at core driver implementation to understand how registers and bits are ordered.
{driver_core}

Do not comment any code and do not add any extra text.
Just provide the template content.

As a example driver use the following files
{example_driver}
"""

app = typer.Typer()


def read_python_files(path: str) -> str:
    prompt_parts = []
    p = pathlib.Path(path)
    for file_path in p.glob("*.py"):
        logging.info(f"Reading file: {file_path}")
        prompt_parts.append(f"File: {file_path.name}\n")
        prompt_parts.append("```python\n")
        prompt_parts.append(file_path.read_text())
        prompt_parts.append("\n```\n\n")

    return "\n".join(prompt_parts)


@app.command()
def create_template(example_driver_path: str, out_path: str):
    current_path = pathlib.Path(__file__).parent
    example_driver = read_python_files(example_driver_path)
    model_content = (current_path / "driver_model.py").read_text()
    driver_core = read_python_files(current_path.parent)

    res = llm.with_structured_output(Template).invoke(
        prompt.format(
            model_content=model_content,
            driver_core=driver_core,
            example_driver=example_driver,
        )
    )
    out_file = pathlib.Path(out_path)
    out_file.write_text(res.generated_template)
    logging.info(f"Template written to {out_file}")


@app.command()
def render(model_path: str, code_path: str):
    model_data = pathlib.Path(model_path).read_text()
    model = DriverModel.model_validate_json(model_data)
    driver_code = render_template(model)
    out_file = pathlib.Path(code_path)
    out_file.write_text(driver_code)


if __name__ == "__main__":
    app()
