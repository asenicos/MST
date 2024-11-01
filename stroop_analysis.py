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
path='d:\\my_scripts\\py\\stroopy-master\\Data\\'
os.chdir(path)
data=pd.read_csv(exp, sep=";")
congr = np.where([data['congruent'] ==1, data['Accuracy']==1], data['RT'],np.nan)[0]
ncongr = np.where([data['congruent'] ==0, data['Accuracy']==1], data['RT'],np.nan)[0]
fig=np.vstack((ncongr, congr))
fig=pd.DataFrame(fig).transpose()
fig.boxplot()
for i, d in enumerate(fig):
   y = fig[d]
   x = np.random.normal(i + 1, 0.04, len(y))
   plt.scatter(x, y)
plt.show()

print('Size of Stroop effect is', round((medians[0,1]-medians[1,1])*1000,3), '+/-', round((sems[0,1]-sems[1,1])*1000,3), 'ms')
#Size of Stroop effect is 119.591 +/- 1.243 ms
print('Analyzed ', len(data), ' trials, accuracy is ', round(len(data[data['Accuracy']==1])/len(data)*100,1), '%.')
#Analyzed  144  trials, accuracy is  95.8 %.
medians = data.groupby(['congruent', 'Accuracy'])['RT'].median()
sems = data.groupby(['congruent', 'Accuracy'])['RT'].sem()
t_statistic, p_value = ttest_ind(ncongr[np.isfinite(ncongr)], congr[np.isfinite(congr)])
# Output the results
print("t-statistic",round(t_statistic,3))
print("p-value:", round(p_value,3))
#t-statistic: 2.755
#p-value: 0.007

#by colors 
colors =  ['green','magenta','black', 'orange','white','skyblue','yellow','red','cyan', 'brown','blue']#pd.unique(pd.Series(data.colour))
#sns.catplot(data=data, kind='box', col='colour', x='congruent', y='RT', hue='colour', sharey=True, height=4)    
sns.boxplot(x = data['congruent'], y = data['RT'], hue = data['colour'],palette = colors).legend_.remove()

#by colors grouped
sns.set_context("paper", font_scale=0.8)
sns.boxplot(x = data['colour'], y = data['RT'], hue = data['congruent'], gap=0.2)
