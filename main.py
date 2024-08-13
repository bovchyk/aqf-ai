import argparse
import uuid
import sys

from src.utils.common import init_logger
from src.preprocess.main_preprocess import preprocess_raw_files

def main(args):

    # Switch case to run different flow
    match args.action:
        case "answer":
            print("TODO, not implemented answer")

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

    # create DB, populate and index it
    # TODO

    e = "parse_files_and_index_db flow completed successfully."
    print(e)
    return logger.info(e)

def answer_one_question():

    return 0

def get_args():

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument("--questionnaire-file-path", dest="questionnaire_path")
    parser.add_argument("--filled-questionnaire-files-path", dest="input_files_path")
    parser.add_argument("--action", dest="action")

    args, _ = parser.parse_known_args()

    return args

if __name__ == "__main__":
    
    args = get_args()
    print(args)

    args.run_id = str(uuid.uuid4())

    logger = init_logger(args)

    main(args)
