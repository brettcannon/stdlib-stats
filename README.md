# stdlib-stats

Various statistics on Python's standard library.

XXX stored to a sqlite3 database

## Map module to public module
Public availability is (mostly) determined by documentation existing in
`Doc/library/`.

`private_modules.json` maps public modules to any private modules they depend
on. For modules that are "cheating" and using private modules directly instead
of their equivalent public API, they not listed as a dependent
(e.g. `multiprocessing` directly using `_weakrefset` instead of going through
`weakref`).

## Map file to module
Ignores Argument Clinic files and tests, but includes header files.

`file_map.json` maps module name to relative file paths in a git clone.

## Module details

- `required.json` lists the modules required to start Python (based on
  `python -v -S -c pass`).
- `usage.json` lists the modules used by the 4000 most downloaded projects
   over the past year according to `top-pypi-packages-365-days.json` from
   [Top PyPI Packages](https://hugovk.github.io/top-pypi-packages/) and
   downloaded by
   [isidentical/syntax_test_suite](https://github.com/isidentical/syntax_test_suite).

XXX

- Commit details (first commit, total commits, commits since released)
- Release and date the module was introduced (inferred by the firt date of a
  `X.Y.0` release that comes after the earliest commit of any file for a module)
- Number of open PRs (based on files edited by PRs targeting `master`)
- Category according to https://docs.python.org/3/library/

XXX https://en.wikipedia.org/wiki/History_of_Python#Table_of_versions
