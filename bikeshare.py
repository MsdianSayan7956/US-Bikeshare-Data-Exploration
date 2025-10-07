import pandas as pd
import time
import os
import numpy as np
from datetime import datetime


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Map possible user inputs to standard city names
    city_mapping = {
        'chicago': 'chicago',
        'chi': 'chicago',
        'c': 'chicago',
        'new york': 'new_york_city',
        'new york city': 'new_york_city',
        'ny': 'new_york_city',
        'nyc': 'new_york_city',
        'washington': 'washington',
        'wa': 'washington',
        'dc': 'washington',
        'w': 'washington'
    }

    # Get user input for city
    while True:
        city_input = input(
            "\nWhich city would you like to see data for? Chicago, New York, or Washington?\n").strip().lower()
        city = city_mapping.get(city_input)
        if city:
            break
        else:
            print("Sorry, that's not a valid city. Please choose from Chicago, New York, or Washington.")

    # Get user input for time filter
    time_filter_options = ['month', 'day', 'both', 'none']
    while True:
        time_filter = input(
            "\nWould you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter.\n"
        ).strip().lower()
        if time_filter in time_filter_options:
            break
        else:
            print(f"Please enter a valid option: {', '.join(time_filter_options)}.")

    # Initialize month and day with default values
    month = 'all'
    day = 'all'

    # Month mapping with abbreviations
    month_mapping = {
        'jan': 'january', 'january': 'january', '1': 'january',
        'feb': 'february', 'february': 'february', '2': 'february',
        'mar': 'march', 'march': 'march', '3': 'march',
        'apr': 'april', 'april': 'april', '4': 'april',
        'may': 'may', '5': 'may',
        'jun': 'june', 'june': 'june', '6': 'june'
    }

    # Get user input for month if needed
    if time_filter in ['month', 'both']:
        while True:
            month_input = input("\nWhich month? January, February, March, April, May, or June?\n").strip().lower()
            month = month_mapping.get(month_input)
            if month:
                break
            else:
                print("Please enter a valid month from January to June (full name or 3-letter abbreviation).")

    # Day mapping with abbreviations
    day_mapping = {
        'mon': 'monday', 'monday': 'monday', '1': 'monday',
        'tue': 'tuesday', 'tuesday': 'tuesday', '2': 'tuesday',
        'wed': 'wednesday', 'wednesday': 'wednesday', '3': 'wednesday',
        'thu': 'thursday', 'thursday': 'thursday', '4': 'thursday',
        'fri': 'friday', 'friday': 'friday', '5': 'friday',
        'sat': 'saturday', 'saturday': 'saturday', '6': 'saturday',
        'sun': 'sunday', 'sunday': 'sunday', '7': 'sunday'
    }

    # Get user input for day if needed
    if time_filter in ['day', 'both']:
        while True:
            day_input = input(
                "\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n"
            ).strip().lower()
            day = day_mapping.get(day_input)
            if day:
                break
            else:
                print("Please enter a valid day of the week (full name or 3-letter abbreviation).")

    print('-' * 40)
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
    # Try different possible file locations
    possible_paths = [
        f'{city}.csv',
        f'data/{city}.csv',
        f'../data/{city}.csv',
        f'../{city}.csv',
    ]

    df = None
    for file_path in possible_paths:
        try:
            df = pd.read_csv(file_path)
            break
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

    if df is None:
        print(f"Could not find the data file for {city}.")
        return None

    # Convert the Start Time column to datetime
    try:
        df['Start Time'] = pd.to_datetime(df['Start Time'])
    except Exception as e:
        print(f"Error converting Start Time to datetime: {e}")
        return None

    # Extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month) + 1
        df = df[df['month'] == month_num]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def format_seconds(seconds):
    """Convert seconds to a more readable format (days, hours, minutes, seconds)"""
    if pd.isna(seconds):
        return "N/A"

    seconds = int(seconds)
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    if len(parts) > 2:
        return ", ".join(parts[:-1]) + f", {parts[-1]}"
    elif len(parts) == 2:
        return f"{parts[0]}, {parts[1]}"
    else:
        return parts[0]


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    if df is None or df.empty:
        print("No data available for the selected filters.")
        return

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    try:
        # Display the most common month
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        popular_month_num = df['month'].mode()[0]
        popular_month = months[popular_month_num - 1]
        print(f'Most Common Month: {popular_month}')

        # Display the most common day of the week
        popular_day = df['day_of_week'].mode()[0]
        print(f'Most Common Day: {popular_day}')

        # Display the most common start hour
        popular_hour = df['hour'].mode()[0]
        print(f'Most Common Start Hour: {popular_hour}:00')

    except Exception as e:
        print(f"Error calculating time statistics: {e}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    if df is None or df.empty:
        print("No data available for the selected filters.")
        return

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        # Display most commonly used start station
        popular_start_station = df['Start Station'].mode()[0]
        print(f'Most Commonly Used Start Station: {popular_start_station}')

        # Display most commonly used end station
        popular_end_station = df['End Station'].mode()[0]
        print(f'Most Commonly Used End Station: {popular_end_station}')

        # Display a most frequent combination of start station and end station trip
        df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
        popular_trip = df['Trip'].mode()[0]
        print(f'Most Frequent Trip: {popular_trip}')

    except Exception as e:
        print(f"Error calculating station statistics: {e}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    if df is None or df.empty:
        print("No data available for the selected filters.")
        return

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
        # Clean the data - remove any invalid durations
        valid_durations = df['Trip Duration'].dropna()
        if len(valid_durations) == 0:
            print("No valid trip duration data available.")
            return

        # Display total travel time
        total_travel_time = valid_durations.sum()
        print(f'Total Travel Time: {format_seconds(total_travel_time)}')

        # Display mean travel time
        mean_travel_time = valid_durations.mean()
        print(f'Average Travel Time: {format_seconds(mean_travel_time)}')

    except Exception as e:
        print(f"Error calculating trip duration statistics: {e}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    if df is None or df.empty:
        print("No data available for the selected filters.")
        return

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print('Counts of User Types:')
        for user_type, count in user_types.items():
            print(f'  {user_type}: {count}')

        # Display gender information (only available for NYC and Chicago)
        if city in ['chicago', 'new_york_city']:
            if 'Gender' in df.columns:
                gender_counts = df['Gender'].value_counts()
                valid_genders = df['Gender'].dropna()

                if len(valid_genders) > 0:
                    print('\nCounts of Gender:')
                    for gender, count in gender_counts.items():
                        print(f'  {gender}: {count}')
                else:
                    print("\nNo gender data available")
            else:
                print("\nGender data not available for this dataset.")

        # Display birth year statistics (only available for NYC and Chicago)
        if city in ['chicago', 'new_york_city']:
            if 'Birth Year' in df.columns:
                valid_birth_years = df['Birth Year'].dropna()

                if len(valid_birth_years) > 0:
                    earliest_birth_year = int(valid_birth_years.min())
                    most_recent_birth_year = int(valid_birth_years.max())
                    most_common_birth_year = int(valid_birth_years.mode()[0])

                    print(f'\nEarliest Birth Year: {earliest_birth_year}')
                    print(f'Most Recent Birth Year: {most_recent_birth_year}')
                    print(f'Most Common Birth Year: {most_common_birth_year}')

                else:
                    print("\nNo valid birth year data available")
            else:
                print("\nBirth year data not available for this dataset.")

    except Exception as e:
        print(f"Error calculating user statistics: {e}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def display_raw_data(df):
    """Displays raw data upon request by the user."""
    if df is None or df.empty:
        print("No data available for the selected filters.")
        return

    i = 0
    while i < len(df):
        show_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').strip().lower()
        if show_data in ['yes', 'y']:
            print(df.iloc[i:i + 5])
            i += 5

            if i >= len(df):
                print("\nNo more raw data to display.")
                break
        elif show_data in ['no', 'n']:
            break
        else:
            print("Please enter a valid response (yes or no).")


def main():
    """Main function to run the bikeshare data analysis."""
    while True:
        try:
            # Get user preferences
            city, month, day = get_filters()

            # Load and filter data
            df = load_data(city, month, day)

            if df is None:
                print("Failed to load data. Please check your data files and try again.")
                restart = input('\nWould you like to try again? Enter yes or no.\n').strip().lower()
                if restart not in ['yes', 'y']:
                    print("Thank you for using the BikeShare data analysis tool. Goodbye!")
                    break
                else:
                    continue

            if df.empty:
                print("No data matches your filter criteria.")
                restart = input('\nWould you like to try different filters? Enter yes or no.\n').strip().lower()
                if restart not in ['yes', 'y']:
                    print("Thank you for using the BikeShare data analysis tool. Goodbye!")
                    break
                else:
                    continue

            # Perform all analyses
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)

            # Offer to display raw data
            display_raw_data(df)

            # Ask if user wants to restart
            restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
            if restart not in ['yes', 'y']:
                print("Thank you for using the BikeShare data analysis tool. Goodbye!")
                break

        except KeyboardInterrupt:
            print("\nAnalysis interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()