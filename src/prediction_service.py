import pandas as pd
from functions import validate_skills_list, validate_duration, load_data
import numpy as np

prp_data_path = "data/processed/prp_data.csv"
df = load_data(prp_data_path)

def get_skills_intersection_index(skills_list):
    intersection_skill_row_index = list(np.where(df["skills"].astype("str").str.lower().apply(lambda x: skills_list[0].lower() in x))[0])
    for skill in skills_list:
        sub_index = list(np.where(df["skills"].astype("str").str.lower().apply(lambda x: skill.lower() in x))[0])
        intersection_skill_row_index = list(set(intersection_skill_row_index) & set(sub_index))
    return intersection_skill_row_index

def get_recommendation(skills_list, duration):
    skills_list = validate_skills_list(skills_list)
    duration = validate_duration(duration)
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
    return recommended_df