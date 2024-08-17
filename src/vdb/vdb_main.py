import os
import logging
from langchain_openai import ChatOpenAI

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from uuid import uuid4

# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

from src.utils.common import get_vectore_store

logger = logging.getLogger(__name__)

def update_vector_db(structured_qa_pairs: dict[list]):
    # Log
    logger.info("Start populating vector store")

    # Create Chroma documents (question as content, answer as metadata)
    documents = []
    for file in structured_qa_pairs:
        quest, answ = tuple(structured_qa_pairs[file].keys())
        # print(structured_qa_pairs[file][quest], structured_qa_pairs[file][answ])
        
        ids=0
        for quest_, answ_ in zip(structured_qa_pairs[file][quest], structured_qa_pairs[file][answ]):
            # print(quest_, answ_)
            documents += [Document(
                page_content = quest_,
                metadata = {
                    "source": file,
                    "answer": answ_
                },
                id = ids
            )]
            ids += 1

    # Log
    logger.info("Question-answer (Chroma Documents) pairs formed.")

    try:
        # Get vector store
        vector_store = get_vectore_store()

        # Log
        logger.info("Vector store obtained")

        # Define uuids for every Document
        uuids = [str(uuid4()) for _ in range(len(documents))]

        # Add/Update Documents into vector store
        vector_store.add_documents(documents=documents, ids=uuids)

        # Log
        logger.info("Documents added to vector store")
    except:
        e = "Error in get_vector_store or add_documents block"
        logger.error(e)
        raise Exception(e)

    return True

def retreive_similar_docs(question, docs_filter=None):
    # Log
    logger.info("Start retriving similar docs from vdb")

    vector_store = get_vectore_store()

    results = vector_store.similarity_search(
        question,
        k=3,
        # filter={"source": "Adyen_SQ.xls"}, # TODO impletent additional filtration using docs_filter input param
    )

    # Log
    logger.info("Similar docs found, here content: ")
    for res in results:
        logger.info(f"* {res.page_content} [{res.metadata}]")
    
    return results
