from langchain_openai import ChatOpenAI

from .config import conf

llm = ChatOpenAI(model=conf.model_name, temperature=0, api_key=conf.openai_api_key)
