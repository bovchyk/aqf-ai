import logging
import os
from argparse import Namespace

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