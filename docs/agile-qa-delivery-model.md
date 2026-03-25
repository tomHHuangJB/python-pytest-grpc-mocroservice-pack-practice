# Agile QA Delivery Model

## Objective

This document defines how QA activities fit into an iterative delivery model for the order workflow system.

## QA Participation By Sprint Phase

### Backlog Refinement

QA responsibilities:

- review upcoming stories for testability
- identify external dependencies, environment needs, and risk areas
- clarify acceptance criteria and failure scenarios
- propose the correct test split across unit, integration, contract, UI, and regression layers

Outputs:

- clarified acceptance criteria
- initial risk notes
- testability and environment questions

### Sprint Planning

QA responsibilities:

- estimate test design and automation effort
- identify environment, data, and tooling prerequisites
- flag stories that require contract, persistence, or UI coverage
- agree on regression impact with engineering and product

Outputs:

- test tasks added to sprint scope
- effort estimates
- dependency and sequencing notes

### In-Sprint Development

QA responsibilities:

- review implementation changes early
- add or update automated tests in parallel with feature work
- validate that logging, error handling, and interfaces support diagnosis
- collaborate with developers on root-cause analysis

Outputs:

- incremental automation updates
- defect reports
- design feedback

### Pre-Merge / Pre-Release

QA responsibilities:

- execute regression suites
- verify contract compatibility
- confirm no persistence regressions
- evaluate release risk and open defects

Outputs:

- execution summary
- release recommendation
- traceability to implemented stories and risks

## Agile Quality Gates

- acceptance criteria are testable and agreed before implementation begins
- required automated coverage is present before merge
- high-risk regressions are blocked until resolved or formally accepted
- consumer/provider and gRPC contract drift is not allowed to pass silently

## Collaboration Expectations

QA is not a downstream role in this model.
QA contributes to:

- requirement clarity
- testability decisions
- interface and error-handling quality
- release risk communication

This is the expected operating model for a senior SQA engineer in an Agile team.
