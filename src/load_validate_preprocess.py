
import pandas as pd
import argparse
from logger.myLogger import getmylogger
from validator.validator import validate_data
from preprocessor.preprocessor import preprocess_data
from functions import read_params

logger = getmylogger(__name__)


def validate_raw_data(config_path):
    config = read_params(config_path)
    data_path = config["data"]["raw_data_path"]
    data = pd.read_csv(data_path)
    val_data = validate_data(data)
    val_data.log_bad_data() # logged bad data
    data = val_data.filter_out_bad_data()
    return data


def preprocess_validated_data(config_path):
    config = read_params(config_path)
    processed_data_path = config["data"]["prp_data_path"]
    data = validate_raw_data(config_path)
    prp_data = preprocess_data(data)
    prp_data = prp_data.run_all_preprocessing()
    prp_data.to_csv(processed_data_path, index = False)
    logger.info("Saved preprocessed data!")


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    preprocess_validated_data(config_path=parsed_args.config)