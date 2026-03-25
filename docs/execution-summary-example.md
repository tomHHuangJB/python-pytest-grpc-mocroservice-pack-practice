# Execution Summary Example

## Build

- branch: `main`
- environment: local / GitHub Actions

## Coverage Areas

- unit
- integration
- api
- grpc
- contract
- ui when browser dependencies are installed

## Result Summary

- Passed: core service, API, gRPC, SQLite, and contract tests
- Conditional: UI browser tests require Playwright browser installation

## Release Recommendation

Proceed only if the non-UI suite passes and there are no unresolved high-severity persistence or contract failures.
