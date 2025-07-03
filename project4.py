

'''TOP CUSTOMER ANALYZER'''

import pandas as pd
from rapidfuzz import process


FILE_NAME = "for_project4.csv"
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
    for cols in df.select_dtypes(include="object").columns:
        try: 
            df[cols] = pd.to_datetime(df[cols])

        except:
            pass

    return df
        

'''clean the data'''
def clean_text(df):
        for cols in df.select_dtypes(include="object").columns:
            try:
                df[cols] = df[cols].str.strip().str.title()



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
    targets = ["Customer_ID","Customer_Name","Product","Order_Quantity","Profits"]
    match = fuzzy_matcher(df,targets,THRESHOLD)

    if match:
        try: 
            highest_ordering_customer = df.groupby(match["Customer_ID"])[match["Order_Quantity"]].sum().sort_values(ascending=False)

            top_purchased_items_individually = df.groupby([match["Customer_ID"],match["Customer_Name"],match["Product"]]) [match["Order_Quantity"]].sum().reset_index().sort_values(by = match["Order_Quantity"],ascending=False)

            most_profitable_customer = df.groupby([match["Customer_ID"],match["Customer_Name"]])[match["Profits"]].sum().reset_index().sort_values(by=match["Profit"],ascending=False)
            

            return highest_ordering_customer,top_purchased_items_individually,most_profitable_customer


        except Exception as e:
            print(f"Error in analyzing top customers due to : {e}")




'''Behavioural analysis of customer'''
def behavioural_analysis(df):
    targets = ["Date","Order_Quantity","Customer_ID"]
    match = fuzzy_matcher(df,targets,THRESHOLD)
    if match:

        df["month"] = df[match["Date"]].dt.to_period("M")
        no_of_monthly_orders =  df.groupby("month")[match["Order_Quantity"]].sum()

        frequency_of_monthly_orders = df.groupby("month")[match["Order_Quantity"]].size()

        customers_monthly_order_frequency = df.groupby(["month",match["Customer_ID"]])[match["Order_Quantity"]].size()

        customers_total_orders_monthlty = df.groupby(["month",match["Customer_ID"]])[match["Order_Quantity"]].sum().sort_values(ascending=False)

        print("The monthly order of each individual is")
        print(customers_total_orders_monthlty)



def main():
    
    try:
     df = load_data(FILE_NAME)

    except Exception as e:
        print(f"error in calling the data loading function due to: {e}")

    to_date_time(df)
    clean_text(df)
    top_customers(df)
    behavioural_analysis(df)

    

if __name__ == "__main__":
    main()
