
import pandas as pd
from rapidfuzz import process

FILE_NAME = "mini_sales_data.csv"

STRING_COLS = ["Month","Age_Group","Customer_Gender","Country","State","Product_Category","Sub_Category","Product"]

INTEGER_COLS = ["Order_Quantity","Unit_Cost","Unit_Price","Profit","Cost","Revenue"]


'''Load the datas'''
def load_data(file_name):
    try:
        df = pd.read_csv(file_name)
        return df
    
    except FileNotFoundError as e:
        print(f"{e} occurred")


'''Conversion of date to datetime objects'''
def to_date_time(df):
    for col in df.select_dtypes(include="object").columns:
        try:
            df[col] = pd.to_datetime(df[col])


        except Exception:
            pass
    print("Conversion successful")
    return df


'''making all the string values clean and uniform'''
def uniform_string_values(df):
    for col in df.select_dtypes(include="string").columns:
        try: 
            df[col] = df[col].str.strip().str.title()
            print("The strings are cleaned and they are standarized")
            return df

        except Exception:
            pass


'''Get user's Preference'''
def user_preference():
    USER_INPUT = input("==Do you want the analysis for all the data(A) of for the data of specific time range(T)?==").upper()
    if USER_INPUT == "T":
        return True 

    elif (USER_INPUT == "A"):
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
def fuzzy_matcher(df,targets):
    try:
        target_storage = []
        for target in targets:
            match,score,_ = process.extractOne(target,df.columns)
            if score >= 80:
                target_storage.append(score)
            else:
                pass
        if all(score>=80 for score in target_storage):
            return True

    except Exception:
        pass





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
        pass




'''insights on profits'''
def profit(df):
    targets = ["Product","Profit"]
    if(fuzzy_matcher(df,targets)):
        return df.groupby(targets[0])[targets[1]].sum().sort_values(ascending=False)
    
    else:
        pass


'''Average order Quantity'''
def average_order_quantity(df):
    targets = ["Product","Order_Quantity"]
    if (fuzzy_matcher(df,targets)):
        return df.groupby(targets[0])[targets[1]].mean().sort_values(ascending=False)
    
    else:
        pass


'''Geographical insights on sales'''
def sales_by_region(df):
    targets = ["Country","Product","Order_Quantity"]
    if (fuzzy_matcher(df,targets)):
        sellings_on_each_country =  df.groupby([targets[0],targets[1]])[targets[2]].sum().sort_values(ascending=False)

        highest_selling_product_by_country = df.groupby([targets[1],targets[0]])[targets[2]].sum().sort_values(ascending=False)

        return sellings_on_each_country,highest_selling_product_by_country



'''sales insights based on personal traits'''
def sales_by_personal_traits(df):
    targets = ["Product","Customer_Age","Age_Group","Order_Quantity","Customer_Gender"]
    if (fuzzy_matcher(df,targets)):
        highest_buying_group = df.groupby(targets[2])[targets[3]].sum().sort_values(ascending=False)

        highest_buying_gender = df.groupby([targets[0],targets[4]])[targets[3]].sum().sort_values(ascending=False)

        popular_products_by_age = df.groupby([targets[0],targets[2]])[targets[3]].sum().sort_values(ascending=False)


        return highest_buying_group,highest_buying_gender,popular_products_by_age


            
def main():
    try: 
        df = load_data(FILE_NAME)

    except Exception as e: 
        print(f"An error occurred {e}")

    to_date_time(df)
    uniform_string_values(df)

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

    print("\n==The highest buying age group is==\n")
    print(popular_products_by_age)



if __name__ == "__main__":
    main()

