

# '''Movie  Rating Analyzer'''

import pandas as pd
from rapidfuzz import process
import streamlit as st


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
            df[string_col] = df[string_col].str.strip().str.title()
            
            
        except Exception as e:
            return f"Errror in cleaning the string columns due to {e}"
        
    return df


# '''cleans the date column from the dataset'''
def clean_dates(df,date):
    try:
        df[date] = df[date].str.strip().astype(int)      # Convert the year into uniform values, no need to make it a datatime obj in this case
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



#'''Display the data analysis using streamlit'''

def apply_analysis(df,ready_to_use_columns):
    analysis_choice = st.radio("How do you want to analyze the dataset?: ",["Year wise","Genre wise"],index=None)

    if (analysis_choice == "Year wise"):
        st.session_state.branch_view = "year_wise_analysis"

    elif (analysis_choice == "Genre wise"):
        st.session_state.branch_view = "genre_wise_analysis"


    if analysis_choice:
        if (st.session_state.branch_view == "year_wise_analysis"):
            average_rating_per_year,total_movies_released_each_year =  year_wise_analysis(df,ready_to_use_columns["Year"],ready_to_use_columns["Rating"],ready_to_use_columns["Title"])
            st.subheader("The year wise analysis is: ")
            st.write("The average rating per year is: ")
            st.write(average_rating_per_year)
            st.write("The total movies released each year are: ")
            st.write(total_movies_released_each_year)


    if analysis_choice:
        if (st.session_state.branch_view == "genre_wise_analysis"):
            average_ratings_per_genre,most_frequent_genres = genre_wise_analysis(df,ready_to_use_columns["Genre"],ready_to_use_columns["Rating"],ready_to_use_columns["Year"])
            st.subheader("The Genre wise analysis is: ")
            st.write("Average rating per genre: ")
            st.write(average_ratings_per_genre)
            st.write("Genre with highes no of movies: ")
            st.write(most_frequent_genres)



#'''apply the filters to the data and show the filtered df using streamlit.'''
def apply_filter(df,ready_to_use_columns):

    st.subheader("Filter Type: ")
    filter_choice = st.radio("Choose the filter: ",["Genre","Country","Language","Release Date"],index=None)

    if (filter_choice == "Genre"):
        st.session_state.branch_view = "genre_filter"

    elif (filter_choice == "Country"):
        st.session_state.branch_view = "country_filter"

    elif(filter_choice == "Language"):
        st.session_state.branch_view = "language_filter"

    elif(filter_choice == "Release Date"):
        st.session_state.branch_view = "releasedate_filter"



    if st.session_state.branch_view == "genre_filter":
        genre_input = st.text_input("Enter the genre").strip().title()
        
        if genre_input:

            if genre_input in df[ready_to_use_columns["Genre"]].values:
                st.write("The filtered dataset by genre is: ")
                st.write(filter_by_genre(df,genre_input,ready_to_use_columns["Genre"]))

            else:
                st.write("Genre not available, enter one of the following: ")
                st.write(df[ready_to_use_columns["Genre"]].unique()) 



    if st.session_state.branch_view == "country_filter":
        country_input = st.text_input("Enter the country: ").strip().title()

        if country_input:
            if country_input in df[ready_to_use_columns["Country"]].values:
                st.write("The filtered dataset by country is: ")
                st.write(filter_by_country(df,country_input,ready_to_use_columns["Country"]))

            else:
                st.write("Country not available, enter one of the following: ")
                st.write(df[ready_to_use_columns["Country"]].unique()) 




    if st.session_state.branch_view == "language_filter":

        language_input = st.text_input("Enter the language: ").strip().title()

        if language_input:
            if language_input in df[ready_to_use_columns["Language"]].values:
                st.write("The filtered dataset by language is: ")
                st.write(filter_by_language(df,language_input,ready_to_use_columns["Language"]))

            else:
                st.write("language not available, enter one of the following: ")
                st.write(df[ready_to_use_columns["Language"]].unique()) 



    if st.session_state.branch_view == "releasedate_filter":

        start_date = st.text_input("Enter the start date")
        end_date = st.text_input("Enter the end date: ")

        if (start_date and end_date):
            try:
                start_date = int(start_date)
                end_date = int(end_date)

            except Exception as e: 
                st.write(f"Error converting the date due to {e}")

            if (start_date and end_date in df[ready_to_use_columns["Year"]].unique()):

                st.write("The filtered dataset by release date is: ")
                st.write(filter_by_release_date(df,start_date,end_date,ready_to_use_columns["Year"]))
    
            else:
                st.write("Please provide a valid year between:\n"
                         f"{df[ready_to_use_columns["Year"]].min()} and {df[ready_to_use_columns["Year"]].max()}")



def main():
        
    defaults = {
        "main_view": None,
        "branch_view" : None,
        "file" : None,
        "df" : None,
        
    }


    for key,value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value



    st.header("MOVIE RATING ANALYZER: ")

    uploaded_file = st.file_uploader("Enter yout csv file: ")

    if uploaded_file:
        df = load_data(uploaded_file)
        ready_to_use_columns = fuzzy_matcher(df, TARGETS,THRESHOLD)
        clean_string_columns(df)
        clean_dates(df,ready_to_use_columns["Year"])
        
        # st.write(df)

    col4,col1, col2, col3 = st.columns(4)

    try:
            
        if col4.button("Basic info"):
            if uploaded_file:
                st.session_state.main_view = "basic info"
            

            else:
                st.warning("Please upload the file first")


        if col1.button("Whole DS"):
            if uploaded_file:
                st.session_state.main_view = "whole ds"

            else:
                st.warning("Please upload the file first!!")


        if col2.button("Apply Filter"):
            if uploaded_file:
                st.session_state.main_view = "filter ds"
            else:
                st.warning("Please upload the file first!!")


        if col3.button("Analysis"):
            if uploaded_file:
                st.session_state.main_view = "analyze"

            else:
                st.warning("Please upload the file first!!")


        
        if (st.session_state.main_view == "basic info"):
            st.subheader("The basic info of the given dataset is: ")
            st.write(show_basic_info(df,ready_to_use_columns["Year"]))

        elif (st.session_state.main_view == "whole ds"):
            st.subheader("The whole dataset is: ")
            st.write(df)

        elif (st.session_state.main_view == "filter ds"):
            apply_filter(df,ready_to_use_columns)

        elif (st.session_state.main_view == "analyze"):
            apply_analysis(df,ready_to_use_columns)


    
    except Exception as e:
        st.warning(f"ERROR: {e}")

if __name__ == "__main__":




    main()
    
