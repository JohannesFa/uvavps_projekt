import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def percentage_correct(filename: str):
    df = pd.read_csv(filename)
