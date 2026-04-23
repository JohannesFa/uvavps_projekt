import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import re
from pandas.compat.numpy.function import MEAN_DEFAULTS

"""
def total_percentage_correct(filename: str):
    df = pd.read_csv(filename)
    return df['Model Correct'].mean() * 100

def percentage_each_domain(filename: str):
    df = pd.read_csv(filename)
    return df.groupby('Domain')['Model Correct'].mean() * 100

def total_percentage_of_all_models():
    file_names = os.listdir(path='.')
    df = pd.DataFrame()
    df['Mean'] = ''
    for x in file_names:
        if x.startswith('res_'):
            model_name = x.replace('res_', '').replace('.csv','')
            df.loc[model_name] = {'Mean': total_percentage_correct(x)}
    return df

def percentage_each_domain_of_all_models():
    file_names = os.listdir(path='.')
    df = pd.DataFrame()
    for x in file_names:
        if x.startswith('res_'):
            model_name = x.replace('res_', '').replace('.csv','')
            if len(df.columns) == 0:
                df = pd.DataFrame(columns=list(pd.read_csv(x).groupby('Domain').groups.keys()))
            df.loc[model_name] = percentage_each_domain(x)
    return df.transpose()

"""

def get_all_models_df():
    files = os.listdir()

    result_files = []
    for file in files:
        if re.search('res_.*\\.csv',file):
            result_files.append(file)
    
    pd_list = []
    for file in result_files:
        df = pd.read_csv(file,delimiter="|")
        pd_list.append(df)

    return pd_list, result_files
    

def plot_graph(df: pd.DataFrame):
    df.plot()
    plt.show()


if __name__ == "__main__":
    models_df_list, model_names = get_all_models_df()
    

    dict_list = []

    correct_by_domain_list = []

    for model_index, model_df in enumerate(models_df_list):
        #print(model_df)
        model_name = model_names[model_index]
        model_mean = model_df['Model Correct'].mean()*100
        correct_by_domain = model_df.groupby('Domain')['Model Correct'].mean() * 100
        correct_by_domain_list.append(correct_by_domain)

        dict_list.append({"Model_name": model_name,"Correct_by_domain":correct_by_domain, "Mean":model_mean})
    #print(total_percentage_of_all_models())

    model_metrics_df = pd.DataFrame(dict_list,columns=["Model_name", "Correct_by_domain", "Mean"])

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_rows", None)
    pd.set_option('display.max_colwidth', None)
    print(model_metrics_df)