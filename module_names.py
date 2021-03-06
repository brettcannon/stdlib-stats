#!/usr/bin/python3.10
"""Dump `sys.stdlib_module_names` to `module_names.json`."""

import json
import sys


with open("module_names.json", "w", encoding="utf-8") as file:
    json.dump(sorted(sys.stdlib_module_names), file, indent=2)
