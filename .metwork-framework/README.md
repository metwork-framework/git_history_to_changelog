## What is it?

**GHTC** (**G**it **H**istory **T**o **C**hangelog) is yet another tool to generate a
changelog from git history (with [conventional commit spec](https://www.conventionalcommits.org/)).

## Why another tool?

Just because we didn't find an existing tool matching our needs.

## How to use it?

```console
Usage: ghtc [OPTIONS] REPO_ROOT

Arguments:
  REPO_ROOT  the fullpath to the git repository  [required]

Options:
  --tags-regex TEXT               regex to select tags to show on changelog
                                  [default: ^v[0-9]]

  --starting-rev TEXT             starting revision
  --remove-duplicates-entries / --no-remove-duplicates-entries
                                  if True, remove duplicate entries  [default:
                                  True]

  --unreleased / --no-unreleased  if True, add a section about unreleased
                                  changes  [default: True]

  --include-type TEXT             include (only) given conventional types in
                                  changelog (can be used multiple times, all
                                  types by default), available types: other,
                                  build, chore, style, ci, refactor, test,
                                  docs, perf, fix, feat  [default: ]

  --title TEXT                    [default: CHANGELOG]
  --unreleased-title TEXT         [default: [Unreleased]]
  --help                          Show this message and exit.
```

The generated CHANGELOG is sent to standard output.
