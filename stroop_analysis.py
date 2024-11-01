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
exp='stroop.csv'
path='.\\Data\\'
os.chdir(path)
data=pd.read_csv(exp, sep=";")
ncongr=data.query('Accuracy == 1 and congruent == 0')['RT']
congr=data.query('Accuracy == 1 and congruent == 1')['RT']
ncongr=ncongr.reset_index(drop=True)
congr=congr.reset_index(drop=True)
adata=data.query('Accuracy == 1')#adata=accurate responses only

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
#Size of Stroop effect is 119.591 +/- 1.243 ms
print('Analyzed ', len(data), ' trials, accuracy is ', round(len(data[data['Accuracy']==1])/len(data)*100,1), '%.')
#Analyzed  144  trials, accuracy is  95.8 %.
t_statistic, p_value = ttest_ind(ncongr[np.isfinite(ncongr)], congr[np.isfinite(congr)])
# Output the results
print("t-statistic",round(t_statistic,3))
print("p-value:", round(p_value,3))
#t-statistic 3.076
#p-value: 0.003

#by colors 
colors =  sorted(pd.unique(pd.Series(data.colour)))
#sns.catplot(data=data, kind='box', col='colour', x='congruent', y='RT', hue='colour', sharey=True, height=4)    
sns.boxplot(x = adata['congruent'], y = adata['RT'], hue = sorted(adata['colour']),palette = colors).legend_.remove()

#by colors grouped
sns.set_context("paper", font_scale=0.8)
sns.boxplot(x = adata['colour'], y = adata['RT'], hue = adata['congruent'], gap=0.2)
