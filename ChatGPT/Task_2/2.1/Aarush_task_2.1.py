import requests
from datetime import datetime
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
# GitHub token and headers
MyTok = "asdf"  
head = {'Authorization': f'token {MyTok}'}

# List of all Java files in the repository
Jfile = [
    'rootbeerlib/src/main/java/com/scottyab/rootbeer/RootBeerNative.java','app/src/main/java/com/scottyab/rootbeer/sample/CheckRootTask.java','app/src/main/java/com/scottyab/rootbeer/sample/MainActivity.java',
    'app/src/main/java/com/scottyab/rootbeer/sample/TextViewFont.java','rootbeerlib/src/main/java/com/scottyab/rootbeer/Const.java', 'rootbeerlib/src/main/java/com/scottyab/rootbeer/RootBeer.java',
    'rootbeerlib/src/main/java/com/scottyab/rootbeer/util/QLog.java','rootbeerlib/src/main/java/com/scottyab/rootbeer/util/Utils.java','rootbeerlib/src/test/java/com/scottyab/rootbeer/RootBeerTest.java',
    'app/src/androidTest/java/com/scottyab/rootbeer/ApplicationTest.java','rootbeerlib/src/androidTest/java/com/scottyab/rootbeer/ApplicationTest.java','app/src/main/java/com/scottyab/rootchecker/Const.java','app/src/main/java/com/scottyab/rootchecker/MainActivity.java',
    'app/src/main/java/com/scottyab/rootchecker/RootCheck.java','app/src/main/java/com/scottyab/rootchecker/RootCheckNative.java','app/src/main/java/com/scottyab/rootchecker/util/QLog.java' ]

# Map files to indices from 0 to 16
FileI = {file: idx for idx, file in enumerate(Jfile)}

# Function to get commits for a file in a repo
def GC(repo, path):
    url = f"https://api.github.com/repos/{repo}/commits"
    par = {'path': path}
    Res = requests.get(url, headers=head, params=par)
    return Res.json() if Res.status_code == 200 else []

# Fetch commit data for all Java files
Fetched = []
for Jvf in Jfile:
    commits = GC('scottyab/rootbeer', Jvf)
    for commit in commits:
        author = commit['commit']['author']['name']
        date = commit['commit']['author']['date']
        Fetched.append({'file': Jvf, 'author': author, 'date': date})

# Process commit data for scatter plot
ProcessD = datetime.strptime('2015-01-01', '%Y-%m-%d')  
week = [(datetime.strptime(entry['date'], '%Y-%m-%dT%H:%M:%SZ') - ProcessD).days / 7 for entry in Fetched]
NumF = [FileI[entry['file']] for entry in Fetched]
Auth = [entry['author'] for entry in Fetched]

# Count the number of commits per author
commit_count_per_author = Counter(Auth)

# Sort authors by the number of commits (highest to lowest)
sorted_authors_by_commits  = sorted(commit_count_per_author , key=commit_count_per_author .get, reverse=True)

# Assign each author a unique color index
author_color_mapping  = {author: i for i, author in enumerate(sorted_authors_by_commits )}

# Generate a list of color indices for each author in the commit history
color_indices_per_author  = [author_color_mapping [author] for author in Auth]

# Plot scatter plot
plt.scatter(NumF, week, c=ColorIn, cmap='tab10', s=100, alpha=0.8)  

# Set axis limits and labels
plt.xlim(-1, 17)  
plt.ylim(0, 370)  
plt.xlabel('Files')
plt.xticks(ticks=range(len(Jfile)), labels=range(len(Jfile)))
plt.ylabel('Weeks')
plt.title('Files Touched by Authors')

# Colorbar with sorted commit counts in reverse
colorbar = plt.colorbar(ticks=range(len(SortAuth)), label='The Number of Commits', orientation='vertical')
colorbar.set_ticks(range(len(SortAuth)))
colorbar.set_ticklabels(list(reversed([NumberOFA[author] for author in SortAuth])))

plt.show()
