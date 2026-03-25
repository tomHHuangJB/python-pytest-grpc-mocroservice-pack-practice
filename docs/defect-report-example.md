# Defect Report Example

## Title

Order API returns `201` but order is not persisted in SQLite repository

## Environment

- local FastAPI provider
- Python 3.12
- SQLite-backed order repository

## Steps To Reproduce

1. Start the local app.
2. Submit `POST /orders` with valid payload.
3. Call `GET /orders/{order_id}` with the returned ID.

## Expected Result

The order should be returned successfully and exist in the database.

## Actual Result

The create request returns `201`, but the follow-up `GET` returns `404`.

## Evidence

- request/response logs
- failing pytest test name
- SQLite query result showing zero matching rows

## Severity

High, because the API reports success while persistence is incorrect.
