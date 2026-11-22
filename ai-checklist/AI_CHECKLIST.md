# ROYALTY — AI Execution & Build Checklist

> **For AI Agents:** Check `[x]` here **only after** you have implemented the item and observed its automated test/command pass. Never touch `checklist/` or `qa/`.

---

## 1. Packaging & Repo Hygiene
- [ ] Create `pyproject.toml` pinning runtime & dev dependencies (`fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, `boto3`, `httpx`, `pytest`, `schemathesis`)
- [ ] Add `.gitignore` (`.env`, `.venv/`, `__pycache__/`, `*.pyc`, `*.db`) and remove tracked `__pycache__` files from git

---

## 2. Kiro Spec-Driven Artifacts (`.kiro/specs/royalty/`)
- [ ] Create `.kiro/specs/royalty/requirements.md` (EARS-syntax requirements synced with `openapi.yaml`)
- [ ] Create `.kiro/specs/royalty/design.md` (architecture, locking, Careem MCP & Bedrock boundaries)
- [ ] Create `.kiro/specs/royalty/tasks.md` (ordered implementation tasks)

---

## 3. Backend API & Dual-Mode Persistence (`src/royalty/`)
- [ ] Preserve existing `src/royalty/algorithm.py` invariants (`60/40 → 40/60`, `28/72 → 14/86`, 10h fatigue cap, JOD 1.50/1.0 km wash guard, `remaining_reward_budget_jod`)
- [ ] Implement `src/royalty/db.py` supporting zero-setup SQLite (`BEGIN IMMEDIATE`) and PostgreSQL (`SELECT ... FOR UPDATE`) using `001_initial_schema.sql`
- [ ] Implement `src/royalty/api.py` (FastAPI) matching `docs/api/openapi.yaml` (`/loyalty/status`, `/events/trips/completed`, `/rewards/{id}/redeem`, `/family-benefits/assign`, `/recommendations`, `/preferences`)
- [ ] Enforce `Idempotency-Key` deduplication on all `POST` mutations and atomic `outbox_events` writes

---

## 4. Careem MCP Bridge & AWS Bedrock Co-Pilot
- [ ] Implement `src/royalty/careem_mcp_client.py` (Streamable HTTP, OAuth 2.0 PKCE `S256`, 8s timeout, 30s circuit breaker)
- [ ] Enforce HITL confirmation gate so ⚠️ mutating tools (`cart_grocery_checkout`, `apply_promotion_code`, `create_ride`) **never** auto-execute or auto-retry on timeout
- [ ] Implement `src/royalty/copilot.py` using `boto3` (`bedrock-runtime`) `Converse` API with PII-free prompts and offline deterministic fallback

---

## 5. Live-Wired Bilingual RTL UI (`docs/ui-prototype/index.html`)
- [ ] Connect `Hub`, `Pass`, `For You`, and `Family` tabs to live FastAPI `/v1/*` endpoints
- [ ] Add interactive Trip/Fatigue/Budget-Cap Simulator bar for technical verification
- [ ] Add 1-click **Arabic (`العربية`) RTL** (`dir="rtl"`) toggle

---

## 6. Automated Verification Suite (`tests/`)
- [ ] Keep all 5 existing tests in `tests/test_royalty.py` passing
- [ ] Add `tests/test_concurrency.py` (10-thread concurrent redeem race test → 1× `201`, 9× `409`)
- [ ] Add `tests/test_idempotency.py` (duplicate `TripCompleted` replay test)
- [ ] Add `tests/test_mcp_safety.py` (mutating-tool timeout zero-retry + consent-off zero-MCP-call tests)
- [ ] Run `schemathesis` OpenAPI contract fuzzing and `gitleaks` secret scan with zero errors
