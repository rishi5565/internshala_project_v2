from functions import read_params, read_json
import argparse
from web_scraper.scraper import scraper
from logger.myLogger import getmylogger

logger = getmylogger(__name__)


def webscrap_data(config_path):
    config = read_params(config_path)
    args_dict_json = config["scraper"]["args_dict_path"]
    args_dict = read_json(args_dict_json)
    logger.info("Scraping with the passed arguments.....")
    scraper(args_dict)
    logger.info("Scraping done! Raw data saved!")




if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    webscrap_data(config_path=parsed_args.config)