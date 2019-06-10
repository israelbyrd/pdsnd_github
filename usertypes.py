#!python
#There are different types of users specified in the "User Type" column.
#Find how many there are of each type and store the counts in a pandas
#series in the user_types variable.

import pandas as pd

filename="chicago.csv"
#load data into dataframe
df=pd.read_csv(filename)

#print value counts for user user_types
usertypes=df["User Type"].value_counts()

print(usertypes)
