import json
import operator
import sys

import git  # gitpython


with open("file_map.json", "rb") as file:
    file_map = json.load(file)

file_paths = []
for paths in file_map.values():
    file_paths.extend(paths)
file_paths.sort()

file_stats = {}
repo = git.Repo(sys.argv[1])
for path in file_paths:
    print(path)
    commits = list(repo.iter_commits(paths=path))
    commits.sort(key=operator.attrgetter("committed_date"))
    file_stats[path] = {
        "oldest": commits[0].committed_datetime.date().isoformat(),
        "newest": commits[-1].committed_datetime.date().isoformat(),
        "sha": [commit.hexsha for commit in commits]
    }


with open("commit_stats.json", "w", encoding="utf-8") as file:
    json.dump(file_stats, file, indent=2, sort_keys=True)
