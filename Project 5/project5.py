

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



'''Loads the file and makes it a dataframe'''
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
  
    except Exception as e:
        return f"Error in loading the data due to {e}"
    
'''A fuzzymatcher to make sure that slightly changed column names also matches'''
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


'''cleans the strings columns from the dataset'''
def clean_string_columns(df):
    for string_col in df.select_dtypes(include="object").columns:
        try:
            df[string_col] = string_col.str.strip().str.title()
            return df
            
        except Exception as e:
            return f"Errror in cleaning the string columns due to {e}"
        


'''cleans the date column from the dataset'''
def clean_dates(df,date):
    try:
        df[date] = df[date].str.strip().astype(int)      # Convert the year into uniform values, no need to make it a datatime obj in this case
        print("Date cleaning successful")
        return df

    except Exception as e:
        return f"Error in cleaning the date due to {e}"
    

'''shows the basic info as a intro to the user about the dataset'''
def show_basic_info(df,year):
    total_no_of_movies = len(df)
    columns_names = list(df.columns)
    return (f"The number of movies we have here are: {total_no_of_movies}\n"
           f" from the year {df[year].min()} - {df[year].max()}\n"
           f"You will get the information about {columns_names}\n"

           )

'''Filters movies based on the language'''
def filter_by_language(df,user_input,language):
    try:
        filtered_df = df[ df[language] == user_input]

        return filtered_df

    except Exception as e:
        return f"Error in filtering by language due to {e}"

'''Filters the movies based on the movie genre'''
def filter_by_genre(df,user_input,genre):
    try:
        filtered_df = df[df[genre] == user_input]
        return filtered_df

    except Exception as e:
        return f"Error in filtering by genre due to {e}"



'''Filters the movie based on the given country'''
def filter_by_country(df,user_input,country):
    try:
        filtered_df = df[df[country] == user_input]

        return filtered_df

    except Exception as e:
        return f"Error in filtering by country due to {e}"
    

'''Filters the movies based on the given release date'''
def filter_by_release_date(df,start,end,release_date):
    try:
        filtered_df = df[(df[release_date] >= start) & (df[release_date] <= end)]
        return filtered_df
    
    except Exception as e:
        return f"Error in filtering by release date due to {e}"


    


'''Shows insights based on the movie genre'''
def genre_wise_analysis(df,genre,rating,release_date):
    try:
        average_ratings_per_genre = df.groupby(genre)[rating].mean().sort_values(ascending=False)
        most_frequent_genres = df.groupby(genre)[release_date].size().sort_values(ascending=False)
        return average_ratings_per_genre,most_frequent_genres

    except Exception as e:
        return f"Error in genre wise analysis due to {e}"



'''Shows insights based on the release year'''
def year_wise_analysis(df,plt,release_date,rating,movie):
    try:
        average_rating_per_year = df.groupby(release_date)[rating].mean().sort_values(ascending=False)
        average_rating_per_year.plot(kind = "bar")
        plt.title("Average Ratings Per Year")
        plt.xlabel("Year")
        plt.ylabel("Rating")
        average_rating_per_year = plt.show()
        total_movies_released_each_year = df.groupby(release_date)[movie].size().sort_values(ascending=False)
        total_movies_released_each_year.plot(title="Movies Released Each Year",kind="bar")
        total_movies_released_each_year = plt.show()
        return average_rating_per_year,total_movies_released_each_year

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
        print("The whole dataset is: ")
        print(df)

    elif(user_choice == "F"):
        apply_filter = input("how do you want to Filter the dataset?" 
        "Release_year(Y),Movie_Genre(G),Language(L),Country(C): ").upper()


        if (apply_filter == "Y"):
            pass

        elif (apply_filter == "G"):
            genre_choice = input("Enter the genre for the movie: ").title()
            filtered_df_by_genre = filter_by_genre(df,genre_choice,ready_to_use_columns["Genre"])
            print("The df with the entered genre is: ")
            print(filtered_df_by_genre)

        elif (apply_filter == "L"):
            language_choice = input("Enter the language for the movie: ").title()
            filtered_df_by_language = filter_by_language(df,language_choice,ready_to_use_columns["Language"])
            print("The filtered datset by provided language is: ")
            print(filtered_df_by_language)


        elif (apply_filter == "C"):
            country_choice = input("Enter the country name: ").title()
            filtered_df_by_country = filter_by_country(df,country_choice,ready_to_use_columns["Country"])
            print("The filtered dataset by provided country is: ")
            print(filtered_df_by_country)


    elif (user_choice == "A"):
        analysis_filter = input("Enter how do you want to see the analysis?" 
        "analysis by Release_Year(Y) or analysis by Movie_Genre(G): ").upper()
        if (analysis_filter == "Y"):
            print("The year wise analyis is: ")

            average_ratings_per_year, total_movies_released_per_year =  year_wise_analysis(df,plt,ready_to_use_columns["Year"],ready_to_use_columns["Rating"],ready_to_use_columns["Title"])
            print("The average ratings per year of the movies is: ")
            print(average_ratings_per_year)
            print("The no of movies released per year is:")
            print(total_movies_released_per_year)
    
        elif (analysis_filter == "G"):
            print("The genre wise analysis is: ")
            average_rating_per_genre,frequently_released_genre = genre_wise_analysis(df,ready_to_use_columns["Genre"],ready_to_use_columns["Rating"],ready_to_use_columns["Year"])
            print("The average ratings per genre is: ")
            print(average_rating_per_genre)
            print("The frequently released genre is: ")
            print(frequently_released_genre)
    


if __name__ == "__main__":
    main()