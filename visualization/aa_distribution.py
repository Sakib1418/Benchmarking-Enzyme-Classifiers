#!/usr/bin/env python
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
from utils import gaussian_aa
from utils import frac_of_aa

list_aa = 'ARNDCQEGHILKMFPSTWYV'
a = 0

df_EC = pd.read_csv('vis_results/df_EC.csv', sep = ',')

if os.path.exists('vis_results/percent_aa.csv'):
    percent_aa = pd.read_csv('vis_results/percent_aa.csv', sep = ',')
else:
    for i in list_aa:
        percent_aa = frac_of_aa(df_EC,str(i))
        print(f"number of aa done: {a}")
        a+=1
    percent_aa.to_csv('vis_results/percent_aa.csv')


enz_percent_aa = percent_aa[percent_aa['EC number'].isnull() == False]
nonenz_percent_aa = percent_aa[percent_aa['EC number'].isnull()]


gaussian_aa(enz_percent_aa,nonenz_percent_aa)