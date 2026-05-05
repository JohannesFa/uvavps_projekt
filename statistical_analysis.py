import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

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



def extract_size(name):
    import re

    # standard xxb
    m = re.search(r'(\d+(?:\.\d+)?)(?=b(?:-|_|\.|$))', name)
    if m:
        return float(m.group(1))

    # eNb patterns
    m = re.search(r'e(\d+(?:\.\d+)?)b', name)
    if m:
        return float(m.group(1))

    return np.nan

if __name__ == "__main__":
    models_df_list, model_names = get_all_models_df()
    

    dict_list = []

    correct_by_domain_list = []

    for model_index, model_df in enumerate(models_df_list):
        model_name = model_names[model_index].lstrip('res_').rstrip('.csv')
        model_mean = model_df['Model Correct'].mean()*100
        correct_by_domain = model_df.groupby('Domain')['Model Correct'].mean() * 100
        correct_by_domain_list.append(correct_by_domain)

        dict_list.append({"Model Name": model_name,"Correct By Domain":correct_by_domain, "All Mean":model_mean})

    model_metrics_df = pd.DataFrame(dict_list)

    model_metrics_df["Param Size"] = model_metrics_df['Model Name'].apply(extract_size)

    model_metrics_df = model_metrics_df.sort_values("Param Size")

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_rows", None)
    pd.set_option('display.max_colwidth', None)

    model_metrics_df = model_metrics_df.set_index("Model Name")
    expanded_df = model_metrics_df["Correct By Domain"].apply(pd.Series)
    expanded_df["All Mean"] = model_metrics_df["All Mean"]
    expanded_df.index = model_metrics_df.index

    #print(expanded_df)
    
    ax = expanded_df.plot(kind="bar")
    ax.set_xticks(range(-1, len(expanded_df)-1))
    ax.set_xticklabels(expanded_df.index, rotation=45)
    plt.tight_layout()
    plt.show()   


    print(expanded_df)

    expanded_df["Param Size"] = model_metrics_df["Param Size"]
    plt.plot(model_metrics_df["Param Size"], expanded_df["All Mean"])
    plt.plot(model_metrics_df["Param Size"], expanded_df["Advanced Math"])
    plt.plot(model_metrics_df["Param Size"], expanded_df["Algebra"])
    plt.plot(model_metrics_df["Param Size"], expanded_df["Geometry and Trigonometry"])
    plt.plot(model_metrics_df["Param Size"], expanded_df["Problem-Solving and Data Analysis"])
    plt.show()



