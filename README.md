# stdlib-stats

Various statistics on Python's standard library.

See `stats.ipynb` for charts that show the data in various ways.

You can also run an interactive Jupyter session using Binder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/brettcannon/stdlib-stats/main?filepath=stats.ipynb)

## Organized data

`stdlib.csv` contains various details about the modules in the stdlib. The table
is built using various JSON files found in this repository (discussed below).
To tweak how various things are treated, you can edit the JSON files and
run `aggregate.py` to update it accordingly.

The `category_usage.csv` counts the number of projects which use a specify
module category. It also tallies all the commits the category is made up of.

The `stats.ipynb` is a Jupyter notebook which contains various charts that try
to analyze the data from the CSV in various ways.

## Raw data

### Map module to public module
Public availability is (mostly) determined by documentation existing in
`Doc/library/`.

`private_modules.json` maps public modules to any private modules they depend
on. For modules that are "cheating" and using private modules directly instead
of their equivalent public API, they not listed as a dependent
(e.g. `multiprocessing` directly using `_weakrefset` instead of going through
`weakref`).

### Map file to module
Ignores Argument Clinic files and tests, but includes header files.

`file_map.json` maps module name to relative file paths in a git clone.

### Modules required to start Python
`required.json` lists the modules required to start Python (based on
`python -v -S -c pass`).

### Usage of a module in the public
`usage.json` lists the modules used by the 4000 most downloaded projects
over the past year on PyPI.

The list of projects is listed in `top-pypi-packages-365-days.json` as fetched
from [Top PyPI Packages](https://hugovk.github.io/top-pypi-packages/). The
projects are downloaded by
[isidentical/syntax_test_suite](https://github.com/isidentical/syntax_test_suite).


### Grouped by category
`categories.json` groups modules by category accoring to the
[library index](https://docs.python.org/3/library/index.html).

The `__future__` module is specially treated and put in its own category.

### Commit stats per file
`commit_stats.json` tracks the oldest, newest, and SHA hashes of all the commits
made on a specific file.
