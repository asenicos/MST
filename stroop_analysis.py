# -*- coding: utf-8 -*-
"""
@author: asenic
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import ttest_ind


#read Stroop test results
exp='stroop16inv.csv'
exp='stroop17normen.csv'
exp='stroop21inv.csv'
path='d:\\my_scripts\\py\\stroopy-master\\Data\\'
os.chdir(path)
data=pd.read_csv(exp, sep=";")
ncongr=data.query('Accuracy == 0 and congruent == 0 and Response != "down"')['RT']
congr=data.query('Accuracy == 0 and congruent == 1 and Response != "down"')['RT']
ncongr=ncongr.reset_index(drop=True)
congr=congr.reset_index(drop=True)
adata=data.query('Accuracy == 0 and Response != "down"')#adata=accurate responses only

nacc=data.query('Accuracy == 1 and congruent == 0 and Response != "down"')['RT']
cacc=data.query('Accuracy == 1 and congruent == 1 and Response != "down"')['RT']
print('Accuracy for congruent: ',round(len(congr)/(len(cacc)+len(congr))*100,2), '%')
print('Accuracy for noncongruent: ',round(len(ncongr)/(len(nacc)+len(ncongr))*100,2), '%')

#boxplot with scatter
sns.boxplot(x = adata['congruent'], y = adata['RT'], hue = adata['congruent'], gap=0.2)    
for i in [0,1]:
    y = adata.RT[adata.congruent==i].dropna()
    x = np.random.normal(i, 0.04, size=len(y))
    plt.plot(x, y, 'k.', alpha=0.5)

#statistics
medians = data.groupby(['congruent', 'Accuracy'])['RT'].median()
sems = data.groupby(['congruent', 'Accuracy'])['RT'].sem()
print('Size of Stroop effect is', round((medians[0,1]-medians[1,1])*1000,3), '+/-', round((sems[0,1]-sems[1,1])*1000,3), 'ms.')
print('Size of Stroop effect is', round((medians[0,0]-medians[1,0])*1000,3), '+/-', round((sems[0,0]-sems[1,0])*1000,3), 'ms.')#inverted
#Size of Stroop effect is 119.591 +/- 1.243 ms
print('Analyzed ', len(data), ' trials, accuracy is ', round(len(data[data['Accuracy']==1])/len(data)*100,1), '%.')
#Analyzed  144  trials, accuracy is  95.8 %.
t_statistic, p_value = ttest_ind(ncongr[np.isfinite(ncongr)], congr[np.isfinite(congr)])
# Output the results
print("t-statistic",round(t_statistic,3))
print("p-value:", round(p_value,10))
#t-statistic 3.076
#p-value: 0.003

#by colors 
#colors =  ['green','magenta','black', 'orange','white','skyblue','yellow','red','cyan', 'brown','blue']
colors =  sorted(pd.unique(pd.Series(data.colour)))
adata=adata.sort_values('colour')
sns.boxplot(x = adata['congruent'], y = adata['RT'], hue = adata['colour'],palette = colors).legend_.remove()

#by colors grouped
sns.set_context("paper", font_scale=0.8)
sns.boxplot(x = adata['colour'], y = adata['RT'], hue = adata['congruent'], gap=0.2)

# data[(data['congruent']==0) & (data['Accuracy']==1)]
# data[data['Accuracy']==1]['congruent']==0
# data[data['Accuracy']==1][['congruent']==0]['RT']
# ncongr=data.query('Accuracy == 1 and congruent == 0')['RT']
# congr=data.query('Accuracy == 0 and congruent == 1')['RT']


