# Python Pytest Grpc Mocroservice Pack Practice

This repo is a focused practice project for API and Microservice testing. It is intentionally small, but it covers the Python and pytest topics that are likely to come up:

- fixtures
- parametrized tests
- markers
- mocking and stubbing dependencies
- negative-path testing
- state validation after failures
- basic integration-style workflow tests
- API client tests with response validation
- FastAPI endpoint tests
- gRPC microservice tests

## Project Shape

The sample domain is an order service with:

- inventory dependency
- pricing rules
- order repository
- validation and error handling
- HTTP API layer with FastAPI
- API client validation using `httpx`
- gRPC inventory microservice and client

This keeps the examples close to system-testing discussions you may need in the interview.

## Quick Start

```bash
cd /Users/tomhuang/Documents/job/resume/doble/python-pytest-grpc-mocroservice-pack-practice
python3 -m venv .venv
unalias deactivate 2>/dev/null
source .venv/bin/activate
pip install -e ".[dev]"
unset PYTEST_PLUGINS
pytest
```

## Start And Run Tests

### First-Time Setup

```bash
cd /Users/tomhuang/Documents/job/resume/doble/python-pytest-grpc-mocroservice-pack-practice
python3 -m venv .venv
unalias deactivate 2>/dev/null
source .venv/bin/activate
pip install -e ".[dev]"
python -m grpc_tools.protoc -I proto --python_out=src --grpc_python_out=src proto/order_app/grpc_contracts/inventory.proto
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
```

## Practice Goals

Use this repo to practice:

- how fixtures reduce duplication
- how parametrization improves coverage
- how mocks or stubs isolate dependencies
- how to verify no partial writes happen on failure
- how to separate unit and integration tests with markers
- how to validate API responses and error payloads
- how to test FastAPI endpoints without external environments
- how to test a microservice dependency over gRPC
- how to validate cross-service effects and failure handling

## Suggested Interview Drills

1. Explain what each fixture in `tests/conftest.py` does.
2. Walk through one parametrized test and explain why it is better than separate copy-paste tests.
3. Explain how the inventory stub is used to simulate success, timeout, and out-of-stock behavior.
4. Explain why the service validates DB-like state after failure scenarios.
5. Walk through the API client tests and explain how schema validation catches payload drift.
6. Walk through the FastAPI endpoint tests and explain dependency override usage.
7. Walk through the gRPC tests and explain how service-to-service failures are mapped into domain errors.
8. Add one more API or gRPC negative-path test before your interview.

## Useful Commands

```bash
unset PYTEST_PLUGINS && pytest
unset PYTEST_PLUGINS && pytest -m unit
unset PYTEST_PLUGINS && pytest -m integration
unset PYTEST_PLUGINS && pytest -m api
unset PYTEST_PLUGINS && pytest -m grpc
unset PYTEST_PLUGINS && pytest --cov=order_app --cov-report=term-missing
```

## CI

GitHub Actions is configured in `.github/workflows/python-ci.yml`.
It:

- installs the package and dev dependencies
- regenerates protobuf stubs
- fails if generated gRPC files are out of date
- runs the full pytest suite with coverage on Python 3.11 and 3.12

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

## Microservice Practice

The repo now has two service interaction styles:

- HTTP via FastAPI for endpoint and client testing
- gRPC for service-to-service inventory reservation

The gRPC path is useful for interview prep because it lets you discuss:

- protobuf contracts
- generated stubs
- service dependency failures
- timeout mapping
- no partial writes after downstream failure
