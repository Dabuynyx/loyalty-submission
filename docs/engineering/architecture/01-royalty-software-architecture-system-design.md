# 01 — Royalty Software Architecture & System Design

**Role:** Principal Software Architecture Specification  
**Implementation Status:** Prototype core (`src/royalty/algorithm.py`, `src/royalty/mcp_server.py`) verified; production backend, DB, and frontend are **documented for Phase 2+ implementation**.

---

## 1. Repository & Code Audit (Gap Analysis)

We audited the existing repository (`src/royalty/`, `tests/`, `docs/`) against the full product & MCP specification:

| Area | Status | Details & Gap Analysis |
| :--- | :--- | :--- |
| **Core Split & Cap Algorithm** | **Implemented (Prototype)** | `src/royalty/algorithm.py` implements `DEFAULT_FLEET_TIERS` (`60/40 → 40/60`), `INDEPENDENT_JORDAN_TIERS` (`28/72 → 14/86`), `calculate_trip_xp`, `resolve_tier`, `remaining_reward_budget_jod`, `issue_family_promo`, `apply_season_soft_reset`. |
| **Unit Tests** | **Implemented (5/5 Passing)** | `tests/test_royalty.py` verifies 60% cap, budget cap guard, 10h fatigue cap, wash-trip guard, soft reset, and MCP status tool. |
| **Captain MCP Extension** | **Partially Implemented** | `src/royalty/mcp_server.py` provides an in-memory JSON-RPC 2.0 stdio prototype. Lacks OAuth/JWT verification, PostgreSQL persistence, and live Careem MCP client bridge. |
| **Careem Official MCP** | **Verified External** | `mcp.careemapis.com/mcp` exposes 50 consumer tools across 8 domains (OAuth 2.0 + PKCE `S256`). Zero Captain-side tools exist. |
| **Production Backend, DB, API, Outbox** | **Missing (Specified Here)** | Needs FastAPI/HTTP API (`docs/api/openapi.yaml`), PostgreSQL (`001_initial_schema.sql`), outbox worker, and partner adapters. |
| **Careem Internal Integrations** | **Unverified** | Careem Dispatch `TripCompleted` webhook, Careem Promo Minting API, and Careem Pay payout ledger require Careem engineering sign-off. |

**Unchanged Core Invariants:** `DEFAULT_FLEET_TIERS`, `INDEPENDENT_JORDAN_TIERS`, 10h daily XP cap, JOD 1.50 / 1.0 km wash-trip guard, and `remaining_reward_budget_jod` must remain unchanged.

---

## 2. System Definition, Actors & Boundaries

**Royalty** is an externalized loyalty, progression, and household-benefit orchestration system. It **does not** own trip dispatch, fare metering, driver GPS tracking, or core payment settlement—those remain strictly owned by **Careem**.

### Actors & Authorization Matrix

| Actor | Authorized Operations |
| :--- | :--- |
| **Captain** | View status/tier/receipts, opt-in/out of lifestyle personalization, manage up to 3 family beneficiaries, issue/redeem rewards. |
| **Eligible Family Member** | Redeem account-bound `BEIT-*` promo codes inside Careem Consumer App / Careem MCP (`apply_promotion_code`, `cart_grocery_checkout`). |
| **Royalty Administrator** | Configure `country_configs`, `loyalty_seasons`, `max_reward_budget_pct`, and `reward_catalog` (all actions audit-logged). |
| **Careem Operations** | Onboard local `partner_organizations`, view regional budget dashboards, resolve cash-settlement holds. |
| **Reward Partner** | Validate/reconcile partner-funded vouchers via signed webhook/API. |
| **Careem Dispatch / Identity** | Emit `TripCompleted` events; issue OAuth 2.0 PKCE tokens. |

---

## 3. Architecture Decision: Modular Monolith (MVP) → Services (Target)

Per **ADR-0001**, Royalty launches as a **Modular Monolith** backed by PostgreSQL + Transactional Outbox (`docs/diagrams/architecture/system-architecture.mmd`):
- **Why Modular Monolith for MVP:** Single ACID transaction boundary for `reward_budgets` locking (`SELECT ... FOR UPDATE`), zero distributed-transaction overhead, and fast iteration for a small team.
- **Internal Modules:** `api_gateway`, `auth_rbac`, `reward_engine`, `catalog_redemption`, `family_service`, `personalization`, `mcp_bridge`, `regional_config`, `audit_observability`.
- **Target Regional Architecture:** Partitioned PostgreSQL by `country_code` + extracted async workers for `personalization` and `analytics` once trip volume exceeds 500k/day.

---

## 4. Component Specifications

| Component | Purpose | Inputs / Outputs | Failure Modes & Scaling |
| :--- | :--- | :--- | :--- |
| **Royalty REST API** | External HTTP interface (`openapi.yaml`) | JWT + JSON → HTTP JSON | Rate-limited (100 req/min/Captain); stateless horizontal scaling. |
| **Reward & Budget Engine** | Deterministic split, XP & budget cap | `TripCompleted` / Claim → `Split` + `BudgetDelta` | Row lock contention mitigated by per-Captain row; idempotent via `idempotency_key`. |
| **Beit Careem Family Service** | Beneficiary verification & code minting | `captain_id`, `beneficiary_id` → `BEIT-*` code | Max 3 beneficiaries; fails closed if budget cap reached. |
| **MCP Bridge** | Invokes Careem MCP (`OAuth2 PKCE`) + hosts Captain MCP | Tool calls → Structured JSON | Circuit breaker (5 failures → 30s open); **never auto-retries mutating tools**. |
| **Personalization & Consent** | Opt-in lifestyle ranking | `consent_records` + `get_activities` → Ranked offers | Falls back to cold-start quests if consent=false or Careem MCP unavailable. |
| **Audit & Outbox Worker** | Reliable event publishing & compliance trail | `outbox_events` → Event Bus / Partner Webhook | Dead-letter queue after 5 exponential retries; alert if lag > 30s. |
