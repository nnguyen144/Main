#!/usr/bin/env python
# coding: utf-8

# In[24]:

import json
import requests
import csv
from datetime import datetime
import pandas as pd
import os
import matplotlib.pyplot as plt

def github_auth(url, lsttoken, ct):
    """
    Authenticate with the GitHub API using a token from a list of tokens.

    Args:
        url (str): The API endpoint URL to send the request to.
        lsttoken (list): A list of authentication tokens to use for the API requests.
        ct (int): The current index of the token to use from the list.

    Returns:
        tuple: A tuple containing:
            - jsonData (dict or None): The JSON response data from the API request, or None if an error occurred.
            - ct (int): The updated index of the token to be used for the next request.
    """
    jsonData = None
    try:
        ct = ct % len(lstTokens)  # Ensure the token index wraps around the list length
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1  # Move to the next token
    except Exception as e:
        print(e)  # Print the exception message
    return jsonData, ct

firstDate = '2015-06-19'
firstDateObj = datetime.strptime(firstDate, '%Y-%m-%d').date()

def weeksToDate(date):
    """
    Calculate the number of weeks from a fixed starting date to a given date.

    Args:
        date (str): The date string in 'YYYY-MM-DD' format to calculate weeks from.

    Returns:
        int: The number of complete weeks between the fixed starting date and the given date.
    """
    dateObj = datetime.strptime(date, '%Y-%m-%d').date()
    daysObj = (dateObj - firstDateObj)
    weeks = daysObj.days / 7  # Calculate the number of weeks
    return int(weeks)

ct = 0
repo = 'scottyab/rootbeer'

df = pd.read_csv('file_rootbeer.csv', usecols=['Filename'])

list = []
for row in range(df.shape[0]):
    file = (df.loc[row].at["Filename"])
    commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?path=' + file
    shaDetails, ct = github_auth(commitsUrl, lstTokens, ct)
    shaDetails = shaDetails[0]
    commitjson = shaDetails['commit']
    author = commitjson['author']
    name = author['name']
    date = author['date']
    date = date[0:10]
    weeks = (weeksToDate(date))
    list.append((name, row, weeks))

x = []
y = []
for i in range(len(list)):
    x.append((list[i][1]))
    y.append((list[i][2]))

plt.scatter(x, y)
plt.show()

# In[ ]:
