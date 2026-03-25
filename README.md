# Python Pytest Grpc Mocroservice Pack Practice

This repo is a focused practice project for API and Microservice testing. It is intentionally small, but it covers the Python and pytest topics that are likely to come up:

- fixtures
- parametrized tests
- markers
- mocking and stubbing dependencies
- negative-path testing
- state validation after failures
- basic integration-style workflow tests
- SQLite-backed persistence testing
- API client tests with response validation
- FastAPI endpoint tests
- SOAP service tests
- GraphQL API tests
- gRPC microservice tests
- WebSocket realtime tests
- webhook callback tests
- message-driven event tests
- Playwright UI tests
- Pact consumer/provider contract tests

## Project Shape

The sample domain is an order service with:

- inventory dependency
- pricing rules
- order repository
- SQLite-backed repository option
- validation and error handling
- HTTP API layer with FastAPI
- SOAP endpoint for XML-based request/response coverage
- GraphQL endpoint for query and mutation coverage
- API client validation using `httpx`
- gRPC inventory microservice and client
- WebSocket endpoint for realtime order events
- webhook receiver for callback-style integration
- in-memory event bus for message-driven order events
- HTML demo page for UI automation
- Pact-ready HTTP contract surface with create and read endpoints

This keeps the examples close to realistic system-testing and service-validation discussions.

## Quick Start

```bash
cd /Users/tomhuang/Documents/job/resume/doble/python-pytest-grpc-mocroservice-pack-practice
python3 -m venv .venv
unalias deactivate 2>/dev/null
source .venv/bin/activate
pip install -e ".[dev]"
./scripts/install_playwright_chromium.sh
unset PYTEST_PLUGINS
pytest
```

## Start And Run Tests

### Quick Script Options

If you want a shorter command path, use the helper scripts:

```bash
./scripts/run_pytest.sh
./scripts/run_pytest_non_ui.sh
./scripts/generate_grpc_stubs.sh
./scripts/install_playwright_chromium.sh
./scripts/run_docker_stack.sh
./scripts/stop_docker_stack.sh
```

### First-Time Setup

```bash
cd /Users/tomhuang/Documents/job/resume/doble/python-pytest-grpc-mocroservice-pack-practice
python3 -m venv .venv
unalias deactivate 2>/dev/null
source .venv/bin/activate
pip install -e ".[dev]"
python -m grpc_tools.protoc -I proto --python_out=src --grpc_python_out=src proto/order_app/grpc_contracts/inventory.proto
./scripts/install_playwright_chromium.sh
unset PYTEST_PLUGINS
pytest
```

### Normal Daily Run

```bash
cd /Users/tomhuang/Documents/job/resume/doble/python-pytest-grpc-mocroservice-pack-practice
unalias deactivate 2>/dev/null
source .venv/bin/activate
unset PYTEST_PLUGINS
pytest
```

### Run Specific Test Groups

```bash
unset PYTEST_PLUGINS && pytest -m unit
unset PYTEST_PLUGINS && pytest -m integration
unset PYTEST_PLUGINS && pytest -m api
unset PYTEST_PLUGINS && pytest -m grpc
unset PYTEST_PLUGINS && pytest -m ui
unset PYTEST_PLUGINS && pytest -m contract
```

## Environment Setup

The repo now includes a simple Docker-based environment for local app startup:

```bash
./scripts/run_docker_stack.sh
```

The FastAPI app will be available at `http://localhost:8000`.

To stop it:

```bash
./scripts/stop_docker_stack.sh
```

## Practice Goals

This repo can be used to answer the following questions:

- how fixtures reduce duplication
- how parametrization improves coverage
- how mocks or stubs isolate dependencies
- how to verify no partial writes happen on failure
- how to separate unit and integration tests with markers
- how to validate API responses and error payloads
- how to test FastAPI endpoints without external environments
- how to test a microservice dependency over gRPC
- how to test SOAP XML request/response handling
- how to test GraphQL query and mutation flows
- how to test WebSocket realtime event delivery
- how to test inbound webhooks safely
- how to test message-driven event publishing and subscribers
- how to validate cross-service effects and failure handling
- how to verify persistence with SQLite-backed tests
- how to write Playwright UI tests with pytest
- how to verify HTTP consumer/provider contracts with Pact

Questions this repo helps you answer:

