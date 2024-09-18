import numpy as np
import matplotlib.pyplot as plt


filename = "data/file_rootbeer_authorsFileTouches.csv"

data = np.genfromtxt(filename, delimiter=",", dtype=None, encoding="utf-8", names=True)

filenames = data['Filename']
authors = data['Author']
week_numbers = data['Week_Number']


unique_filenames = np.unique(filenames)
filename_idx = {filename: idx for idx,filename in enumerate(unique_filenames)}


unique_authors = np.unique(authors)
author_commit_counts = {author: np.sum(authors==author) for author in unique_authors}


'''
#project commits per developer
plt.figure(figsize=(10,5))
plt.bar(author_commit_counts.keys(), author_commit_counts.values(), color='blue')
plt.xticks(rotation=45, ha="right")
#plt.ylabel("Number of Commits")
#plt.xlabel("Developers")
'''

#Project progress by the week.
plt.figure(figsize=(14,8))
colors = plt.get_cmap('tab10')

unique_authors = np.unique(authors)
author_colors = {author: colors(i / len(unique_authors)) for i, author in enumerate(unique_authors)}


for author in unique_authors:
    mask = (authors == author)
    x_values = np.array([filename_idx[filename] for filename in filenames[mask]])
    y_values = week_numbers[mask]
    plt.scatter(x_values, y_values, label=author, color=author_colors[author])


plt.xticks(ticks=list(filename_idx.values()), labels=[str(idx) for idx in range(len(unique_filenames))], rotation=0)
plt.xlabel("File")
plt.ylabel("Weeks")
plt.legend(title="Authors", bbox_to_anchor=(1.05,1), loc="upper left")









plt.tight_layout()

#plt.savefig("data/commits_developer_week.png", format="png", dpi=300)
plt.show()



