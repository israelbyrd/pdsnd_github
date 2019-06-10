#!python
import pandas as pd

print("Reading chicago.csv file")
chicago=pd.read_csv("chicago.csv")
print("chicago.head:\n{}".format(chicago.head()))
print("chicago.columns:\n{}".format(chicago.columns))
print("chicago.describe():\n{}".format(chicago.describe()))
print("chicago.info():\n{}".format(chicago.info()))
print("chicago.isnull().sum():\n{}".format(chicago.isnull().sum()))
for name in chicago.columns:
  print("chicago[{}].value_counts():\n{}".format(name,chicago[name].value_counts()))
  print("chicago[{}].unique():\n{}".format(name,chicago[name].unique()))
