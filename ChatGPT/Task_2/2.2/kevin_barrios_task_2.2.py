import json  # Importing the JSON module to handle JSON data
import csv   # Importing the CSV module (not used in the code, but imported)
import os    # Importing the OS module (not used in the code, but imported)
import requests  # Importing the Requests library to make HTTP requests

# My GitHub token
MyTok = "NILL"  # Replace with your GitHub personal access token

# Function to retrieve commits from the specified repository
def RetriveC(repo, path, tok):
    # Construct the URL to access the commits for the specified repo and path
    url = "https://github.com/scottyab/rootbeer" + repo + "/commits"
    # Set up the authorization headers using the provided token
    heads = {'Authorization': 'token ' + tok}
    
    # Send a GET request to the constructed URL with the headers and parameters
    resp = requests.get(url, headers=heads, params={'path': path})
    
    # Check if the response is successful
    if resp.status_code == 200:
        # Return the response JSON data as a Python object
        return json.loads(resp.text)
    else:
        # Return an empty list if the request failed
        return []

# Function to extract commit author and date information from commit data
def History(commits):
    info = []  # Initialize a list to store commit information
    for c in commits:  # Iterate over each commit in the commits list
        # Extract the author's name and commit date, handling potential missing data
        author = c['commit']['author']['name'] if 'commit' in c and 'author' in c['commit'] else None
        date = c['commit']['author']['date'] if 'commit' in c and 'author' in c['commit'] else None
        
        # If both author and date are present, append to info list
        if author and date:
            info.append((author, date))
    return info  # Return the list of author and date tuples

# Function to retrieve commit history for multiple files in a repository
def CAD(repo, files, tok):
    all_data = {}  # Initialize a dictionary to hold commit data for all files
    for f in files:  # Iterate over each file in the provided list
        # Get commit history for the current file
        hist = RetriveC(repo, f, tok)
        # Store the extracted history in the all_data dictionary
        all_data[f] = History(hist)
    return all_data  # Return the dictionary containing commit data for all files

# Main execution block
if __name__ == "__main__":
    target = 'scottyab/rootbeer'  # Set the target repository
    # List of file paths to track commit history
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
    
    # Get commit information for the specified repository and files
    commit_info = CAD(target, Jsv, MyTok)

    # Print the commit information for each file
    for file, data in commit_info.items():
        print("Commit Log for " + file)  # Print the file name
        for a, d in data:  # Iterate through the commit data for the file
            print(a + " did a commit on " + d)  # Print the author and date of each commit
        print("-------------------------------------------------")  # Print a separator for readability
