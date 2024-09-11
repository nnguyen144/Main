import json
import requests
import numpy as np
import matplotlib.pyplot as plt
import os
import randomcolor
from matplotlib.lines import Line2D
from datetime import datetime

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
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

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo, datelist, colordict, colorlist, authorlist):
    ipage = 1  # url page counter
    ct = 0  # token counter

    # input programming languages of repo
    languageExtensions = [".java", ".kt", ".ktm", "kts", ".cpp", ".c", ".cmake", ".cmake.in"]

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break

            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                commit = shaObject['commit']
                author = commit['author']
                authorName = author['name']
                commitDate = author['date']
                a = datetime.fromisoformat(commitDate[:-1])
                a.strftime('%Y-%m-%d')
                datelist.append(a)
                if not authorName in colordict:
                    colordict[authorName] = randomcolor.RandomColor().generate()
                    authorlist.append(authorName)
                

                
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    isSourceFile = False
                    filename = filenameObj['filename']
                    for x in languageExtensions:
                        if filename.endswith(x):
                            isSourceFile = True
                    if not isSourceFile:
                        continue
                    colorlist.append(colordict[authorName][0])
                    #fileDict = {
                    #    "author": authorName,
                    #    "date": commitDate
                    #}
                    if not filename in dictfiles.keys():
                        dictfiles[filename] = [commitDate]
                    else:
                        dictfiles[filename].append(commitDate)
                    # print(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]

dictfiles = dict()
datelist = []
colorlist = []
colordict = dict()
authorlist = []
countfiles(dictfiles, lstTokens, repo, datelist, colordict, colorlist, authorlist)

# Find starting date
earliest_date = min(datelist)

file = repo.split('/')[1]

def weeks_since_earliest_date(y):
    b = datetime.fromisoformat(y[:-1])
    b.strftime('%Y-%m-%d')
    return round(abs((earliest_date - b).days)/7)

xlist = []
ylist = []
counter = 0
for x in list(dictfiles.keys()):
    for y in dictfiles[x]:
        xlist.append(counter)
        ylist.append(weeks_since_earliest_date(y))
    counter += 1
legendset = []
for x in authorlist:
    legendset.append(Line2D([0], [0], color=colordict[x][0], lw=4))

plt.scatter(xlist, ylist, c = colorlist)
plt.legend(legendset, authorlist, loc = 'upper left', fontsize=7, bbox_to_anchor=(.98, 1))

plt.xlabel('file')
plt.ylabel('weeks')
plt.title('When/How Many Times\nEach Author Touched a File')
plt.show()


