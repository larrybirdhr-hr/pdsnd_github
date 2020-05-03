import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input('Which city would you like to explore: chicago, new york city, washington \n')
        city = city.lower()
        if city in cities:
            break
        else:
            print('hmmm! Looks like there is a typo! Please enter only chicago, new york city or washington')


    # get user input for month (all, january, february, ... , june)
    # user can input January, February, March, April, May, June, or 1, 2, 3, 4, 5,6       
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    months_n = ['1', '2', '3', '4', '5', '6']
    while True:
        month = input('Which month would you like to explore: January, February, March, April, May, June or all \n')
        if month.title() in months:
            month = month.title()
            break
        elif month in months_n:
            month = months[int(month)-1]
            break
        elif month =='all' or month =='All':
            month = 'all'
            break
        else:
            print('hmmm! Looks like there is a typo! Please reenter. Please enter only the monthes')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    # user can input Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or 
    #        Mo, Tu, We, Th, Fr, Sa, Su
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days_s = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    while True:
        day = input('Which weekday would you like to explore: Mo, Tu, We, Th, Fr, Sa, Su or all \n')
        if day.title() in days_s:
            day = days[days_s.index(day.title())]
            break
        elif day.title() in days:
            day = day.title() 
            break
        elif day == 'all' or day == 'All':
            day ='all'
            break
        else:
            print('hmmm! Looks like there is a typo! Please enter only the days')


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
    

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower())+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] ==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        # days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        # day = days.index(day.title())
        df = df[df['day_of_week']==day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('The most common month is {}'.format(months[df['month'].mode()[0]-1]))


    # display the most common day of week
    print('The most common day of week is {}'.format(df['day_of_week'].mode()[0]))

    df['hour'] = df['Start Time'].dt.hour

    # display the most common start hour
    print('The most common start hour is {}'.format(df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is {}'.format(df['Start Station'].value_counts().idxmax()))


    # display most commonly used end station
    print('The most common end station is {}'.format(df['End Station'].value_counts().idxmax()))

    # display most frequent combination of start station and end station trip
    df['station_pair'] = 'Start at: '+df['Start Station']+' End at: '+df['End Station']
    print('The most frequent combination of start station and end station trip is {}'.format(df['station_pair'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40) 


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # pd.options.display.float_format = "{:,.2f}".format
    # display total travel time
    print('The total travel time is {:.2f} seconds'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('The average travel time is {:.2f} seconds'.format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users. it takes additionaly arg city, as washington has no gender, birth year"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    for i in user_types.index:
        print('The count of user type {} is {}'.format(i, user_types[i]))


    # Display counts of gender for chicago and new york city, 
    # For washington, we display no gender or birth year information
    if city in ['chicago', 'new york city']:
        gender_counts = df['Gender'].value_counts()
        for i in gender_counts.index:
            print('The count of gender {} is {}'.format(i, gender_counts[i]))
        ## Display the birth years for the selected city
        print('The earliest year of birth is {}'.format(df['Birth Year'].min()))
        print('The most recent year of birth is {}'.format(df['Birth Year'].max()))
        print('The most common year of birth is {}'.format(df['Birth Year'].mode()[0]))
    else:
        print('No gender or birth year information for Washington.')


    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        ## take the user input, it takes yes or y anything else would be considered as no
        ## it shows the raw data 5 entries every time, until user input no or n.
        raw = input('Would you like to see raw data \n')
        
        if raw.lower()=='yes' or raw.lower()=='y':
            df.drop(columns = ['station_pair', 'month', 'day_of_week','hour'], inplace = True)
            i = 5
            print(df.iloc[i-5:i])
            i+=5
            while i<=len(df):
                see_more = input('Would you like to see more?\n')
                if see_more.lower()!='no' and see_more.lower()!='n':
                    print(df.iloc[i-5:i])
                    i+=5
                else:
                    break
            ## print the last piece of data that is not part of the 5 segment
            print(df.iloc[i-5:])
    

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
