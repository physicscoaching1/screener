# -*- coding: utf-8 -*-
# NSE List of Securities https://www.nseindia.com/corporates/content/securities_info.htm

# In[2]:
from selenium import webdriver
#from selenium.webdriver import ActionChains
import pandas as pd
import time
import os
import warnings
from bs4 import BeautifulSoup, Comment
import re
import numpy as np

warnings.filterwarnings(action='once')

#%%

newdatafolder = '31_03_2018'

#%%
cwd = os.getcwd()
oneupdirectory = os.path.dirname(cwd)
twoupdirectory = os.path.dirname(oneupdirectory)


# In[3]:
stocklistpath = oneupdirectory
pathannual=os.path.join(oneupdirectory, 'data', 'screener', newdatafolder, 'Annual')
pathquaterly=os.path.join(oneupdirectory, 'data', 'screener', newdatafolder, 'Quaterly')
pathttm=os.path.join(oneupdirectory, 'data', 'screener', newdatafolder, 'TTM')
pathannualreports=os.path.join(oneupdirectory, 'data', 'screener', newdatafolder, 'Annual_Reports')

#%%
#Delete the previous content of error file it it exist

try:
    errorfilename= 'error1.csv'
    fd = open(errorfilename,'w')
    fd.close()

except:
    pass


#%%

#stocklistfilename  = 'error1.csv'
stocklistfilename  = 'EQUITY_L_NSE.csv'

stocklisfilenamewithBSEcodeandsector = 'EQUITY_NSE_WITH BSECODE_AND_SECTOR.csv'

errorfilename= 'error1.csv'

#path=oneupdirectory

#stocklist = pd.read_csv(os.path.join(stocklistpath,stocklistfilename), usecols=['SYMBOL'])
stocklist = pd.read_csv(os.path.join(stocklistpath, stocklistfilename), usecols=['SYMBOL'])
stocklist['downloadedflag'] = stocklist['SYMBOL']
stocklist['bsecode'] = stocklist['SYMBOL']
stocklist['sector'] = stocklist['SYMBOL']

#%%
alreadydownloaded = "downloaded.csv"

try:
    stocklist2 = pd.read_csv(alreadydownloaded, usecols=['SYMBOL', 'downloadedflag', 'bsecode', 'sector'])
    
except:
    stocklist2 = stocklist

#%%
    
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 

try:
    chromedriverpath = r"C:\Users\abhis\Desktop\Chromedrive\chromedriver.exe"
    
    browser = webdriver.Chrome(chromedriverpath, options=options)
    
except:

    browser = webdriver.PhantomJS(service_log_path=os.path.devnull)


# In[5]:


loginurl = "https://www.screener.in/login/"
browser.get(loginurl)
time.sleep(2.22)
username = browser.find_element_by_id("id_username")
password = browser.find_element_by_id("id_password")

username.send_keys("abhishek.iitkgp@gmail.com")
password.send_keys("keshav123")

browser.find_element_by_xpath('//*[@id="top"]/div/div/form/fieldset/div[3]/button').click()
time.sleep(3.16)




#%%

each = '20MICRON'


try: 
    url = "https://www.screener.in/company/" + each + '/consolidated'
    #url = "https://www.screener.in/company/" + each
    
    
    browser.get(url)
    time.sleep(2.22)
    
    browser.find_element_by_xpath('//*[@id="balancesheet"]/div/div/table/tbody/tr[9]/td[1]').click()
    time.sleep(.5)
    
    browser.find_element_by_xpath('//*[@id="cashflow"]/div/div/table/tbody/tr[1]/td[1]').click()
    time.sleep(0.6)
    
    browser.find_element_by_xpath('//*[@id="cashflow"]/div/div/table/tbody/tr[5]/td[1]').click()
    time.sleep(0.5)
    
    pagesource = browser.page_source.encode('utf-8')
    data = pd.read_html(pagesource)
    
    Quaterly = data[1]
    Quaterly = Quaterly.set_index('Unnamed: 0')
    Quaterly.index.name = None
    Quaterly = Quaterly.transpose()
    Quaterly.index = Quaterly.index.to_datetime()
    
    
