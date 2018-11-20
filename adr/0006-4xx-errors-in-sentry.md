# 6. Keep 4xx errors in Sentry

Date: 2018-10-19

Originally Decided: 2017

## Status

Accepted

## Context

We're tracking errors to Sentry (which is a Kiwi.com standard).
Sentry allows tracking client errors such as 404s in addition to just the server errors.

## Decision

We enabled sending the client errors.

## Consequences

This helps us in these ways:

- It helps design URL routing based on how people expect it to be:
  for example, we changed from `/services/<service_id>/` to `services/<service_owner>/<service_name>`
  because we saw in Sentry that people manually typed these URLs and expected them to work.
- This notified us that we were missing a `/favicon.ico`,
  and later notified us again when static file serving was buggy and `/favicon.ico` stopped being reachable.
- Multiple times 404 errors were actually caused by bugs in our URL routing,
  which would've been very difficult to find out about without Sentry events.

As a downside, we will get false positive notifications when people make typos in URLs they visit.
People rarely type URLs out though, so the amount of these errors should be bearable.