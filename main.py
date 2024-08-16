import argparse
import uuid

from src.utils.common import init_logger
from src.preprocess.main_preprocess import preprocess_raw_files
from src.vdb.vdb_main import update_vector_db, retreive_similar_docs
from src.llm.form_answer import form_answer_with_rag_qa_pairs

def main(args):

    # Switch case to run different flow
    match args.action:
        case "answer":
            answer_one_question(args)

        case "indexdb":
            parse_files_and_index_db(args)
        
        case _:
            e = "Incorrect `action` argument!"
            logger.error(e)
            raise Exception(e)


def parse_files_and_index_db(args):

    # preprocess unstructured files
    structured_qa_pairs = preprocess_raw_files(args)

    # TODO logic to define what is already processed
    #   - check vector DB existance
    #   - get list of already indexed files (copare by date_modified?) 

    try:
        # create DB, populate and index it
        update_vector_db(structured_qa_pairs)

        e = "parse_files_and_index_db flow completed successfully."
        logger.info(e)

    except:
        e = "An error within adding/updating Documents into the vector store."
        logger.error(e)
        raise Exception(e)


def answer_one_question(args):

    # Log
    logger.info(f"Start question processing, question: {args.question}")

    # Retrieve similar docs
    retrieved_docs = retreive_similar_docs(args.question)

    # Form answer
    answer = form_answer_with_rag_qa_pairs(args.question, retrieved_docs)

    # Log
    logger.info(f"Answer formed, answer: {answer}")
    print(answer)


def get_args():

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument("--questionnaire-file-path", dest="questionnaire_path")
    parser.add_argument("--question", dest="question")
    parser.add_argument("--filled-questionnaire-files-path", dest="input_files_path")
    parser.add_argument("--action", dest="action", choices=["answer", "indexdb"])

    args, _ = parser.parse_known_args()

    return args

if __name__ == "__main__":
    
    args = get_args()

    args.run_id = str(uuid.uuid4())
    print(args)

    logger = init_logger(args)

    main(args)
