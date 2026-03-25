# Test Strategy

## 1. Objective

This document defines the test strategy for the order workflow practice repository.
Its purpose is to explain how quality is assessed, which risks are prioritized, what test layers are used, and how the automated suites are intended to work together.
The strategy is intended to support practical planning, execution, and quality decision making for the current implementation.

## 2. Strategy Principles

The strategy is based on the following principles:

- risk-based prioritization over equal treatment of all scenarios
- layered testing to catch defects at the lowest useful level
- deterministic automation with clear failure diagnosis
- explicit verification of side effects, not only response codes
- contract awareness across HTTP and gRPC boundaries
- keeping UI coverage focused on business-critical user journeys

## 3. Product Risks Driving The Strategy

The main product and implementation risks are:

- invalid input accepted by the service
- incorrect error mapping from downstream inventory failures
- order persistence occurring when the business flow should fail
- drift between HTTP consumer expectations and provider behavior
- UI behavior diverging from actual backend state
- gRPC contract or generated stub drift
- environment inconsistency between local development and CI execution

These risks determine where deeper automation and explicit regression controls are applied.

## 4. Test Pyramid And Coverage Intent

### Unit Layer

Intent:

- validate business rules quickly and deterministically
- isolate failures in logic before involving HTTP, gRPC, persistence, or browser layers

Examples:

- pricing calculation
- request validation
- dependency error translation
- missing-order handling
- API client parsing and schema validation

### Integration Layer

Intent:

- validate interactions across service, repository, FastAPI, and gRPC boundaries
- verify state transitions and downstream effects

Examples:

- FastAPI create and get order workflows
- SQLite persistence and retrieval
- no partial writes on timeout or business failure
- gRPC-based order workflow behavior

### Contract Layer

Intent:

- verify that the provider still satisfies consumer-facing expectations
- catch interface drift that may not be visible in provider-only testing

Examples:

- Pact consumer generation for create and get order
- Pact provider verification against the live FastAPI provider

### UI Layer

Intent:

- validate customer-visible workflow behavior
- confirm that browser interactions and rendered feedback remain aligned with backend results

Examples:

- successful order creation from the UI
- out-of-stock error presentation in the UI

## 5. Why Each Layer Exists

The repository does not rely on a single test type because each layer answers a different quality question:

- unit tests answer whether logic is correct in isolation
- integration tests answer whether components collaborate correctly
- contract tests answer whether external expectations remain compatible
- UI tests answer whether the user-facing path still works

This separation improves diagnosis speed and reduces overreliance on slower end-to-end coverage.

## 6. Scope By Capability

### HTTP API

Covered through:

- direct FastAPI endpoint tests
- API client tests
- Pact consumer/provider verification

Main checks:

- status codes
- payload shape
- error details
- persistence side effects

### gRPC Dependency

Covered through:

- gRPC client unit tests
- service integration tests through the order workflow
- protobuf generation checks in CI

Main checks:

- successful reservation flow
- out-of-stock mapping
- timeout mapping
- no persistence after dependency failure

### Persistence

Covered through:

- SQLite repository integration tests
- FastAPI plus SQLite end-to-end persistence checks

Main checks:

- successful write
- retrieval by ID
- zero writes after failed flow

### UI

Covered through:

- Playwright browser tests against the local FastAPI provider

Main checks:

- submission flow
- rendered confirmation
- rendered error feedback

## 7. Regression Strategy

Regression is divided into practical execution groups:

### Fast Regression

- unit
- integration
- api
- grpc
- contract

Purpose:

- quick developer feedback
- CI compatibility checks

### Full Regression

- all non-UI suites plus UI suite

Purpose:

- confirm business workflow stability before pushing or demonstrating the repo

### Build Integrity Checks

- gRPC stub regeneration
- CI matrix validation
- Pact verification

Purpose:

- detect environment or interface drift

## 8. Environment Strategy

The strategy intentionally supports more than one execution model:

- local virtual environment for day-to-day development
- Docker Compose for local environment bring-up
- GitHub Actions for repeatable CI execution

This is important because environment management itself is part of the JD-aligned skill set.

## 9. Entry And Exit Rules

### Entry Rules

- required dependencies installed
- virtual environment active for local runs
- generated gRPC files in sync
- Playwright browser installed when UI tests are included

### Exit Rules

- target suites pass
- no unexpected generated-file diff exists
- no open high-severity issue remains against the primary order workflow
- CI passes on supported versions

## 10. Defect Containment Philosophy

This strategy explicitly tries to prevent the following false confidence patterns:

- API returns success but data is not persisted correctly
- dependency fails but the service response hides the root behavior
- UI looks correct while backend contract has drifted
- provider tests pass while consumer expectations have changed

Because of that, the strategy emphasizes:

- side-effect checks
- state verification
- contract verification
- layered coverage instead of UI-only validation

## 11. Reporting And Traceability

Execution results are intended to map back to:

- test plan
- TestRail-style test case inventory
- execution summary
- defect report examples
- traceability matrix

This ensures the strategy is not only about code execution but also about QA communication and release confidence.

## 12. Summary

The strategy is appropriate for this repository because it balances:

- speed and maintainability
- functional depth and cross-layer validation
- developer feedback and stakeholder reporting
- technical automation and QA process visibility

That combination is what makes the repository a stronger technical reference and closer to industry-standard QA practice.
