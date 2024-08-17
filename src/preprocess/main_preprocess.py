import os
import logging
import glob
import pandas as pd
import spacy
import itertools

from argparse import Namespace
from re import search

# init logger
logger = logging.getLogger(__name__)
TARGET_SHEET_NAMES=os.getenv("TARGET_SHEET_NAMES")

def preprocess_raw_files(args: Namespace) -> dict:
    # define path to the files 
    input_files_path = os.path.join(os.getcwd(), args.input_files_path)
    if not os.path.exists(input_files_path): 
        e = f"Incorrect files path provided: {input_files_path}"
        logger.error(e)
        raise Exception(e)
    
    # check spacy model for existance, if not then download
    # Load spacy 
    nlp = load_spacy_model("en_core_web_md")

    qa_pairs = {}
    # loop over all files in folder
    for file in glob.glob(input_files_path + '/*'):
        fname, extension = os.path.splitext(os.path.basename(file))
        match extension:
            case ".xls" | ".xlsx":
                q_a = parse_xls(file, nlp)
            case _:
                raise Exception(f"File extension {extension} not realized yet. Contact Valentyn.")

        # form dict of q_a file paris inside general qa_pairs dict
        qa_pairs[fname+extension] = q_a

    return qa_pairs


def load_spacy_model(model_name):
    # Function to check if a model is already installed
    def is_model_installed(model_name):
        try:
            spacy.load(model_name)
            return True
        except OSError:
            return False

    # Check if the model is installed, if not, download it
    if not is_model_installed(model_name):
        logger.info(f"Model '{model_name}' not found. Downloading...")
        spacy.cli.download(model_name)
        logger.info(f"Model '{model_name}' loading...")
        nlp = spacy.load("en_core_web_md")
    else:
        logger.info(f"Model '{model_name}' is already installed, loading...")
        nlp = spacy.load("en_core_web_md")

    return nlp


def parse_xls(file_name_path: str, nlp: object) -> dict:
    # Log
    logger.info("Xls/xlsx parsing started.")

    # Read all sheets of file
    file_dict = pd.read_excel(file_name_path, sheet_name=None)
    sheet_names = list(file_dict.keys())
    
    # Find sheets using regexp
    # Split the string by comma
    patterns_list = TARGET_SHEET_NAMES.split(",")
    patterns_list = [x.strip() for x in patterns_list]
    
    # Search sheet names matching sheet name patterns
    sheet_names_list = []
    for pattern in patterns_list:
        sheet_names_list += [s for s in sheet_names if search(pattern, s)]
    # Remove duplicates from the list
    sheet_names_list = list(set(sheet_names_list))

    # internal, nlp object is not iterable so it should be inside this method
    #   fyi: non iterables can't be passed through map()
    def _spacy_similarity(doc1, doc2):
        return nlp(doc1).similarity(nlp(doc2))

    # Load data from the sheet
    #   TODO for now, we assume that there is only a one sheet corresponding to the match
    #   logic if there are two or more sheets corresponding to the match
    if not sheet_names_list == None:
        df = file_dict[sheet_names_list[0]]
        # Drop rows with NaN in any column
        df.dropna(inplace=True)
        df.reset_index(inplace=True, drop=True)
        
        # calculated text similarities between two pairs of columns
        for (col1, col2) in itertools.combinations(list(df.columns), 2):
            df[col1 + "<bovchyk>" + col2] = list(map(_spacy_similarity, df[col1], df[col2]))

        # finds columns pair with highest text similarity
        col_pair = df.select_dtypes(include=float).mean().idxmax()
        col1, col2 = col_pair.split("<bovchyk>")

        # filter question-answer dataframe to return
        q_a = df[[col1, col2]].to_dict(orient='list')
    
        # Log 
        logger.info("Xls/xlsx parsing completed.")
    
    else:
        e = f"No sheet found with 'Question' regexp match to find for q_a pairs."
        logger.error(e)
        raise Exception(e)

    return q_a