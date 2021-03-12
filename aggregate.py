import csv
import json
import pathlib


PATH = pathlib.Path("stdlib.csv")


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

    used_by = {module: set() for module in data}
    with open("usage.json", "rb") as file:
        usage = json.load(file)
    for project, modules in usage.items():
        for module in modules:
            public_name = private_to_public[module]
            used_by[public_name].add(project)
    for module, projects in used_by.items():
        data[module]["project_count"] = len(projects)

    with PATH.open("w", newline="", encoding="utf-8") as file:
        columns = ["name", "category", "project_count"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data.values())


if  __name__ == "__main__":
    main()
