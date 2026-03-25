# Design Review Checklist

## Objective

This checklist is used during feature design and implementation review to ensure the system remains testable, diagnosable, and consistent.

## Functional Design Review

- Are acceptance criteria explicit and testable?
- Are negative scenarios defined, not only happy paths?
- Are error codes and error details specified?
- Are persistence expectations clear for both success and failure flows?

## API And Contract Review

- Does the HTTP contract change affect existing consumers?
- Are Pact updates required?
- Does the gRPC `.proto` contract change require compatibility review?
- Are generated clients or stubs affected?

## Persistence Review

- What data must be written on success?
- What data must not be written on failure?
- Is retrieval behavior defined clearly?
- Are there transaction or partial-write risks?

## UI Review

- Does the UI need to surface backend failure details clearly?
- Which user journeys justify browser automation?
- Are selectors and page states stable enough for maintainable tests?

## Environment And Observability Review

- Are logs sufficient for debugging failures?
- Can the feature be exercised locally and in CI?
- Are new environment variables, services, or Docker changes required?

## Release And Regression Review

- Which existing suites must be updated?
- Which regression areas are high risk?
- Is additional test data or provider-state setup required?

## Decision Standard

A design is not considered test-ready until:

- key risks are identified
- interfaces are specified
- failure behavior is defined
- observability is adequate
- required automation impact is understood
