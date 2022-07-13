from scraper_functions import format_categories, format_locations
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from custom_exceptions import TooManyPages

def scraper(args_dict):

    base_url = "https://internshala.com/internships/"
    cat = args_dict["category"]
    wfh = args_dict["wfh"]
    loc = args_dict["location"]

    if wfh == "yes":
        base_url += "work-from-home-"
        wfh_status = True
        base_url += format_categories(cat, wfh_status)
    elif wfh == "no":
        wfh_status = False
        base_url += format_categories(cat, wfh_status)

    if len(loc) > 0:
        base_url += format_locations(loc)

    req = requests.get(base_url)
    soup = BeautifulSoup(req.content, "html.parser")
    total_pages = int(soup.find(id='total_pages').text.strip())

    if total_pages > 3:
        raise TooManyPages
    
    else:

        main_df = pd.DataFrame()

        for page in range(total_pages):
            pg_url = base_url
            pg_url += f"/page-{page+1}/"
            # print(pg_url)
            req_pg = requests.get(pg_url)
            soup = BeautifulSoup(req_pg.content, "html.parser")
            internships = soup.find_all(class_ = 'heading_4_5 profile')
            for internship in tqdm(internships):
                sub_info = {}
                sub_url = "https://internshala.com"
                sub_url += internship.find('a', href=True)["href"]
                req_sub_pg = requests.get(sub_url)
                sub_soup = BeautifulSoup(req_sub_pg.content, "html.parser")
                sub_info["title"] = sub_soup.find(class_ = 'profile_on_detail_page').text.strip()
                sub_info["company"] = sub_soup.find(class_ = 'heading_6 company_name').find('a').text.strip()
                sub_info["location"] = [i.text.strip() for i in sub_soup.find_all(class_ = 'location_link')]
                info = sub_soup.find(class_ = 'internship_other_details_container')
                other_details = info.find_all(class_ = 'item_body')
                sub_info["duration"] = other_details[1].text.strip()
                sub_info["stipend"] = other_details[2].text.strip()
                sub_info["apply_by"] = other_details[3].text.strip()
                sub_info["applicants"] = sub_soup.find(class_ = 'applications_message').text.strip()
                skills_raw = sub_soup.find(class_ = 'heading_5_5',string = 'Skill(s) required')
                try:
                    skills_raw = skills_raw.findNext(class_ = 'round_tabs_container')
                    skills_raw.find_all(class_ = 'round_tabs')
                    sub_info["skills"] = [i.text.strip() for i in skills_raw.find_all(class_ = 'round_tabs')]
                except(AttributeError):
                    sub_info["skills"] = []
                try:
                    perks_raw = sub_soup.find(class_ = 'heading_5_5',string = 'Perks')
                    perks_raw = perks_raw.findNext(class_ = 'round_tabs_container')
                    sub_info["perks"] = [i.text.strip() for i in perks_raw.find_all(class_ = 'round_tabs')]
                except(AttributeError):
                    sub_info["perks"] = []
                sub_info["openings"] = sub_soup.find_all(class_='text-container')[-1].text.strip()
                sub_info["url"] = sub_url
                sub_df = pd.DataFrame([sub_info])
                main_df = pd.concat([main_df, sub_df], ignore_index=True)

        return main_df.to_csv("data/raw/raw_scraped.csv", index=False)

# scraper({
#     "category": ["Machine Learning"],
#     "wfh": "yes",
#     "location": []
# })