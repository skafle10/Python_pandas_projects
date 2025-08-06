

# '''Movie  Rating Analyzer'''
import os
import pandas as pd
from rapidfuzz import process
import matplotlib.pyplot as plt
import streamlit as st


# BASE_DIR = os.path.dirname(__file__)
# FILE_NAME = "movie_ratings_dataset.csv"
# FILE_PATH = os.path.join(BASE_DIR,FILE_NAME)
THRESHOLD = 80
TARGETS = ["Title","Genre","Year","Rating","Votes","Runtime","Country","Language","Review"]



# '''Loads the file and makes it a dataframe'''
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
  
    except Exception as e:
        return f"Error in loading the data due to {e}"
    
# '''A fuzzymatcher to make sure that slightly changed column names also matches'''
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


# '''cleans the strings columns from the dataset'''
def clean_string_columns(df):
    for string_col in df.select_dtypes(include="object").columns:
        try:
            df[string_col] = string_col.str.strip().str.title()
            return df
            
        except Exception as e:
            return f"Errror in cleaning the string columns due to {e}"
        


# '''cleans the date column from the dataset'''
def clean_dates(df,date):
    try:
        df[date] = df[date].str.strip().astype(int)      # Convert the year into uniform values, no need to make it a datatime obj in this case
        print("Date cleaning successful")
        return df

    except Exception as e:
        return f"Error in cleaning the date due to {e}"
    

# '''shows the basic info as a intro to the user about the dataset'''
def show_basic_info(df,year):
    total_no_of_movies = len(df)
    columns_names = list(df.columns)
    return (f"The number of movies we have here are: {total_no_of_movies}\n"
           f" from the year {df[year].min()} - {df[year].max()}\n"
           f"You will get the information about {columns_names}\n"

           )

# '''Filters movies based on the language'''
def filter_by_language(df,user_input,language):
    try:
        filtered_df = df[ df[language] == user_input]

        return filtered_df

    except Exception as e:
        return f"Error in filtering by language due to {e}"

# '''Filters the movies based on the movie genre'''
def filter_by_genre(df,user_input,genre):
    try:
        filtered_df = df[df[genre] == user_input]
        return filtered_df

    except Exception as e:
        return f"Error in filtering by genre due to {e}"



# '''Filters the movie based on the given country'''
def filter_by_country(df,user_input,country):
    try:
        filtered_df = df[df[country] == user_input]

        return filtered_df

    except Exception as e:
        return f"Error in filtering by country due to {e}"
    

# '''Filters the movies based on the given release date'''
def filter_by_release_date(df,start,end,release_date):
    try:
        filtered_df = df[(df[release_date] >= start) & (df[release_date] <= end)]
        return filtered_df
    
    except Exception as e:
        return f"Error in filtering by release date due to {e}"


    


# '''Shows insights based on the movie genre'''
def genre_wise_analysis(df,genre,rating,release_date):
    try:
        average_ratings_per_genre = df.groupby(genre)[rating].mean().sort_values(ascending=False)
        most_frequent_genres = df.groupby(genre)[release_date].size().sort_values(ascending=False)
        return average_ratings_per_genre,most_frequent_genres

    except Exception as e:
        return f"Error in genre wise analysis due to {e}"



# '''Shows insights based on the release year'''
def year_wise_analysis(df,release_date,rating,movie):
    try:
        average_rating_per_year = df.groupby(release_date)[rating].mean().sort_values(ascending=False)
        total_movies_released_each_year = df.groupby(release_date)[movie].size().sort_values(ascending=False)
        return average_rating_per_year,total_movies_released_each_year



    except Exception as e:
        return f"Error in year wise analysis due to {e}"




def apply_analysis(df,ready_to_use_columns):

    if (st.session_state.main_view == "analysis"):
        
        st.subheader("Enter how do you want to analyze the movies: ")
        col1, col2 = st.columns(2)            
        with col1:
            if st.button("RELEASE_YEAR"):
                st.session_state.branch_view = "year"

            if (st.session_state.branch_view == "year"):
                st.subheader("The year wise analyis is: ")
                average_ratings_per_year, total_movies_released_per_year =  year_wise_analysis(df,ready_to_use_columns["Year"],ready_to_use_columns["Rating"],ready_to_use_columns["Title"])
                st.write("The average ratings per year of the movies is: ")
                st.write(average_ratings_per_year)
                st.write("The no of movies released per year is:")
                st.write(total_movies_released_per_year)
                    


        with col2:
            if st.button("GENRE"):
                st.session_state.branch_view = "genre"

            if (st.session_state.branch_view == "genre"):
        
                st.subheader("The genre wise analysis is: ")
                average_rating_per_genre,frequently_released_genre = genre_wise_analysis(df,ready_to_use_columns["Genre"],ready_to_use_columns["Rating"],ready_to_use_columns["Year"])
                st.write("The average ratings per genre is: ")
                st.write(average_rating_per_genre)
                st.write("The frequently released genre is: ")
                st.write(frequently_released_genre)
                    



