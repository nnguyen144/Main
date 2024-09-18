import json
import requests
import csv
import matplotlib.pyplot as plt
import os
import numpy as np
import datetime

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

fileupdatehistory = dict()
filetypes ={"kts", "cpp", "java"}
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

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
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    splitfilename = filename.split('.')

                    if len(splitfilename) < 2  or splitfilename[1] not in filetypes:
                        continue
                    githubtime = shaObject['commit']['author']['date']
                    date = datetime.datetime.strptime(githubtime, "%Y-%m-%dT%H:%M:%SZ")

                    dictfiles[filename] = dictfiles.get(filename, 0) + 1
                    if filename in fileupdatehistory:
                        history = fileupdatehistory[filename]
                        timediff = history[0] - date
                        timediff = timediff.total_seconds()
                        weeks = divmod(timediff, 604800)[0]
                        currhist = fileupdatehistory[filename]
                        currhist.append(weeks)
                        fileupdatehistory[filename] = currhist
                    else:
                        fileupdatehistory[filename] = [date]

            ipage += 1
    except Exception as e:
        print(e)
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

SrcFiles = []

with open('data/file_rootbeer.csv') as file:
    csvFile = csv.DictReader(file)
    for col in csvFile:
        SrcFiles.append(col['Filename'])


dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)

for key in fileupdatehistory.keys():
    history = fileupdatehistory[key]
    history[0] = 0
    fileupdatehistory[key] = history

for key in fileupdatehistory:
    plt.scatter([key]*len(fileupdatehistory[key]), fileupdatehistory[key])


plt.show()
