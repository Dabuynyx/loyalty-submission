# 11 — Royalty Beginner-to-End Code Implementation Guide

**Audience:** Junior to Senior Engineers starting from scratch on `Dabuynyx/loyalty-submission`  
**Goal:** Walk step-by-step from an empty laptop setup to a working, tested, Careem-MCP-connected Royalty application—without guessing what to build next.

---

## Step 0 — Prerequisites & Local Environment Setup

1. **Install Required Tools:**
   - **Python 3.12+** (matches existing `src/royalty/` prototype)
   - **PostgreSQL 16+** (or Docker Desktop to run Postgres locally)
   - **Node.js 20+** (only needed if running Careem's Local Sandbox or MCP Inspector)
   - **Git & GitHub CLI (`gh`)**
2. **Clone & Verify Existing Prototype:**
   ```bash
   git clone https://github.com/Dabuynyx/loyalty-submission.git
   cd loyalty-submission
   python3 -m unittest discover -s tests -v   # Expect: 5/5 tests OK
   ```
3. **Create Virtual Environment & Copy Env Template:**
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   cp docs/engineering/glossary-and-env.md .env.example  # Extract the .env block into .env
   ```
   > **Never commit `.env`** — add `.env` and `.venv/` to `.gitignore` first.

---

## Step 1 — Set Up the PostgreSQL Database

1. **Start Local Postgres (via Docker):**
   ```bash
   docker run --name royalty-pg -e POSTGRES_USER=royalty_user \
     -e POSTGRES_PASSWORD=CHANGE_ME_LOCAL -e POSTGRES_DB=royalty_dev \
     -p 5432:5432 -d postgres:16
   ```
2. **Apply Migration `001_initial_schema.sql`:**
   ```bash
   psql postgresql://royalty_user:CHANGE_ME_LOCAL@localhost:5432/royalty_dev \
     -f docs/schemas/database/001_initial_schema.sql
   ```
3. **Seed Jordan (`JO`) Config & Season 11:**
   - Insert `country_configs` row for `JO` (`JOD`, `ar`, `Asia/Amman`, `max_reward_budget_pct = 0.2200`, `is_active = true`).
   - Insert `loyalty_seasons` + 6 `loyalty_tiers` rows matching `DEFAULT_FLEET_TIERS` (`60/40 → 40/60`) and `INDEPENDENT_JORDAN_TIERS` (`28/72 → 14/86`).

---

## Step 2 — Build the Modular Monolith Skeleton

Organize `src/royalty/` cleanly without breaking existing `algorithm.py` or `mcp_server.py`:

```text
src/royalty/
  __init__.py
  algorithm.py          # EXISTING — keep pure math & invariants intact
  mcp_server.py         # EXISTING — extend with DB persistence in Step 6
  config.py             # NEW: Pydantic settings reading .env
  db.py                 # NEW: SQLAlchemy/psycopg async pool + session helper
  auth.py               # NEW: JWT / Careem OAuth2 PKCE token verifier
  routers/
    captains.py         # GET status, progression, eligibility, recommendations
    rewards.py          # GET catalog, POST redeem (with SELECT FOR UPDATE)
    family.py           # GET/POST Beit Careem beneficiaries & promo assignment
    events.py           # POST /events/trips/completed (idempotent)
    admin.py            # Country configs, budgets, partner offers (Admin RBAC)
  workers/
    outbox_worker.py    # Polls outbox_events WHERE published = FALSE
```

**Recommended Stack:** **FastAPI** + **Pydantic v2** + **psycopg 3 (or SQLAlchemy 2.0)** + **Alembic** + **pytest**.

---

## Step 3 — Implement Authentication & RBAC (`auth.py`)

1. Validate `Authorization: Bearer <jwt>` on every `/v1/*` endpoint against Careem Identity's JWKS (`https://identity.careem.com/.well-known/openid-configuration`).
2. Extract `sub` (mapped to `captain_refs.careem_captain_ref`) and `role` (`CAPTAIN | FAMILY | ADMIN | OPS`).
3. **Ownership Check:** A `CAPTAIN` token may **only** access `/captains/{captain_id}/*` where `captain_id` belongs to their `sub`. Return `403 Forbidden` otherwise.

---

## Step 4 — Wire the Reward Engine & Budget Lock (`rewards.py`, `events.py`)

1. **Idempotent `TripCompleted` Handler (`POST /events/trips/completed`):**
   - Check `Idempotency-Key` header; if already in `progression_history`, return `202` immediately.
   - Inside `BEGIN ... COMMIT`:
     1. Lock `reward_budgets` row with `SELECT ... FOR UPDATE`.
     2. Call `calculate_trip_xp(...)` and `calculate_trip_split(...)` from `src/royalty/algorithm.py`.
     3. Update `loyalty_accounts` (`season_xp`, `current_tier`) and `reward_budgets` (`gross_fares_local`, `uplift_paid_local`).
     4. Insert `progression_history` + `outbox_events` (`TierUpgraded` if tier increased).
2. **Atomic Reward Redemption (`POST /captains/{id}/rewards/{reward_id}/redeem`):**
   - Require `Idempotency-Key` header.
   - Lock `reward_budgets` + `reward_inventory` (`FOR UPDATE`).
   - Verify `remaining_reward_budget_jod >= reward.direct_cost_local` (always passes if `PARTNER_FUNDED` where `direct_cost_local == 0`).
   - Deduct inventory, insert `reward_transactions` (`ISSUE`), and call partner webhook; if partner fails (`503`), insert compensating `REFUND` transaction.

---

## Step 5 — Implement Beit Careem Family Benefits (`family.py`)

1. **Register Beneficiary:** Enforce max **3 active beneficiaries** per `captain_id` and OTP verification of the family member's Careem account.
2. **Assign Promo (`POST .../family-benefits/assign`):**
   - Verify `current_tier >= 3`.
   - Lock `reward_budgets`, check `remaining_reward_budget_jod >= amount_local`, mint single-use `BEIT-*` code bound to `careem_consumer_ref`, and insert into `promotional_codes`.

---

## Step 6 — Connect Careem Official MCP + Sandbox Testing

1. **Test Locally First (Zero Risk):**
   - Set up Careem's **Local Sandbox** (`builders.careem.com/docs/sandbox`) and connect MCP Inspector or Claude/Cursor to verify `user_info`, `search_groceries_items`, `create_grocery_cart_with_quantities` ⚠️, and `cart_get_basket_price`.
2. **Connect to Production Careem MCP (`https://mcp.careemapis.com/mcp`):**
   - Implement OAuth 2.0 Authorization Code + PKCE (`S256`) using Hackathon Client ID `1790a895-9cef-48b7-9a57-ec5670d50c41` and scopes `openid profile offline_access`.
   - **Mandatory Safety Rules:**
     - `8s` timeout per MCP call.
     - Circuit breaker (5 failures → 30s open).
     - **NEVER auto-retry ⚠️ mutating tools** (`cart_checkout`, `cart_grocery_checkout`, `create_ride`, `apply_promotion_code`). Always show the user the exact total and wait for `"yes"`.

---

## Step 7 — Implement Consent-Driven Personalization (`personalization`)

1. Check `consent_records` for `LIFESTYLE_PERSONALIZATION`.
2. If `granted = false`: return **cold-start quests** (Safe-Shift break, Weekly Flex 15 rides) and **never** call Careem MCP `get_activities`.
3. If `granted = true`: read coarse food/grocery categories, filter `reward_catalog` by `country_code` + `tier` + `remaining_budget`, and attach a plain-English `explanation_text`.

---

## Step 8 — Connect the Frontend UI (`docs/ui-prototype/index.html`)

1. Port the 4-tab prototype (`Hub`, `Pass`, `For You`, `Family`) into React / React Native / Flutter using the exact design tokens in **Doc 09** (`#007A3D`, `#00A859`, `#ECFDF5`, `#F59E0B`).
2. Add Arabic **RTL (`dir="rtl"`)** + English LTR toggle.
3. Implement all 4 required UI states per screen: **Loading (skeleton)**, **Empty (100 Endowed XP)**, **Error (409 Budget Cap / retry)**, and **Offline (cached tier banner)**.

---

## Step 9 — Run the Full Verification Suite

1. **Unit & Algorithm Tests:** `python3 -m unittest discover -s tests -v`
2. **Concurrency Stress Test:** Fire 10 parallel `POST /redeem` requests against the same `reward_budgets` row → assert **only 1** returns `201` and **9** return `409 Conflict`.
3. **OpenAPI Contract Fuzzing:** Run `schemathesis run docs/api/openapi.yaml --base-url http://localhost:8000/v1`.
4. **Secret Scan:** Run `gitleaks detect` before every push.

---

## Step 10 — Deploy to Staging & Launch the 200-Captain Amman Pilot

1. Deploy container + Postgres to Staging pointing at `https://mcp.sandbox.careemapis.com/mcp`.
2. Verify `country_configs` for `JO` has Careem Finance sign-off on `max_reward_budget_pct`.
3. Enable `is_active = true` for 200 Amman Captains, monitor the **Budget Guard** and **Outbox Lag** dashboards, and iterate before expanding to `AE`, `SA`, and `EG`.
