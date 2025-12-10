import tempfile
from typing import Any

import aiofiles
import aiohttp
from jinja2 import Template
from langchain_community.document_loaders import PyPDFLoader

from . import driver_template


async def extract_text_from_pdf(pdf_path: str) -> tuple[str, tuple]:
    loader = PyPDFLoader(pdf_path)
    docs = await loader.aload()
    content = "".join(d.page_content for d in docs)
    return content, tuple(docs)


async def read_pdf(pdf_path_or_url: str) -> str:
    if pdf_path_or_url.endswith(".pdf"):
        return await extract_text_from_pdf(pdf_path_or_url)
    elif pdf_path_or_url.startswith("http://") or pdf_path_or_url.startswith(
        "https://"
    ):
        async with aiohttp.ClientSession() as session:
            async with session.get(pdf_path_or_url) as response:
                response.raise_for_status()
                with tempfile.NamedTemporaryFile(
                    suffix=".pdf", delete=False
                ) as tmp_file:
                    tmp_file_path = tmp_file.name
                    async with aiofiles.open(tmp_file_path, mode="wb") as f:
                        await f.write(await response.read())
                    return await extract_text_from_pdf(tmp_file_path)
    else:
        raise ValueError("The provided path or URL is not a valid PDF.")


def render_template(model: Any):
    jinja_template = Template(driver_template.TEMPLATE)
    return jinja_template.render(model=model)
