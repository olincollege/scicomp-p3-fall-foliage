import pandas as pd
import matplotlib.pyplot as plt
from tree import Tree_Specific
import numpy as np

params = pd.read_csv("params.csv")
p = params.iloc[0].tolist()
this_tree = Tree_Specific(*p[2:], year = 2010)

printed_y90 = False
for doy in range(170, 366):
    this_tree.update_senescence(doy)
    if this_tree.sen_daily[doy - 1] > this_tree.y_crit and not printed_y90:
        print(doy)
        printed_y90 = True

plt.plot(this_tree.sen_daily)
plt.show()