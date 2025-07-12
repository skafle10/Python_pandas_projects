

'''Movie  Rating Analyzer'''

import pandas as pd



FILE_NAME = "movie_ratings_dataset.csv"


def load_data(file_name):
    try:
        df = pd.read_csv(file_name)
    except Exception as e:
        return f"Error in loading the data due to {e}"

def clean_string_columns():
    pass