except:
    
    url = "https://www.screener.in/company/" + each
    #url = "https://www.screener.in/company/" + each
    
    
    browser.get(url)
    time.sleep(2.22)
    
    browser.find_element_by_xpath('//*[@id="balancesheet"]/div/div/table/tbody/tr[9]/td[1]').click()
    time.sleep(.5)
    
    browser.find_element_by_xpath('//*[@id="cashflow"]/div/div/table/tbody/tr[1]/td[1]').click()
    time.sleep(0.6)
    
    browser.find_element_by_xpath('//*[@id="cashflow"]/div/div/table/tbody/tr[5]/td[1]').click()
    time.sleep(0.5)
    
    pagesource = browser.page_source.encode('utf-8')
    data = pd.read_html(pagesource)
    
    Quaterly = data[1]
    Quaterly = Quaterly.set_index('Unnamed: 0')
    Quaterly.index.name = None
    Quaterly = Quaterly.transpose()
    Quaterly.index = pd.to_datetime(Quaterly.index)
#    Quaterly.index = Quaterly.index.to_datetime()
#PeerComparision = data[0]
#PeerComparision = PeerComparision.set_index('Name')
#PeerComparision = PeerComparision.drop('S.No.', 1)
#print (PeerComparision)



# In[16]:


ProfitandLoss = data[2]
ProfitandLoss = ProfitandLoss.set_index('Unnamed: 0')
ProfitandLoss.index.name = None
ProfitandLoss = ProfitandLoss.transpose()
ProfitandLoss['NPM'] = ProfitandLoss['Net Profit']/ProfitandLoss['Sales']*100
ProfitandLoss['Tax Rate'] = ProfitandLoss['Tax']/ProfitandLoss['Profit before tax']*100
ProfitandLoss['YOY Sales Growth'] = ((ProfitandLoss['Sales'] -ProfitandLoss['Sales'].shift(1))
                                     /(ProfitandLoss['Sales'].shift(1))*100)
ProfitandLoss['YOY Op Profit Growth'] = ((ProfitandLoss['Operating Profit'] -ProfitandLoss['Operating Profit'].shift(1))
                                  /(ProfitandLoss['Operating Profit'].shift(1))*100)
ProfitandLoss['YOY Net Profit Growth'] = ((ProfitandLoss['Net Profit'] -ProfitandLoss['Net Profit'].shift(1))
                                  /(ProfitandLoss['Net Profit'].shift(1))*100)
ProfitandLoss['EPS Growth'] = ((ProfitandLoss['EPS (unadj)'] -ProfitandLoss['EPS (unadj)'].shift(1))
                                  /(ProfitandLoss['EPS (unadj)'].shift(1))*100)
#ProfitandLoss.index = ProfitandLoss.index.to_datetime()
ProfitandLossWoTTM = ProfitandLoss.iloc[0:-1]
ProfitandLossWoTTM.index = pd.to_datetime(ProfitandLossWoTTM.index)
#ProfitandLossWoTTM.index = ProfitandLossWoTTM.index.to_datetime()
print (ProfitandLossWoTTM)


# In[17]:


BalanceSheet = data[3]
BalanceSheet = BalanceSheet.set_index('Unnamed: 0')
BalanceSheet.index.name = None
BalanceSheet = BalanceSheet.transpose()
#BalanceSheet.index = BalanceSheet.index.to_datetime()
BalanceSheet.index = pd.to_datetime(BalanceSheet.index)
#BalanceSheet.index =BalanceSheet.index.strftime("%Y-%m")
#print (BalanceSheet)

CashFlow = data[4]
CashFlow = CashFlow.set_index('Unnamed: 0')
CashFlow.index.name = None
CashFlow = CashFlow.transpose()
#CashFlow.index = CashFlow.index.to_datetime()
CashFlow.index = pd.to_datetime(CashFlow.index)
#print (CashFlow)


