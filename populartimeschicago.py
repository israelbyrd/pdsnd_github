#!python
import pandas as pd
filename='chicago.csv'

#load file into data frame
df=pd.read_csv(filename)

#Convert the start time column to date time and extract the hour
df['hour']=pd.to_datetime(df['Start Time']).dt.hour

#find the most common hour
popularhour = df['hour'].mode()[0]

print("Most frequent start hour was {}".format(popularhour))
