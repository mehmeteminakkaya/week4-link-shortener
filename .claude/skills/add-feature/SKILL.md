---
name: add-feature
description: Implement one feature from docs/TASKS.md in this link shortener, test-first. Use when asked to add, build, or implement a task or feature in this repository.
---

# Add a feature (test-first)

Follow these steps in order. Do not skip ahead to editing `main.py`.

1. **Read.** Open the selected task in `docs/TASKS.md` and re-read `AGENTS.md`
   (boundaries and conventions).
2. **Inspect.** Read `main.py` and `test_main.py`. Note the DB schema, which routes
   are affected, and whether the schema changes.
3. **State the plan.** Write down, before editing: the expected behavior (success and
   failure status codes), the files you will change, and any risk (route conflicts,
   existing `links.db` files, name clashes with generated codes).
4. **Failing test first.** Add behavioral tests to `test_main.py`: one per success
   behavior and at least one failure/edge case. Run `pytest` and confirm the new tests
   fail for the right reason.
5. **Implement the smallest change.** Stay inside the product boundaries in `AGENTS.md`.
   No new dependencies, no refactors that are not required by the task.
6. **Verify.** Run the full `pytest`. The original 3 tests and the new tests must pass.
7. **Summarize.** Report what changed (files and behavior), the test results, and
   any remaining risks or follow-ups. Do not claim anything you did not run.
