


import pandas as pd
import matplotlib.pyplot as plt

dict = {"Name" : ["Messi","Ronaldo","Haland"," Pogba"],
        "Age" : [39,40,26,29]}


df = pd.DataFrame(dict)
df.plot()
plt.show()
print("The dataframe is: ")
print(df)
