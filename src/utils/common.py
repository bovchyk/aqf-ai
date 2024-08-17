import logging
import os
from argparse import Namespace

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma

OPENAI_LLM_MODEL=os.getenv("OPENAI_LLM_MODEL")
OPENAI_EMBEDDING_MODEL=os.getenv("OPENAI_EMBEDDING_MODEL")
COLLECTION_NAME= os.getenv("COLLECTION_NAME")

def init_logger(args: Namespace) -> None:
    """
    Logger initiation.

    Args:
        args (Namespace): command line arguments
    
    Returns:
        logger (object): returns logger object
    """
    
    path = os.path.join(os.getcwd(),'data/logs')

    if not os.path.exists(path):
        os.mkdir(path)

    logging.basicConfig(filename=path+'/'+args.run_id+'.log', level=logging.DEBUG)

    logger = logging.getLogger(__name__)

    # logger.info(f"Logging initialized successfully, run_id: {args.run_id}")

    return logger

def get_vectore_store():

    vector_db_path = os.path.join(os.getcwd(), 'src/vdb/chroma_langchain_db')

    # Create vector store
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=vector_db_path,  # Where to save data locally, remove if not neccesary
    )

    return vector_store

def get_llm():

    return ChatOpenAI(model=OPENAI_LLM_MODEL)