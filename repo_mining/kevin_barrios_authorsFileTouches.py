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

# Helper function to process files in a commit
def process_commit_files(files, dict_files, author_name, author_touch_date, start_date):
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    touch_date = datetime.strptime(author_touch_date, date_format)
    start_date = datetime.strptime(start_date, date_format)
    week_diff = (touch_date - start_date).days // 7

    for file in files:
        filename = file['filename']
        if not any(ext in filename for ext in [".java", ".c", ".cpp", ".kt", "CMake"]):
            continue

        if filename not in dict_files:
            dict_files[filename] = {'count': 0, 'authors': {}}

        dict_files[filename]['count'] += 1

        if author_name not in dict_files[filename]['authors']:
            dict_files[filename]['authors'][author_name] = {'touches': 0, 'dates': []}

        dict_files[filename]['authors'][author_name]['touches'] += 1
        dict_files[filename]['authors'][author_name]['dates'].append(week_diff)

# Main function to count files and commits
def count_files(dict_files, tokens, repo):
    page_num = 1
    token_index = 0
    start_date = None

    # Fetch repository data to get the start date
    try:
        repo_url = f'https://api.github.com/repos/{repo}'
        repo_data, token_index = github_request(repo_url, tokens, token_index)
        start_date = repo_data['created_at']
    except Exception as e:
        print(f"Error fetching repository data: {e}")
        exit(1)

    # Fetch commit data and process files in commits
    while True:
        try:
            commits_url = f'https://api.github.com/repos/{repo}/commits?page={page_num}&per_page=100'
            commits, token_index = github_request(commits_url, tokens, token_index)

            if not commits:  # Break loop if no more commits
                break

            for commit in commits:
                sha = commit['sha']
                author_name = commit['commit']['author']['name']
                author_touch_date = commit['commit']['author']['date']

                # Fetch commit details to get the files
                try:
                    sha_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
                    sha_details, token_index = github_request(sha_url, tokens, token_index)
                    process_commit_files(sha_details['files'], dict_files, author_name, author_touch_date, start_date)
                except Exception as e:
                    print(f"Error fetching commit details for SHA {sha}: {e}")
                    continue

            page_num += 1
        except Exception as e:
            print(f"Error fetching commits data: {e}")
            exit(1)
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
