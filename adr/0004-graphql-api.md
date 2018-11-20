# 4. GraphQL API

Date: 2018-07-17

## Status

Accepted

## Context

We need API for the Zoo to expose issues, analytics data, etc.

## Decision

We will create API by GraphQL specification. Pagination will be done according
to Relay server specification. We considered to build REST API, but we decided
that for fresh new APIs is the GraphQL right choice.

## Consequences

We will have API with great flexibility. Easy to use by modern frontend clients.
It may be little odd for backend devs used to work with REST APIs, but they
should get used to it quickly.
