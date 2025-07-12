

import pandas as pd
import openpyxl

file_name = "weather_data.csv"
df = pd.read_csv(file_name)
print("This is just the raw data")
# print(df)
df["Average_temp"] = df[['High Temp (°C)', 'Low Temp (°C)']].mean(axis=1)
df.sort_values(by="Average_temp",inplace=True,ascending=False)
cols = list(df.columns)
cols[3],cols[4] = cols[4],cols[3]
new_df = df[cols]
print(new_df)
print("The hottest days are: ")
hot_df = new_df[["Date","Average_temp"]].head()
print(hot_df)

# with open("hottest.csv",'w') as hot:
#     hot.write("TOP 5 HOTTEST DAYS THIS MONTH\n")
#     hot_df.to_csv(hot, index=False)


with pd.ExcelWriter('hottest.xlsx',engine="openpyxl") as writer:
    workbook = writer.book
    sheet_name = "sheet1"
    hot_df.to_excel(writer,index=False,startrow=1,sheet_name=sheet_name)
    worksheet = writer.sheets[sheet_name]
    worksheet.cell(row=1,column=1,value="TOP 5 HOTTEST DAYS THIS MONTH")


