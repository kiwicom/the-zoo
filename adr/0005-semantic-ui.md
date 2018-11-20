# 5. Use Semantic UI

Date: 2018-06-06

## Status

Accepted

## Context

We were using [Material Design Lite](https://getmdl.io/) as our front-end CSS framework.
The selection of offered components is quite limited and most of them just include
the basic logic. We have to dedicate a big amount of time writing front-end code and it's
hard to compose the provided components as they are mainly meant to be used in a single
way because of the strong Material design guidelines.

We aim to focus on logic, not on developing front-end components. We need a solution
that can offer a high number of already built components. The components should be
easy to configure and to compose together as our UI sometimes needs components that
are not contemplated on the common guidelines.

## Decision

We will use [Semantic UI](https://semantic-ui.com/), as it's an open source and robust framework.
It has a wide range of components, it's easily customizable and it uses modern
approaches. It's really well documented, although usually documentation is not even
needed as it's really intuitive to work with it.

## Consequences

We will stop using the old and deprecated [Material Design Lite](https://getmdl.io/)
framework and all the front-end will be rewritten using [Semantic UI](https://semantic-ui.com/)
