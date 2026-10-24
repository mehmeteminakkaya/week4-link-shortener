---
paths:
  - "test_*.py"
  - "**/test_*.py"
  - "**/conftest.py"
---

# Test rules

These apply only when reading or editing test files.

- Test through the public API: `client.post("/shorten", ...)`, `client.get(...)`.
  Do not import or call `encode()`, `get_db()`, or touch `links.db` directly in assertions.
- Every feature gets at least one success test and one failure/edge test
  (status code **and** response body or header).
- Tests share one on-disk `links.db` and run in any order. Never assert on a specific
  generated code or row id (e.g. `"b"`); use the code returned by `POST /shorten`.
- Each test creates its own links; no test may rely on data from another test.
- Redirect checks use `follow_redirects=False` and assert `307` plus the `location` header.
- Assert behavior (status, JSON, headers), not implementation details.
- Keep new tests in `test_main.py` unless the file becomes hard to scan.
