# stdlib-stats
Various statistics on Python's standard library

## Stats to collect
- Release and date the module was introduced (inferred by the firt date of a `X.Y.0` release that comes after the earliest commit of any file for a module)
- Required to start CPython (based on `python -v -S -c "pass"`)
- Number of open PRs (based on files edited by PRs targeting `master`)
- Number of commits (based on total commits for all files that make up the module)
- Number of hits in some public search tool (?)

## Tables
### Map module to public module
Public availability is determined by documentation existing in `Doc/library/`.

### Map file to module
Ignore Argument Clinic files, but includes header files.

### Module details
