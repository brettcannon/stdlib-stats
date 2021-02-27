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

Data is verified via `private_modules.py`.

## Map file to module
Ignores Argument Clinic files, but includes header files.

XXX

## Module details

- Release and date the module was introduced (inferred by the firt date of a
  `X.Y.0` release that comes after the earliest commit of any file for a module)
- Required to start CPython (based on `python -v -S -c "pass"`)
- Number of open PRs (based on files edited by PRs targeting `master`)
- Number of commits (based on total commits for all files that make up the module)
- Usage by public projects/repos count

XXX
