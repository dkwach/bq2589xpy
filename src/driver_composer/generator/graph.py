from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from .driver_model import DriverModel
from .llm import llm
from .retrieve import make_retriever, retrieve_documents
from .utils import read_pdf, render_template


class AgentConfig(BaseModel):
    fraction_of_doc_to_use: float = Field(
        0.3,
        description="Fraction of the document to use for retrieval",
        ge=0.0,
        le=1.0,
    )
    register_keywords: list[str] | None = Field(
        [
            "Registers",
            "Register Map",
            "Register Description",
            "Register Summary",
        ],
        description="Keywords to identify register-related sections in the datasheet",
    )


class InputState(BaseModel):
    datasheet: str
    datasheet_pages: list[int] | None = None
    additonal_information: str | None = None
    config: AgentConfig = AgentConfig()


class OutputState(BaseModel):
    driver_code: str | None = None
    model: DriverModel | None = None


class InternalState(InputState, OutputState):
    datasheet_content: str | None = None
    datasheet_docs: list | None = None
    docs_with_registers: list | None = None


async def read_datasheet(state: InternalState) -> InternalState:
    content, docs = await read_pdf(state.datasheet)
    state.datasheet_content = content
    state.datasheet_docs = docs

    return state


async def retrieve_docs_with_registers(state: InternalState) -> InternalState:
    state.docs_with_registers = await retrieve_documents(
        retriever=make_retriever(state.datasheet_docs, state.config.fraction_of_doc_to_use),
        query=", ".join(state.config.register_keywords),
    )
    return state


async def set_docs_with_registers(state: InternalState) -> InternalState:
    state.docs_with_registers = state.datasheet_docs[*state.datasheet_pages]
    return state


async def create_driver_model(state: InternalState) -> InternalState:
    structured_llm = llm.with_structured_output(DriverModel)
    prompt_parts = [
        "Extract all registers from the following datasheet content.",
        "Provide the register name, address, description, and fields,"
        "(with their name, bit offset, bit width, description, access type, and default value).",
        "Reserved/Dummy fields should also be included with their bit offset and width. "
        "(In case of two or more reserved fields call them Reserved1, Reserved2, etc.)",
        "If there are no registers, return an empty list.",
        "\n\nDatasheet Content:\n",
        state.datasheet_content,
    ]
    if state.additonal_information:
        prompt_parts.insert(
            3,
            f"\n\nAdditional Information:\n{state.additonal_information}\n\n",
        )

    prompt = "".join(prompt_parts)
    state.model = await structured_llm.ainvoke(prompt)
    return state


async def generate_driver_code(state: InternalState) -> InternalState:
    driver_code = render_template(state.model)
    state.driver_code = driver_code
    return state


def create_graph() -> StateGraph:
    builder = StateGraph(InternalState, input_schema=InputState, output_schema=OutputState)
    builder.add_node("read_datasheet", read_datasheet)
    builder.add_node("retrieve_docs_with_registers", retrieve_docs_with_registers)
    builder.add_node("set_docs_with_registers", set_docs_with_registers)
    builder.add_node("create_driver_model", create_driver_model)
    builder.add_node("generate_driver_code", generate_driver_code)

    builder.add_edge(START, "read_datasheet")
    builder.add_conditional_edges(
        "read_datasheet",
        lambda state: "set_docs_with_registers" if state.datasheet_pages else "retrieve_docs_with_registers",
    )
    builder.add_edge("set_docs_with_registers", "create_driver_model")
    builder.add_edge("retrieve_docs_with_registers", "create_driver_model")
    builder.add_edge("create_driver_model", "generate_driver_code")

    builder.add_edge("generate_driver_code", END)

    graph = builder.compile()

    return graph