1. What does each fixture in `tests/conftest.py` do, and why is fixture-based setup better than repeating setup inside every test?
2. Which parametrized test best shows how one test can cover multiple rules without copy-paste duplication?
3. How is the inventory stub used to simulate success, timeout, and out-of-stock behavior while keeping tests deterministic?
4. How do the tests prove that failure scenarios do not leave partial writes behind?
5. How do the API client tests validate both success payloads and schema drift?
6. How do the FastAPI endpoint tests exercise the service without needing any external environment?
7. How do the gRPC tests show mapping from service-to-service failures into domain-level errors?
8. How do the SQLite-backed tests prove persistence behavior and no-partial-write guarantees with real storage?
9. How do the Pact tests prove consumer and provider stay aligned?
10. Why are the Playwright UI tests intentionally narrow, and what value do they add beyond API tests?
<<<<<<< HEAD
11. How does the SOAP endpoint show XML-based service testing?
12. How do the GraphQL tests prove both mutation and query behavior?
13. How do the WebSocket and webhook tests cover realtime and callback integrations?
14. How does the event-bus example demonstrate message-driven testing?
=======
>>>>>>> 69e7893 (Add idempotency coverage and clean POC wording)

## Useful Commands

```bash
unset PYTEST_PLUGINS && pytest
unset PYTEST_PLUGINS && pytest -m unit
unset PYTEST_PLUGINS && pytest -m integration
unset PYTEST_PLUGINS && pytest -m api
unset PYTEST_PLUGINS && pytest -m grpc
unset PYTEST_PLUGINS && pytest -m contract
unset PYTEST_PLUGINS && pytest -m ui
unset PYTEST_PLUGINS && pytest --cov=order_app --cov-report=term-missing
```

### UI Setup

Playwright Chromium installation is part of the standard setup:

```bash
./scripts/install_playwright_chromium.sh
unset PYTEST_PLUGINS && pytest -m ui
```

## CI

GitHub Actions is configured in `.github/workflows/python-ci.yml`.
It:

- installs the package and dev dependencies
- regenerates protobuf stubs
- fails if generated gRPC files are out of date
- runs non-UI tests with coverage on Python 3.11 and 3.12
- runs Playwright UI tests in a dedicated Chromium-enabled job

## QA Docs

The `docs/` folder contains QA planning, execution, and governance artifacts:

- `test-plan.md`
- `test-strategy.md`
- `test-cases.md`
- `agile-qa-delivery-model.md`
- `test-estimation.md`
- `design-review-checklist.md`
- `tooling-mapping.md`
- `regression-checklist.md`
- `defect-report-example.md`
- `execution-summary-example.md`
- `testrail-test-cases.csv`
- `testrail-test-runs.csv`
- `traceability-matrix.md`

## Troubleshooting

### PyCharm Or zsh Error: `defining function based on alias 'deactivate'`

If you see an error like this:

```bash
.venv/bin/activate:4: defining function based on alias `deactivate'
.venv/bin/activate:4: parse error near `()'
```

Your shell already has an alias named `deactivate`.
Fix it before activating the virtual environment:

```bash
unalias deactivate 2>/dev/null
source .venv/bin/activate
```

You can confirm the cause with:

```bash
alias deactivate
```

### Pytest Fails Because Of `pytest_html`

If pytest fails with an error mentioning `pytest_html`, your shell environment is injecting a global pytest plugin that is not installed in this repo environment.

Use:

```bash
unset PYTEST_PLUGINS
pytest
```

### gRPC Stub Files Need Regeneration

If protobuf or gRPC-related imports fail, regenerate the generated files:

```bash
python -m grpc_tools.protoc -I proto --python_out=src --grpc_python_out=src proto/order_app/grpc_contracts/inventory.proto
```

Then rerun:

```bash
unset PYTEST_PLUGINS
pytest
```

### Playwright Browser Not Installed

If UI tests fail because Chromium is missing, complete the required browser setup with:

```bash
./scripts/install_playwright_chromium.sh
```

Then rerun:

```bash
unset PYTEST_PLUGINS
pytest -m ui
```

## Service Styles Covered

The repo now covers these major service and integration styles:

- REST over HTTP with FastAPI endpoints under `src/order_app/api.py`
- SOAP over XML with `POST /soap/orders`
- GraphQL with `POST /graphql`
- gRPC with the inventory service under `src/order_app/grpc_microservices/`
- WebSocket realtime messaging with `/ws/orders`
- webhook callbacks with `POST /webhooks/inventory-events`
- message-driven integration with `src/order_app/eventing.py`

<<<<<<< HEAD
The tests show how each style is validated:
=======
The gRPC path is useful because it lets you work through:
>>>>>>> 69e7893 (Add idempotency coverage and clean POC wording)

- REST and HTTP contract coverage in `tests/integration/test_fastapi_orders_api.py` and `tests/contracts/test_order_api_contracts.py`
- SOAP, GraphQL, WebSocket, webhook, and event-bus coverage in `tests/integration/test_additional_service_types.py`
- gRPC service-to-service coverage in `tests/integration/test_order_workflow_grpc.py`
