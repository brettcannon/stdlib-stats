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
        elif item.is_dir() and item.name not in {"clinic", "test", "tests", "idle_test"}:
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
            elif item.name in {"addrinfo.h", "getaddrinfo.c", "getnameinfo.c",
                               "socketmodule.c", "socketmodule.h"}:
                add_path("_socket", item)
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
            elif item.stem == "signalmodule":
                add_path("_signal", item)
            elif item.name == "symtablemodule.c":
                add_path("_symtable", item)
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
            if item.name in {"_xxtestfuzz", "clinic"}:
                continue
            elif item.name == "expat":
                add_directory("xml", item)
            elif item.name == "_sqlite":
                add_directory("_sqlite3", item)
            elif item.name == "cjkcodecs":
                for subitem in item.iterdir():
                    if subitem.stem in MAPPING:
                        add_path(subitem.stem, subitem)
                    elif f"_{subitem.stem}" in MAPPING:
                        add_path(f"_{subitem.stem}", subitem)
                add_directory("encodings", item)
            elif item.name in MAPPING:
                add_directory(item.name, item)
            else:
                raise ValueError(f"don't know what to do with {item!r}")
        else:
            raise ValueError(f"don't recognize what {item!r} is")

    for module, paths in MAPPING.items():
        if module == "_ast":
            paths.append("Python/Python-ast.c")
        elif module == "_imp":
            paths.append("Python/import.c")
        elif module == "_msi":
            paths.append("PC/_msi.c")
        elif module == "_string":
            paths.append("Objects/unicodeobject.c")
        elif module == "_warnings":
            paths.append("Python/_warnings.c")
        elif module == "builtins":
            paths.append("Python/bltinmodule.c")
        elif module == "marshal":
            paths.append("Python/marshal.c")
        elif module == "msvcrt":
            paths.append("PC/msvcrtmodule.c")
        elif module == "sys":
            paths.append("Python/sysmodule.c")
        elif module == "winreg":
            paths.append("PC/winreg.c")
        elif module == "winsound":
            paths.append("PC/winsound.c")
        elif module == "_posixshmem":
            rel_path = "Modules/_multiprocessing/posixshmem.c"
            paths.append(rel_path)
            MAPPING["_multiprocessing"].remove(rel_path)
        elif not paths:
            raise ValueError("not paths for", module)

    for file_paths in MAPPING.values():
        file_paths.sort()

    with open("file_map.json", "w", encoding="utf-8") as file:
        json.dump(MAPPING, file, sort_keys=True, indent=2)
