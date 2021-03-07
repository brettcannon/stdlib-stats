import json
import pathlib
import sys

repo = pathlib.Path(sys.argv[1])
library_docs = repo / "Doc" / "library"
index_file = library_docs / "index.rst"

with (library_docs / "index.rst").open("r", encoding="UTF-8") as file:
    index_lines = file.readlines()

category_filenames = []
for line in index_lines:
    cleaned_line = line.strip()
    if cleaned_line.endswith(".rst"):
        category_filenames.append(cleaned_line)

with open("module_names.json", "r", encoding="UTF-8") as file:
    module_names = frozenset(json.load(file))

categories = {}
found = set()
for category_filename in category_filenames:
    category_file = library_docs / category_filename
    category_name = category_filename.removesuffix(".rst")
    print("Category:", category_name)
    with category_file.open("r", encoding="UTF-8") as file:
        category_lines = file.readlines()
    members = set()
    for line in category_lines:
        cleaned_line = line.strip()
        if not cleaned_line.endswith(".rst"):
            continue
        # Handles both suffix and submodules.
        doc_name = cleaned_line.partition(".")[0]
        if doc_name not in module_names:
            print(doc_name, "?")
        else:
            members.add(doc_name)
            found.add(doc_name)
            if doc_name == "profile":
                for name in ["cProfile", "pstats"]:
                    members.add(name)
                    found.add(name)
            elif doc_name == "codecs":
                members.add("encodings")
                found.add("encodings")
            elif doc_name == "typing":
                members.add("lib2to3")
                found.add("lib2to3")
            elif doc_name == "tkinter":
                members.add("idlelib")
                found.add("idlelib")
            elif doc_name == "turtle":
                members.add("turtledemo")
                found.add("turtledemo")
    if members:
        categories[category_name] = sorted(members)

with open("private_modules.json", "r", encoding="UTF-8") as file:
    module_visibility = json.load(file)
private_modules = {name for modules in module_visibility.values() for name in modules}

categories["eastereggs"] = ["antigravity", "this"]
found.update(categories["eastereggs"])
categories["experiment"] = ["_xxsubinterpreters"]
found.add("_xxsubinterpreters")

if diff := module_names - private_modules - found:
    print("Public modules with no category:", sorted(diff))

with open("categories.json", "w", encoding="UTF-8") as file:
    json.dump(categories, file, sort_keys=True, indent=2)
