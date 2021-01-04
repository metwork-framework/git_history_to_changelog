# git_history_to_changelog (ghtc)

## What is it?

**GHTC** (**G**it **H**istory **T**o **C**hangelog) is yet another tool to generate a
changelog from git history (with [conventional commit spec](https://www.conventionalcommits.org/)).

## Why another tool?

Just because we didn't find an existing tool matching our needs.

## How to use it?

```console
Usage: ghtc [OPTIONS] REPO_ROOT

Arguments:
  REPO_ROOT  [required]

Options:
  --tags-regex TEXT               [default: ^v[0-9]]
  --starting-rev TEXT
  --remove-duplicates-entries / --no-remove-duplicates-entries
                                  [default: True]
  --unreleased / --no-unreleased  [default: True]
  --include-type TEXT             [default: ]
  --title TEXT                    [default: CHANGELOG]
  --unreleased-title TEXT         [default: [Unreleased]]
  --help                          Show this message and exit.
```

The generated CHANGELOG is sent to standard output.
