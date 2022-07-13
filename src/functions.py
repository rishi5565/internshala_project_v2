import pandas as pd
import ast
import yaml
import json
from collections import Counter
import operator

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def read_json(file_path):
    with open(file_path) as json_file:
        file = json.load(json_file)
    return file


def load_data(prp_data_path):
    df = pd.read_csv(prp_data_path, parse_dates=["apply_by"])
    df["skills"] = df["skills"].apply(lambda x: ast.literal_eval(x))
    df["perks"] = df["perks"].apply(lambda x: ast.literal_eval(x))
    df["apply_by"] = df["apply_by"].astype("int")
    return df


def validate_skills_list(skills_list, all_skills):
    condition = 0
    for skill in skills_list:
        if not skill.lower() in [i.lower() for i in all_skills]:
            condition = 1
            break
    if condition == 1:
        raise AttributeError("Skill entered not in list of skills.")
    elif condition == 0:
        return skills_list
    

def validate_duration(duration):
    try:
        return int(duration)
    except:
        raise AttributeError("Enter number of months as integer in duration.")


def get_stats(prp_data_path):

    df = load_data(prp_data_path)
    stats_dict = {}

    #### DURATION ####
    stats_dict['duration_avg'] = round(df["duration"].mean())
    stats_dict['duration_min'] = round(df["duration"].min())
    stats_dict['duration_min_count'] = (df["duration"] == stats_dict['duration_min']).sum()
    stats_dict['duration_max'] = round(df["duration"].max())
    stats_dict['duration_max_count'] = (df["duration"] == stats_dict['duration_max']).sum()

    #### STIPEND ####
    stats_dict['stipend_avg'] = round(df["stipend"].mean())
    stats_dict['stipend_max'] = round(df["stipend"].max())
    stats_dict['stipend_max_count'] = (df["stipend"] == stats_dict['stipend_max']).sum()

    #### APPLY BY ####
    stats_dict['least_days'] = df["apply_by"].sort_values()[0:1].tolist()[0]
    stats_dict['least_days_internship_count'] = (df["apply_by"] == stats_dict['least_days']).sum()

    #### APPLICANTS ####
    stats_dict['early_appl_stage'] = (df["applicants"] == 0).sum()
    stats_dict['thousand_plus'] = (df["applicants"] == 1000).sum()

    stats_dict['applicants_series'] = df[(df["applicants"] != 0) & (df["applicants"] != 1000)]["applicants"]
    stats_dict['applicants_avg'] = round(stats_dict['applicants_series'].mean())
    stats_dict['applicants_min'] = round(stats_dict['applicants_series'].min())
    stats_dict['applicants_max'] = round(stats_dict['applicants_series'].max())

    #### SKILLS ####
    s_list = []
    for i in df["skills"]:
        s_list += i
    skill_cnt = dict(Counter(s_list))
    skill_cnt_dict = dict(sorted(skill_cnt.items(), key=operator.itemgetter(1),reverse=True))
    skill_count_df = pd.DataFrame(skill_cnt_dict.items(), columns=['Skill', 'Count'])
    stats_dict['top10_skill_df'] = skill_count_df[:10]

    all_skills = []
    for skills in df["skills"]:
        all_skills += skills
    stats_dict["all_skills"] = list(set(all_skills))

    #### PERKS ####
    p_list = []
    for i in df["perks"]:
        p_list += i
    perk_cnt = dict(Counter(p_list))
    perk_cnt_dict = dict(sorted(perk_cnt.items(), key=operator.itemgetter(1),reverse=True))
    perk_count_df = pd.DataFrame(perk_cnt_dict.items(), columns=['Skill', 'Count'])
    stats_dict['top10_perk_df'] = perk_count_df[:5]

    #### OPENINGS ####
    stats_dict['openings_avg'] = round(df["openings"].mean())
    stats_dict['openings_max'] = round(df["openings"].max())

    return stats_dict