## In[18]:
#
#
#pd.options.display.float_format = '{:.2f}'.format
#Ratios = pd.DataFrame(index=BalanceSheet.index)
#Ratios['Receivables Sales Ratio'] = BalanceSheet['Trade receivables']/ProfitandLossWoTTM['Sales']
#Ratios['Inventory Sales Ratio'] = BalanceSheet['Inventories']/ProfitandLossWoTTM['Sales']
#Ratios['Operating Cash Flow to Net Profit'] = CashFlow['Cash from Operating Activity']/ProfitandLossWoTTM['Net Profit']
#Ratios['Depreciation to Fixed Assets'] = ProfitandLossWoTTM['Depreciation']/BalanceSheet['Fixed Assets']
#Ratios['Depreciation to Gross Fixed Assets'] = ProfitandLossWoTTM['Depreciation']/(BalanceSheet['Fixed Assets']+
#                                                                                   BalanceSheet['CWIP'])
#Ratios['Return on Equity'] = 100*ProfitandLossWoTTM['Net Profit']/(BalanceSheet['Share Capital']+BalanceSheet['Reserves'])
#Ratios['Return on Capital Employed'] = 100*(ProfitandLossWoTTM['Net Profit']+ProfitandLossWoTTM['Interest']+ProfitandLossWoTTM['Tax'])/(BalanceSheet['Share Capital']
#                                                                +BalanceSheet['Reserves']+ BalanceSheet['Borrowings'])
#Ratios['Debt to Equity Ratio'] = BalanceSheet['Borrowings']/(BalanceSheet['Share Capital']+BalanceSheet['Reserves'])
#Ratios['Interest Coverage Ratio'] = (ProfitandLossWoTTM['Net Profit']+ProfitandLossWoTTM['Interest']+ProfitandLossWoTTM['Tax'])/(ProfitandLossWoTTM['Interest'])
#Ratios['Financial Leverage Ratio'] = BalanceSheet['Total Assets']/(BalanceSheet['Share Capital']+BalanceSheet['Reserves'])
##print (Ratios)
#
#
#GrowthRates = pd.DataFrame(index=BalanceSheet.index)
#GrowthRates['YOY Sales Growth'] = ProfitandLossWoTTM['YOY Sales Growth']
#GrowthRates['YOY Op Profit Growth'] = ProfitandLossWoTTM['YOY Op Profit Growth']
#GrowthRates['YOY Net Profit Growth'] = ProfitandLossWoTTM['YOY Net Profit Growth']
#
#Ratios['Inventory Turnover Ratio'] = 1/Ratios['Inventory Sales Ratio']
#Ratios['Account Receivables Turnover Ratio'] =  1/Ratios['Receivables Sales Ratio']
#Ratios['Fixed Assets Turnover Ratio'] = ProfitandLossWoTTM['Sales']/BalanceSheet['Fixed Assets']
##Ratios['Working Capital Turnover Ratio'] = (1)/ProfitandLossWoTTM['Sales']
#
##print (GrowthRates)
#
#
## In[24]:
#
#
#result = ProfitandLossWoTTM.join([BalanceSheet, CashFlow, Ratios])
##print(result)
#
##%%
#i=0
#filename = each + '.csv'
##export Annual data
#
#result.to_csv(os.path.join(pathannual,filename))
##export Quaterly data
#Quaterly.to_csv(os.path.join(pathquaterly,filename))
#stocklist2['downloadedflag'].iloc[i] = 'yes'
#stocklist2.to_csv(alreadydownloaded)
#
##%%Second Part
#
## Sector
soup = BeautifulSoup(pagesource)
for element in soup(text=lambda text: isinstance(text, Comment)):
    element.extract()
#    
#Head= soup.find('h1')
#sector = (Head.small.text)
#stocklist2['sector'].iloc[i] = sector
#
#
## TTM Values + Promototer Holdings
Head4= soup.findAll('h4')

