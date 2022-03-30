#!/usr/bin/env python
# coding: utf-8



#all imports (initially required)

import os
import shutil
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rc

if os.path.exists('vis_results/'):
    print('previous vis result found')
    shutil.rmtree('vis_results/')
    print('vis_results deleted')
else:
    print('vis_results not found, will be created')


os.mkdir('vis_results/')
print('vis_results created')



#figure parameter set up 
plt.rcParams['figure.dpi'] = 800
plt.rcParams["figure.figsize"] = [15.0, 6.0]
# get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg'")
# get_ipython().run_line_magic('matplotlib', 'inline')




#total uniprot reveiwed sequences
df_uniprot = pd.read_csv('uniprot-reviewed_04_12.tab', sep = '\t')
print('uniprt database loaded')
print('length of Uniprot datasize: ', len(df_uniprot))




#total results
df_result = pd.read_csv('ECPred_result_15_12.csv',sep = '\t', low_memory=False)
df_result = df_result[['Entry','EC_Predicted']]
print('length of result datasize: ', len(df_result))

df = pd.merge(df_uniprot,df_result, on = ['Entry'], how = 'left')


df = df[df['EC_Predicted'].notnull()]

df_EC = df[['Entry','EC number','EC_Predicted','Length','Sequence']]


total_match = df_EC[df_EC['EC_Predicted']== df_EC['EC number']]
total_match.to_csv('vis_results/total_match.csv')




no_prediction = df_EC[df_EC['EC_Predicted'] == 'no Prediction']
no_prediction.to_csv('vis_results/no_prediction.csv')




no_prediction_but_E = no_prediction[no_prediction['EC number'].notnull()]
no_prediction_but_E.to_csv('vis_results/no_prediction_but_enzyme.csv')




non_enzyme_correct = df_EC[(df_EC['EC_Predicted'] == 'non Enzyme') & (df_EC['EC number'].isnull())]
non_enzyme_correct.to_csv('vis_results/non_enzyme_correct.csv')




PNEBE = df_EC[(df_EC['EC_Predicted'] == 'non Enzyme') & (df_EC['EC number'].isnull() == False)]
PNEBE.to_csv('vis_results/predicted_non_enzyme_but_enzyme.csv')




a = ((df_EC['EC_Predicted'] == 'no Prediction') == False)
b = ((df_EC['EC_Predicted'] == 'non Enzyme') == False)
c = (df_EC['EC number'].isnull())

PEBnonE = df_EC[a&b&c]
PEBnonE.to_csv('vis_results/predicted_enzyme_but_non_enzyme')




new_digit = df_EC.copy()

new_digit = new_digit[(new_digit['EC number'].isnull() == False)]
new_digit = new_digit[(new_digit['EC_Predicted'] == 'no Prediction') == False]
new_digit = new_digit[(new_digit['EC_Predicted'] == 'non Enzyme') == False]
new_digit = new_digit[(new_digit['EC_Predicted'] == new_digit['EC number']) == False]



def EC_separator(new_digit):
    lst = []
    EC_number = list(new_digit['EC number'])
    EC_predicted = list(new_digit['EC_Predicted'])
    for j in range(len(EC_number)):
        
        kst = []

        for i in EC_number[j].split('; '):
            a = 'first not match'
            if EC_predicted[j].split('.')[0] == i.split('.')[0]:
                a = 'first matched'
                kst.append(a)
                break
            kst.append(a)

        for i in EC_number[j].split('; '):
            b = 'second not match'
            if EC_predicted[j].split('.')[1] == '-' :
                b = 'second blank'
                kst.append(b)
                break
            elif EC_predicted[j].split('.')[1] == i.split('.')[1]:
                b = 'second matched'
                kst.append(b)
                break
            kst.append(b)

        for i in EC_number[j].split('; '):
            c = 'third not matched'
            if EC_predicted[j].split('.')[2] == '-' :
                c = 'third blank'
                kst.append(c)
                break
            elif EC_predicted[j].split('.')[2] == i.split('.')[2]:
                c = 'third matched'
                kst.append(c)
                break
            kst.append(c)
                
        for i in EC_number[j].split('; '):
            d = 'fourth not match'
            if EC_predicted[j].split('.')[3] == '-' :
                d = 'fourth blank'
                kst.append(d)
                break
            elif EC_predicted[j].split('.')[3] == i.split('.')[3]:
                d = 'fourth matched'
                kst.append(d)
                break
            kst.append(d)

        lst.append(kst)
    
    return lst




