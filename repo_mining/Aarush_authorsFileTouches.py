import json
import csv
import os
import requests

# My Gethub token
MyTok = "asdfasdfa"  

# function to get commits
def RetriveC(repo, path, tok):
    url = "https://github.com/scottyab/rootbeer"+repo+ "/commits"
    heads = {'Authorization': 'token '+tok}
    resp = requests.get(url, headers=heads, params={'path': path})
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        return []

def History(commits):
    info = []
    for c in commits:
        author=c['commit']['author']['name'] if 'commit' in c and 'author' in c['commit'] else None
        date=c['commit']['author']['date'] if 'commit' in c and 'author' in c['commit'] else None
        if author and date:
            info.append((author, date))
    return info

def CAD(repo, files, tok):
    all_data = {}
    for f in files:
        hist = RetriveC(repo, f, tok)
        all_data[f] = History(hist)
    return all_data

if __name__ == "__main__":
    target = 'scottyab/rootbeer'
    Jsv = ['rootbeerlib/src/main/java/com/scottyab/rootbeer/RootBeerNative.java','app/src/main/java/com/scottyab/rootbeer/sample/CheckRootTask.java','app/src/main/java/com/scottyab/rootbeer/sample/MainActivity.java',
    'app/src/main/java/com/scottyab/rootbeer/sample/TextViewFont.java','rootbeerlib/src/main/java/com/scottyab/rootbeer/Const.java', 'rootbeerlib/src/main/java/com/scottyab/rootbeer/RootBeer.java',
    'rootbeerlib/src/main/java/com/scottyab/rootbeer/util/QLog.java','rootbeerlib/src/main/java/com/scottyab/rootbeer/util/Utils.java','rootbeerlib/src/test/java/com/scottyab/rootbeer/RootBeerTest.java',
    'app/src/androidTest/java/com/scottyab/rootbeer/ApplicationTest.java','rootbeerlib/src/androidTest/java/com/scottyab/rootbeer/ApplicationTest.java','app/src/main/java/com/scottyab/rootchecker/Const.java','app/src/main/java/com/scottyab/rootchecker/MainActivity.java',
    'app/src/main/java/com/scottyab/rootchecker/RootCheck.java','app/src/main/java/com/scottyab/rootchecker/RootCheckNative.java','app/src/main/java/com/scottyab/rootchecker/util/QLog.java' ]
    # Get commit information
    commit_info = CAD(target, Jsv, MyTok)
    
    # Print commit info
    for file, data in commit_info.items():
        print("Commit Log for "+file)
        for a, d in data:
            print(a+" did a commit on "+d)
        print("-------------------------------------------------")