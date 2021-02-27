# stdlib-stats

Various statistics on Python's standard library.

## Statistics

### Required for startup

Determined by whether the module is used to run `-S -c "pass"`.

### LOC

XXX

### Open PRs

XXX take into account module age

### Commits

XXX take into account module age

### Usage in the community

XXX

## Technical

### Connecting private modules to their public dependents

`private_modules.json` maps public modules to any private modules they depend
on. For modules that are "cheating" and using private modules directly instead
of their equivalent public API, they not listed as a dependent
(e.g. `multiprocessing` directly using `_weakrefset` instead of going through
`weakref`).

Data is verified via `private_modules.py`.

### Mapping paths to modules

XXX

### Counting LOC

XXX

### Module age

XXX

### Collecting module usage on GitHub

XXX

### Usage by the community

XXX
