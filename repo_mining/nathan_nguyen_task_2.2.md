### Documentation: GitHub File Commit Analyzer

#### **Purpose**
This script is designed to interact with the GitHub API to analyze the file history of a given GitHub repository. It counts and categorizes all files with specific extensions that have been modified in the repository's commits. Additionally, it tracks the author and date of modification for each relevant file. The goal is to build a dictionary of files that provides information on the authors who modified them and when the changes occurred.

#### **How the Script Works**

1. **Setup**: 
   - The script first checks if a directory named `data` exists, and if not, it creates it. This is a placeholder for potential file storage or logging but is not used further in the script.
   - It then imports the required modules: 
     - `json`: for handling JSON responses from the GitHub API.
     - `requests`: for making HTTP requests to the GitHub API.
     - `os`: for interacting with the operating system to check for and create directories.

2. **GitHub Authentication (`github_auth`)**: 
   - This function takes three parameters:
     - `url`: the GitHub API endpoint to request data from.
     - `lsttoken`: a list of GitHub personal access tokens (useful when making multiple authenticated requests).
     - `ct`: a counter used to rotate between tokens.
   - It sends a GET request to the specified URL, using the token from the list. The response is returned as a JSON object, and the token counter (`ct`) is incremented.

3. **Commit Analyzer (`countfiles`)**:
   - This function takes four parameters:
     - `dictfiles`: a dictionary that stores the list of files and corresponding commit information (author and date).
     - `lsttokens`: a list of GitHub authentication tokens.
     - `repo`: the GitHub repository to analyze (in the format `owner/repository`).
   - The function iterates over multiple pages of commits retrieved from the GitHub API (using pagination) and examines each commit:
     - It extracts the commit SHA (unique identifier for the commit), author name, and commit date.
     - It then fetches the details of the commit using its SHA to retrieve the list of files modified in that commit.
     - If a file has one of the specified extensions (e.g., `.java`, `.cpp`, `.kt`), the script records the author's name and the commit date.
     - The information is stored in a dictionary (`dictfiles`), where each file is a key, and the value is a list of commit details (author and date).

4. **Supported File Extensions**:
   - The script is set to analyze files with specific extensions related to programming languages such as Java (`.java`), Kotlin (`.kt`), and C++ (`.cpp`).
   - The supported extensions are stored in the `language_extensions` set.

5. **Execution Flow**:
   - The function `countfiles()` is called with the following parameters:
     - `dictfiles`: an empty dictionary to store results.
     - `lstTokens`: a list of GitHub tokens (empty in the script, but should be filled by the user).
     - `repo`: a GitHub repository (in this case, `scottyab/rootbeer`, but other commented-out repos are also suggested).
   - After fetching and analyzing the data, the total number of relevant files is printed, and for each file, the author and modification date are printed in a user-friendly format.

#### **Key Components**:
1. **Authentication Handling**:
   - The script uses GitHub personal access tokens for authenticated API requests, which is essential to avoid rate limits on GitHub's API, especially for repositories with a large number of commits.
   - The `ct` counter rotates through the tokens, allowing the script to continue making authenticated requests even when one token hits the rate limit.

2. **Commit Data Processing**:
   - The script fetches commits in batches (100 commits per page) and iterates through each commit to gather relevant information.
   - It then processes the files in each commit, filtering out files that don’t match the specified extensions and storing details of the relevant ones.

3. **Error Handling**:
   - Basic error handling is implemented using `try`-`except` blocks to catch and suppress exceptions. If an error occurs during data fetching, it is printed to the console, and the script exits with an error code.

4. **Example Use Case**:
   - This script could be used for code analysis to determine who worked on specific files, how often those files were modified, or to investigate how the codebase evolved over time.
   - By focusing on particular file types (e.g., `.java`, `.cpp`), it allows you to narrow the analysis to specific parts of the codebase.

#### **How to Use**:
- Fill in the `lstTokens` list with your GitHub personal access tokens.
- Set the desired repository to analyze in the `repo` variable.
- Run the script, and it will print the total number of relevant files and a detailed log of which authors modified each file and when.
