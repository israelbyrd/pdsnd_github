#!python
#This is a bit of a bigger task, which involves choosing a dataset to load and
#filtering it based on a specified month and day. In the quiz below,
#you'll implement the load_data() function, which you can use directly in your
#project. There are four steps:
# Load the dataset for the specified city. Index the global CITY_DATA
#   dictionary object to get the corresponding filename for the given city name.
# Create month and day_of_week columns. Convert the "Start Time" column to
#   datetime and extract the month number and weekday name into separate
#   columns using the datetime module.
# Filter by month. Since the month parameter is given as the name of the month,
#   you'll need to first convert this to the corresponding month number.
#   Then, select rows of the dataframe that have the specified month and
#   reassign this as the new dataframe.
# Filter by day of week. Select rows of the dataframe that have the specified
#   day of week and reassign this as the new dataframe.
#   (Note: Capitalize the day parameter with the title() method to match the
#    title case used in the day_of_week column!)

import pandas as pd
citydata={'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv',
          'washington': 'washington.csv'}

def loaddata(city, month, day):
  """
  Loads data for the specified city and filters by month and day if applicable.

  Args:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
  Returns:
  df - pandas DataFrame containing city data filtered by month and day
  """
  #load data into data frame.
  df=pd.read_csv(citydata[city])

  #convert the start time column to datetime
  df['Start Time']=pd.to_datetime(df['Start Time'])

  #extract month and day of week from start time to create new columns
  df['month'] = df['Start Time'].dt.month
  df['day_of_week'] = df['Start Time'].dt.weekday_name

  #filter by month if applicable
  if month != 'all':
    #use the index of the months list to get the corresponding int
    months=['january','february','march','april','may','june','july','august','september','october','november','december']
    month = months.index(month)+1

    #filter dataframe by month
    df=df[df['month']==month]

  #filter by day if applicable
  if day != 'all':
    df=df[df['day_of_week']==day.title()]

  return df

df=loaddata('chicago','march','friday')
print('filtered df:\n{}'.format(df))
