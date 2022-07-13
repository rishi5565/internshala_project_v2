from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
from preprocessor.preprocessor import preprocess_data
import json

class validate_data:
    def __init__(self, df):
        self.df = df
        self.prp_df = preprocess_data(self.df)

    def log_bad_data(self):
        self.bad_data_index = self.prp_df[self.prp_df.isna().any(axis=1)].index.to_list()
        self.bad_data = self.df.loc[self.bad_data_index].to_json()
        with open("bad_data_log.json", "w") as f:
            json.dump(self.bad_data, f)
            f.close()

    def filter_out_bad_data(self):
        return self.df.drop(self.bad_data_index, axis=0)


