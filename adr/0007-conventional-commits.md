# 7. Enforce conventional commit style

Date: 2019-11-08

## Status

Accepted

## Context

We always wanted to have a consistent commit message styling, we used coala's CommitBear to help with
this task but besides just a bit more clarity in the commit history, it doesn't bring that much value.

Now that we'll be getting rid of coala in favour of pre-commit hooks, we need an alternative solution,
and we can use this change to also step up our game regarding commit messages.

## Decision

We will use the [conventional commits](https://www.conventionalcommits.org) convention for writing our commit messages
from now on. Besides forcing us to keep a consistent commit message styling, it will also bring much
more value, like:

* Automatically generating CHANGELOGs
* Automatically determining a semantic version bump (based on the types of commits landed)
* Communicating the nature of changes to teammates, the public, and other stakeholders
* Having different CI steps based on the nature of the commits added to the MR
* Having insights about how much time/effort is spent on the different areas of the development

## Consequences

We will be enforcing the conventional commit style with a CI job as the first step, and once we'll
replace coala with pre-commit we will be able to also run it locally before committing.