#%%
l = []
for  j, each1 in enumerate (Head4):
    print(each1.contents)

#%%
mylist = []
for  j, each1 in enumerate (Head4):
    try:
        #Property = str(each.contents[0].encode('utf-8'))
        Property = str(each1.contents[0].encode('utf-8'))
        #Substitute unwanted characters from the Property Field
        Property = re.sub('b', '', Property)
        Property = re.sub("'", '', Property)
        
        ValueMatString = str(each1.contents[2].encode('utf-8'))
                #Substitute unwanted characters from the Property Field
        ValueMatString = re.sub('b', '', ValueMatString)
        ValueMatString = re.sub("'", '', ValueMatString)
        
        Value = ValueMatString
        
        try:
            #Extract the real numbers from the strings
            Valuematrix = (re.findall(r"[-+]?\d*\.\d+|\d+", ValueMatString))
            #get the last real number
            Value = Valuematrix[-1]
        except:
            pass
        mylist.append([Property, Value])
    except:
        pass
    
#%%
#
mylist = np.transpose(mylist)  
df = pd.DataFrame(np.transpose(mylist))

#%%
#df.to_csv(os.path.join(pathttm,filename), header = False, index = False)
#
#
##Annual Reports File          
#links = soup.findAll('a')
#linklist = []
#for link in links:
#    linklist.append([link.text, link.get('href')])
#   
#df2 = pd.DataFrame(np.transpose(linklist))
#df2.columns = df2.iloc[0]
#df2 = df2.reindex(df2.index.drop(0))
#
#colNames = df2.columns[df2.columns.str.contains(pat = 'Financial Year')] 
#
#
#AnnualReport = df2[colNames]
#
#AnnualReport.to_csv(os.path.join(pathannualreports,filename), index = False)
#
#
## BSE Code
#BSEurl = df2['BSE'].iloc[0]
#Segments = BSEurl.rpartition('/')
#Segments1 = Segments[0].rpartition('/')
#bsecode = Segments1[2]
#stocklist2['bsecode'].iloc[i] = bsecode
#
#stocklist2.to_csv(alreadydownloaded)
#stocklist2.to_csv(os.path.join(stocklistpath, stocklisfilenamewithBSEcodeandsector))
#
#print("Success:", each)



#%%
browser.quit()
stocklist2.to_csv(alreadydownloaded)


# In[ ]:




























