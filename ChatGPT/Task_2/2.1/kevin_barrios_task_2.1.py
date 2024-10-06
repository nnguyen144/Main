import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(api_url, token_list, current_token_index):
    json_data = None
    try:
        current_token_index = current_token_index % len(token_list)
        headers = {'Authorization': 'Bearer {}'.format(token_list[current_token_index])}
        response = requests.get(api_url, headers=headers)
        json_data = json.loads(response.content)
        current_token_index += 1
    except Exception as e:
        print(e)
    return json_data, current_token_index

# @file_touch_counts, empty dictionary of files
# @token_list, GitHub authentication tokens
# @repository, GitHub repo

file_extensions = {"kts", "cpp", "java"}
def count_files(file_touch_counts, token_list, repository):
    current_page = 1  # URL page counter
    current_token_index = 0  # Token counter

    try:
        # Loop through all the commit pages until the last returned empty page
        while True:
            page_str = str(current_page)
            commits_url = f'https://api.github.com/repos/{repository}/commits?page={page_str}&per_page=100'
            json_commits, current_token_index = github_auth(commits_url, token_list, current_token_index)

            # Break out of the while loop if there are no more commits in the pages
            if len(json_commits) == 0:
                break
            # Iterate through the list of commits in the current page
            for commit_object in json_commits:
                sha = commit_object['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                sha_url = f'https://api.github.com/repos/{repository}/commits/{sha}'
                sha_details, current_token_index = github_auth(sha_url, token_list, current_token_index)
                files_json = sha_details['files']
                for file_object in files_json:
                    filename = file_object['filename']
                    split_filename = filename.split('.')

                    if len(split_filename) < 2 or split_filename[1] not in file_extensions:
                        continue
                    file_touch_counts[filename] = file_touch_counts.get(filename, 0) + 1
                    print(commit_object['commit']['author']['name'] + ' | ' + commit_object['commit']['author']['date'])
                    print(filename)
                    print("\n\n")
            current_page += 1
    except:
        print("Error receiving data")
        exit(0)

# GitHub repo
repository = 'scottyab/rootbeer'
# repository = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repository = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repository = 'mendhak/gpslogger'

# Put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise, they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
token_list = [""]

file_touch_counts = dict()
count_files(file_touch_counts, token_list, repository)
print('Total number of files: ' + str(len(file_touch_counts)))

repository_name = repository.split('/')[1]
# Change this to the path of your file
file_output = 'data/file_' + repository_name + '.csv'
rows = ["Filename", "Touches"]
file_csv = open(file_output, 'w')
writer = csv.writer(file_csv)
writer.writerow(rows)

highest_touch_count = None
highest_touch_filename = None
for filename, count in file_touch_counts.items():
    rows = [filename, count]
    writer.writerow(rows)
    if highest_touch_count is None or count > highest_touch_count:
        highest_touch_count = count
        highest_touch_filename = filename
file_csv.close()
print('The file ' + highest_touch_filename + ' has been touched ' + str(highest_touch_count) + ' times.')
