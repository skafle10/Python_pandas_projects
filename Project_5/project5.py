

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




#Applies filter bsed on language,genre,country
def filter(df,user_input,filterby):
    try:
        filtered_df = df[ df[filterby] == user_input]
        return filtered_df
    
    except Exception as e:
        return f"Error in filtering due to {e}"
    
    

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



def analyze_group(df,**columns):
    if all(key in columns for key in ["grouping_column","func_type"]) :   #we must mention full condition twice, if we do if "sth" and "other" in (...) then it will just check if sth which is a string and always true and that true is compare with  2nd condition
        if columns["func_type"] == "mean_sort":
            mean_analyzed_data = df.groupby(columns["grouping_column"])[columns["operated_column"]].mean().sort_values(ascending=False)
            return mean_analyzed_data
        
        elif columns["func_type"] == "size_sort":
            st.write("WE are inside size sort")
            size_analyzed_data =  df.groupby(columns["grouping_column"]).size().sort_values(ascending=False)
            return size_analyzed_data
        
        else:
            raise ValueError(f"Invalid func type {columns["func_type"]}")
        


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
            st.subheader("The year wise analysis is: ")
            st.write("The average rating per year is: ")
            st.write(analyze_group(df,grouping_column = ready_to_use_columns["Year"], operated_column = ready_to_use_columns["Rating"] ,func_type = "mean_sort"))
            st.write("The total movies released each year are: ")
            st.write(analyze_group(df,grouping_column = ready_to_use_columns["Year"],func_type = "size_sort"))


    if analysis_choice:
        if (st.session_state.branch_view == "genre_wise_analysis"):

            st.subheader("The Genre wise analysis is: ")
            st.write("Average rating per genre: ")
            st.write(analyze_group(df,grouping_column = ready_to_use_columns["Genre"], operated_column = ready_to_use_columns["Rating"] ,func_type = "mean_sort"))
        
            st.write("Genre with highest no of movies: ")
            st.write(analyze_group(df,grouping_column = ready_to_use_columns["Genre"], operated_column = "messi",func_type = "size_sort"))



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


    if filter_choice:
        if st.session_state.branch_view == "genre_filter":
            genre_input = st.selectbox("Select the genre: ", df[ready_to_use_columns["Genre"]].unique(), index=None )     # we can pass not only list but bunch of other objects like - list, tuple, dictionary, numpyarray, etc.
            if genre_input:
                if genre_input in df[ready_to_use_columns["Genre"]].values:
                    st.write("The filtered dataset by genre is: ")
                    st.write(filter(df,genre_input,ready_to_use_columns["Genre"]))

    if filter_choice:
        if st.session_state.branch_view == "country_filter":
            country_input = st.selectbox("Select the country: ",df[ready_to_use_columns["Country"]].unique(),index = None)
            if country_input:
                if country_input in df[ready_to_use_columns["Country"]].values:
                    st.write("The filtered dataset by country is: ")
                    st.write(filter(df,country_input,ready_to_use_columns["Country"]))


    if filter_choice:
        if st.session_state.branch_view == "language_filter":
            language_input = st.selectbox("Select the language: ", df[ready_to_use_columns["Language"]].unique(),index=None)
            if language_input:
                if language_input in df[ready_to_use_columns["Language"]].values:
                    st.write("The filtered dataset by language is: ")
                    st.write(filter(df,language_input,ready_to_use_columns["Language"]))

    if filter_choice:
        if st.session_state.branch_view == "releasedate_filter":
            start_date = st.selectbox("Select the start date: ",df[ready_to_use_columns["Year"]].unique(),index=None)
            end_date = st.selectbox("Select the end date: ", df[ready_to_use_columns["Year"]].unique(),index=None)
            if (start_date and end_date in df[ready_to_use_columns["Year"]].unique()):
                st.write("The filtered dataset by release date is: ")
               


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
    
