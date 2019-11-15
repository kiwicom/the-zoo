# 3. Save ADRs into adr dir

Date: 2018-07-09

## Status

Accepted

## Context

We need dir to save ADRs into.

## Decision

We will save ADRs into top level `adr` dir. Another option was to put them into `docs/adr`
along with Sphinx docs, but they might be bit hidden there.

## Consequences

We have documentation in two dirs - `adr` and `docs`. But they are different kind of documentation,
so should not matter.
