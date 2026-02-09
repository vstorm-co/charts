# Future TODOs — preview_app

Date: 2026-02-04

This document captures prioritized robustness and hardening tasks for the preview_app API + frontend. Each item is prioritized (Critical → High → Medium → Low) and maps to suggested files/changes.

## Critical (fix immediately)

- Restrict CORS origins
  - Files: preview_app/api_server.py
  - Notes: Replace `allow_origins=["*"]` with explicit dev/origin list.

- Add prompt validation and limits
  - Files: preview_app/api_server.py
  - Notes: Use Pydantic `Field` validators (min/max length, disallow empty/unsafe chars).

- Agent execution timeout
  - Files: preview_app/api_server.py
  - Notes: Wrap `agent.run(...)` with `asyncio.wait_for(..., timeout=...)` and handle `TimeoutError`.

- Request timeout handling
  - Files: preview_app/api_server.py, preview_app/src/App.jsx
  - Notes: Enforce per-request timeout server-side and use `AbortController` client-side.

- Atomic file writes & file locking
  - Files: preview_app/api_server.py
  - Notes: Write to a temp file then atomically `replace()`. Use file locks (fcntl on Unix) when updating `status.json`.

- Rate limiting
  - Files: preview_app/api_server.py
  - Notes: Add a simple rate limiter (e.g., `slowapi`/Redis-backed limiter) for `/api/generate`.

- Graceful shutdown handlers
  - Files: preview_app/api_server.py
  - Notes: Use FastAPI `shutdown` events and signal handlers to flush state and close resources.

## High (next)

- File error recovery & retries
  - Files: preview_app/api_server.py
  - Notes: Add retry with exponential backoff for transient IO failures (e.g., `tenacity`).

- Request ID logging & tracing
  - Files: preview_app/api_server.py
  - Notes: Generate a UUID per request and include it in logs and `status.json` for correlation.

- Enhance health endpoint
  - Files: preview_app/api_server.py
  - Notes: Return service state (writable files, agent ready) and timestamp.

- Log requests & responses
  - Files: preview_app/api_server.py
  - Notes: Log truncated prompt, status message, UI element size, and errors with stack traces.

- Frontend timeouts & retries
  - Files: preview_app/src/App.jsx
  - Notes: Add `AbortController` timeouts and retry strategy (3 attempts, exponential backoff).

- Frontend error boundary
  - Files: preview_app/src/App.jsx
  - Notes: Wrap generated component rendering in an `ErrorBoundary` to avoid full-app crashes.

- Polling timeout and backoff
  - Files: preview_app/src/App.jsx
  - Notes: Stop polling after a configurable timeout / switch to exponential backoff when errors occur.

## Medium

- Environment and config validation
  - Files: pyproject.toml, preview_app/api_server.py
  - Notes: Validate required env vars at startup and fail fast with clear error messages.

- Caching and response compression
  - Files: preview_app/api_server.py
  - Notes: Consider caching generated UI for identical prompts and compressing large responses.

- API versioning & docs
  - Files: preview_app/api_server.py
  - Notes: Add `openapi` metadata and version prefix (e.g., `/api/v1`).

## Low

- Monitoring & metrics
  - Files: preview_app/api_server.py
  - Notes: Add basic Prometheus metrics (request durations, success/failure counters).

- Tests for generation flow
  - Files: preview_app/test_chart.py, preview_app/api_server.py
  - Notes: Add unit/integration tests that simulate the agent (mock) and file updates.

---

Suggested next steps:

1. Implement the items in **Critical** one-by-one (start with CORS, validation, and timeouts).
2. Run the app locally and exercise `/api/generate` with edge-case prompts.
3. Add automated tests for the generate flow and file-write semantics.

If you want, I can start implementing these tasks in order — tell me which item to begin with.
