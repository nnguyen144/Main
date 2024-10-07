import json  # Importing the JSON module to handle JSON data
import csv   # Importing the CSV module (not used in the code, but imported)
import os    # Importing the OS module (not used in the code, but imported)
import requests  # Importing the Requests library to make HTTP requests

# My GitHub token
MyTok = "NILL"  # Replace with your GitHub personal access token

""" Function to retrieve commits from the specified repository """
def RetriveC(repo, path, tok):
    # 1) Construct the URL to access the commits for the specified repo and path
    # 2) Set up the authorization headers using the provided token
    url = "https://github.com/scottyab/rootbeer" + repo + "/commits"
    heads = {'Authorization': 'token ' + tok}
    
    # 3) Send a GET request to the constructed URL with the headers and parameters
    resp = requests.get(url, headers=heads, params={'path': path})
    
    # 4) Check if the response is successful
    # 4a) Return the response JSON data as a Python object
    # 4b) Return an empty list if the request failed 
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        return []

""" Function to extract commit author and date information from commit data """
def History(commits):
    # 1) Initialize a list to store commit information
    info = []  

    # 2) Iterate over each commit in the commits list
    #    Extract the author's name and commit date, handling potential missing data
    #    If both author and date are present, append to info list
    for c in commits:  
        author = c['commit']['author']['name'] if 'commit' in c and 'author' in c['commit'] else None
        date = c['commit']['author']['date'] if 'commit' in c and 'author' in c['commit'] else None
        
        if author and date:
            info.append((author, date))

    # 3) Return the list of author and date tuples
    return info

""" Function to retrieve commit history for multiple files in a repository """
def CAD(repo, files, tok):
    # 1) Initialize a dictionary to hold commit data for all files
    all_data = {}  

    # 2) Iterate over each file in the provided list
    #    Get commit history for the current file
    #    Store the extracted history in the all_data dictionary
    for f in files:  
        hist = RetriveC(repo, f, tok)
        all_data[f] = History(hist)

    # 3) Return the dictionary containing commit data for all files
    return all_data  

""" Main execution block """
if __name__ == "__main__":

    # 1) Set the target repository
    target = 'scottyab/rootbeer' 
    # 2) Create list of file paths to track commit history
    Jsv = [
        'rootbeerlib/src/main/java/com/scottyab/rootbeer/RootBeerNative.java',
        'app/src/main/java/com/scottyab/rootbeer/sample/CheckRootTask.java',
        'app/src/main/java/com/scottyab/rootbeer/sample/MainActivity.java',
        'app/src/main/java/com/scottyab/rootbeer/sample/TextViewFont.java',
        'rootbeerlib/src/main/java/com/scottyab/rootbeer/Const.java',
        'rootbeerlib/src/main/java/com/scottyab/rootbeer/RootBeer.java',
        'rootbeerlib/src/main/java/com/scottyab/rootbeer/util/QLog.java',
        'rootbeerlib/src/main/java/com/scottyab/rootbeer/util/Utils.java',
        'rootbeerlib/src/test/java/com/scottyab/rootbeer/RootBeerTest.java',
        'app/src/androidTest/java/com/scottyab/rootbeer/ApplicationTest.java',
        'rootbeerlib/src/androidTest/java/com/scottyab/rootbeer/ApplicationTest.java',
        'app/src/main/java/com/scottyab/rootchecker/Const.java',
        'app/src/main/java/com/scottyab/rootchecker/MainActivity.java',
        'app/src/main/java/com/scottyab/rootchecker/RootCheck.java',
        'app/src/main/java/com/scottyab/rootchecker/RootCheckNative.java',
        'app/src/main/java/com/scottyab/rootchecker/util/QLog.java'
    ]
    
    # 3) Get commit information for the specified repository and files
    commit_info = CAD(target, Jsv, MyTok)

    # 4) Print the commit information for each file
    #       - Print the file name
    #       - Iterate through the commit data for the file AND
    #           - Print the author and date of each commit
    #       - Print a separator for readability
    for file, data in commit_info.items():
        print("Commit Log for " + file)  
        for a, d in data:  
            print(a + " did a commit on " + d)  
        print("-------------------------------------------------")  
