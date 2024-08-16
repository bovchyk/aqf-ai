import os

from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from uuid import uuid4

from src.utils.common import get_llm, get_vectore_store



LANGCHAIN_TRACING_V2=os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT=os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT=os.getenv("LANGCHAIN_PROJECT")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

def form_answer_with_rag_qa_pairs(question, retrieved_docs) -> str:

    llm = get_llm()

    vector_store = get_vectore_store()

    # по ходу `retreive_similar_docs(question, docs_filter=None)` з src/vdb/vdb_main.py лишнє
    #   треба тільки розібратися як ленгчейн працює (додати doc.metadata["answer"])


    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vector_store.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain.invoke(question)
