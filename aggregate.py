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

    # XXX file_map.json

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


    with PATH.open("w", newline="", encoding="utf-8") as file:
        columns = ["name", "required", "category", "project_count"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data.values())

    with CATEGORY_USAGE_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["category", "project_count"])
        writer.writerows((category, len(users))
                         for category, users in category_used_by.items())


if  __name__ == "__main__":
    main()
