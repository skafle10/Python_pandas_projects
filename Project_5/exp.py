

import pandas as pd

import os

df = pd.DataFrame ( {"genre" : ["Action","Action,Comedy","Action","Comedy","Action,Thriller"]  }
                   
                   )


lis = df["genre"].unique()

print(lis)
a = type(lis)
print(a)

# print(df)