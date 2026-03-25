# Traceability Matrix

| Requirement / Risk | Test Area | Automated Coverage |
| --- | --- | --- |
| System testing across layers | API, SQLite, gRPC, UI | `tests/integration`, `tests/ui` |
| Regression testing | Full pytest suite, CI matrix | `.github/workflows/python-ci.yml` |
| Functional testing for order workflows | create/get order API, UI form, gRPC reservation | `test_fastapi_orders_api.py`, `test_order_page_playwright.py`, `test_order_workflow_grpc.py` |
| Test plan and execution artifacts | QA docs and TestRail-style files | `docs/test-plan.md`, `docs/testrail-test-cases.csv`, `docs/testrail-test-runs.csv` |
| Defect tracking and reporting | defect example and execution summary | `docs/defect-report-example.md`, `docs/execution-summary-example.md` |
| Environment setup and maintenance | Docker and helper scripts | `Dockerfile`, `docker-compose.yml`, `scripts/run_docker_stack.sh` |
| Cross-product implementation consistency | Pact consumer/provider verification | `tests/contracts/test_order_api_contracts.py` |
| UI and API automation | Playwright, FastAPI API tests | `tests/ui`, `tests/integration/test_fastapi_orders_api.py` |
| Database testing | SQLite repository integration tests | `tests/integration/test_sqlite_repository.py`, `tests/integration/test_fastapi_sqlite_api.py` |
| gRPC API testing | gRPC client and workflow tests | `tests/unit/test_inventory_grpc_client.py`, `tests/integration/test_order_workflow_grpc.py` |
