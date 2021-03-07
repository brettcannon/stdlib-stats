import ast
import json
import os
import pathlib
import sys
from typing import Any, Container


class ImportVisitor(ast.NodeVisitor):

    def __init__(self, looking_for: Container[str]):
        self._looking_for = looking_for
        self.found = set()

    def _handle_name(self, full_name: str):
        name = full_name.partition(".")[0]
        if name in self._looking_for:
            self.found.add(name)

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            self._handle_name(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if not node.level and node.module:
            self._handle_name(node.module)


with open("module_names.json", "r", encoding="UTF-8") as file:
    module_names = frozenset(json.load(file))


found_in_projects = {}
# Directory containing project directories.
project_count = 0
for project_dir in pathlib.Path(sys.argv[1]).iterdir():
    if not project_dir.is_dir() or "-" not in project_dir.name:
        continue
    found_modules = set()
    # Traverse through project directory.
    for dirpath, dirnames, filenames in os.walk(project_dir):
        directory = pathlib.Path(dirpath)
        for filename in filenames:
            file_path = directory / filename
            if file_path.suffix == ".py":
                with file_path.open("rb") as source_file:
                    raw_source = source_file.read()
                try:
                    nodes = ast.parse(raw_source)
                except (SyntaxError, ValueError):
                    continue
                visitor = ImportVisitor(module_names)
                try:
                    visitor.visit(nodes)
                except RecursionError:
                    pass
                found_modules |= visitor.found
    found_in_projects[project_dir.name] = frozenset(found_modules)
    project_count += 1
    if not project_count % 100:
        print(project_count)

project_results = {project: sorted(modules)
                   for project, modules in found_in_projects.items()}

with open("usage.json", "w", encoding="UTF-8") as file:
    json.dump(project_results, file, sort_keys=True, indent=2)
