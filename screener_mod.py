# -*- coding: utf-8 -*-
"""
Needs to be Checked
"""

import pandas as pd
#import time
import os

newdatafolder = '31_03_2018'

#%%

#MergeAnnual
cwd = os.getcwd()

oneupdirectory = os.path.dirname(cwd)
twoupdirectory = os.path.dirname(oneupdirectory)

filename='SPAL.csv' 
#filename = each + '.csv'
print(cwd)
newdata = pd.read_csv(os.path.join(cwd, 'data', newdatafolder, 'Annual', filename), index_col = 0)
#if New Data contains 
newdata.index = pd.to_datetime(newdata.index, errors='ignore', format = "%Y/%m/%d")
 


#%%

#stocklistpath = r'/home/physicscoaching1/datadownload'
stocklistpath=oneupdirectory
stocklistfilename  = 'EQUITY_L_NSE.csv' 

stocklist = pd.read_csv(os.path.join(stocklistpath, stocklistfilename), usecols=['SYMBOL'])


stocklist['combinedflag'] = stocklist['SYMBOL']

#%%
alreadycombined = "modified.csv"

try:
    stocklist2 = pd.read_csv(alreadycombined, usecols=['SYMBOL', 'combinedflag'])
    
except:
    stocklist2 = stocklist
    
#%%



#%%

errorfilename= 'combinederror.csv'
i = 0
for i, each in enumerate (stocklist['SYMBOL']):
    
    if ((stocklist['combinedflag'].iloc[i] != stocklist2['combinedflag'].iloc[i])):
    
        try:
            filename='SPAL.csv' 
            #filename = each + '.csv'
            newdata = pd.read_csv(os.path.join(cwd, 'data', newdatafolder, 'Annual', filename))
            existingdata = pd.read_csv(os.path.join(cwd, 'data', 'Annual', filename))
            
            data = pd.concat([newdata, existingdata], verify_integrity=False)
            data = data[data.index.duplicated(keep='first')]
            
            stocklist2['combinedflag'].iloc[i] = 'yes'
            #stocklist2.to_csv(alreadycombined)
           
        except:
            fd = open(errorfilename,'a')
            fd.write('\n')
            #fd.write(each)
            fd.close()
            #print("Failed:", each)
            
stocklist2.to_csv(alreadycombined)
        
#%%

        
        