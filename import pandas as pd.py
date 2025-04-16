import pandas as pd 

# read the datasets 
df1 = pd.read_csv(r"C:\Users\Christian\OneDrive - University of Perpetual Help System JONELTA\Desktop\ELECTIBZ\data_1.csv") 
df2 = pd.read_csv(r"C:\Users\Christian\OneDrive - University of Perpetual Help System JONELTA\Desktop\ELECTIBZ\data_2.csv") 

# print the datasets 
print(df1.head()) 
print(df2.head()) 
concat_data = pd.concat([df1, df2], ignore_index=True) 
print(concat_data) 

merge_data = pd.merge(df1, df2, how='outer') 
print(merge_data) 