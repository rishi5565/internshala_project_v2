import pandas as pd
import numpy as np
import ast

class preprocess_data:
    def __init__(self, df):
        self.df = df

    def prep_duration(self):
        self.df["duration"] = self.df["duration"].str.replace("Months", "")
        self.df["duration"] = self.df["duration"].str.replace("Month", "")
        self.df["duration"] = self.df["duration"].apply(lambda x: float(x.strip()) if x.strip().isnumeric() else np.NaN)

    def prep_stipend(self):
        self.df["stipend"] = self.df["stipend"].apply(lambda x: x.split(" ")[0])
        self.df["stipend"] = self.df["stipend"].str.replace("Unpaid", "0")
        
        def clean_stipend(row): # a function to clean stipend, return nulls for wrong type of values
            try:
                if len(row.split("-")) == 2:
                    return (float(row.split("-")[0]) + float(row.split("-")[0]))/2  #average
                else:
                    try:
                        return float(row)
                    except:
                        return np.nan
            except:
                np.nan

        self.df["stipend"] = self.df["stipend"].apply(clean_stipend)

    def prep_apply_by(self):
        self.df["apply_by"] = pd.to_datetime(self.df["apply_by"], errors="raise")

    def prep_applicants(self):
        self.df["applicants"] = self.df["applicants"].str.replace("Be an early applicant", "0")
        self.df["applicants"] = self.df["applicants"].apply(lambda x: x.split(" ")[0])
        self.df["applicants"] = self.df["applicants"].str.replace("+", "", regex=True)
        self.df["applicants"] = self.df["applicants"].apply(lambda x: float(x.strip()) if x.strip().isnumeric() else np.NaN)

    def prep_skills(self):
        self.df["skills"] = self.df["skills"].apply(lambda x: ast.literal_eval(x))

    def prep_perks(self):
        self.df["perks"] = self.df["perks"].apply(lambda x: ast.literal_eval(x))

    def run_all_preprocessing(self):
        self.prep_duration()
        self.prep_stipend()
        self.prep_apply_by()
        self.prep_applicants()
        self.prep_skills()
        self.prep_perks()
        return self.df



