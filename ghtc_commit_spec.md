# GHTC commit specification

## Why another specification?

To be able to have long changelog entries in git commit messages
which should be wrapped at 72 characters for body and 50 characters for title.

## Format

Use `<changelog>{TYPE}: your changelog entry</changelog>`.

"your changelog entry" is a free string and can be wrapped on multiple lines but
`<changelog>` and `</changelog>` tags must not be cut by a new line character.

*note: carriage returns will be stripped from "your changelog entry" string.*

`{TYPE}` can be:

- a [keepachangelog](https://keepachangelog.com) type:
  - `added`
  - `fixed`
  - `changed`
  - `deprecated`
  - `removed`
  - `security`
  - `performance`
  - (or) `other`
- (or) a [conventional commit](https://www.conventionalcommits.org) type:
  - `feat`: mapped to `added`
  - `fix`: mapped to `fixed`
  - `build`, `chore`, `ci`, `doc`, `docs`, `style`, `refactor`, `test`, `tests`: mapped to `other`
  - `security`: mapped to `security`
  - `perf`, `perfs`: mapped to `performance`
  - `deprecated`: mapped to `deprecated`
  - `removed`: mapped to `removed`

You can use several `<changelog>{TYPE}: {MESSAGE}</changelog>` blocks in the same commit message
(useful for "squashed commits" for example).
