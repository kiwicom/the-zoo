# 5. Use Fomantic UI

Date: 2019-10-21

## Status

Accepted

## Context

We were using [Semantic UI](https://semantic-ui.com/), as it's an open source and robust framework.
It has a wide range of components, it's easily customizable and it uses modern
approaches. It's really well documented, although usually documentation is not even
needed as it's really intuitive to work with it.

Unfortunately, the project is not as maintained as before, and the development of new components
is stale.

[Fomantic UI](https://fomantic-ui.com/) picked up where Semantic UI left, and offers a drop-in replacement,
with a higher quantity of components, and the development can be considered active.

## Decision

We will use [Fomantic UI](https://fomantic-ui.com/), the community fork of `Semantic UI`. The
support on this project is fast and on point, and the roadmap aligns nicely with our development,
as the maintainers are planning to offer first party support for Vue components, and ditch the
jQuery dependency.

## Consequences

We will stop using the unmaintained [Semantic UI](https://semantic-ui.com/)
framework and we will use [Fomantic UI](https://fomantic-ui.com/)
