# Regression Checklist

- Run unit, integration, API, and gRPC pytest markers.
- Regenerate protobuf stubs and verify there is no diff.
- Run contract tests to confirm consumer and provider stay aligned.
- Run Playwright UI tests if browser dependencies are available.
- Confirm SQLite-backed tests still show no partial writes after failures.
- Review GitHub Actions output for both Python versions.
