# Test Estimation Approach

## Objective

This document defines how testing effort is estimated for changes to the order workflow system.

## Estimation Inputs

Testing effort is estimated from the following factors:

- functional scope size
- number of components touched
- regression impact
- contract change impact
- persistence impact
- UI impact
- environment and data setup complexity
- uncertainty level

## Estimation Dimensions

### 1. Analysis And Test Design

Includes:

- requirement review
- ambiguity resolution
- risk assessment
- test-scope selection

### 2. Automation Development

Includes:

- unit and integration updates
- API and contract test changes
- UI automation changes
- fixture and helper refactoring

### 3. Environment And Data Setup

Includes:

- Docker or local environment changes
- Playwright setup
- protobuf regeneration
- test data preparation

### 4. Execution And Diagnosis

Includes:

- local regression execution
- CI diagnosis
- flaky or environment-related failure analysis

### 5. Reporting And Closeout

Includes:

- execution summary
- defect filing
- risk communication

## Example Estimation Heuristic

### Small Change

Characteristics:

- one layer touched
- low regression impact
- no contract or database change

Typical QA effort:

- 0.5 to 1 day

### Medium Change

Characteristics:

- service plus API or persistence touched
- moderate regression impact
- existing automation needs extension

Typical QA effort:

- 1 to 3 days

### Large Change

Characteristics:

- multiple layers touched
- contract or schema change involved
- UI, API, and persistence all affected
- environment or tooling updates required

Typical QA effort:

- 3 to 5+ days, with explicit risk review

## Estimation Example For This Repository

If a feature changes:

- order request schema
- gRPC inventory behavior
- UI submission flow

Then QA estimate should include:

- API contract updates
- provider verification updates
- gRPC stub regeneration and tests
- UI automation updates
- regression execution across all impacted layers

This should not be estimated as a single “API test update”; it is a multi-layer change with cross-component regression risk.
