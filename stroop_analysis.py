# -*- coding: utf-8 -*-
"""
@author: asenic
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind


#read Stroop test results
exp='stroop6.csv'
path='d:\\my_scripts\\py\\stroopy-master\\Data\\'
os.chdir(path)
data=pd.read_csv(exp, sep=";")
means = data.groupby(['congruent', 'Accuracy'])['RT'].mean()
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

t_statistic, p_value = ttest_ind(ncongr[np.isfinite(ncongr)], congr[np.isfinite(congr)])
# Output the results
print(f"t-statistic: {t_statistic}")
print(f"P-value: {p_value}")
# t-statistic: 3.76125479473406
# P-value: 0.0004767207214359306

#for colors separately
cred = np.vstack((congr, data['colour']=='red'))
outr=np.where(cred[1], cred[0], np.nan)#only red
cgreen = np.vstack((congr, data['colour']=='green'))
outg=np.where(cgreen[1], cgreen[0], np.nan)#only green
cblue = np.vstack((congr, data['colour']=='blue'))
outb=np.where(cblue[1], cblue[0], np.nan)#only blue
cyel = np.vstack((congr, data['colour']=='yellow'))
outy=np.where(cyel[1], cyel[0], np.nan)#only green

#ncong
nred = np.vstack((ncongr, data['colour']=='red'))
noutr=np.where(nred[1], nred[0], np.nan)#only red
ngreen = np.vstack((ncongr, data['colour']=='green'))
noutg=np.where(ngreen[1], ngreen[0], np.nan)#only green
nblue = np.vstack((ncongr, data['colour']=='blue'))
noutb=np.where(nblue[1], nblue[0], np.nan)#only blue
nyel = np.vstack((ncongr, data['colour']=='yellow'))
nouty=np.where(nyel[1], nyel[0], np.nan)#only green

fig=np.vstack((outr, outg, outb, outy, noutr, noutg, noutb, nouty))
fig=pd.DataFrame(fig).transpose()
fig.boxplot()
for i, d in enumerate(fig):
   y = fig[d]
   x = np.random.normal(i + 1, 0.04, len(y))
   plt.scatter(x, y)
plt.show()