lst = EC_separator(new_digit)

for i in range(4):
    new_digit['match'+str(i+1)] = [j[i] for j in lst]




a = new_digit['match1'] == 'first matched'
b = new_digit['match2'] == 'second matched'
c = new_digit['match3'] == 'third matched'
d = new_digit['match4'] == 'fourth matched'

total_correct = new_digit[a & b & c & d]
total_correct.to_csv('vis_results/correct_to_fourth_digit.csv')




third_digit_correct = new_digit[a & b & c & (d == False)]
third_digit_correct.to_csv('vis_results/correct_to_third_digit.csv')




second_digit_correct = new_digit[a & b & (c == False) & (d == False)]
second_digit_correct.to_csv('vis_results/correct_to_second_digit.csv')




first_digit_correct = new_digit[a & (b == False) & (c == False) & (d == False)]
first_digit_correct.to_csv('vis_results/correct_to_first_digit.csv')




first_digit_wrong = new_digit[a == False]
first_digit_wrong.to_csv('vis_results/first_digit_wrong.csv')

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

color = ['#54d157']
# plot bars in stack manner
plt.bar(x, y1, color= 'b')#color[0])
plt.bar(x, y2, bottom=y1, color='c')
plt.bar(x, y3, bottom=y1+y2, color='y')
plt.bar(x, y4, bottom=y1+y2+y3, color= 'g')
plt.bar(x, y5, bottom= y1+y2+y3+y4, color = 'r')#'#ff9500')
# plt.legend(label_list_lengths[::-1], bbox_to_anchor=(1.5,1.5), ncol=5,loc='center')

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
# plt.legend(label_list_digits, bbox_to_anchor=(1.5,1.5), ncol=5,loc='center')
plt.savefig('vis_results/overall_performance.png', format='png', dpi=800)




ranges = list(np.linspace(0,1000,21))
ranges.append(int(100000))
# print('ranges', ranges)


def count_ranges(dataframe): 
    range_ = dataframe.groupby(pd.cut(dataframe.Length, ranges)).count().Length
    range_ = pd.DataFrame(range_)
    range_ = range_.rename(columns={'Length': 'name'})
    range_ = [i for i in range_['name']]
    return range_

dataframes = [total_match,
              third_digit_correct,
             second_digit_correct,
             first_digit_correct,
             first_digit_wrong,
              no_prediction]

list_ranges = []
for i in dataframes:
    list_ranges.append(count_ranges(i))

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
# plt.legend(legends, bbox_to_anchor=(1.5,1.5), ncol=1,loc='upper right')
# Show graphic
# plt.tick_params(axis='x', which='both', bottom=True,top=False, labelbottom= True)
# plt.xticks(r, names, rotation = 90)
plt.ylabel('Percentage of the Total')
plt.xlabel('bin edges')
plt.savefig('vis_results/performance_wrt_length.png', format='png', dpi=800)
plt.show()



dataframes = [total_match,
              third_digit_correct,
             second_digit_correct,
             first_digit_correct,
             first_digit_wrong,
              no_prediction_but_E]

EC_list = []
for dataframe in dataframes:
    EC_list.append([i.split('.')[0] for i in dataframe['EC number']])
    
    
EC = ['1','2','3','4','5','6']
diction = {}
vector = {'c':EC_list[0],'d':EC_list[1],'e':EC_list[2],'f':EC_list[3],'g':EC_list[4],'h':EC_list[5]}

for i in vector:
    for j in range(len(EC)):
        key = i+'EC'+EC[j]
        value = vector[i].count(EC[j])
        diction[key] = value

keys = []
for i in range(len(EC)):
    f = []
    for j in vector:
        key = j+'EC'+EC[i]
        f.append(key)
    keys.append(f)

list_EC = []
for i in range(6):
    a = []
    for j in range(6):
        a.append(diction[keys[i][j]])
    list_EC.append(a)

