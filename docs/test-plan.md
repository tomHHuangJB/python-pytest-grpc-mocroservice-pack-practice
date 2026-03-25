# Test Plan

## 1. Document Purpose

This test plan defines the quality strategy for the `python-pytest-grpc-mocroservice-pack-practice` repository.
It governs validation of a microservice-oriented system that includes UI, HTTP API, gRPC, persistence, and contract-testing layers.

This document is maintained as a product-facing QA artifact for planning, execution, reporting, and release confidence.

## 2. System Under Test

The system under test is an order workflow composed of the following functional areas:

- FastAPI HTTP provider for order creation and retrieval
- order service business layer
- SQLite-backed repository option for persistence validation
- gRPC-based inventory dependency for service-to-service communication
- browser-facing HTML page for UI automation practice
- Pact consumer/provider contract layer for HTTP interaction verification

Primary business workflow:

1. user or client submits an order
2. order service validates request data
3. inventory dependency is called to reserve stock
4. if inventory succeeds, the order is persisted and returned
5. if inventory fails, the system must return the correct error and avoid partial writes

## 3. Quality Objectives

The primary quality objectives are:

- verify the correctness of core order creation and retrieval flows
- verify resilience and error handling across service boundaries
- verify that persistence behavior is correct, especially under failure conditions
- verify that HTTP contracts remain compatible with consumer expectations
- verify that UI behavior remains aligned with backend outcomes
- verify that the repository can be executed repeatedly in local and CI environments with deterministic results

## 4. Scope

### In Scope

- functional testing of create and get order HTTP endpoints
- service-layer validation and negative-path behavior
- repository behavior using in-memory and SQLite implementations
- gRPC inventory dependency behavior, including success, out-of-stock, and timeout conditions
- Pact consumer/provider verification for HTTP provider compatibility
- Playwright UI validation for the browser order workflow
- CI execution across supported Python versions
- test documentation, execution reporting, and traceability artifacts

### Out Of Scope

- performance benchmarking beyond lightweight correctness checks
- load, soak, and stress testing
- security penetration testing
- browser compatibility beyond the Playwright Chromium path currently implemented
- production-grade infrastructure concerns such as secrets management, distributed tracing backends, or real external service deployment

## 5. Test Strategy

The strategy is layered, risk-based, and automation-first.
Lower test layers isolate failures earlier and reduce diagnosis cost.
Higher test layers validate cross-component behavior and customer-visible outcomes.

### 5.1 Unit Testing

Purpose:

- validate business logic deterministically
- isolate validation, pricing, ID handling, client error mapping, and repository-independent behavior

Coverage includes:

- pricing rules
- request validation
- dependency failure mapping
- missing-order handling
- API client response and error parsing
- gRPC client behavior in isolation from the order workflow

### 5.2 Integration Testing

Purpose:

- validate interaction between multiple components within the service boundary
- confirm side effects such as persistence behavior and no-partial-write guarantees

Coverage includes:

- FastAPI endpoint-to-service-to-repository workflows
- SQLite persistence and retrieval
- gRPC inventory integration with the order service
- downstream timeout and out-of-stock handling
- repository state after failed operations

### 5.3 Contract Testing

Purpose:

- verify that the HTTP provider remains compatible with consumer expectations
- detect interface drift before integration failures appear downstream

Coverage includes:

- Pact consumer generation for create and get order interactions
- Pact provider verification against the live FastAPI app
- provider-state control for deterministic verification

### 5.4 UI Testing

Purpose:

- confirm that the browser-facing order flow correctly represents backend outcomes
- ensure UI assertions are tied to real service behavior rather than mocked page state only

Coverage includes:

- successful order creation from the HTML form
- user-visible error behavior for out-of-stock responses

### 5.5 Regression Strategy

Regression is executed primarily through:

- full local pytest suite
- non-UI CI matrix execution on Python 3.11 and 3.12
- dedicated UI CI execution with Playwright Chromium
- protobuf regeneration checks to detect contract drift in generated gRPC files

## 6. Risk Assessment

The most important quality risks in the current system are:

### High Risk

- incorrect persistence after downstream failure
- API contract drift between consumer and provider
- incorrect mapping of downstream gRPC failures into domain or HTTP errors
- false-positive success responses where database state is wrong

### Medium Risk

- UI still appearing correct while backend behavior regresses
- environment inconsistency between local and CI execution
- generated protobuf files falling out of sync with the `.proto` contract

### Lower Risk

- cosmetic UI issues in the simple HTML page
- non-critical documentation drift

Risk response:

- high-risk areas receive direct automated coverage at more than one layer where practical
- persistence integrity is validated through explicit repository state checks
- contract compatibility is verified through Pact and protobuf workflows

