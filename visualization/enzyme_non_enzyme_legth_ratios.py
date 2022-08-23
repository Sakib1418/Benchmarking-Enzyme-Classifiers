#!/usr/bin/env python
import pandas as pd 
from utils import count_ranges
import numpy as np
import matplotlib.pyplot as plt

enz= pd.read_csv('vis_results/enzymes.csv')
nonenz= pd.read_csv('vis_results/non-enzymes.csv')


ranges = list(np.linspace(0,1000,21))
ranges.append(int(100000))
print('ranges', ranges)

#figure parameter set up 
# plt.rcParams['figure.dpi'] = 800
# plt.rcParams["figure.figsize"] = [15.0, 6.0]


dataframes = [enz,nonenz]

list_ranges = []
for i in dataframes:
    list_ranges.append(count_ranges(i, ranges))



r = [i for i in range(len(ranges)-1)]

# plot
barWidth = 1
# names = [0,100,200,300,400,500,600,700,800,900,1000,100000]
names = [(str(ranges[i])+'-'+str(ranges[i+1])) for i in range(len(ranges)-1)]

raw_data = {'c': list(list_ranges[0]),
            'd': list(list_ranges[1])}

df = pd.DataFrame(raw_data)
 
# From raw value to percentage
totals = [i+j for i,j in zip(df['c'],df['d'])]


red1Bars = [i / j * 100 for i,j in zip(df['d'], totals)]
red2Bars = [i / j * 100 for i,j in zip(df['c'], totals)]



color = ['#016262','#ff7f50']
# Create green Bars
plt.bar(r, red1Bars, color=color[-1], edgecolor='white', width=barWidth)
# Create orange Bars
plt.bar(r, red2Bars, bottom=red1Bars, color=color[-2], edgecolor='white', width=barWidth)
# Create blue Bars

plt.xlabel('Bin range')
plt.ylabel('Percentage')
plt.xticks(r, names, rotation = 90)
# legends = ['Total match','Third digit', 'Second digit', 'First digit', 'Wrong prediction', 'No prediction']
# legends = legends[::-1]
plt.legend(['enzymes', 'non-enzymes'],)
plt.ylim(0,100)
# plt.tick_params(axis='x', which='both', bottom=True,top=False, labelbottom= True)
# plt.tick_params(axis='y', which='both', bottom=True,top=False, labelbottom= True)
plt.savefig('vis_results/effect_of_length_on_enzymatic_reaction.png', format='png', dpi=500)
plt.show()