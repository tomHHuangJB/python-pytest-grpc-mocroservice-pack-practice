# Test Plan

## Scope

This practice repo covers order creation across UI, HTTP API, repository, and gRPC inventory dependency layers.

## Main Risks

- invalid order validation
- downstream inventory failures
- partial persistence after failures
- drift between API consumer expectations and provider behavior
- UI flow breaking while API tests still pass

## Test Levels

- unit: pricing, service validation, client behavior
- integration: FastAPI workflows, SQLite persistence, gRPC service interactions
- UI: Playwright browser flow against the local FastAPI app
- contract: Pact consumer/provider verification for the HTTP API

## Entry Criteria

- dependencies installed
- gRPC stubs generated
- virtual environment active

## Exit Criteria

- full non-UI pytest suite passes
- UI suite passes when browsers are installed
- no unexpected diff in generated gRPC files
- CI passes on supported Python versions
