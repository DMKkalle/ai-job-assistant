# API contract

## GET /health

Returns:

```json
{"status": "ok"}
```

## POST /analyses

Compares candidate skills and evidence against required and preferred job skills.

## POST /jobs

Creates and persists a job.

## GET /jobs/{job_id}

Returns one persisted job or `404` if it does not exist.

## GET /jobs

Returns persisted jobs in stable ID order.

Query parameters:

- `limit`: 1–100, default 20
- `offset`: 0 or greater, default 0
