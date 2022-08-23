#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
from utils import EC_list
import numpy as np

plt.rcParams['figure.dpi'] = 100
plt.rcParams["figure.figsize"] = [15.0, 6.0]
# %config InlineBackend.figure_format = 'svg'
# %matplotlib inline

total_match = pd.read_csv('vis_results/total_match.csv', sep = ',')
third_digit_correct = pd.read_csv('vis_results/correct_to_third_digit.csv', sep = ',')
second_digit_correct = pd.read_csv('vis_results/correct_to_second_digit.csv', sep = ',')
first_digit_correct = pd.read_csv('vis_results/correct_to_first_digit.csv', sep = ',')
first_digit_wrong = pd.read_csv('vis_results/first_digit_wrong.csv', sep = ',')
no_prediction_but_E = pd.read_csv('vis_results/no_prediction_but_enzyme.csv', sep = ',')



dataframes = [total_match,
              third_digit_correct,
             second_digit_correct,
             first_digit_correct,
             first_digit_wrong,
              no_prediction_but_E]





list_EC = EC_list(dataframes)


r = [0,1,2,3,4,5]

# plot
barWidth = 1
names = ('EC1','EC2','EC3','EC4','EC5','EC6')

# Data
r = [0,1,2,3,4,5]
raw_data = {'c': list_EC[5],
            'd': list_EC[4],
            'e': list_EC[3],
            'f': list_EC[2],
            'g': list_EC[1],
            'h': list_EC[0]}
df = pd.DataFrame(raw_data)

 
# From raw value to percentage
totals = [i+j+k+l+m+n for i,j,k,l,m,n in zip(df['c'],df['d'], df['e'], df['f'],df['g'],df['h'])]


greenBars = [i / j * 100 for i,j in zip(df['c'], totals)]
orangeBars = [i / j * 100 for i,j in zip(df['d'], totals)]
blueBars = [i / j * 100 for i,j in zip(df['e'], totals)]
redBars = [i / j * 100 for i,j in zip(df['f'], totals)]
red1Bars = [i / j * 100 for i,j in zip(df['g'], totals)]
red2Bars = [i / j * 100 for i,j in zip(df['h'], totals)]


color = ['#016262','#279292','#06C1C1','#66FFFF','#FFCC99','#FF0000']
# Create green Bars
plt.bar(r, greenBars, color=color[-1], edgecolor='white', width=barWidth)
# Create orange Bars
plt.bar(r, orangeBars, bottom=greenBars, color=color[-2], edgecolor='white', width=barWidth)
# Create blue Bars
plt.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color=color[-3], edgecolor='white', width=barWidth)
# Create blue Bars
plt.bar(r, redBars, bottom=[i+j+k for i,j,k in zip(greenBars, orangeBars,blueBars)], color= color[-4], edgecolor='white', width=barWidth)
#
plt.bar(r, red1Bars, bottom=[i+j+k+l for i,j,k,l in zip(greenBars, orangeBars, blueBars, redBars)], color=color[-5], edgecolor='white', width=barWidth)
# Create blue Bars
plt.bar(r, red2Bars, bottom=[i+j+k+l+m for i,j,k,l,m in zip(greenBars, orangeBars,blueBars,redBars,red1Bars)], color=color[-6], edgecolor='white', width=barWidth)




legends = ['Total match', 'Third digit', 'Second digit', 'First digit', 'Wrong prediction', 'No prediction but Enzyme']
legends = legends[::-1]
# Custom x axis
plt.ylim(0,110)
# plt.yticks(color='w')
plt.xticks(r, names)
plt.ylabel('Percentage of the total')
plt.xlabel('\nEC classes')
# plt.tick_params(axis='x', which='both', bottom=False,top=False, labelbottom= False)
# plt.tick_params(axis='y', which='both', bottom=False,top=False, labelbottom= False)
# plt.legend(legends, bbox_to_anchor=(1.5,1.5), ncol=1,loc='upper right')
# Show graphic
plt.savefig('vis_results/Performance_on_EC_number.png', format='png', dpi=800)
plt.show()