#!/usr/bin/env python
# coding: utf-8

# In[55]:


import json
import requests
import csv
from datetime import datetime
import pandas as pd
import os
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

firstDate='2015-06-19'
firstDateObj=datetime.strptime(firstDate,'%Y-%m-%d').date()
def weeksToDate(date):
    dateObj=datetime.strptime(date,'%Y-%m-%d').date()
    daysObj= (dateObj-firstDateObj)
    weeks= daysObj.days/7
    return int(weeks)

ct=0
repo = 'scottyab/rootbeer'

df=pd.read_csv('file_rootbeer.csv',usecols=['Filename'])


for row in range (df.shape[0]):
    file= (df.loc[row].at["Filename"])
    commitsUrl = 'https://api.github.com/repos/'+repo+'/commits?path='+file
    shaDetails, ct = github_auth(commitsUrl, lstTokens, ct)
    shaDetails=shaDetails[0]
    commitjson=shaDetails['commit']
    author=commitjson['author']
    name=author['name']
    date=author['date']
    date= date[0:10]
    print (file)
    print (name)
    print(weeksToDate(date))





