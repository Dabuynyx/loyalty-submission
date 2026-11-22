# 02 — Royalty Database Design & Data Dictionary

**Database Engine:** PostgreSQL 16+ (ACID transactions, `JSONB`, `SELECT ... FOR UPDATE`, partial indexes)  
**Reference Migration:** [`docs/schemas/database/001_initial_schema.sql`](../../schemas/database/001_initial_schema.sql)  
**ER Diagram Source:** [`docs/diagrams/database/er-diagram.mmd`](../../diagrams/database/er-diagram.mmd)

---

## 1. Data Ownership & Boundary Classification

| Classification | Entities / Fields | Rule |
| :--- | :--- | :--- |
| **A. Owned by Royalty** | `loyalty_seasons`, `loyalty_tiers`, `loyalty_accounts`, `reward_budgets`, `progression_history`, `reward_catalog`, `reward_inventory`, `reward_transactions`, `promotional_codes`, `consent_records`, `captain_preferences`, `personalized_recommendations`, `outbox_events`, `audit_events` | Royalty is the system of record. |
| **B. Owned by Careem** | Captain legal identity, vehicle/LTRC docs, live GPS telemetry, trip fare calculation, payment card tokens, Careem Pay wallet balance | **Never owned by Royalty.** |
| **C. Referenced Externally** | `careem_captain_ref` (opaque UUID/string), `careem_consumer_ref`, `source_trip_id` | Stored as opaque external IDs (never phone numbers or emails as primary keys). |
| **D. Never Copied into Royalty** | Passwords, OAuth client secrets, raw credit card PANs, national ID scans, raw home street addresses | Strictly prohibited from Royalty DB. |

---

## 2. Core Data Dictionary (22 Entities)

| Table | Primary Key | Key Foreign Keys & Unique Constraints | Retention & PII Class |
| :--- | :--- | :--- | :--- |
| `country_configs` | `country_code` (`CHAR(2)`) | `CHECK (max_reward_budget_pct <= 0.50)` | Permanent · Public/Config |
| `city_configs` | `city_id` (`VARCHAR(32)`) | FK → `country_configs` | Permanent · Config |
| `captain_refs` | `captain_id` (`UUID`) | `UNIQUE(careem_captain_ref)`, FK → `country_configs`, `city_configs` | Account lifetime · Pseudonymous |
| `loyalty_seasons` | `season_id` (`UUID`) | FK → `country_configs` | 7 years (financial audit) · Internal |
| `loyalty_tiers` | `tier_id` (`SERIAL`) | FK → `loyalty_seasons`, `UNIQUE(season_id, fleet_type, tier_number)` | 7 years · Config |
| `loyalty_accounts` | `account_id` (`UUID`) | FK → `captain_refs`, `loyalty_seasons`, `UNIQUE(captain_id, season_id)` | 7 years · Internal |
| `reward_budgets` | `budget_id` (`UUID`) | `UNIQUE FK` → `loyalty_accounts` | 7 years · Financial |
| `progression_history` | `history_id` (`UUID`) | FK → `loyalty_accounts`, `UNIQUE(idempotency_key)` | 7 years · Financial/Audit |
| `partner_organizations` | `partner_id` (`UUID`) | FK → `country_configs` | Contract + 7 years · B2B |
| `reward_catalog` | `reward_id` (`UUID`) | FK → `country_configs`, `partner_organizations` | 7 years · Catalog |
| `reward_inventory` | `reward_id` (`UUID`) | `PK/FK` → `reward_catalog` | Season + 1 year · Inventory |
| `family_beneficiaries` | `beneficiary_id` (`UUID`) | FK → `captain_refs`, `UNIQUE(captain_id, careem_consumer_ref)` | Until revoked + 90d · Pseudonymous |
| `promotional_codes` | `promo_id` (`UUID`) | `UNIQUE(code)`, FK → `captain_refs`, `reward_catalog` | 7 years · Financial |
| `reward_transactions` | `tx_id` (`UUID`) | FK → `loyalty_accounts`, `reward_catalog`, `UNIQUE(idempotency_key)` | 7 years · Financial Ledger |
| `consent_records` | `consent_id` (`UUID`) | FK → `captain_refs`, `UNIQUE(captain_id, purpose)` | Account + 5 years · Compliance |
| `captain_preferences` | `captain_id` (`UUID`) | `PK/FK` → `captain_refs` | Deleted on opt-out · Restricted |
| `personalized_recommendations` | `rec_id` (`UUID`) | FK → `captain_refs`, `reward_catalog` | 30 days TTL · Restricted |
| `outbox_events` | `event_id` (`UUID`) | Partial index `(published, created_at) WHERE NOT published` | 14 days post-publish · Internal |
| `audit_events` | `audit_id` (`UUID`) | Index `(actor_id, created_at DESC)` | 7 years immutable · Audit |

*(Note: `reward_policies`, `admin_actions`, `experiment_assignments`, and `analytics_events` follow the same `country_code` + `UUID` key pattern and 2–7 year retention tiers.)*

---

## 3. Indexing & Migration Strategy
- **Hot Path Indexes:** `idx_loyalty_accounts_captain` for O(1) status lookup; `idx_outbox_unpublished` partial index keeps background polling sub-millisecond.
- **Zero-Downtime Migrations:** Expand-and-contract pattern (add nullable columns → backfill → enforce `NOT NULL` → drop old columns in subsequent release). Managed via Alembic/Flyway with automated rollback scripts.
