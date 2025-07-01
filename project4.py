

'''TOP CUSTOMER ANALYZER'''

import pandas as pd
from rapidfuzz import process


FILE_NAME = "customers-100.csv"
THRESHOLD = 80



'''Load the raw data samples'''
def load_data(file_name):
    try: 
        df = pd.read_csv(file_name)
        return df
    
    except Exception as e:
        print(f"Error in loading the data due to: {e}")


'''Convert the date to datetime object'''
def to_date_time(df):
    for cols in pd.select_dtypes(include="objects").columns:
        try: 
            df[cols] = pd.to_datetime(df[cols])

        except:
            pass

    return df
        

'''clean the data'''
def clean_text(df):
        for cols in pd.select_dtypes(include="object").columns:
            try:
                df[cols] = df[cols].str.strip().str.title


            except Exception as e:
             print(f"Error in cleaning the text columns due to: {e}")

        return df




'''A reuseable fuzzy matcher function'''
def fuzzy_matcher(df,targets,threshold):
    matched = {}

    try:
        for target in  targets: 
            match,score,_ = process.extractOne(target,df.columns)


            if score>= threshold:
                matched[target] = match

        
    except Exception as e:
        print(f"Error in fuzzymatching due to {e}")

    return matched if len(matched) == len(targets) else None



'''Insights based on customers'''
def top_customers(df):
    targets = ["Customer id",]
    




def main():
    try:
     load_data(FILE_NAME)

    except Exception as e:
        print(f"error in calling the data loading function due to: {e}")

    

if __name__ == "__main__":
    main()
