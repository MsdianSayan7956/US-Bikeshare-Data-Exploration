# US-Bikeshare-Data-Exploration
(Udacity) Programming for Data Science Nanodegree 1st Project: Exploring Bike share data from 3 different cities

Project Overview

Overview
This project is an interactive Python script that analyzes bikeshare data from three major US cities: Chicago, New York City, and Washington, D.C. Users can filter the data by month and/or day of the week and view various statistics, including the most frequent travel times, popular stations and trips, trip durations, and user demographics. The script also allows users to view raw data in batches upon request.
The project demonstrates data analysis using Pandas, handling user inputs with validation, and computing descriptive statistics.

Features

User Input Handling: Prompts for city selection (Chicago, New York, Washington) with flexible input mapping (e.g., "NYC" or "ny" for New York). Filters by month (January-June), day of the week, both, or none.
Data Filtering and Loading: Loads CSV data for the selected city and applies filters using Pandas.
Statistics:

Most common month, day, and hour of travel.
Most popular start and end stations, and frequent trips.
Total and average trip durations (formatted in days, hours, minutes, seconds).
User type counts, gender distribution, and birth year stats (where available; not in Washington data).


Raw Data Display: Iteratively shows 5 rows of raw data at a time until the user declines or data ends.
Error Handling: Graceful handling of invalid inputs, missing files, and empty datasets.

Data Source: The data used in this project was provided by Udacity for AWS Data Engineer Stream program.

Tools and Libraries:
Python 3: This project is built using the Python programming language. Further documentation can be found at the official Python website.(https://www.python.org/)
pandas: The primary library used for data manipulation and analysis in this project. The official documentation is an excellent resource for learning more about its capabilities: pandas documentation.(https://pandas.pydata.org/docs/)
Coding Conventions:
PEP 8 -- Style Guide for Python Code: The script aims to follow the styling guidelines outlined in PEP 8 to ensure code readability and consistency. You can read the full guide here(https://peps.python.org/pep-0008/)

PEP 257 -- Docstring Conventions: The docstrings for each function follow the conventions described in PEP 257. More details can be found here(https://peps.python.org/pep-0257/)