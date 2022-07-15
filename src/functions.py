import pandas as pd
import ast
import yaml
import json
from collections import Counter
import operator
import matplotlib.pyplot as plt
import seaborn as sns



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

def dump_json(dump_file_path, dictionary):
    with open(dump_file_path, "w") as f:
        json.dump(dictionary, f)
        f.close()

def load_json(json_file_path):
    with open(json_file_path, "r") as f:
        json_file = json.load(f)
        f.close()
        return json_file

def get_stats(prp_data_path):

    df = load_data(prp_data_path)
    stats_dict = {}

    #### DURATION ####
    duration_avg = round(df["duration"].mean())
    duration_min = round(df["duration"].min())
    duration_min_count = (df["duration"] == duration_min).sum()
    duration_max = round(df["duration"].max())
    duration_max_count = (df["duration"] == duration_max).sum()
    stats_dict["avg_dur"] = f"Average duration is {duration_avg} month(s)"
    stats_dict["min_dur"] = f"Minimum duration is {duration_min} month(s) offered by {duration_min_count} internship(s)"
    stats_dict["max_dur"] = f"Maximum duration is {duration_max} month(s) offered by {duration_max_count} internship(s)"

    #### STIPEND ####
    stipend_avg = round(df["stipend"].mean())
    stipend_max = round(df["stipend"].max())
    stipend_max_count = (df["stipend"] == stipend_max).sum()
    stats_dict["st_avg"] = f"Average stipend is Rs.{stipend_avg} / month"
    stats_dict["st_max"] = f"Maximum stipend is Rs.{stipend_max} / month offered by {stipend_max_count} internship(s)"

    #### APPLY BY ####
    least_days = df["apply_by"].sort_values()[0:1].tolist()[0]
    least_days_internship_count = (df["apply_by"] == least_days).sum()
    if least_days <= 0:
        stats_dict["least_count"] = f"Hurry up! {least_days_internship_count} internships expiring by today!!!"
    else:
        stats_dict["least_count"] = f"Hurry up! {least_days_internship_count} internships expiring in {least_days} day(s)!"

    #### APPLICANTS ####
    early_appl_stage = (df["applicants"] == 0).sum()
    thousand_plus = (df["applicants"] == 1000).sum()
    stats_dict["eas"] = f"{early_appl_stage} internships are in early application stage, apply fast !!!"
    stats_dict["tplus"] = f"{thousand_plus} internships have 1000+ applicants, not very likely to receive response..."

    applicants_series = df[(df["applicants"] != 0) & (df["applicants"] != 1000)]["applicants"]
    applicants_avg = round(applicants_series.mean())
    stats_dict["appl_avg"] = f"Average applicants is {applicants_avg} / internship"


    #### SKILLS ####
    s_list = []
    for i in df["skills"]:
        s_list += i
    skill_cnt = dict(Counter(s_list))
    skill_cnt_dict = dict(sorted(skill_cnt.items(), key=operator.itemgetter(1),reverse=True))
    skill_count_df = pd.DataFrame(skill_cnt_dict.items(), columns=['Skill', 'Count'])
    top10_skill_sr = skill_count_df[:10].set_index("Skill").squeeze()
    sns.set()
    ax = sns.barplot(x = top10_skill_sr.values, y = top10_skill_sr.index, color='b')
    abs_values = top10_skill_sr.values
    ax.bar_label(container=ax.containers[0], labels=abs_values)
    plt.title("Most Demanded 10 Skills")
    plt.xlabel("Count")
    plt.ylabel("Skill")
    plt.savefig("webapp/static/top10skill.png", bbox_inches = "tight")
    plt.close()


    all_skills = []
    for skills in df["skills"]:
        all_skills += skills
    stats_dict["all_skills"] = ", ".join(list(set(all_skills)))

    #### PERKS ####
    p_list = []
    for i in df["perks"]:
        p_list += i
    perk_cnt = dict(Counter(p_list))
    perk_cnt_dict = dict(sorted(perk_cnt.items(), key=operator.itemgetter(1),reverse=True))
    perk_count_df = pd.DataFrame(perk_cnt_dict.items(), columns=['Perks', 'Count'])
    top5_perk_sr = perk_count_df[:5].set_index("Perks").squeeze()
    ax = sns.barplot(x = top5_perk_sr.values, y = top5_perk_sr.index, color='b')
    abs_values = top5_perk_sr.values
    ax.bar_label(container=ax.containers[0], labels=abs_values)
    plt.title("Most Offered 5 Perks")
    plt.xlabel("Count")
    plt.ylabel("Perk")
    plt.savefig("webapp/static/top5perk.png", bbox_inches = "tight")
    plt.close()


    #### OPENINGS ####
    openings_avg = round(df["openings"].mean())
    openings_max = round(df["openings"].max())
    stats_dict["avg_opn"] = f"Average openings is {openings_avg} / internship"
    stats_dict["max_opn"] = f"Maximum openings in an internship is {openings_max}"

    return stats_dict

#     with open("stats_dict.json", "w") as f:
#         json.dump(stats_dict, f)
#         f.close()

# get_stats("data/processed/prp_data.csv")


