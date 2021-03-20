import csv
import json
import pathlib


PATH = pathlib.Path("stdlib.csv")
CATEGORY_USAGE_PATH = pathlib.Path("category_usage.csv")

def main():

    with open("private_modules.json", "rb") as file:
        visibility = json.load(file)

    data = {module: {"name": module} for module in visibility}

    # For algorithmic simplicity, have every public module include itself as
    # "private".
    private_to_public = {}
    for module, private_modules in visibility.items():
        private_to_public[module] = module
        for private_module in private_modules:
            private_to_public[private_module] = module

    with open("categories.json", "rb") as file:
        categories = json.load(file)
    for category, modules in categories.items():
        for module in modules:
            data[module]["category"] = category
    category_data = {category: {"name": category} for category in categories}

    module_commit_stats = {}
    category_commit_stats = {}
    with open("file_map.json", "rb") as file:
        file_map = json.load(file)
    with open("commit_stats.json", "rb") as file:
        file_commit_stats = json.load(file)
    for module, files in file_map.items():
        public_module = private_to_public[module]
        category = data[public_module]["category"]
        module_stats = module_commit_stats.setdefault(public_module, {})
        for path in files:
            file_stats = file_commit_stats[path]
            module_stats.setdefault("sha", set()).update(file_stats["sha"])
            category_commit_stats.setdefault(category, set()).update(file_stats["sha"])
            if (newest := file_stats["newest"]) > module_stats.get("newest", "1900-01-01"):
                module_stats["newest"] = newest
            if (oldest := file_stats["oldest"]) < module_stats.get("oldest", "9999-01-01"):
                module_stats["oldest"] = oldest
    for module, stats in module_commit_stats.items():
        data[module]["oldest_commit"] = stats["oldest"]
        data[module]["newest_commit"] = stats["newest"]
        data[module]["commit_count"] = len(stats["sha"])
    for category, sha in category_commit_stats.items():
        category_data[category]["commits"] = len(sha)

    with open("pull_requests.json", "rb") as file:
        pull_requests = json.load(file)
    path_to_module = {}
    for module, paths in file_map.items():
        public_module = private_to_public[module]
        for path in paths:
            path_to_module[path] = public_module
    module_prs = {module: set() for module in data}
    category_prs = {category: set() for category in categories}
    for pr, paths in pull_requests.items():
        for path in paths:
            try:
                module = path_to_module[path]
            except KeyError:
                continue
            category = data[module]["category"]
            module_prs[module].add(pr)
            category_prs[category].add(pr)
    for module, prs in module_prs.items():
        data[module]["pr_count"] = len(prs)
    for category, prs in category_prs.items():
        category_data[category]["pr_count"] = len(prs)

    with open("required.json", "rb") as file:
        required_modules = json.load(file)
    for module in required_modules:
        public_module = private_to_public[module]
        data[public_module]["required"] = True
    for  module_data in data.values():
        if "required" not in module_data:
            module_data["required"] = False

    used_by = {module: set() for module in data}
    category_used_by = {category: set() for category in categories}
    with open("usage.json", "rb") as file:
        usage = json.load(file)
    for project, modules in usage.items():
        for module in modules:
            public_name = private_to_public[module]
            used_by[public_name].add(project)
            category_used_by[data[public_name]["category"]].add(project)
    for module, projects in used_by.items():
        data[module]["project_count"] = len(projects)
    for category, projects in category_used_by.items():
        category_data[category]["project_count"] = len(projects)


    with PATH.open("w", newline="", encoding="utf-8") as file:
        columns = ["name", "required", "category", "project_count",
                   "oldest_commit", "newest_commit", "commit_count", "pr_count"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data.values())

    with CATEGORY_USAGE_PATH.open("w", newline="", encoding="utf-8") as file:
        columns = ["name", "project_count", "commits", "pr_count"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(category_data.values())


if  __name__ == "__main__":
    main()
