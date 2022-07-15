import pandas as pd
from functions import validate_skills_list, validate_duration, load_data
import numpy as np

prp_data_path = "data/processed/prp_data.csv"
df = load_data(prp_data_path)

def get_all_skills(prp_data_path):
    df = load_data(prp_data_path)
    all_skills = []
    for skills in df["skills"]:
        all_skills += skills
    return list(set(all_skills))


def get_skills_intersection_index(skills_list):
    intersection_skill_row_index = list(np.where(df["skills"].astype("str").str.lower().apply(lambda x: skills_list[0].lower() in x))[0])
    for skill in skills_list:
        sub_index = list(np.where(df["skills"].astype("str").str.lower().apply(lambda x: skill.lower() in x))[0])
        intersection_skill_row_index = list(set(intersection_skill_row_index) & set(sub_index))
    return intersection_skill_row_index

def get_recommendation(user_input_dict, prp_data_path):
    all_skills_list = get_all_skills(prp_data_path)
    skills_list = validate_skills_list(user_input_dict["skills"], all_skills_list)
    duration = validate_duration(user_input_dict["duration"])
    intersection = get_skills_intersection_index(skills_list)
    while not len(intersection) > 0:
        if len(skills_list) > 0:
            skills_list = skills_list[:-1]
            intersection = get_skills_intersection_index(skills_list)
        else:
            break
    skill_intersect_df = df.loc[intersection]
    top10_result_index = list(skill_intersect_df["duration"].apply(lambda x: abs(x-duration)).sort_values()[:10].index)
    recommended_df = df.loc[top10_result_index].sort_values(["applicants"])
    recommended_df["duration"] = recommended_df["duration"].apply(lambda x: f"{str(int(x))} month(s)")
    recommended_df["stipend"] = recommended_df["stipend"].apply(lambda x: f"Rs.{str(int(x))} / month")
    recommended_df["apply_by"] = recommended_df["apply_by"].apply(lambda x: f"{str(x)} days" if x > 0 else "Today!!")
    return recommended_df[['title', 'company', 'duration', 'stipend', 'apply_by', 'openings', 'url']]


# print((get_recommendation({
#     "skills": ["Machine Learning, deep learning"], "duration": "3"
# }, "data\processed\prp_data.csv")).head())