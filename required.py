import json
import re
import subprocess
import sys

IMPORT_RE = re.compile(r"^import '?([^\s\.']+)'? #")

call = subprocess.run([sys.executable, "-v", "-S", "-c", "pass"],
                      capture_output=True, encoding="utf-8", check=True)

module_names = set()
for line in call.stderr.splitlines():
    if match := IMPORT_RE.match(line):
        name = match.groups()[0]
        if name.startswith("_frozen_importlib"):
            name = "importlib"
        module_names.add(name)
        print(name)

with open("required.json", "w", encoding="UTF-8") as file:
    json.dump(sorted(module_names), file, indent=2)
