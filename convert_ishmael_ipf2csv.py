# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 14:18:52 2021

@author: Sebastian Menze
"""

import numpy as np
import pandas as pd


listlocation=r"C:\Users\a5278\Documents\passive_acoustics\linn_filelist\Orkney_april17.ipf"
timekey='%y%m%d_%H%M%S_AU_SO02.wav'

df=pd.read_csv(listlocation,delimiter=' ',header=None)
df_oneline=pd.read_csv(listlocation,header=None)

ix_categories= np.where( df.iloc[:,0]!='StartFile:' )[0]
categories=pd.unique(df_oneline.iloc[ix_categories,0])

annotations=pd.DataFrame(columns=[ np.append('Time',categories) ])
ix_timestamp= np.where( df.iloc[:,0]=='StartFile:' )[0]

b= df.iloc[ix_timestamp,1].str.replace("'",'').str.split('\\',expand=True)
annotations['Time']=  pd.to_datetime( b.iloc[:,-1].values,format=timekey )

annotations.iloc[:,1:]=np.zeros([ annotations.shape[0] , annotations.shape[1]-1 ])

for i_cat in range(len(categories)):
    cat=categories[i_cat]
    ix=np.where( df_oneline.iloc[:,0]==cat )[0]
    for ixx in ix:
        c=ixx-ix_timestamp
        c[c<0]=99999
        ix_t=ix_timestamp[ np.argmin(c) ]
        timestamp=pd.to_datetime( df.iloc[ix_t,1].replace("'",'').split('\\')[-1]  ,format=timekey )
        ix_time=np.where( annotations['Time']==timestamp )[0]
        
        annotations.iloc[ix_time,i_cat+1]=1
        
annotations.to_csv(  listlocation[:-4]+'.csv',index=False)   