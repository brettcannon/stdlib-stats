"""Validate data in private_modules.json.

Keys are a list of all public/documented modules. The values are the lists of
private/non-public modules that the public module relies on.
"""

import json
import pathlib
import sys

with open("module_names.json", "rb") as file:
    module_names = frozenset(json.load(file))


repo_location = pathlib.Path(sys.argv[1])
library_docs = repo_location / "Doc" / "library"
public_modules = {
    "lib2to3",  # In 2to3.rst
    "this",  # Easter egg
    "antigravity",  # Easter egg
    "cProfile",  # In profile.rst
    "pstats",  # In profile.rst
    "turtledemo",  # In turtle.rst
    "encodings",  # In codecs.rst
    "idlelib",  # For IDLE
    "_xxsubinterpreters",  # For testing subinterpreters
}

for item in library_docs.iterdir():
    filename = item.name
    if not filename.endswith(".rst") or filename == "pyexpat.rst":
        continue

    name = filename.partition(".")[0]
    if name in module_names:
        public_modules.add(name)

public_modules = frozenset(public_modules)
private_modules = module_names - public_modules

with open("private_modules.json", "rb") as file:
    module_mapping = json.load(file)
written_public_modules = frozenset(module_mapping.keys())
if diff := written_public_modules - public_modules:
    print("Modules recorded as public but are private:", diff)
    sys.exit(1)
elif diff := public_modules - written_public_modules:
    print("Public modules not recorded:", diff)

written_private_modules = frozenset(
    name for names in module_mapping.values() for name in names
)
if diff := private_modules - written_private_modules:
    print("Private modules not recorded:", diff)
elif diff := written_private_modules - private_modules:
    print("Modules misclassified as private:", diff)
