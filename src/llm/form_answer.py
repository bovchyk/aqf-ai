import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

from src.utils.common import get_llm

LANGCHAIN_TRACING_V2=os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT=os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT=os.getenv("LANGCHAIN_PROJECT")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

def form_answer_with_rag_qa_pairs(question, retrieved_docs) -> str:
    # TODO as idea: move `retrieved_docs=retreive_similar_docs(args.question)`` from main py her
    
    # Define llm client
    llm = get_llm()
    
    # Generate context string
    context = ""
    for ind in range(0, len(retrieved_docs)):
        context += "\n\nQuestion:" + retrieved_docs[ind].page_content
        context += "Answer:" + retrieved_docs[ind].metadata["answer"]


    # Template
    template = """Use the answers to similar questions within QA_PAIRS section to answer the question at the end.
    If QA_PAIRS section is empty, just say that you don't know, don't try to make up an answer.
    Select the most relevant question-answer pairs and provide reference/requirement points if eligible and according to existing answers. 
    Use two sentences maximum and keep the answer as concise as possible.

    QA_PAIRS:
    {context}

    USER_QUESTION:
    {question}
    Helpful answer:"""
    custom_rag_prompt = PromptTemplate.from_template(template)
    
    # Define langchain chain    
    rag_chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    # Invoke the chain
    llm_response = rag_chain.invoke({
        "context": context,
        "question": question
    })

    return llm_response
