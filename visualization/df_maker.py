#!/usr/bin/env python
# coding: utf-8


from collections import Counter
import os 
import shutil
from utils import EC_separator
import pandas as pd


if os.path.exists('vis_results/'):
    print('previous vis result found')
    shutil.rmtree('vis_results/')
    print('vis_results deleted')
else:
    print('vis_results not found, will be created')


os.mkdir('vis_results/')
print('vis_results created')




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
df_EC.to_csv('vis_results/df_EC.csv')

print('total database created')

enz= df_EC[df_EC['EC number'].isnull() == False]
enz.to_csv('vis_results/enzymes.csv')

nonenz= df_EC[df_EC['EC number'].isnull()]
nonenz.to_csv('vis_results/non-enzymes.csv')

print('enzyme and non enzyme dataframes created')

total_match = df_EC[df_EC['EC_Predicted']== df_EC['EC number']]
total_match.to_csv('vis_results/total_match.csv')

print('total match database created.')

no_prediction = df_EC[df_EC['EC_Predicted'] == 'no Prediction']
no_prediction.to_csv('vis_results/no_prediction.csv')

no_prediction_but_E = no_prediction[no_prediction['EC number'].notnull()]
no_prediction_but_E.to_csv('vis_results/no_prediction_but_enzyme.csv')

non_enzyme_correct = df_EC[(df_EC['EC_Predicted'] == 'non Enzyme') & (df_EC['EC number'].isnull())]
non_enzyme_correct.to_csv('vis_results/non_enzyme_correct.csv')

PNEBE = df_EC[(df_EC['EC_Predicted'] == 'non Enzyme') & (df_EC['EC number'].isnull() == False)]
PNEBE.to_csv('vis_results/predicted_non_enzyme_but_enzyme.csv')

print('no prediction, \nno prediction but enzyme, \nnon enzyme correct, \npredicted not enzyme but enzyme are created')

a = ((df_EC['EC_Predicted'] == 'no Prediction') == False)
b = ((df_EC['EC_Predicted'] == 'non Enzyme') == False)
c = (df_EC['EC number'].isnull())

PEBnonE = df_EC[a&b&c]
PEBnonE.to_csv('vis_results/predicted_enzyme_but_non_enzyme')

print('predicted enzyme but non enzyme are created')

new_digit = df_EC.copy()

new_digit = new_digit[(new_digit['EC number'].isnull() == False)]
new_digit = new_digit[(new_digit['EC_Predicted'] == 'no Prediction') == False]
new_digit = new_digit[(new_digit['EC_Predicted'] == 'non Enzyme') == False]
new_digit = new_digit[(new_digit['EC_Predicted'] == new_digit['EC number']) == False]

print('digit database created')

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

print('all dataframes created successfully.')