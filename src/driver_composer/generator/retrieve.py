import nltk
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from nltk.tokenize import word_tokenize

nltk.download("punkt_tab")


def make_retriever(docs: list, fraction_of_doc_to_use: float) -> BaseRetriever:
    fraction_of_doc_to_use = 0.25
    k_top = int(len(docs) * fraction_of_doc_to_use)
    return BM25Retriever.from_documents(docs, preprocess_func=word_tokenize, k=k_top)


async def retrieve_documents(retriever: BaseRetriever, query: str) -> list[Document]:
    results = await retriever.ainvoke(query)
    return results
