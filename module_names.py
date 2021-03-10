#!/usr/bin/python3.10
"""Dump `sys.stdlib_module_names` to `module_names.json`."""

import json
import sys

module_names = set(sys.stdlib_module_names)
# https://bugs.python.org/issue43456
module_names.remove("_xxsubinterpreters")

with open("module_names.json", "w", encoding="utf-8") as file:
    json.dump(sorted(module_names), file, indent=2)
