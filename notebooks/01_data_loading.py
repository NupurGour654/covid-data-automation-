
import pandas as pd
import os

def load_csv(file_name):
    data_path = os.path.join("../data", file_name)
    return pd.read_csv(data_path)
