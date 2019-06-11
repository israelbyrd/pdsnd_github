#!python
import time #to measure function time.
import pandas as pd
import numpy as np
pd.set_option('display.expand_frame_repr', False)
CITY_DATA = { 'chicago': 'chicago.csv',
              'newyork': 'new_york_city.csv',
              'newyorkcity': 'new_york_city.csv',
              'washington': 'washington.csv' }

months=['january','february','march','april','may','june',
        'july','august','september','october','november','december']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Select data to explore: Chicago, New York City, or Washington.\ncity data: ").lower().replace(" ","")
    while city not in CITY_DATA.keys():
        city = input("\n\nInvalid input. Select Chicago, New York City, or Washington data to explore.\ncity data: ").lower().replace(" ","")
    # get user input for month (all, january, february, ... , june)
    month = input("Data is available for January through June. Select a month or 'all' to explore all data.\nFilter by month: ").lower().replace(" ","")
    #default to 'all' if nothing entered.
    if not month:
        month = 'all'
    while month not in ['january','february','march','april','may','june', 'all']:
        month = input("Invalid entry. Select from 'January', 'February', 'March', 'April', 'May', or 'June' to filter by month, or 'all' to include all data.\nFilter by month: ").lower().replace(" ","")
        #default to 'all' if nothing entered.
        if not month:
            month = 'all'
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Select day of interest (e.g. 'Sunday'), or 'all' to include all days.\nDay filter: ").lower().replace(" ","")
    #default to 'all' if nothing entered.
    if not day:
        day = 'all'
    while day not in ['sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','all']:
        day=input("Invalid entry. Select a day of the week or 'all' to include data from all days.\nDay filter: ").lower().replace(" ","")
        if not day:
            day = 'all'
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Load data into data frame
    df=pd.read_csv(CITY_DATA[city])
    #change column names for easier typing and access
    newnames=list(map(lambda s: s.replace(' ','').lower(), df.columns))
    namedict=dict(zip(df.columns,newnames))
    df.rename(columns=namedict,inplace=True)
    if 'birthyear' in df.columns: #birthyear not available for all cities
        #Birth year is a float because is contains NAs.
        #Cast to pandas nullable integer type.
        df.birthyear=df.birthyear.astype(pd.Int64Dtype())
    #Convert the start time column to datetime
    df.starttime = pd.to_datetime(df.starttime)
    #extract month and day of the week from start time to new columns
    df['month'] = df.starttime.dt.month
    df['dayofweek'] = df.starttime.dt.weekday_name
    #filter by month if applicable
    if month != 'all':
        #index the months to get the corresponding int
        month=months.index(month)+1
        #filter by month
        df=df[df.month==month]
    if day != 'all':
        df=df[df.dayofweek == day.title()]
    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print("The most common")
    #Display most common month, if not filtered by month
    if month == 'all':
        print("  month: {}".format(months[df.month.mode()[0]].title()))
    # display the most common day of week if not filtered by day
    if day == 'all':
        print("  day: {}".format(df.dayofweek.mode()[0].title()))
    # display the most common start hour
    print("  start hour: {}".format(df.starttime.dt.hour.mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    print("The most common")
    print("  Origin station: {}".format(df.startstation.mode()[0]))
    # display most commonly used end station
    print("  destination station: {}".format(df.endstation.mode()[0]))
    # display most frequent combination of start station and end station trip
    trip=df.startstation+" station to "+df.endstation+" station"
    print("  Trip: {}.".format(trip.mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df,day):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time. tripduration column is in seconds but Convert
    # to hours for the total. 60 sec/min * 60 min/hour = 360 seconds/hour
    print("Customers biked for {} hours on {} between {} and {}.".format(round(df.tripduration.sum()/360,2),
    'all days' if day == 'all' else day.title()+"s",
    df.starttime.min().strftime("%B %d %Y"), pd.to_datetime(df.endtime).max().strftime("%B %d %Y")))
    # display mean travel time in minutes
    print("Average trip duration was {} minutes for this same set of data.".format(round(df.tripduration.mean()/60)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats ...\n')
    start_time = time.time()
    # Display counts of user types
    print("Count of user types:\n{}\n".format(df.usertype.value_counts()))
    # Display counts of gender. Not available for washington
    if 'gender' in df.columns:
        print("Count of customers by gender:\n{}\n".format(df.gender.value_counts()))
    # Display earliest, most recent, and most common year of birth
    # Not available for all cities
    # Rather than filter by city, filter on whether 'birghtyear' column
    # is available. This makes it easier to incorporate new city data.
    if 'birthyear' in df.columns:
        print("Eldest customer was born in {}.".format(df.birthyear.min()))
        print("Youngest customer was born in {}.".format(df.birthyear.max()))
        print("Customer's most common birth year was {}.".format(df.birthyear.mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    """
    Generates descriptive statistics for bikeshare data.
    Only one city can be processed at a time.
    City and filters selected by text prompts.
    """
    while True:
        city, month, day = get_filters()
        print("Loading {} data with filter settings: month = {}, day = {}.\n".format(city.title(), month, day))
        df = load_data(city, month, day)
        print("These filters result in a data set of {} customer bike trips.".format(len(df)))
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df,day)
        user_stats(df)
        showraw=input("Type 'yes' to show first 5 lines of raw data: ").lower().replace(" ","")
        first=0
        last=5
        while True:
            if showraw == 'yes':
                print("Raw data rows {} through {}.\n{}".format(first,last-1 if last<len(df) else len(df)-1,df[first:last].drop(['unnamed:0','month','dayofweek'],axis=1)))
                first=last
                last+=5
                if last > len(df):
                    print("All raw data shown.\n")
                    break
                showraw=input("Type 'yes' to show next 5 lines of the raw data: ").lower().replace(" ","")
            elif showraw == 'no':
                break
            else:
                showraw=input("Invalid response. Type 'yes' to show more data, type 'no' to move on: ").lower().replace(" ","")

        restart = input("\nType 'yes' to restart bike share analysis or type 'no' to quit: ").lower().replace(" ","")
        while restart != 'no' and restart != 'yes':
            restart = input("Invalid response. Type 'yes' to restart bike share analysis or type 'no' to quit: ").lower().replace(" ","")
        if restart.lower() != 'yes': #Exit on yes. Doesn't execute on input other than yes or no - stuck in loop above.
            break


if __name__ == "__main__":
	main()
