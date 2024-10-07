import json
import requests
import csv

import os

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
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    STARTDATE = None
    try:
        repoUrl = 'https://api.github.com/repos/' + repo
        jsonRepoData, ct = github_auth(repoUrl, lsttokens, ct)
        if jsonRepoData:
            STARTDATE = jsonRepoData['created_at']
            #print(STARTDATE)
    except:
        print("Error receiving data (start commit)")
        exit(0)

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            try:
                jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)
            except:
                print("error reciving data for commits page, skipping")
                ipage+=1
                continue

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']

                author_name = shaObject['commit']['author']['name']
                author_touch_date = shaObject['commit']['author']['date']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                try:
                    shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                except:
                    print("error reciving data for commit details SHA")
                    continue
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    #Adapted CollectFiles script to only collect source files for repo 'scottyab/rootbeer'
                    if filename.endswith(".java") or filename.endswith(".c") or filename.endswith(".cpp") or filename.endswith(".kt") or "CMake" in filename:
                        if filename not in dictfiles:
                            dictfiles[filename] = {
                                    'count': 0,
                                    'authors': {}
                            }
                        dictfiles[filename]['count'] += 1
                        if author_name not in dictfiles[filename]['authors']:
                            dictfiles[filename]['authors'][author_name] = {
                                    'touches': 0,
                                    'dates': []
                            }
                        dictfiles[filename]['authors'][author_name]['touches'] += 1
                        #calc how many weeks
                        date_format = "%Y-%m-%dT%H:%M:%SZ"
                        touch_date = datetime.strptime(author_touch_date, date_format)
                        start_date = datetime.strptime(STARTDATE, date_format)
                        diff = touch_date - start_date
                        week_count = diff.days // 7
                        dictfiles[filename]['authors'][author_name]['dates'].append(week_count)
                        print(filename)
            ipage += 1
    except:
        print("Error receiving data, skipping")
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
lstTokens = ["fd02a694b606c4120b8ca7bbe7ce29229376ee",
                "16ce529bdb32263fb90a392d38b5f53c7ecb6b",
                "8cea5715051869e98044f38b60fe897b350d4a"]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '_authorsFileTouches.csv'
rows = ["Filename", "Author", "Touch Count", "Week Number"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigauthorname = None
for filename, filedata in dictfiles.items():
    for author, authordata in filedata['authors'].items():
        for date in authordata['dates']:
            rows = [filename, author, authordata['touches'], date]
            writer.writerow(rows)
            count = int(authordata['touches'])
            if bigcount is None or count > bigcount:
                bigcount = count
                bigauthorname = author 
fileCSV.close()
print('The author ' + bigauthorname + ' has touched ' + str(bigcount) + ' files.')
