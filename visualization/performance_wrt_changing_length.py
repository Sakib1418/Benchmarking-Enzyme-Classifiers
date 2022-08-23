#!/usr/bin/env python

import numpy as np
import pandas as pd
from utils import count_ranges
import matplotlib.pyplot as plt

ranges = list(np.linspace(0,1000,21))
ranges.append(int(100000))


total_match = pd.read_csv('vis_results/total_match.csv', sep = ',')
third_digit_correct = pd.read_csv('vis_results/correct_to_third_digit.csv', sep = ',')
second_digit_correct = pd.read_csv('vis_results/correct_to_second_digit.csv', sep = ',')
first_digit_correct = pd.read_csv('vis_results/correct_to_first_digit.csv', sep = ',')
first_digit_wrong = pd.read_csv('vis_results/first_digit_wrong.csv', sep = ',')
no_prediction = pd.read_csv('vis_results/no_prediction.csv', sep = ',')

dataframes = [total_match,
              third_digit_correct,
             second_digit_correct,
             first_digit_correct,
             first_digit_wrong,
              no_prediction]

list_ranges = []
for i in dataframes:
    list_ranges.append(count_ranges(i,ranges))

# print(list_ranges)

r = [i for i in range(len(ranges)-1)]

# plot
barWidth = 1
# names = [0,100,200,300,400,500,600,700,800,900,1000,100000]
names = [(str(ranges[i])+'-'+str(ranges[i+1])) for i in range(len(ranges)-1)]

raw_data = {'c': list(list_ranges[0]),
            'd': list(list_ranges[1]), 
            'e': list(list_ranges[2]),
            'f': list(list_ranges[3]),
            'g': list(list_ranges[4]),
            'h': list(list_ranges[5])}

df = pd.DataFrame(raw_data)
 
# From raw value to percentage
totals = [i+j+k+l+m+n for i,j,k,l,m,n in zip(df['c'],df['d'], df['e'], df['f'], df['g'], df['h'])]

greenBars = [i / j * 100 for i,j in zip(df['h'], totals)]
orangeBars = [i / j * 100 for i,j in zip(df['g'], totals)]
blueBars = [i / j * 100 for i,j in zip(df['f'], totals)]
redBars = [i / j * 100 for i,j in zip(df['e'], totals)]
red1Bars = [i / j * 100 for i,j in zip(df['d'], totals)]
red2Bars = [i / j * 100 for i,j in zip(df['c'], totals)]

color = ['#016262','#279292','#06C1C1','#66FFFF','#FFCC99','#ff7f50']
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


legends = ['Total match','Third digit', 'Second digit', 'First digit', 'Wrong prediction', 'No prediction']
legends = legends[::-1]
plt.ylim(0,100)
# Custom x axis
plt.xticks(r, names, rotation = 90)
# plt.yticks(ticks = None, labels = None)
plt.legend(legends, bbox_to_anchor=(1.5,1.5), ncol=1,loc='upper right')
# Show graphic
# plt.tick_params(axis='x', which='both', bottom=True,top=False, labelbottom= True)
# plt.xticks(r, names, rotation = 90)
plt.ylabel('Percentage of the Total')
plt.tight_layout()
plt.xlabel('bin edges')
plt.savefig('vis_results/performance_wrt_length.png', format='png', dpi=200)
plt.show()