## 7. Test Environment Strategy

### Local Environment

Local execution supports:

- Python virtual environment
- direct pytest execution
- Playwright browser installation for UI testing
- Docker Compose startup for the FastAPI provider environment

### CI Environment

CI supports:

- dependency installation from `pyproject.toml`
- gRPC stub regeneration
- non-UI regression coverage on Python 3.11 and 3.12
- dedicated UI execution on Python 3.12 with Chromium

### Environment Controls

- tests are designed to be deterministic and isolated
- temporary databases are created per test where SQLite persistence is used
- in-memory or stubbed dependencies are used where full external systems are unnecessary
- local shell issues such as injected pytest plugins are documented in the README

## 8. Test Data Strategy

Test data is intentionally lightweight and deterministic.

Examples:

- standard valid customer and SKU combinations
- out-of-stock SKUs to simulate business failure
- timeout SKUs to simulate dependency failure
- fixed order IDs in contract and UI scenarios where deterministic assertions are required

Data principles:

- use explicit values rather than randomly generated data for core regression tests
- isolate persistence state per test to avoid inter-test coupling
- prefer representative domain data over volume

## 9. Entry Criteria

Execution may begin when:

- repository dependencies are installed successfully
- virtual environment is active for local execution
- gRPC stubs are generated and in sync with the proto file
- Playwright browser is installed for UI execution
- test environment is reachable locally or via CI runner

## 10. Exit Criteria

Execution is considered acceptable when:

- all required unit, integration, API, gRPC, and contract tests pass
- UI tests pass in environments where browser dependencies are installed
- no unexpected diff exists in generated gRPC files
- no open high-severity defect remains against core order workflows
- CI completes successfully on supported Python versions

## 11. Deliverables

Primary QA deliverables for this repository are:

- automated test suite under `tests/`
- CI workflow definitions under `.github/workflows/`
- test plan, regression checklist, defect example, and execution summary
- TestRail-style test case and test run exports
- traceability matrix linking risks and requirements to coverage

## 12. Defect Management Approach

Defects should be documented with:

- clear title
- environment and build context
- reproducible steps
- expected vs actual result
- severity and business impact
- evidence such as logs, API payloads, screenshots, or database query results

Special emphasis should be placed on:

- persistence mismatches
- contract incompatibilities
- incorrect status-code or error-detail behavior
- UI/backend inconsistencies

## 13. Reporting Approach

Execution reporting should summarize:

- what suites were run
- what environment was used
- pass/fail/block counts
- open risks and known limitations
- release or merge recommendation

Supporting examples are maintained in:

- `docs/execution-summary-example.md`
- `docs/testrail-test-runs.csv`

## 14. Roles And Ownership

For this practice repository, QA ownership includes:

- test design
- automation implementation
- environment setup guidance
- regression execution
- defect reporting examples
- contract and cross-layer validation

Development ownership is assumed for:

- product code changes under `src/`
- interface evolution requiring coordinated updates to API, gRPC, and UI layers

In practice, high-quality outcomes require collaboration between both roles, especially when service contracts or persistence behavior change.

## 15. Assumptions And Constraints

Assumptions:

- local machine can create and activate Python virtual environments
- Playwright browser installation is permitted where UI tests are run
- local or CI environment can bind loopback ports for contract and UI test execution

Constraints:

- the system is intentionally small and does not model production-grade infrastructure
- the UI is a lightweight HTML page, not a full SPA
- Docker support is currently oriented toward the HTTP provider app only

## 16. Approval Recommendation

<<<<<<< HEAD
<<<<<<< HEAD
This test plan is appropriate for a small but realistic QA repository because it:
=======
This test plan is appropriate for a small but realistic QA practice repository because it:
>>>>>>> 0dfdd0b (Add senior QA docs, TestRail artifacts, and Docker setup)
=======
This test plan is appropriate for a small but realistic QA repository because it:
>>>>>>> 69e7893 (Add idempotency coverage and clean POC wording)

- applies layered automation instead of relying on a single test type
- prioritizes high-risk failure modes such as contract drift and partial persistence
- includes both technical validation and QA process artifacts
<<<<<<< HEAD
<<<<<<< HEAD
- demonstrates a maintainable, repeatable test execution model suitable for technical review and ongoing extension
=======
- demonstrates a maintainable, repeatable test execution model suitable for interview discussion and portfolio use
>>>>>>> 0dfdd0b (Add senior QA docs, TestRail artifacts, and Docker setup)
=======
- demonstrates a maintainable, repeatable test execution model suitable for technical review and ongoing extension
>>>>>>> 69e7893 (Add idempotency coverage and clean POC wording)
