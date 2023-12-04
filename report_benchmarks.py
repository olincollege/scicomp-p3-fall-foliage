"""
Calculates and reports the mean error with benchmark values
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tree import TreeModeller

def calculate_values(df):
    """
    Calculate the day of the year when the senescence crosses the threshold

    Args:
        df (Dataframe): The dataframe of parameter inputs

    Returns:
        An integer day of the year when threshold is crossed
            Returns None if threshold is missing/never crossed
    """
    # Create a treee model
    tree_model = TreeModeller(df["species"], df["type"] , df["year"])

    # Loop through second half of year
    for doy in range(170, 366):
        # Update senescence
        tree_model.update_senescence(doy)

        # Check if threshold has been crossed
        if tree_model.sen_daily[doy - 1] > tree_model.get_threshold(df["percent"]):
            return doy

    return None

# The "calculated_benchmarks.csv" file needs to be generated the first time
# this file is run (and is not tracked by Git)
# Check if file can be read from (i.e. it exists)
try:
    print("Checking if calculated benchmarks exist...")
    calc_benchmarks = pd.read_csv("calculated_benchmarks.csv")

# If file doesn't exist, calculate the day values the threshold is crossed for all input parameters
except FileNotFoundError:
    print("They don't exist! Calculating now, this may take a while...")
    benchmarks = pd.read_csv("benchmark_values.csv")

    # Apply above function to all rows to calculate values for benchmarking
    benchmarks["calc_threshold"] = benchmarks.apply(calculate_values, axis = 1)

    # Ignore rows with any empty cells
    benchmarks = benchmarks.dropna()

    # Save as (untracked) CSV file
    benchmarks.to_csv("calculated_benchmarks.csv")

# Once benchmarks have been calculated and the CSV file exists, plot RMSE for input variables
finally:
    print("You have the calculated benchmarks, plotting RMSE values")
    calc_benchmarks = pd.read_csv("calculated_benchmarks.csv")

    categories = []
    # Valid input categories
    valid = {"species", "type", "year", "percent"}
    inputted = False

    # Keep asking for input until valid input is provided
    while not inputted:
        cat_in = input("Enter 1 or 2 categories, comma-separated: ")

        # Split into lists and remove whitespaces
        categories = [cat.strip() for cat in cat_in.split(',')]

        # Check if provided categories is a subset of the valid ones
        if not set(categories).issubset(valid):
            print("Error! Only enter valid, comma-separated categories with no other punctuation")

        # Check if a valid number of cateories has been entered
        elif len(categories) not in [1, 2]:
            print("Error! Enter one or two categories")

        # Continue if everything is correct
        else:
            inputted = True

    # Calculate Root Mean Square Error (RMSE) between provided and calculated values
    rmse_df = calc_benchmarks.groupby(categories).apply(\
        lambda group: np.sqrt(((group["threshold"] - group["calc_threshold"]) ** 2).mean()))

    # Reset index to plot RMSE values
    rmse_df = rmse_df.reset_index(name='RMSE')

    plt.figure(figsize = (10, 6))
    # Plot normal bar graphs if one category
    if len(categories) == 1:
        sns.barplot(x = categories[0], y='RMSE', data=rmse_df)

    # Plot grouped bar graphs if two categories
    else:
        sns.barplot(x = categories[0], y = "RMSE", hue = categories[1], data = rmse_df)

    # Add title and axes labels, and display
    plt.title("RMSE by Categories")
    plt.xlabel(categories[0])
    plt.ylabel("RMSE (days)")
    plt.show()