list_EC = list(np.array(list_EC).T)



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




plt.rcParams["figure.figsize"] = [25.0, 10.0]
plt.rcParams["savefig.bbox"] = 'tight'




# %matplotlib inline
error_dataframe = [no_prediction_but_E,PNEBE,first_digit_wrong]
def error_count(error_dataframe):
    
    error_name = ['no_prediction','PNEBE','first_digit_wrong']
    plt.subplots(1,3)

    for i in range(len(error_dataframe)):
        print(type(i))
        cnt = Counter(error_dataframe[i]['EC number'])
        top = 20
        
        sorted_class = cnt.most_common()[:top]
        classes = [c[0] for c in sorted_class]
        counts = [c[1] for c in sorted_class]
        
        plt.subplot(1,3,i+1)

        plt.bar(range(len(classes)),counts)
        plt.xticks(range(len(classes)), classes, fontsize = 10, rotation = 'vertical')
        plt.title(error_name[i], fontsize = 20)
    plt.savefig('vis_results/top_mistakes.png', format = 'png', dpi = 1000)    
    plt.show()
error_count(error_dataframe)




#figure parameter set up 
plt.rcParams['figure.dpi'] = 800
plt.rcParams["figure.figsize"] = [15.0, 6.0]





def frac_of_aa(dataframe,i):
    dataframe['Frac_Counter_'+str(i)] = dataframe.apply(lambda row: row['Sequence'].count(str(i))/row['Length'], axis = 1)
    return dataframe

list_aa = 'ARNDCQEGHILKMFPSTWYV'

for i in list_aa:
    percent_aa = frac_of_aa(df_EC,str(i))




enz = percent_aa[percent_aa['EC number'].isnull() == False]
nonenz = percent_aa[percent_aa['EC number'].isnull()]




import matplotlib.pyplot as ax

dataframes = [enz,nonenz]

