# 12 — Royalty Technical Intensification Blueprint (6 Core Upgrades)

**Purpose:** Deep technical specification for taking Royalty from a documented prototype (`src/royalty/algorithm.py`, `src/royalty/mcp_server.py`, static UI mockup) to a **30/30 production-grade, judge-ready engineering system**—without breaking any existing invariants.  
**Status:** Specification Only (No production code written in this document).

---

## Overview of the 6 Technical Upgrades

| # | Upgrade | Target Location | Core Problem Solved |
| :---: | :--- | :--- | :--- |
| **1** | **Live FastAPI Backend & Dual-Mode DB** | `src/royalty/api.py`, `db.py` | Turns `openapi.yaml` and `001_initial_schema.sql` into a real, persistent, idempotent REST API. |
| **2** | **Live Careem MCP Client Bridge** | `src/royalty/careem_mcp_client.py` | Connects Royalty to `mcp.careemapis.com/mcp` (or Local Sandbox) via OAuth 2.0 PKCE + HITL safety. |
| **3** | **AWS Bedrock Co-Pilot AI Engine** | `src/royalty/copilot.py` | Delivers PII-free Arabic/English shift summaries & lifestyle deal phrasing via Bedrock. |
| **4** | **Live-Wired, Bilingual RTL UI** | `docs/ui-prototype/index.html` | Connects the 4-tab Careem UI to live API state with Arabic RTL & interactive trip simulation. |
| **5** | **Kiro Spec-Driven Artifacts** | `.kiro/specs/royalty/` | Formalizes EARS requirements, design invariants, and task tracking for Kiro workflows. |
| **6** | **Packaging & Concurrency QA** | `pyproject.toml`, `tests/` | Enforces race-condition safety, idempotency, OpenAPI contract fuzzing, and clean repo hygiene. |

---

## Upgrade 1 — Live FastAPI Backend & Dual-Mode Persistence (`api.py` + `db.py`)

### 1.1 Why Dual-Mode Persistence?
- **Zero-Setup Evaluation (SQLite):** Judges or local developers can run the entire server with `uvicorn` in 1 command without installing PostgreSQL or Docker.
- **Production Parity (PostgreSQL 16):** The exact same SQLAlchemy 2.0 / SQL DDL (`docs/schemas/database/001_initial_schema.sql`) runs against PostgreSQL in staging/production simply by changing `DATABASE_URL`.

### 1.2 Transaction & Concurrency Mechanics
- **Idempotency Middleware:** Every `POST` mutation (`TripCompleted`, `Redeem`, `FamilyAssign`) requires an `Idempotency-Key` UUID header. Before executing business logic, the handler checks `progression_history` or `reward_transactions`. If found, it returns the cached response (`200`/`202`) without mutating state.
- **Row-Level Locking:**
  - In **PostgreSQL**, `SELECT ... FROM reward_budgets WHERE account_id = :id FOR UPDATE` serializes concurrent claims for the same Captain.
  - In **SQLite**, `BEGIN IMMEDIATE` acquires a write lock at transaction start, guaranteeing identical race-condition safety during local demos.
- **Transactional Outbox:** Every tier upgrade (`TierUpgraded`) or promo issuance (`FamilyBenefitAssigned`) inserts into `outbox_events` in the **same** database commit, ensuring zero lost notifications.

---

## Upgrade 2 — Live Careem MCP Client Bridge (`careem_mcp_client.py`)

### 2.1 Connection & OAuth 2.0 PKCE Flow
1. **Discovery:** Fetch `https://mcp.careemapis.com/.well-known/oauth-protected-resource` (RFC 9728) and `https://identity.careem.com/.well-known/openid-configuration`.
2. **Auth Code + PKCE (`S256`):** Generate `code_verifier` + `code_challenge`, authenticate via Careem Identity with scopes `openid profile offline_access`, and store `access_token` / `refresh_token` strictly in memory or encrypted OS keychain—**never** in logs or git.
3. **Transport:** Streamable HTTP (`POST https://mcp.careemapis.com/mcp`) with `Authorization: Bearer <access_token>`.

### 2.2 Reliability & Mutating-Tool Safety Gate
- **Timeouts & Retries:** `8.0s` per-call timeout. Read-only tools (`user_info`, `get_activities`, `food_dish_search`, `search_groceries_items`, `cart_get_basket_price`) retry up to **2×** with jittered exponential backoff.
- **Circuit Breaker:** Opens for **30 seconds** after 5 consecutive `5xx`/timeout responses, degrading Royalty gracefully to core split/tier/catalog features.
- **Strict HITL Gate for ⚠️ Mutating Tools:** `apply_promotion_code`, `create_grocery_cart_with_quantities`, `cart_grocery_checkout`, `cart_checkout`, and `create_ride` **never** execute automatically and **never** auto-retry on timeout. The bridge returns a `ConfirmationRequired` payload containing exact items, delivery address, and final JOD total for explicit user approval.

---

## Upgrade 3 — AWS Bedrock "Co-Pilot AI" Engine (`copilot.py`)

### 3.1 Architecture & Strict Determinism Boundary
- **Client:** `boto3.client("bedrock-runtime", region_name=settings.AWS_REGION)` calling the Bedrock `Converse` API (default model configured via `BEDROCK_MODEL_ID`).
- **What Bedrock DOES:**
  1. Generates warm, motivating **Arabic & English end-of-shift summaries** (*"أحسنت يا كابتن أحمد!"*).
  2. Writes concise, plain-English **lifestyle offer explanations** for the `For You` tab (e.g., explaining why a partner-funded post-shift burger deal was surfaced).
  3. Answers Captain *"How do I reach Tier 5?"* questions using exact deterministic gaps (`xp_to_next_tier`, `rating`, `cancel_rate`).
- **What Bedrock NEVER DOES:** Bedrock **never** computes commission splits, XP, or `remaining_reward_budget_jod`. Those numbers are computed beforehand by `src/royalty/algorithm.py` and injected as read-only facts into the system prompt.
- **PII-Free Prompt Contract:** Only `tier_name`, `driver_pct`, `xp_to_next`, `remaining_budget_local`, and coarse category tags (`["burgers", "coffee"]`) are sent to Bedrock. Zero names, phone numbers, GPS coordinates, or trip IDs leave Royalty.
- **Offline Deterministic Fallback:** If AWS credentials are absent or Bedrock times out, `copilot.py` falls back cleanly to pre-audited Arabic/English templates so tests and local demos never crash.

---

## Upgrade 4 — Live-Wired, Bilingual RTL Captain UI (`docs/ui-prototype/index.html`)

### 4.1 Connecting the 4-Tab Prototype to Real State
- Replace hardcoded JS values with `fetch("/v1/captains/cap_ahmad/loyalty/status")` and live `POST` calls for:
  - **Simulate Trip Bar (Demo/QA Control):** Buttons to trigger `Normal Ride (JOD 5)`, `Peak Cashless Ride (JOD 8)`, `Wash Ride (JOD 1.20 → 0 XP)`, or `10h Fatigue Cap Test`, watching the XP bar and `driver_pct` update live from the backend.
  - **Family Tab:** Calling `POST /v1/captains/{id}/family-benefits/assign` with a generated `Idempotency-Key` UUID, decrementing `Remaining Season Reward Budget` live and showing `409 Conflict` gracefully when the budget cap is reached.
- **1-Click Arabic (`العربية`) RTL Toggle:** Switches `<html dir="rtl" lang="ar">` and translates all labels, receipts, and tier names cleanly to verify WCAG 2.1 AA and RTL layout integrity.

---

## Upgrade 5 — Kiro Spec-Driven Engineering Artifacts (`.kiro/specs/royalty/`)

To align directly with the **Kiro** toolchain in the judging criteria, maintain a synchronized spec folder:
- `.kiro/specs/royalty/requirements.md` — Formal **EARS-syntax** requirements (*"WHEN a `TripCompleted` event arrives with a duplicate `Idempotency-Key`, THE Royalty Engine SHALL return 202 without mutating `reward_budgets`"*).
- `.kiro/specs/royalty/design.md` — Component boundaries, SQL locking strategy, and Careem MCP vs. Bedrock isolation rules.
- `.kiro/specs/royalty/tasks.md` — Ordered, checkable implementation tasks mapped 1:1 to `docs/engineering/roadmap/10`.

---

## Upgrade 6 — Production Packaging, Git Hygiene & Concurrency QA

1. **`pyproject.toml` & Clean `.gitignore`:**
   - Pin dependencies (`fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, `boto3`, `httpx`, `pytest`, `schemathesis`) and remove tracked `__pycache__/*.pyc` artifacts from git.
2. **Concurrency & Race-Condition Test (`tests/test_concurrency.py`):**
   - Launch **10 parallel threads** calling `POST /rewards/{id}/redeem` against a Captain with only `JOD 5.00` remaining budget → assert **exactly 1** returns `201 Created`, **9** return `409 Conflict`, and `remaining_reward_budget_jod == 0.00` (never negative).
3. **MCP Safety & Idempotency Tests (`tests/test_mcp_safety.py`):**
   - Simulate a `10s` timeout on `cart_grocery_checkout` ⚠️ → assert `call_count == 1` (proving mutating tools never auto-retry).
   - Replay the same `TripCompleted` `Idempotency-Key` 3 times → assert XP and `gross_fares_local` increment **once**.
4. **OpenAPI Contract Fuzzing:**
   - Run `schemathesis run docs/api/openapi.yaml` against the local FastAPI app in CI to guarantee zero drift between documentation and implementation.
