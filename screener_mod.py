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
 


#%%
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
    
    if ((stocklist['combinedflag'].iloc[i] != 'yes')):
    
        try:
            filename = each + '.csv'
            data = pd.read_csv(os.path.join(cwd, 'data', 'Annual', filename))
            
            data['EPS Growth'] = ((data['EPS (unadj)'] -data['EPS (unadj)'].shift(1))
                                              /(data['EPS (unadj)'].shift(1))*100)
            data['Return on Capital Employed'] = 100*(data['Net Profit']+data['Interest']+data['Tax'])/(data['Share Capital']
                                                                            +data['Reserves']+ data['Borrowings'])
            data['Interest Coverage Ratio'] = (data['Net Profit']+data['Interest']+data['Tax'])/(data['Interest'])
            data['Financial Leverage Ratio'] = data['Total Assets']/(data['Share Capital']+data['Reserves'])
            data['Account Receivables Turnover Ratio'] =  1/data['Receivables Sales Ratio']
            data['Inventory Turnover Ratio'] = 1/data['Inventory Sales Ratio']
            data['Fixed Assets Turnover Ratio'] = data['Sales']/data['Fixed Assets']
            
            data.to_csv(os.path.join(cwd, 'data', 'Annual', filename))
            stocklist2['combinedflag'].iloc[i] = 'yes'
            print('success')
            #stocklist2.to_csv(alreadycombined)
           
        except:
            fd = open(errorfilename,'a')
            fd.write('\n')
            #fd.write(each)
            fd.close()
            print("Failed:", each)
            
stocklist2.to_csv(alreadycombined)
        
#%%

        
        