def point_finder(dataframe,amino_acid):

    bins = 30
    list_frac = list(dataframe['Frac_Counter_'+str(amino_acid)])

    zero_out = list(filter(lambda a: a != 0, list_frac))
    zero_out.sort(reverse=False)

    list_points = [-.01]
    for i in [zero_out[len(zero_out)*i//bins] for i in range(1,bins)]:
        list_points.append(i) 
    list_points.append(max(zero_out)+.01)


    return list_points

def number_of_aa(dataframe,i):
    dataframe['Frac_Counter'] = dataframe.apply(lambda row: row['Sequence'].count(str(i))/row['Length'], axis = 1)
    return dataframe

def count_ranges_aa(dataframe, percent_aa, amino_acid):



    aa_range = point_finder(percent_aa, amino_acid)
    range_aa = dataframe.groupby(pd.cut(dataframe.Frac_Counter, aa_range)).count().Frac_Counter
    range_aa = pd.DataFrame(range_aa)
    range_aa = range_aa.rename(columns={'Frac_Counter': 'name'})
    range_aa = [i for i in range_aa['name']]


    return range_aa, aa_range



def plot_aa_enz_non_enz(dataframes, amino_acid_list):
    barWidth = 1
    color = ['#016262','#ff7f50']

    a = 0
    ax.rcParams["figure.figsize"] = [60.0, 15.0]
    ax.subplots(len(amino_acid_list)//5,5)
    point_dict = {}
    for amino_acid in amino_acid_list: 
        a += 1

        for i in dataframes:
            df  = number_of_aa(i, amino_acid)
        aa_list_ranges = []
        
        for i in dataframes:
            
            range_a, ranges = count_ranges_aa(i, percent_aa, amino_acid)
            point_dict[amino_acid] = ranges
            aa_list_ranges.append(range_a)
            

        raw_data = {'d': list(aa_list_ranges[0]), 
                    'e': list(aa_list_ranges[1])}

        df = pd.DataFrame(raw_data)

        # From raw value to percentage
        totals = [i+j for i,j in zip(df['d'], df['e'])]

        greenBars = [i / j * 100 for i,j in zip(df['d'], totals)]
        orangeBars = [i / j * 100 for i,j in zip(df['e'], totals)]


        r = [i for i in range(len(greenBars))]
        
        names = [str(round(ranges[i],3))+'-'+str(round(ranges[i+1],3)) for i in range(len(ranges)-1)]
        
        ax.subplot(len(amino_acid_list)//5,5,a)
        
#         ax.tick_params(axis='x', which='both', bottom=False,top=False, labelbottom=False)
#         ax.tick_params(axis='y', which='both', bottom=False,top=False, labelbottom=False)
        
        ax.bar(r, greenBars, color= color[0], edgecolor='white', width=barWidth)
        ax.bar(r, orangeBars, bottom=greenBars, color=color[1], edgecolor='white', width=barWidth)

        ax.ylim(0,100)
        ax.yticks([])
        ax.ylabel(amino_acid, fontsize = 58, loc= 'center', labelpad = 28, rotation = 0 )
        ax.xticks(r, names, fontsize= 7, rotation = 45)
        
        
    point_dict[amino_acid] = ranges
    point_dict_dataframe = pd.DataFrame(point_dict)
    point_dict_dataframe.to_csv('vis_results/bin_edge_number.csv')
    ax.tight_layout()
    ax.savefig('vis_results/fractional_composition_of_enzyme&non-enzyme.png', format = 'png', dpi = 800)
    ax.show()




list_aa = 'ARNDCQEGHILKMFPSTWYV'
list_aa = list(list_aa)
# len(list_aa)
plot_aa_enz_non_enz(dataframes,list_aa)




import matplotlib.pyplot as ax

dataframes = [total_match,
              third_digit_correct,
             second_digit_correct,
             first_digit_correct,
             first_digit_wrong,
              no_prediction]

def point_finder(dataframe,amino_acid):

    bins = 12
    list_frac = list(dataframe['Frac_Counter_'+str(amino_acid)])

    zero_out = list(filter(lambda a: a != 0, list_frac))
    zero_out.sort(reverse=False)

    list_points = [-.01]
    for i in [zero_out[len(zero_out)*i//bins] for i in range(1,bins)]:
        list_points.append(i) 
    list_points.append(max(zero_out)+.01)


    return list_points

def number_of_aa(dataframe,i):
    dataframe['Frac_Counter'] = dataframe.apply(lambda row: row['Sequence'].count(str(i))/row['Length'], axis = 1)
    return dataframe

def count_ranges_aa(dataframe, percent_aa, amino_acid):



    aa_range = point_finder(percent_aa, amino_acid)
    range_aa = dataframe.groupby(pd.cut(dataframe.Frac_Counter, aa_range)).count().Frac_Counter
    range_aa = pd.DataFrame(range_aa)
    range_aa = range_aa.rename(columns={'Frac_Counter': 'name'})
    range_aa = [i for i in range_aa['name']]


    return range_aa, aa_range



def plot_aa(dataframes, amino_acid_list):
    barWidth = 1
    color = ['#016262','#279292','#06C1C1','#66FFFF','#FFCC99','#ff7f50']

    a = 0
    ax.rcParams["figure.figsize"] = [20.0, 15.0]
    ax.subplots(len(amino_acid_list)//5,5)
    point_dict = {}
    for amino_acid in amino_acid_list: 
        a += 1
        for i in dataframes:
            df  = number_of_aa(i, amino_acid)
        aa_list_ranges = []
        
        for i in dataframes:
            
            range_a, ranges = count_ranges_aa(i, percent_aa, amino_acid)
            point_dict[amino_acid] = ranges
            aa_list_ranges.append(range_a)
            

        raw_data = {'d': list(aa_list_ranges[0]), 
                    'e': list(aa_list_ranges[1]),
                    'f': list(aa_list_ranges[2]),
                    'g': list(aa_list_ranges[3]),
                    'h': list(aa_list_ranges[4]),
                    'i': list(aa_list_ranges[5])}

        df = pd.DataFrame(raw_data)

        # From raw value to percentage
        totals = [i+j+k+l+m+n for i,j,k,l,m,n in zip(df['d'], df['e'], df['f'], df['g'], df['h'],df['i'])]

        greenBars = [i / j * 100 for i,j in zip(df['d'], totals)]
        orangeBars = [i / j * 100 for i,j in zip(df['e'], totals)]
        blueBars = [i / j * 100 for i,j in zip(df['f'], totals)]
        red1 = [i / j * 100 for i,j in zip(df['g'], totals)]
        red2 = [i / j * 100 for i,j in zip(df['h'], totals)]
        red3 = [i / j * 100 for i,j in zip(df['i'], totals)]

        r = [i for i in range(len(greenBars))]
        
        names = [str(round(ranges[i],3))+'-'+str(round(ranges[i+1],3)) for i in range(len(ranges)-1)]
        
        ax.subplot(len(amino_acid_list)//5,5,a)
        
        ax.tick_params(axis='x', which='both', bottom=False,top=False, labelbottom=False)
        ax.tick_params(axis='y', which='both', bottom=False,top=False, labelbottom=False)
        
        ax.bar(r, greenBars, color= color[0], edgecolor='white', width=barWidth)
        ax.bar(r, orangeBars, bottom=greenBars, color=color[1], edgecolor='white', width=barWidth)
        ax.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color=color[2], edgecolor='white', width=barWidth)
        ax.bar(r, red1, bottom=[i+j+k for i,j,k in zip(greenBars, orangeBars,blueBars)], color=color[3], edgecolor='white', width=barWidth)
        ax.bar(r, red2, bottom=[i+j+k+l for i,j,k,l in zip(greenBars, orangeBars, blueBars, red1)], color=color[4], edgecolor='white', width=barWidth)
        ax.bar(r, red3, bottom=[i+j+k+l+m for i,j,k,l,m in zip(greenBars, orangeBars, blueBars, red1,red2)], color=color[5], edgecolor='white', width=barWidth)
        ax.ylim(50,100)
        ax.yticks(r, names)
        ax.ylabel(amino_acid, fontsize = 58, loc= 'center', labelpad = 28, rotation = 0 )
#         ax.xticks(r, names, fontsize= 70, rotation = 45)
        

    ax.tight_layout()
    ax.savefig('vis_results/performance_wrt_amino_acid_comp.png', format = 'png', dpi = 800)
    ax.show()




##main plot for aa
list_aa = 'ARNDCQEGHILKMFPSTWYV'
list_aa = list(list_aa)
# len(list_aa)
plot_aa(dataframes,list_aa)




enz_percent_aa = percent_aa[percent_aa['EC number'].isnull() == False]
nonenz_percent_aa = percent_aa[percent_aa['EC number'].isnull()]




import matplotlib.pyplot as plt
import seaborn as sns

plt.subplots(len(list_aa)//5,5)

list_aa = 'ARNDCQEGHILKMFPSTWYV'
plt.rcParams["figure.figsize"] = [20,15]
a = 0
for i in list_aa:
    a += 1
    plt.subplot(len(list_aa)//5,5,a)
    name = 'Frac_Counter_' + i
    list_1 = enz_percent_aa[name]
    list_2 = nonenz_percent_aa[name]
    sns.kdeplot(list_1, fill= True, color = 'red')
    sns.kdeplot(list_2, fill = True, color = 'blue')
    plt.xlim(0,.2)
    plt.xlabel('fraction compostion of: '+str(i))
    plt.ylabel(i, fontsize = 58, loc= 'center', labelpad = 28, rotation = 0 )
    plt.legend(['enzyme', 'non-enzyme'])
    plt.tight_layout()
plt.savefig('vis_results/gaussian_distribution_amino_acid.png', format = 'png', dpi = 800)
plt.show()



ranges = list(np.linspace(0,1000,21))
ranges.append(int(100000))
# print('ranges', ranges)
#figure parameter set up 
plt.rcParams['figure.dpi'] = 800
plt.rcParams["figure.figsize"] = [15.0, 6.0]


def count_ranges(dataframe): 
    range_ = dataframe.groupby(pd.cut(dataframe.Length, ranges)).count().Length
    range_ = pd.DataFrame(range_)
    range_ = range_.rename(columns={'Length': 'name'})
    range_ = [i for i in range_['name']]
    return range_

dataframes = [enz,nonenz]

list_ranges = []
for i in dataframes:
    list_ranges.append(count_ranges(i))



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


