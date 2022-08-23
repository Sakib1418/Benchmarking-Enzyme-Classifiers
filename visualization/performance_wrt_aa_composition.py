#!/usr/bin/env python

import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
from utils import frac_of_aa
from utils import plot_aa

# plt.rcParams['figure.dpi'] = 100
# plt.rcParams["figure.figsize"] = [15.0, 6.0]
# %config InlineBackend.figure_format = 'svg'
# %matplotlib inline

df_EC = pd.read_csv('vis_results/df_EC.csv', sep = ',')
total_match = pd.read_csv('vis_results/total_match.csv', sep = ',')
third_digit_correct = pd.read_csv('vis_results/correct_to_third_digit.csv', sep = ',')
second_digit_correct = pd.read_csv('vis_results/correct_to_second_digit.csv', sep = ',')
first_digit_correct = pd.read_csv('vis_results/correct_to_first_digit.csv', sep = ',')
first_digit_wrong = pd.read_csv('vis_results/first_digit_wrong.csv', sep = ',')
no_prediction = pd.read_csv('vis_results/no_prediction.csv', sep = ',')


list_aa = 'ARNDCQEGHILKMFPSTWYV'
a = 0

if os.path.exists('vis_results/percent_aa.csv'):
    percent_aa = pd.read_csv('vis_results/percent_aa.csv', sep = ',')
else:
    for i in list_aa:
        percent_aa = frac_of_aa(df_EC,str(i))
        print(f"number of aa done: {a}")
        a+=1
    percent_aa.to_csv('vis_results/percent_aa.csv')
    
    
dataframes = [total_match,
              third_digit_correct,
             second_digit_correct,
             first_digit_correct,
             first_digit_wrong,
              no_prediction]


list_aa = 'ARNDCQEGHILKMFPSTWYV'
list_aa = list(list_aa)

# len(list_aa)
plot_aa(dataframes,percent_aa,list_aa)