import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def total_percentage_correct(filename: str):
    df = pd.read_csv(filename, sep=";")
    df['Model_correct'] = df['Model_correct'].astype(int)
    return df['Model_correct'].mean() * 100



def percentage_correct(filename: str):
    df = pd.read_csv(filename)

def percentage_each_domain(filename: str):
    df = pd.read_csv(filename)
    df.groupby("Domain")[df["Model_correct"] == True]
