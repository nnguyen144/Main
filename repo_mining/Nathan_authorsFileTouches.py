import json
import requests
import os

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, token_counter):
    jsonData = None
    try:
        token_counter = token_counter % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[token_counter])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        token_counter += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, token_counter

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    page_counter = 1  # URL page counter
    token_counter = 0  # token counter

    # Define the relevant file extensions
    language_extensions = {".java", ".kt", ".ktm", ".kts", ".cpp", ".c", ".cmake", ".cmake.in"}

    try:
        while True:
            # Fetch the list of commits from the repository
            commits_url = f'https://api.github.com/repos/{repo}/commits?page={page_counter}&per_page=100'
            json_commits, token_counter = github_auth(commits_url, lsttokens, token_counter)

            # Break if no more commits are available
            if not json_commits:
                break

            for sha_object in json_commits:
                sha = sha_object['sha']
                commit = sha_object['commit']
                author_name = commit['author']['name']
                commit_date = commit['author']['date']

                # Fetch the files modified in the commit
                sha_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
                sha_details, token_counter = github_auth(sha_url, lsttokens, token_counter)
                filesjson = sha_details['files']

                for file in filesjson:
                    filename = file['filename']

                    # Check if the file has a relevant extension
                    if not any(filename.endswith(ext) for ext in language_extensions):
                        continue

                    file_entry = {"author": author_name, "date": commit_date}

                    # Add or append the file information in dictfiles
                    dictfiles.setdefault(filename, []).append(file_entry)

            page_counter += 1

    except Exception as e:
        print(f"Error receiving data: {e}")
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
lstTokens = [""]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]

for x in dictfiles.keys():
    for y in dictfiles[x]:
        print(y['author'] + " accessed the file " + x + " on " + y['date'] + ".")
