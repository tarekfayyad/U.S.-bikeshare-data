import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day or all to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Please, enter your search criteria : \n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please choose a city: Chicago, New York City, Washington or All : ')
        city = city.lower()
        city_list = ['chicago', 'new york city', 'washington','all']
        if city in city_list:
            break
        else:
            print('Please enter valid input!!')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please choose a month: January, February, March, April, May,June or All : ')
        month = month.lower()
        month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        if month in month_list:
            break
        else:
            print('Please enter valid input!!')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please choose a day: monday, Tuesday, Wednesday, Thursday, Friday, Sunday or All : ')
        day = day.lower()
        day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'sunday', 'all']
        if day in day_list:
            break
        else:
            print('Please enter valid input!!')

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
    if city != 'all':
        # Apply filter with required city
        df = pd.read_csv(CITY_DATA[city])
        #convert start time column to date time to extract month and day
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        # create col containing month name to filter by
        df['month'] = df['Start Time'].dt.month_name()
        # create col containing day name to filter by
        df['weekday'] = df['Start Time'].dt.day_name()
    else:
        # Apply filter with all city
        df1 = pd.read_csv('chicago.csv')
        df2 = pd.read_csv('new_york_city.csv')
        df3 = pd.read_csv('washington.csv')
        df = pd.concat([df1,df2,df3])
        # convert start time column to date time to extract month and day
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        # create col containing month name to filter by
        df['month'] = df['Start Time'].dt.month_name()
        # create col containing day name to filter by
        df['weekday'] = df['Start Time'].dt.day_name()
    if month != 'all' :
        # apply filter with required month
        filt_month = (df['month'] == month.title())
        df = df[filt_month]

    if day != 'all' :
        # apply filter with required day
        filt_day = (df['weekday'] == day.title())
        df = df[filt_day]

    # return df with required criteria of searching
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month_filt = df['month'].value_counts().index[0]
    print('Most common month : ',common_month_filt)

    # display the most common day of week
    common_weekday_filt = df['weekday'].value_counts().index[0]
    print('Most common weekday : ', common_weekday_filt)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour_filt = df['hour'].value_counts().index[0]
    print('Most common hour : ', common_hour_filt)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_used_start_station_filt = df['Start Station'].value_counts().index[0]
    print('Most commonly used start station : ', most_common_used_start_station_filt)

    # display most commonly used end station
    most_common_used_end_station_filt = df['End Station'].value_counts().index[0]
    print('Most commonly used end station : ', most_common_used_end_station_filt)

    # display most frequent combination of start station and end station trip

    df['most_combination'] = df['Start Station']+' '+df['End Station']
    most_freq_combination_filt = df['most_combination'].value_counts().index[0]
    print('Most frequent combination of start station and end station trip : ',most_freq_combination_filt)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # time in second - to turn it to days divide by 24*60*60
    sum_time_filt = df['Trip Duration'].sum()
    print('Total travel time : ',(sum_time_filt/86400).round(2),'Days')


    # display mean travel time
    # time in second - to turn it to minutes divide by 60
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time : ',(mean_travel_time/60).round(2), 'Minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count_filt = df['User Type'].value_counts()
    print('Counts of user types : \n',user_type_count_filt)

    # Display counts of gender
    # Washington city dos not have these data
    try:
        gender_count_filt = df['Gender'].value_counts()
        print('Counts of gender : \n', gender_count_filt)
    except:
        print('Data not available for counts of gender for Washington City.')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_filt = int(df['Birth Year'].min())
        recent_year_filt = int(df['Birth Year'].max())
        common_year_filt = int(df['Birth Year'].value_counts().index[0])
        print('Earliest year of birth : ',earliest_year_filt)
        print('Recent year of birth : ',recent_year_filt)
        print('common year of birth : ',common_year_filt)
    except:
        print('Data not available for earliest, most recent, and most common year of birth for Washington City.')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    # ask user to display raw data
    # display the first 5 rows and so on upon user request
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while True:
        if view_data == 'yes':
            print(df.iloc[0:5])
            start_loc += 5
            view_data = input("Do you wish to continue?: ").lower()
        else: break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
