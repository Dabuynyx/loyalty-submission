# ROYALTY — Software Engineer Quality Assurance Sign-Off

<!--
  AI-LOCK: STRICTLY READ-ONLY FOR ALL AI AGENTS & VIBE-CODING TOOLS.
  NO AI TOOL MAY CHECK BOXES ([x]) OR EDIT THIS FILE.
  HUMAN ENGINEER VERIFICATION REQUIRED.
-->

> **Rule:** Every QA gate below must be executed, observed, and checked (`[ ]` → `[x]`) **manually by a human software engineer**. AI assistants must never auto-check or edit this file.

---

## A. Environment, Packaging & Git Hygiene QA
- [ ] `pyproject.toml` pins all runtime/dev dependencies cleanly and installs in a fresh `.venv` *(Verify: `pip install -e ".[dev]"` | Sign-off: _______)*
- [ ] `.gitignore` excludes `.env`, `.venv/`, `__pycache__/`, `*.pyc`, and local SQLite `*.db` files *(Verify: `git status` | Sign-off: _______)*
- [ ] Secret scan passes with zero leaked tokens, passwords, or AWS/Careem credentials in working tree or git history *(Verify: `gitleaks detect` | Sign-off: _______)*

---

## B. Core Algorithm & Financial Invariant QA
- [ ] All unit tests pass in a clean environment *(Verify: `python3 -m unittest discover -s tests -v` | Sign-off: _______)*
- [ ] Verified Fleet curve (`60/40 → 40/60`) and Independent Jordan curve (`28/72 → 14/86`) never exceed `60%` / `86%` cap *(Verify: boundary unit test | Sign-off: _______)*
- [ ] Verified `remaining_reward_budget_jod` strictly enforces `uplift + bonuses + family_promo_cost <= gross_fares * max_reward_budget_pct` *(Verify: budget-cap test | Sign-off: _______)*
- [ ] Verified wash-trip guard (`fare < 1.50` or `distance < 1.0`) and `10.0h` daily fatigue cap return `0 XP` *(Verify: boundary test | Sign-off: _______)*
- [ ] Verified season soft reset drops at most `2` tiers and never drops below `legacy_floor_tier` *(Verify: soft-reset test | Sign-off: _______)*

---

## C. Database, Migrations & Transaction Safety QA
- [ ] `docs/schemas/database/001_initial_schema.sql` executes cleanly on PostgreSQL 16 with zero constraint errors *(Verify: `psql -f ...` | Sign-off: _______)*
- [ ] Verified row-level locking (`SELECT ... FOR UPDATE` on Postgres / `BEGIN IMMEDIATE` on SQLite) on `reward_budgets` *(Verify: code & lock test | Sign-off: _______)*
- [ ] Verified `UNIQUE(idempotency_key)` on `progression_history` and `reward_transactions` blocks duplicate processing *(Verify: replay test | Sign-off: _______)*
- [ ] Verified `outbox_events` row is written inside the **exact same** ACID commit as `reward_budgets` updates *(Verify: rollback test | Sign-off: _______)*
- [ ] Verified database migration rollback script restores previous schema cleanly without data loss *(Verify: `alembic downgrade -1` | Sign-off: _______)*

---

## D. API Contract & Concurrency Stress QA
- [ ] OpenAPI 3.1 contract fuzzing passes against live FastAPI `/v1/*` server with zero `500` responses *(Verify: `schemathesis run docs/api/openapi.yaml` | Sign-off: _______)*
- [ ] Concurrency race test: `10` parallel `POST /rewards/{id}/redeem` requests for last `JOD 5.00` budget → **exactly 1** `201 Created`, **9** `409 Conflict`, budget = `0.00` *(Verify: `pytest tests/test_concurrency.py` | Sign-off: _______)*
- [ ] Duplicate `POST /v1/events/trips/completed` with same `Idempotency-Key` returns `202` with zero XP/fare double-counting *(Verify: `pytest tests/test_idempotency.py` | Sign-off: _______)*
- [ ] RBAC ownership check: Captain A's JWT calling `/v1/captains/{captain_B}/loyalty/status` returns `403 Forbidden` *(Verify: auth integration test | Sign-off: _______)*
- [ ] Partner `503` failure during redemption triggers compensating `REFUND` transaction restoring `reward_budgets` *(Verify: mock partner 503 test | Sign-off: _______)*

---

## E. Careem MCP, AWS Bedrock & Kiro Integration QA
- [ ] Careem Local Sandbox tests pass including error-injection scenarios (empty results, validation error, outage) *(Verify: sandbox test run | Sign-off: _______)*
- [ ] Timeout on ⚠️ mutating MCP tools (`cart_grocery_checkout`, `apply_promotion_code`, `create_ride`) executes **1 call only** (zero automatic retries) *(Verify: `pytest tests/test_mcp_safety.py` | Sign-off: _______)*
- [ ] Circuit breaker opens for `30s` after `5` consecutive Careem MCP `5xx`/timeouts while core Royalty API stays `200 OK` *(Verify: chaos test | Sign-off: _______)*
- [ ] AWS Bedrock `copilot.py` prompt inspection confirms **zero PII** (no names, phones, GPS, trip IDs) and deterministic offline fallback works without AWS creds *(Verify: prompt log & offline test | Sign-off: _______)*
- [ ] `.kiro/specs/royalty/` (`requirements.md`, `design.md`, `tasks.md`) matches implemented routes, schema, and tests *(Verify: manual diff | Sign-off: _______)*

---

## F. Frontend Wiring, Arabic RTL & Performance QA
- [ ] `docs/ui-prototype/index.html` (or production UI) fetches live state from `/v1/*` and updates XP/Split/Budget dynamically *(Verify: browser DevTools Network tab | Sign-off: _______)*
- [ ] Arabic (`dir="rtl"`) layout renders cleanly with zero clipped text, broken icons, or contrast failures (`WCAG 2.1 AA`) *(Verify: browser RTL check | Sign-off: _______)*
- [ ] API load test confirms `p99 < 250ms` on `GET /v1/captains/{id}/loyalty/status` under 100 concurrent users *(Verify: `locust` / `k6` | Sign-off: _______)*

---

**Lead Software Engineer Final QA Sign-Off:** `_________________________` · **Date:** `_____________`
