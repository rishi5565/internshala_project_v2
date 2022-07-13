from attr import validate
import pandas as pd
import argparse
from logger.myLogger import getmylogger
# from validator.validator import 

logger = getmylogger(__name__)


def validate_raw_data():
    



    pass




















if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    validate_raw_data(config_path=parsed_args.config)