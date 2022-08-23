#!/usr/bin/env python

#figure parameter set up
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 100
plt.rcParams["figure.figsize"] = [15.0, 6.0]
# %config InlineBackend.figure_format = 'svg'
# %matplotlib inline

import pandas as pd

total_match = pd.read_csv('vis_results/total_match.csv', sep = ',')

no_prediction = pd.read_csv('vis_results/no_prediction.csv', sep = ',')

no_prediction_but_E = pd.read_csv('vis_results/no_prediction_but_enzyme.csv', sep = ',')


non_enzyme_correct = pd.read_csv('vis_results/non_enzyme_correct.csv', sep = ',')

PNEBE = pd.read_csv('vis_results/predicted_non_enzyme_but_enzyme.csv', sep = ',')


PEBnonE = pd.read_csv('vis_results/predicted_enzyme_but_non_enzyme', sep = ',')

total_correct = pd.read_csv('vis_results/correct_to_fourth_digit.csv', sep = ',')


third_digit_correct = pd.read_csv('vis_results/correct_to_third_digit.csv', sep = ',')


second_digit_correct = pd.read_csv('vis_results/correct_to_second_digit.csv', sep = ',')


first_digit_correct = pd.read_csv('vis_results/correct_to_first_digit.csv', sep = ',')

first_digit_wrong = pd.read_csv('vis_results/first_digit_wrong.csv', sep = ',')

df_EC = pd.read_csv('vis_results/df_EC.csv', sep = ',')

import matplotlib.pyplot as plt



dataframes = [no_prediction,
              PNEBE,
              PEBnonE,
              non_enzyme_correct,
              total_match,
              third_digit_correct,
             second_digit_correct,
             first_digit_correct,
             first_digit_wrong]



lengths = [len(i) for i in dataframes[0:4]]
digits = [len(i) for i in dataframes[4:]]
lengths.append(sum(digits))

percent_lengths = [i/sum(lengths) for i in lengths]

percent_digits = [i/sum(digits) for i in digits]

barwidth = 1


# create data
x = ['ECpred \noverall \nperformance']


label_list_lengths  = ['No Prediction',
                       'Predicted Non-Enzyme but Enzyme',
                       'Predicted Enzyme but non-Enzyme',
                       'Non Enzyme Correct',
                       'Predicted EC number'] 


y1 = percent_lengths[4]
y2 = percent_lengths[3]
y3 = percent_lengths[2]
y4 = percent_lengths[1]
y5 = percent_lengths[0]

color = ['b','c','y','g','r']
# plot bars in stack manner
plt.bar(x, y1, color= 'b')#color[0])
plt.bar(x, y2, bottom=y1, color='c')
plt.bar(x, y3, bottom=y1+y2, color='y')
plt.bar(x, y4, bottom=y1+y2+y3, color= 'g')
plt.bar(x, y5, bottom= y1+y2+y3+y4, color = 'r')#'#ff9500')
plt.legend(label_list_lengths[::-1], bbox_to_anchor=(1.5,1.5), ncol=5,loc='center')

# create data
x = ['ECpred \ndigits']



label_list_digits = ['Total correct',
                    'third digit correct',
                    'second digit correct',
                    'first digit correct',
                    'first digit wrong']


y1 = percent_digits[0]
y2 = percent_digits[1]
y3 = percent_digits[2]
y4 = percent_digits[3]
y5 = percent_digits[4]
  
# plot bars in stack manner
colors = ['#377697','#4fa9d9','#72bae0','#a7d4ec','#fdab91']
plt.rcParams["figure.figsize"] = [5,5]
plt.bar(x, y1, color= colors[0])#, width = barwidth)
plt.bar(x, y2, bottom=y1, color = colors[1])#, width = barwidth), width = barwidth)
plt.bar(x, y3, bottom=y1+y2,color = colors[2])#, width = barwidth), width = barwidth)
plt.bar(x, y4, bottom=y1+y2+y3, color = colors[3])#, width = barwidth), width = barwidth)
plt.bar(x, y5, bottom= y1+y2+y3+y4, color = colors[4])#, width = barwidth), width = barwidth)



plt.ylabel("Fraction of the Whole")
plt.legend(label_list_digits, bbox_to_anchor=(1.5,1.5), ncol=5,loc='center')

plt.savefig('vis_results/overall_performance.png', format='png', dpi=800)

print('all done')