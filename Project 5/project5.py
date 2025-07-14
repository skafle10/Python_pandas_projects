

'''Movie  Rating Analyzer'''
import os
import pandas as pd
from rapidfuzz import process

BASE_DIR = os.path.dirname(__file__)
FILE_NAME = "movie_ratings_dataset.csv"
FILE_PATH = os.path.join(BASE_DIR,FILE_NAME)
THRESHOLD = 80
TARGETS = ["Title","Genre","Year","Rating","Votes","Runtime","Country","Language","Review"]


def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
  
    except Exception as e:
        return f"Error in loading the data due to {e}"
    
    
def fuzzy_matcher(df,targets,threshold):
    matched = {}
    unmatched = []
    try:
        for target in targets:
            match,score,_ = process.extractOne(target,df.columns)

            if score >= threshold:
                matched[target] = match

            else:
                unmatched.append(match)

        if unmatched:
            return f"The unmatched column names are: {unmatched}"


    except Exception as e:
        return f"Error in fuzzymatching due to {e}"
    

    return matched



def clean_string_columns(df):
    for string_col in df.select_dtypes(include="object").columns:
        try:
            df[string_col] = string_col.str.strip().str.title()
            return df
            
        except Exception as e:
            return f"Errror in cleaning the string columns due to {e}"
        



def clean_dates(df,date):
    try:
        df[date] = pd.to_datetime(df[date])
        print("Date cleaning successful")
        return df

    except Exception as e:
        return f"Error in cleaning the date due tp {e}"
    


def show_basic_info(df,year):
    total_no_of_movies = len(df)
    columns_names = list(df.columns)
    return (f"The number of movies we have here are: {total_no_of_movies}\n"
           f" from the year {df[year].min()} - {df[year].max()}\n"
           f"You will get the information about {columns_names}\n"

           )


def apply_filters():
    pass


def top_list(df,rating,movie_name):
    top_rated_movies = df.groupby(movie_name)[rating].sort_values(ascending=False).head()
    print("The top rated movies are: ")
    print(top_rated_movies)



def main():
    df = load_data(FILE_PATH)
    clean_string_columns(df)
    ready_to_use_columns = fuzzy_matcher(df,TARGETS,THRESHOLD)

    # print("The matched data which are ready to be used are: ")
    # print(ready_to_use_columns)

    # clean_dates(df,ready_to_use_columns["Year"])

    show_basic_info(df,ready_to_use_columns["Year"])
    top_list(df,ready_to_use_columns["Rating"],ready_to_use_columns["Title"])


if __name__ == "__main__":
    main()