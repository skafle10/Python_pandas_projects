

'''Movie  Rating Analyzer'''
import os
import pandas as pd
from rapidfuzz import process
import matplotlib.pyplot as plt

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


def filter_by_language(df,user_input,language):
    try:
        filtered_df = df[ df[language] == user_input]
        print("the filtred df by language is: ")
        print(filtered_df)

    except Exception as e:
        return f"Error in filtering by language due to {e}"


def filter_by_genre(df,user_input,genre):
    try:
        filtered_df = df[df[genre] == user_input]
        print("The filtered df with required genre is: ")
        print(filtered_df)

    except Exception as e:
        return f"Error in filtering by genre due to {e}"




def filter_by_country(df,user_input,country):
    try:
        filtered_df = df[df[country] == user_input]
        print("The filtered df by country is:")
        print(filtered_df)

    except Exception as e:
        return f"Error in filtering by country due to {e}"

def filter_by_release_date(df,start,end,release_date):
    try:
        filtered_df = df[(df[release_date] >= start) & (df[release_date] <= end)]
        return filtered_df
    
    except Exception as e:
        return f"Error in filtering by release date due to {e}"



def top_list(df,rating,movie_name):
    top_rated_movies = df.sort_values(rating,ascending=False)[[movie_name,rating]].head(10).to_string(index=False)
    



def genre_wise_analysis(df,genre,rating,release_date):
    try:
        average_ratings_genre = df.groupby(genre)[rating].mean().sort_values(ascending=False)
        print("The average ratings per genre is: ")
        print(average_ratings_genre)
        most_frequent_genres = df.groupby(genre)[release_date].size().sort_values(ascending=False)
        print("The most frequent genre is: ")
        print(most_frequent_genres)

    except Exception as e:
        return f"Error in genre wise analysis due to {e}"




def year_wise_analysis(df,plt,release_date,rating,movie):
    try:
        average_rating_per_year = df.groupby(release_date)[rating].mean().sort_values(ascending=False)
        average_rating_per_year.plot(kind = "bar")
        print("The average ratings on each year is: ")
        plt.title("Average Ratings Per Year")
        plt.xlabel("Year")
        plt.ylabel("Rating")
        plt.show()

        total_movies_released_each_year = df.groupby(release_date)[movie].size().sort_values(ascending=False)
        total_movies_released_each_year.plot(title="Movies Released Each Year",kind="bar")
        print("The no of movies released each year is: ")

        plt.show()

    except Exception as e:
        return f"Error in year wise analysis due to {e}"





def main():
    df = load_data(FILE_PATH)
    clean_string_columns(df)
    ready_to_use_columns = fuzzy_matcher(df,TARGETS,THRESHOLD)
    clean_dates(df,ready_to_use_columns["Year"])

    user_choice = input("Enter what you wanna do?"
                        "Apply filter(F), see the whole dataset(U)?" 
                        "or see the analysis(A): ").upper()


    if user_choice == "U":
        pass
    elif(user_choice == "F"):
        apply_filter = input("how do you want to Filter the dataset?" 
        "Release_year(Y),Movie_Genre(G),Language(L),Country(C)").upper()


        if (apply_filter == "Y"):
            pass
        elif (apply_filter == "G"):
            print("The filtered dataset by the provided Genre is: ")
            filter_by_genre(df,"Action",ready_to_use_columns["Genre"])
        elif (apply_filter == "L"):
            print("The filtered datset by provided language is: ")
            filter_by_language(df,"English",ready_to_use_columns["Language"])
        elif (apply_filter == "c"):
            print("The filtered dataset by provided country is :")
            filter_by_country(df,"India",ready_to_use_columns["Country"])

    elif (user_choice == "A"):
        analysis_filter = input("Enter how do you want to see the analysis?" 
        "analysis by Release_Year(Y) or analysis by Movie_Genre(G): ").upper()
        if (analysis_filter == "Y"):
            print("The year wise analyis is: ")
            year_wise_analysis(df,plt,ready_to_use_columns["Year"],ready_to_use_columns["Rating"],ready_to_use_columns["Title"])
    
        elif (analysis_filter == "G"):
            print("The genre wise analysis is: ")
            genre_wise_analysis(df,ready_to_use_columns["Genre"],ready_to_use_columns["Rating"],ready_to_use_columns["Year"])

    


if __name__ == "__main__":
    main()