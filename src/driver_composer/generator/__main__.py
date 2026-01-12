import asyncio
import pathlib

import typer

from .graph import OutputState, create_graph

if __name__ == "__main__":
    app = typer.Typer()

    @app.command()
    def make_driver(
        datasheet_path: str = "examples/MP2722GRH.pdf",
        collected_model_path: str = "examples/mp2722_mode.json",
        driver_path: str = "examples/mp2722_driver.py",
    ):
        graph = create_graph()
        res = asyncio.run(graph.ainvoke({"datasheet": datasheet_path}))

        out = OutputState(**res)
        pathlib.Path(collected_model_path).write_text(out.model.model_dump_json(indent=4))
        pathlib.Path(driver_path).write_text(out.driver_code)

    app()