def apply_filter(df,ready_to_use_columns):

    if (st.session_state.main_view == "apply_filter"):
        st.subheader("how do you want to Filter the dataset?: ")
        col4,col5,col6 = st.columns(3)
        with col4: 
            if st.button("Genre"):
                st.session_state.branch_view = "genre"


        if (st.session_state.branch_view == "genre"):

            genre_choice = st.text_input("Enter the genre for the movie: ").strip().title()
            if genre_choice:    #This is needed because as soon as the block runs stlit sees that genre choice is empty and else block gets runs as well.
                if genre_choice in df[ready_to_use_columns["Genre"]].values:
                    filtered_df_by_genre = filter_by_genre(df,genre_choice,ready_to_use_columns["Genre"])
                    st.write("The df with the entered genre is: ")
                    st.write(filtered_df_by_genre)
                else:
                    st.write("Genre not available, try one of the following: ")
                    st.write((df[ready_to_use_columns["Genre"]].unique()))
                                        


        
        with col5:
            if st.button("Language"):
                st.session_state.branch_view = "language"


        if (st.session_state.branch_view == "language"):
            language_choice = st.text_input("Enter the language for the movie: ").strip().title()

            if language_choice:
                if language_choice in df[ready_to_use_columns["Language"]].unique():
                    filtered_df_by_language = filter_by_language(df,language_choice,ready_to_use_columns["Language"])
                    st.write("The filtered datset by provided language is: ")
                    st.write(filtered_df_by_language)
                else:
                    st.write("Language not available , try one of the following: ")
                    st.write(", ".join(df[ready_to_use_columns["Language"]].unique()))
                



        with col6:
            if st.button("Country"):
                st.session_state.branch_view = "country"

        if (st.session_state.branch_view == "country"):
            country_choice = st.text_input("Enter the country name:").strip().title()
        
            if country_choice:
                # st.write(f"Your country choice is: {country_choice}")

                if country_choice in df[ready_to_use_columns["Country"]].unique():
                    filtered_df_by_country = filter_by_country(df,country_choice,ready_to_use_columns["Country"])
                    st.write("The filtered dataset by provided country is: ")
                    st.write(filtered_df_by_country)

                else:
                    st.write("Country not available, try one of the following: ")
                    st.write(", ".join(df[ready_to_use_columns["Country"]].unique()))





def main():



    st.header("MOVIE RATING ANALYZER")

    uploaded_file = st.file_uploader("upload your csv file: ")
    
    if uploaded_file: 
        df = load_data(uploaded_file)
        clean_string_columns(df)
        ready_to_use_columns = fuzzy_matcher(df,TARGETS,THRESHOLD)
        clean_dates(df,ready_to_use_columns["Year"])
        user_choice = st.subheader("SELECT ONE OF THE FOLLOWING ")


    if not uploaded_file:
        st.warning("Please upload the file first!!")

    if "main_view" not in st.session_state:
        st.session_state.main_view = False

    
    if "branch_view" not in st.session_state:
        st.session_state.branch_view = False




    with st.empty().container():

        col1, col2, col3 = st.columns(3)
        with col1: 
            if st.button("Whole Dataset"):
                st.session_state.main_view = "whole_ds"
            
        if (st.session_state.main_view == "whole_ds"):
                st.write("The whole dataset is: ")
                st.write(df)
            

        with col2:
            if st.button("Analysis"):
                st.session_state.main_view = "analysis"

            
        if (st.session_state.main_view == "analysis"):
            apply_analysis(df,ready_to_use_columns)



        with col3:
            if st.button("Apply Filter"):
                st.session_state.main_view = "apply_filter"

        if (st.session_state.main_view == "apply_filter"):
            apply_filter(df,ready_to_use_columns)


    



if __name__ == "__main__":

    main()
    
