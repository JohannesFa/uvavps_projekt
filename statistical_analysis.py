import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from pandas.compat.numpy.function import MEAN_DEFAULTS


def total_percentage_correct(filename: str):
    df = pd.read_csv(filename)
    return df['Model_correct'].mean() * 100

def percentage_each_domain(filename: str):
    df = pd.read_csv(filename)
    return df.groupby("Domain")["Model_correct"].mean() * 100

def total_percentage_of_all_models():
    file_names = os.listdir(path='.')
    df = pd.DataFrame()
    df['Mean'] = ''
    for x in file_names:
        if x.startswith('res_'):
            model_name = x.replace('res_', '').replace('.csv','')
            df.loc[model_name] = {'Mean': total_percentage_correct(x)}
    return df

def plot_graph(df: pd.DataFrame):
    df.plot()
    plt.show()


print(total_percentage_of_all_models())


