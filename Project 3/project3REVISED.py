
'''SALES DATA ANALYZER'''


import warnings
import pandas as pd
from rapidfuzz import process

FILE_NAME = "mini_sales_data.csv"

STRING_COLS = ["Month","Age_Group","Customer_Gender","Country","State","Product_Category","Sub_Category","Product"]

INTEGER_COLS = ["Order_Quantity","Unit_Cost","Unit_Price","Profit","Cost","Revenue"]

FUZZ_THRESHOLD = 80

'''Load the datas'''
def load_data(file_name):
    try:
        df = pd.read_csv(file_name)
        return df
    
    except FileNotFoundError as e:
        print(f"AN ERROR OCCURED: {e}")



'''Conversion of date to datetime objects'''
def to_date_time(df):

    with warnings.catch_warnings():

        for col in df.select_dtypes(include="object").columns:
            try:
                warnings.simplefilter(action="ignore",category=UserWarning)   #Suppressing the User warning  that is being shown everytime the columns can't be converted as the datatype object
                df[col] = pd.to_datetime(df[col])

            except Exception:
                pass

    print("Conversion successful")
    return df
    


'''making all the string values clean and uniform'''
def uniform_string_values(df):
    for col in df.select_dtypes(include="object").columns:
        try: 
            df[col] = df[col].str.strip().str.title()
 
            

        except Exception as e:
            print(f"AN ERROR OCCURRED: {e}")
    return df


'''Enforcing the column datas'''
def enforce_data_type(df,string_cols,numeric_cols):
    df[string_cols] = df[string_cols].astype("string")
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric,errors ="coerce")
    return df


'''Get user's Preference'''
def user_preference():
    user_input = input("==Do you want the analysis for all the data(A) of for the data of specific time range(T)?==").upper()
    if user_input == "T":
        return True 

    elif (user_input == "A"):
        pass

    else:
        print("wrong command!!!")
        pass




'''Insights based on particular time frame'''
def insights_within_time_constraints(df,start,end):
    try: 
        filtered_df = df[  (df["Date"]>=start)  & (df["Date"]<= end)]
        return filtered_df
    
    except Exception as e:
        print(f"AN ERROR OCCURED: {e}")



'''A reuseable function for matching the columns values'''
def fuzzy_matcher(df,targets,threshold):
    try:
        matched = {}
        for target in targets:
            match,score,_ = process.extractOne(target,df.columns)

            if score >= threshold:
                matched[target] = match

        return matched if len(matched) == len(targets) else None

  


    except Exception as e:
        print(f"AN ERROR OCCURED: {e}")





'''Evaluating total of all the financial transactions'''
def totals(df,int_col):
    try:
        for col in int_col:
            match,score,_ = process.extractOne(col,df.columns)
            if score >= 80:
                result = {df[col].sum().item() for col in int_col}         # .item() is a numpy method that converts
                                                                         # np.int() item to regular int, if not done so the
                                                                         # output will be shown like np.int(total_value). we can also use int() method to convert but specifically for numpy .item() is used
            else:
                pass

        return result
    
    except Exception as e:
        print(f"AN ERROR OCCURED: {e}")




'''insights on profits'''
def profit(df):
    targets = ["Product","Profit"]
    match = fuzzy_matcher(df,targets,FUZZ_THRESHOLD)
    if match:

        return df.groupby(match["Product"])[match["Profit"]].sum().sort_values(ascending=False)
    
    else:
        print("Required column not found for profit calculations")
        return None


'''Average order Quantity'''
def average_order_quantity(df):
    targets = ["Product","Order_Quantity"]
    match = fuzzy_matcher(df,targets,FUZZ_THRESHOLD)

    if match:
        return df.groupby(match["Product"])[match["Order_Quantity"]].mean().sort_values(ascending=False)
    
    else:
        pass


'''Geographical insights on sales'''
def sales_by_region(df):
    targets = ["Country","Product","Order_Quantity"]
    match = fuzzy_matcher(df,targets,FUZZ_THRESHOLD)
    if match:
        sellings_on_each_country =  df.groupby([match["Country"],match["Product"]])[match["Order_Quantity"]].sum().sort_values(ascending=False)

        highest_selling_product_by_country = df.groupby([match["Product"],match["Country"]])[match["Order_Quantity"]].sum().sort_values(ascending=False)

        return sellings_on_each_country,highest_selling_product_by_country



'''sales insights based on personal traits'''
def sales_by_personal_traits(df):
    targets = ["Product","Customer_Age","Age_Group","Order_Quantity","Customer_Gender"]

    match = fuzzy_matcher(df,targets,FUZZ_THRESHOLD)
    if match:
        highest_buying_group = df.groupby(match["Age_Group"])[match["Order_Quantity"]].sum().sort_values(ascending=False)

        highest_buying_gender = df.groupby([match["Product"],match["Customer_Gender"]])[match["Order_Quantity"]].sum().sort_values(ascending=False)

        popular_products_by_age = df.groupby([match["Product"],match["Age_Group"]])[match["Order_Quantity"]].sum().sort_values(ascending=False)


        return highest_buying_group,highest_buying_gender,popular_products_by_age


            
def main():
    try: 
        df = load_data(FILE_NAME)

    except Exception as e: 
        print(f"AN ERROR OCCURED: {e}")

    to_date_time(df)
    print("Now the uniform string values")
    uniform_string_values(df)
    enforce_data_type(df,STRING_COLS,INTEGER_COLS)

    if(user_preference()):
        try:
            START_DATE = pd.to_datetime(input("Enter the start date: "))
            END_DATE = pd.to_datetime(input("Enter the end date: "))

            df = insights_within_time_constraints(df,START_DATE,END_DATE)
            print(f"\n==showing insights from {START_DATE} till {END_DATE} \n")


        except Exception as e:
            print(f"Unable to convert the date due to: {e} ")

    total_values = totals(df,INTEGER_COLS)
    print("\n==The totals for each financial transactions is==\n")
    print(total_values)

    print("\n==The highest selling product are==\n")
    print(profit(df))


    print("\n==The average order quantity of each product is==\n")
    print(average_order_quantity(df))


    print("\n==Insights based on geography==\n")
    sellings_on_each_country,highest_selling_product_by_country = sales_by_region(df)
    print("\n==The selling on each country is==\n")
    print(sellings_on_each_country)
    print("\n==The highest selling product by country is==\n")
    print(highest_selling_product_by_country)
 


    print("\n==The insights based on personal traits are==\n")
    highest_buying_group,highest_buying_gender,popular_products_by_age = sales_by_personal_traits(df)
    print("\n==The highest buying age group is==\n")
    print(highest_buying_group)

    print("\n==The highest buying gender is==\n")
    print(highest_buying_gender)

    print("\n==The popular products among the age group is==\n")
    print(popular_products_by_age)



if __name__ == "__main__":
    main()

