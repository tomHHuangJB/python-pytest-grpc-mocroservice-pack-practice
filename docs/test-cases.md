# Test Cases

## 1. Document Purpose

This document captures representative test cases for the current implementation.
It is intended to complement the automated test suite and the TestRail-style CSV export with a more readable, review-friendly format.

## 2. Test Case Conventions

- Priority levels: High, Medium
- Type values: Functional, Negative, Integration, UI, Contract
- Automation status reflects current repository coverage

## 3. Core Order Workflow Cases

### TC-001 Create Order Successfully

- Priority: High
- Type: Functional
- Preconditions: application running; inventory available for requested SKU
- Steps:
  1. submit `POST /orders` with valid customer, SKU, quantity, and price
- Expected Result:
  1. response status is `201`
  2. response body includes order ID and correct total price
  3. order is persisted successfully
- Automation: Yes
- Coverage Reference: `tests/integration/test_fastapi_orders_api.py`

### TC-002 Get Existing Order By ID

- Priority: High
- Type: Functional
- Preconditions: order already exists
- Steps:
  1. call `GET /orders/{order_id}` for an existing order
- Expected Result:
  1. response status is `200`
  2. response body matches the created order
- Automation: Yes
- Coverage Reference: `tests/integration/test_fastapi_orders_api.py`

### TC-003 Return 404 For Missing Order

- Priority: Medium
- Type: Negative
- Preconditions: requested order ID does not exist
- Steps:
  1. call `GET /orders/missing-order`
- Expected Result:
  1. response status is `404`
  2. error detail clearly states the order was not found
- Automation: Yes
- Coverage Reference: `tests/integration/test_fastapi_orders_api.py`

## 4. Validation And Error Handling Cases

### TC-004 Reject Invalid Payload

- Priority: High
- Type: Negative
- Preconditions: application running
- Steps:
  1. submit `POST /orders` with invalid quantity or invalid schema
- Expected Result:
  1. response status indicates validation failure
  2. no order is persisted
- Automation: Yes
- Coverage Reference: `tests/integration/test_fastapi_orders_api.py`

### TC-005 Reject Out-Of-Stock Order

- Priority: High
- Type: Negative
- Preconditions: inventory dependency configured to report out-of-stock
- Steps:
  1. submit `POST /orders` for an unavailable SKU
- Expected Result:
  1. response status is `409`
  2. error detail explains inventory unavailability
  3. no order is persisted
- Automation: Yes
- Coverage Reference: `tests/integration/test_fastapi_orders_api.py`

### TC-006 Map Dependency Timeout To Service Error

- Priority: High
- Type: Integration
- Preconditions: inventory dependency configured to time out
- Steps:
  1. submit a valid order request that triggers dependency timeout
- Expected Result:
  1. response status is `502` or service error is raised at lower layers
  2. no partial write occurs
- Automation: Yes
- Coverage Reference: `tests/integration/test_fastapi_orders_api.py`, `tests/integration/test_sqlite_repository.py`

## 5. Persistence And Database Cases

### TC-007 Persist Order In SQLite Repository

- Priority: High
- Type: Integration
- Preconditions: SQLite-backed repository configured
- Steps:
  1. create a valid order through the service layer
  2. retrieve the order by ID
- Expected Result:
  1. order count increases
  2. retrieved record matches the created order
- Automation: Yes
- Coverage Reference: `tests/integration/test_sqlite_repository.py`

### TC-008 Verify No Partial Write On Failure

- Priority: High
- Type: Integration
- Preconditions: SQLite-backed repository configured; dependency failure triggered
- Steps:
  1. execute order creation that fails after dependency timeout or business rejection
- Expected Result:
  1. repository remains unchanged
  2. zero unintended rows are persisted
- Automation: Yes
- Coverage Reference: `tests/integration/test_sqlite_repository.py`, `tests/integration/test_fastapi_sqlite_api.py`

## 6. gRPC Cases

### TC-009 Reserve Inventory Through gRPC Successfully

- Priority: High
- Type: Integration
- Preconditions: gRPC inventory service running with available stock
- Steps:
  1. call the gRPC reserve flow through the client or order service
- Expected Result:
  1. reservation succeeds
  2. available stock decreases
  3. order flow continues successfully if invoked through the service
- Automation: Yes
- Coverage Reference: `tests/unit/test_inventory_grpc_client.py`, `tests/integration/test_order_workflow_grpc.py`

### TC-010 Map gRPC Timeout To Dependency Error

- Priority: High
- Type: Negative
- Preconditions: gRPC inventory service configured to time out
- Steps:
  1. call the reserve flow for a timeout SKU
- Expected Result:
  1. dependency error is raised or surfaced correctly
  2. no order is persisted downstream
- Automation: Yes
- Coverage Reference: `tests/unit/test_inventory_grpc_client.py`, `tests/integration/test_order_workflow_grpc.py`

## 7. Contract Cases

### TC-011 Generate Consumer Pact For Create And Get Order

- Priority: High
- Type: Contract
- Preconditions: Pact tooling installed
- Steps:
  1. run the consumer contract test
- Expected Result:
  1. pact file is generated successfully
  2. consumer expectations are recorded for create and get order flows
- Automation: Yes
- Coverage Reference: `tests/contracts/test_order_api_contracts.py`

### TC-012 Verify Provider Against Pact Contract

- Priority: High
- Type: Contract
- Preconditions: provider application running; provider state handler available
- Steps:
  1. run provider verification against generated pact files
- Expected Result:
  1. provider verification passes
  2. create and get order interactions satisfy contract expectations
- Automation: Yes
- Coverage Reference: `tests/contracts/test_order_api_contracts.py`

## 8. UI Cases

### TC-013 Create Order From Browser UI

- Priority: High
- Type: UI
- Preconditions: application running; Playwright browser installed
- Steps:
  1. open `/`
  2. submit the default form
- Expected Result:
  1. confirmation message is displayed
  2. order is created successfully
- Automation: Yes
- Coverage Reference: `tests/ui/test_order_page_playwright.py`

### TC-014 Show Error In Browser UI For Out-Of-Stock Scenario

- Priority: Medium
- Type: UI
- Preconditions: application running; inventory configured as out-of-stock; Playwright browser installed
- Steps:
  1. open `/`
  2. submit form with out-of-stock SKU
- Expected Result:
  1. visible error message is displayed
  2. no successful order confirmation is shown
- Automation: Yes
- Coverage Reference: `tests/ui/test_order_page_playwright.py`

## 9. Recommended Expansion Cases

The following cases would be useful next additions if the repository is expanded further:

- authentication and authorization scenarios
- duplicate submission or idempotency handling
- retry behavior with explicit backoff verification
- malformed gRPC payload or compatibility scenarios
- browser-level field validation and accessibility checks
