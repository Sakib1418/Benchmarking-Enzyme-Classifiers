#!/usr/bin/env python



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


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
    
    
def EC_list(dataframes):
    import numpy as np
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
    return list_EC

def count_ranges(dataframe, ranges):
    range_ = dataframe.groupby(pd.cut(dataframe.Length, ranges)).count().Length
    range_ = pd.DataFrame(range_)
    range_ = range_.rename(columns={'Length': 'name'})
    range_ = [i for i in range_['name']]
    return range_

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



def plot_aa_enz_non_enz(dataframes, percent_aa, amino_acid_list):
    barWidth = 1
    color = ['#016262','#ff7f50']
    import matplotlib.pyplot as ax

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
    
import matplotlib.pyplot as ax
def frac_of_aa(dataframe,i):
    dataframe['Frac_Counter_'+str(i)] = dataframe.apply(lambda row: row['Sequence'].count(str(i))/row['Length'], axis = 1)

    return dataframe

def plot_aa(dataframes, percent_aa, amino_acid_list):
    barWidth = 1
    color = ['#016262','#279292','#06C1C1','#66FFFF','#FFCC99','#ff7f50']

    a = 0
#     ax.rcParams["figure.figsize"] = [20.0, 15.0]
#     ax.subplots(len(amino_acid_list)//5,5)
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
        plt.subplot(len(amino_acid_list)//5,5,a)
        
        plt.tick_params(axis='x', which='both', bottom=False,top=False, labelbottom=False)
        plt.tick_params(axis='y', which='both', bottom=False,top=False, labelbottom=False)
        
        plt.bar(r, greenBars, color= color[0], edgecolor='white', width=barWidth)
        plt.bar(r, orangeBars, bottom=greenBars, color=color[1], edgecolor='white', width=barWidth)
        plt.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color=color[2], edgecolor='white', width=barWidth)
        plt.bar(r, red1, bottom=[i+j+k for i,j,k in zip(greenBars, orangeBars,blueBars)], color=color[3], edgecolor='white', width=barWidth)
        plt.bar(r, red2, bottom=[i+j+k+l for i,j,k,l in zip(greenBars, orangeBars, blueBars, red1)], color=color[4], edgecolor='white', width=barWidth)
        plt.bar(r, red3, bottom=[i+j+k+l+m for i,j,k,l,m in zip(greenBars, orangeBars, blueBars, red1,red2)], color=color[5], edgecolor='white', width=barWidth)
        plt.ylim(50,100)
        plt.yticks(r, names)
#         ax.ylabel(amino_acid, fontsize = 58, loc= 'center', labelpad = 28, rotation = 0 )
#         ax.xticks(r, names, fontsize= 70, rotation = 45)
        

    plt.tight_layout()
    plt.savefig('vis_results/performance_wrt_amino_acid_comp.png', format = 'png', dpi = 100)
    plt.show()        
#         ax.subplot(len(amino_acid_list)//5,5,a)
        
#         ax.tick_params(axis='x', which='both', bottom=False,top=False, labelbottom=False)
#         ax.tick_params(axis='y', which='both', bottom=False,top=False, labelbottom=False)
        
#         ax.bar(r, greenBars, color= color[0], edgecolor='white', width=barWidth)
#         ax.bar(r, orangeBars, bottom=greenBars, color=color[1], edgecolor='white', width=barWidth)
#         ax.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color=color[2], edgecolor='white', width=barWidth)
#         ax.bar(r, red1, bottom=[i+j+k for i,j,k in zip(greenBars, orangeBars,blueBars)], color=color[3], edgecolor='white', width=barWidth)
#         ax.bar(r, red2, bottom=[i+j+k+l for i,j,k,l in zip(greenBars, orangeBars, blueBars, red1)], color=color[4], edgecolor='white', width=barWidth)
#         ax.bar(r, red3, bottom=[i+j+k+l+m for i,j,k,l,m in zip(greenBars, orangeBars, blueBars, red1,red2)], color=color[5], edgecolor='white', width=barWidth)
#         ax.ylim(50,100)
#         ax.yticks(r, names)
# #         ax.ylabel(amino_acid, fontsize = 58, loc= 'center', labelpad = 28, rotation = 0 )
# #         ax.xticks(r, names, fontsize= 70, rotation = 45)
        

#     ax.tight_layout()
#     ax.savefig('vis_results/performance_wrt_amino_acid_comp.png', format = 'png', dpi = 100)
#     ax.show()
    
    
    
import seaborn as sns 
import matplotlib.pyplot as plt

def gaussian_aa(enz_percent_aa, nonenz_percent_aa):
    import seaborn as sns 
    import matplotlib.pyplot as plt
    
    list_aa = 'ARNDCQEGHILKMFPSTWYV'
    plt.rcParams["figure.figsize"] = [20,15]
    plt.subplots(len(list_aa)//5,5)
    a = 0
    for i in list_aa:
        a += 1
        plt.subplot(len(list_aa)//5,5,a)
        name = 'Frac_Counter_' + i
        list_1 = enz_percent_aa[name]
        list_2 = nonenz_percent_aa[name]
        sns.kdeplot(list_1,color = 'red')
        sns.kdeplot(list_2,color = 'blue')
        plt.xlim(0,.2)
        plt.xlabel('fraction compostion of: '+str(i))
        plt.ylabel(i, fontsize = 58, loc= 'center', labelpad = 28, rotation = 0 )
        plt.legend(['enzyme', 'non-enzyme'])
        plt.tight_layout()
    plt.savefig('vis_results/gaussian_distribution_amino_acid.png', format = 'png', dpi = 100)
    plt.show()