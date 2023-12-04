import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tree import Tree_Modeller

def get_threshold_day(tree_model, percent):
    for doy in range(170, 366):
        tree_model.update_senescence(doy)
        if tree_model.sen_daily[doy - 1] > tree_model.get_threshold(percent):
            return doy
    return None

def calculate_values(df):
    this_tree = Tree_Modeller(df["species"], df["type"] , df["year"])
    return get_threshold_day(this_tree, df["percent"])



def calculate_rmse(df, categories):
    return df.groupby(categories).apply(lambda group: np.sqrt(((group["threshold"] - group["calc_threshold"]) ** 2).mean()))

def plot_rmse(df, categories):
    valid = {"species", "type", "year", "percent"}
    if not set(categories).issubset(valid):
        print("ERROR:Enter a valid category!")
        return
    
    if len(categories) not in [1, 2]:
        print("ERROR: Enter 1 or 2 categories")
        return
    
    rmse_df = df.groupby(categories).apply(lambda group: np.sqrt(((group["threshold"] - group["calc_threshold"]) ** 2).mean()))
    rmse_df = rmse_df.reset_index(name='RMSE')
    # Plot grouped bar graphs
    plt.figure(figsize = (10, 6))
    if len(categories) == 1:
        sns.barplot(x = categories[0], y='RMSE', data=rmse_df)

    else:
        sns.barplot(x = categories[0], y = "RMSE", hue = categories[1], data = rmse_df)

    plt.title("RMSE by Categories")
    plt.xlabel(categories[0])
    plt.ylabel("RMSE (days)")
    plt.show()

try:
    calc_benchmarks = pd.read_csv("calculated_benchmarks.csv")

except:
    benchmarks = pd.read_csv("benchmark_values.csv")
    benchmarks["calc_threshold"] = benchmarks.apply(calculate_values, axis = 1)
    benchmarks = benchmarks.dropna()
    benchmarks.to_csv("calculated_benchmarks.csv")

finally:
    calc_benchmarks = pd.read_csv("calculated_benchmarks.csv")
    plot_rmse(calc_benchmarks, ["year", "type"])

        