#each = '20MICRONS'
##code to reindex -- https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.reindex.html
#
#url = "https://www.screener.in/company/" + each
#
#
#browser.get(url)
#time.sleep(2.22)
#
#browser.find_element_by_xpath('//*[@id="balancesheet"]/div/div/table/tbody/tr[9]/td[1]').click()
#time.sleep(.5)
#
#browser.find_element_by_xpath('//*[@id="cashflow"]/div/div/table/tbody/tr[1]/td[1]').click()
#time.sleep(0.6)
#
#browser.find_element_by_xpath('//*[@id="cashflow"]/div/div/table/tbody/tr[5]/td[1]').click()
#time.sleep(0.5)
#
#pagesource = browser.page_source.encode('utf-8')
#data = pd.read_html(pagesource)
#
#
##print (data)
#
#
##PeerComparision = data[0]
##PeerComparision = PeerComparision.set_index('Name')
##PeerComparision = PeerComparision.drop('S.No.', 1)
##print (PeerComparision)
#
#
## In[10]:
#
#
#Quaterly = data[1]
#Quaterly = Quaterly.set_index('Unnamed: 0')
#Quaterly.index.name = None
#Quaterly = Quaterly.transpose()
#Quaterly.index = Quaterly.index.to_datetime()
##print (Quaterly)
#
#
## In[16]:
#
#
#ProfitandLoss = data[2]
#ProfitandLoss = ProfitandLoss.set_index('Unnamed: 0')
#ProfitandLoss.index.name = None
#ProfitandLoss = ProfitandLoss.transpose()
#ProfitandLoss['NPM'] = ProfitandLoss['Net Profit']/ProfitandLoss['Sales']*100
#ProfitandLoss['Tax Rate'] = ProfitandLoss['Tax']/ProfitandLoss['Profit before tax']*100
#ProfitandLoss['YOY Sales Growth'] = ((ProfitandLoss['Sales'] -ProfitandLoss['Sales'].shift(1))
#                                     /(ProfitandLoss['Sales'].shift(1))*100)
#ProfitandLoss['YOY Op Profit Growth'] = ((ProfitandLoss['Operating Profit'] -ProfitandLoss['Operating Profit'].shift(1))
#                                  /(ProfitandLoss['Operating Profit'].shift(1))*100)
#ProfitandLoss['YOY Net Profit Growth'] = ((ProfitandLoss['Net Profit'] -ProfitandLoss['Net Profit'].shift(1))
#                                  /(ProfitandLoss['Net Profit'].shift(1))*100)
#ProfitandLoss['EPS Growth'] = ((ProfitandLoss['EPS (unadj)'] -ProfitandLoss['EPS (unadj)'].shift(1))
#                                  /(ProfitandLoss['EPS (unadj)'].shift(1))*100)
##ProfitandLoss.index = ProfitandLoss.index.to_datetime()
#ProfitandLossWoTTM = ProfitandLoss.iloc[0:-1]
#ProfitandLossWoTTM.index = ProfitandLossWoTTM.index.to_datetime()
##print (ProfitandLossWoTTM)
#
#
## In[17]:
#
#
#BalanceSheet = data[3]
#BalanceSheet = BalanceSheet.set_index('Unnamed: 0')
#BalanceSheet.index.name = None
#BalanceSheet = BalanceSheet.transpose()
#BalanceSheet.index = BalanceSheet.index.to_datetime()
##BalanceSheet.index =BalanceSheet.index.strftime("%Y-%m")
##print (BalanceSheet)
#
#CashFlow = data[4]
#CashFlow = CashFlow.set_index('Unnamed: 0')
#CashFlow.index.name = None
#CashFlow = CashFlow.transpose()
#CashFlow.index = CashFlow.index.to_datetime()
##print (CashFlow)
#
#
## In[18]:
#
#
#pd.options.display.float_format = '{:.2f}'.format
#Ratios = pd.DataFrame(index=BalanceSheet.index)
#Ratios['Receivables Sales Ratio'] = BalanceSheet['Trade receivables']/ProfitandLossWoTTM['Sales']
#Ratios['Inventory Sales Ratio'] = BalanceSheet['Inventories']/ProfitandLossWoTTM['Sales']
#Ratios['Operating Cash Flow to Net Profit'] = CashFlow['Cash from Operating Activity']/ProfitandLossWoTTM['Net Profit']
#Ratios['Depreciation to Fixed Assets'] = ProfitandLossWoTTM['Depreciation']/BalanceSheet['Fixed Assets']
#Ratios['Depreciation to Gross Fixed Assets'] = ProfitandLossWoTTM['Depreciation']/(BalanceSheet['Fixed Assets']+
#                                                                                   BalanceSheet['CWIP'])
#Ratios['Return on Equity'] = 100*ProfitandLossWoTTM['Net Profit']/(BalanceSheet['Share Capital']+BalanceSheet['Reserves'])
#Ratios['Return on Capital Employed'] = 100*(ProfitandLossWoTTM['Net Profit']+ProfitandLossWoTTM['Interest']+ProfitandLossWoTTM['Tax'])/(BalanceSheet['Share Capital']
#                                                                +BalanceSheet['Reserves']+ BalanceSheet['Borrowings'])
#Ratios['Debt to Equity Ratio'] = BalanceSheet['Borrowings']/(BalanceSheet['Share Capital']+BalanceSheet['Reserves'])
#Ratios['Interest Coverage Ratio'] = (ProfitandLossWoTTM['Net Profit']+ProfitandLossWoTTM['Interest']+ProfitandLossWoTTM['Tax'])/(ProfitandLossWoTTM['Interest'])
#Ratios['Financial Leverage Ratio'] = BalanceSheet['Total Assets']/(BalanceSheet['Share Capital']+BalanceSheet['Reserves'])
##print (Ratios)
#
#
#GrowthRates = pd.DataFrame(index=BalanceSheet.index)
#GrowthRates['YOY Sales Growth'] = ProfitandLossWoTTM['YOY Sales Growth']
#GrowthRates['YOY Op Profit Growth'] = ProfitandLossWoTTM['YOY Op Profit Growth']
#GrowthRates['YOY Net Profit Growth'] = ProfitandLossWoTTM['YOY Net Profit Growth']
#
#Ratios['Inventory Turnover Ratio'] = 1/Ratios['Inventory Sales Ratio']
#Ratios['Account Receivables Turnover Ratio'] =  1/Ratios['Receivables Sales Ratio']
#Ratios['Fixed Assets Turnover Ratio'] = ProfitandLossWoTTM['Sales']/BalanceSheet['Fixed Assets']
##Ratios['Working Capital Turnover Ratio'] = (1)/ProfitandLossWoTTM['Sales']
#
##print (GrowthRates)
#
#
## In[24]:
#
#
#result = ProfitandLossWoTTM.join([BalanceSheet, CashFlow, Ratios])
##print(result)
#
##%%
#i=0
#filename = each + '.csv'
##export Annual data
#
#result.to_csv(os.path.join(pathannual,filename))
##export Quaterly data
#Quaterly.to_csv(os.path.join(pathquaterly,filename))
#stocklist2['downloadedflag'].iloc[i] = 'yes'
#stocklist2.to_csv(alreadydownloaded)
#
##%%Second Part
#
## Sector
#soup = BeautifulSoup(pagesource)
#for element in soup(text=lambda text: isinstance(text, Comment)):
#    element.extract()
#    
#Head= soup.find('h1')
#sector = (Head.small.text)
#stocklist2['sector'].iloc[i] = sector
#
#
## TTM Values + Promototer Holdings
#Head4= soup.findAll('h4')
#mylist = []
#for  each1 in enumerate (Head4):
#    try:
#        #Property = str(each.contents[0].encode('utf-8'))
#        Property = str(each1.contents[0].encode('utf-8'))
#        #Substitute unwanted characters from the Property Field
#        Property = re.sub('b', '', Property)
#        Property = re.sub("'", '', Property)
#        
#        ValueMatString = str(each1.contents[2].encode('utf-8'))
#        #Extract the real numbers from the strings
#        Valuematrix = (re.findall(r"[-+]?\d*\.\d+|\d+", ValueMatString))
#        #get the last real number
#        Value = Valuematrix[-1]
#        mylist.append([Property, Value])
#    except:
#        pass
#
##mylist = np.transpose(mylist)  
#df = pd.DataFrame(np.transpose(mylist))
#df.to_csv(os.path.join(pathttm,filename), header = False, index = False)
#
#
##Annual Reports File          
#links = soup.findAll('a')
#linklist = []
#for link in links:
#    linklist.append([link.text, link.get('href')])
#   
#df2 = pd.DataFrame(np.transpose(linklist))
#df2.columns = df2.iloc[0]
#df2 = df2.reindex(df2.index.drop(0))
#
#colNames = df2.columns[df2.columns.str.contains(pat = 'Financial Year')] 
#
#
#AnnualReport = df2[colNames]
#
#AnnualReport.to_csv(os.path.join(pathannualreports,filename), index = False)
#
#
## BSE Code
#BSEurl = df2['BSE'].iloc[0]
#Segments = BSEurl.rpartition('/')
#Segments1 = Segments[0].rpartition('/')
#bsecode = Segments1[2]
#stocklist2['bsecode'].iloc[i] = bsecode
#
#stocklist2.to_csv(alreadydownloaded)
#stocklist2.to_csv(os.path.join(stocklistpath, stocklisfilenamewithBSEcodeandsector))
#
#print("Success:", each)







