

import pandas as pd
import openpyxl
data = {"name":["Ram","Hari","Shyam","Bhola","Bimal","Rajni","David"],
        "Math":[50,60,40,80,60,55,37],
        "Science":[20,65,18,20,17,95,66],
        "English":[70,70,28,30,18,50,46]
        
        }


df = pd.DataFrame(data)
df["Average"] = df.select_dtypes(include="number").mean(axis=1)

df["Result"] = df["Average"].apply(lambda x : "Pass" if x>40 else "Fail")

df.sort_values(by="Average",ascending=False,inplace=True)
print("The original dataframe is given below: ")
print(df)


print("The passed students are : ")

passed_students = df[df["Average"]>=40]
print(passed_students)
# passed_students.to_csv("Passed.csv",index=False)
passed_students.to_excel("passed.xlsx")

print("The students who failed are: ")
failed_students = df[df["Average"]<40]
print(failed_students)
failed_students.to_excel("Failed.xlsx")