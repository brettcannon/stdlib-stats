"""Create file_map.json.

The keys are module names and the values are a list of files that make up that
module.
"""

import json
import os
import pathlib
import sys


REPO = repo=pathlib.Path(sys.argv[1])
with open("module_names.json", "r", encoding="utf-8") as file:
    MAPPING = {name: [] for name in json.load(file)}

def relative_path(path):
    return path.relative_to(REPO).as_posix()


def add_path(module, path):
    MAPPING[module].append(relative_path(path))


def add_directory(module, path):
    """Add files founds in *path* with *extensions* to *found*."""
    for item in path.iterdir():
        if item.is_file():
            add_path(module, item)
        elif item.is_dir() and item.name != "clinic":
            add_directory(module, item)


if __name__ == "__main__":
    for item in (repo / "Lib").iterdir():
        if item.is_file():
            if item.suffix != ".py" or item.name == "__phello__.foo.py":
                continue
            add_path(item.stem, item)
        elif item.is_dir():
            if item.name in {"test", "site-packages"}:
                continue
            else:
                add_directory(item.name, item)
        else:
            raise ValueError(f"don't recognize what {item!r} is")

    for item in (REPO / "Modules").iterdir():
        if item.is_file():
            if item.name in {"README", "Setup", "makesetup", "getpath.c",
                             "config.c.in", "getbuildinfo.c", "main.c",
                             "gc_weakref.txt", "testcapi_long.h"}:
                continue
            if item.name.startswith("xx") or item.name.startswith("_test"):
                continue
            elif item.name in {"addrinfo.h", "getaddrinfo.c", "getnameinfo.c"}:
                add_path("socket", item)
            elif item.stem == "sre_lib":
                add_path("_sre", item)
            elif item.stem == "rotatingtree":
                add_path("_lsprof", item)
            elif item.stem == "_hashopenssl":
                add_path("_hashlib", item)
            elif item.name in {"ld_so_aix.in", "makexp_aix"}:
                add_path("_aix_support", item)
            elif item.stem == "_math":
                for module in ["math", "cmath"]:
                    add_path(module, item)
            elif item.name == "_ssl_data.h":
                add_path("_ssl", item)
            elif item.name == "_scproxy.c":
                add_path("urllib", item)
            elif item.name in {"unicodedata_db.h", "unicodename_db.h"}:
                add_path("unicodedata", item)
            elif item.name == "tkappinit.c":
                add_path("_tkinter", item)
            elif item.name == "overlapped.c":
                for module in ["_winapi", "asyncio"]:
                    add_path(module, item)
            elif item.name == "winreparse.h":
                for module in ["_winapi", "nt"]:
                    add_path(module, item)
            elif item.name == "sre.h":
                add_path("_sre", item)
            elif item.stem in MAPPING:
                add_path(item.stem, item)
            elif item.stem.endswith("module"):
                name = item.stem.removesuffix("module")
                if name in MAPPING:
                    module = name
                elif f"_{name}" in MAPPING:
                    module = f"_{name}"
                else:
                    raise ValueError(item)
                add_path(module, item)
            else:
                raise ValueError(f"don't know what to do with {item!r}")
        elif item.is_dir():
            # XXX walk directories
            pass
        else:
            raise ValueError(f"don't recognize what {item!r} is")

    for file_paths in MAPPING.values():
        file_paths.sort()

    with open("file_map.json", "w", encoding="utf-8") as file:
        json.dump(MAPPING, file, sort_keys=True, indent=2)
