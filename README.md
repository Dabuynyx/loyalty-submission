# ROYALTY — Careem Builders ’26 (Amman, Jordan)

> **Captain-First Loyalty, Household Benefits & Dual-Layer MCP Ecosystem**  
> **Repository:** `Dabuynyx/loyalty-submission`

---

## Executive Summary

> **Canonical Model Notice (v2.0):** Following an architectural & unit-economics red-team review, **Royalty v2.0** standardizes on **Weekly Marginal Brackets (`75% → 85%`, `90%` on peak trips = ~21.5% blended Careem take)**, **Same-Day Digital Cashout for all Captains**, **Incremental-GMV Food Partner Royalty**, and **CBJ/PDPL-compliant Wallet loops (`Ride-to-Table`, `In-Sync Arrival`)**. See **[RED_TEAM_V2_UNIFIED_SPEC.pdf](docs/RED_TEAM_V2_UNIFIED_SPEC.pdf)** as the single source of truth. *(Earlier v1 docs `01`, `03`, `04` and `src/royalty/algorithm.py` reflect the superseded 6-tier `60/40 → 40/60` archive).*

**Royalty** is a next-generation Captain, Merchant, and Wallet loyalty ecosystem built for **Careem Builders ’26** in Amman, Jordan. It solves Jordan's acute multi-homing problem (Careem vs. Uber, Jeeny, Petra Ride, Talabat) by combining:

1. **Weekly Marginal Captain Brackets (`75% → 85%`, `90%` Peak):** Captains earn `75%` (rides 1–30), `80%` (31–55), `85%` (56+), and `90%` on peak/hard-to-serve trips—protecting Careem's ~21.5% blended take-rate while paying maximum marginal value on the *next* ride.
2. **Same-Day Cashout + "Beit Careem" Promo Codes:** Every Captain gets same-day digital cashout on Card/Wallet rides from Day 1 (fixing driver cash-only pushback) plus account-bound household Ride/Food promo codes.
3. **Ride-to-Table & Food Partner Royalty:** Restaurants earn lower commission on *incremental* GMV above their 8-week baseline and sponsor customer rides to their venues via Careem's Super App.
4. **Dual-Layer Careem MCP Architecture:** Audited all **50 tools across 8 domains** on `https://mcp.careemapis.com/mcp`, pairing Careem's Consumer MCP (Best 12 MVP tools) with a custom Royalty extension (`src/royalty/mcp_server.py`).

### Canonical v2.0 Specification
- **[RED_TEAM_V2_UNIFIED_SPEC.pdf](docs/RED_TEAM_V2_UNIFIED_SPEC.pdf)** ([MD](docs/RED_TEAM_V2_UNIFIED_SPEC.md)) — **Single Source of Truth (v2.0)** resolving all v1/v2 inconsistencies, unit-economics leaks, CBJ/JoMoPay compliance, and MCP workflows.

---

## Deliverables (9 Separate PDFs + Editable Markdown)

| # | Document Title | Markdown | PDF |
| :---: | :--- | :---: | :---: |
| **01** | **Royalty Master Product Strategy** | [MD](docs/product-strategy/01-royalty-master-product-strategy.md) | [PDF](docs/product-strategy/01%20%E2%80%94%20Royalty%20Master%20Product%20Strategy.pdf) |
| **02** | **Royalty MCP Technical Architecture** | [MD](docs/technical-architecture/02-royalty-mcp-technical-architecture.md) | [PDF](docs/technical-architecture/02%20%E2%80%94%20Royalty%20MCP%20Technical%20Architecture.pdf) |
| **03** | **Royalty Captain Loyalty & Progression System** | [MD](docs/captain-experience/03-royalty-captain-loyalty-progression-system.md) | [PDF](docs/captain-experience/03%20%E2%80%94%20Royalty%20Captain%20Loyalty%20%26%20Progression%20System.pdf) |
| **04** | **Royalty Incentive Economics & Reward Algorithm** | [MD](docs/incentive-economics/04-royalty-incentive-economics-reward-algorithm.md) | [PDF](docs/incentive-economics/04%20%E2%80%94%20Royalty%20Incentive%20Economics%20%26%20Reward%20Algorithm.pdf) |
| **05** | **Royalty Family Benefits & Partnerships** | [MD](docs/family-benefits/05-royalty-family-benefits-partnerships.md) | [PDF](docs/family-benefits/05%20%E2%80%94%20Royalty%20Family%20Benefits%20%26%20Partnerships.pdf) |
| **06** | **Royalty Competitive Research & Differentiation** | [MD](docs/competitive-research/06-royalty-competitive-research-differentiation.md) | [PDF](docs/competitive-research/06%20%E2%80%94%20Royalty%20Competitive%20Research%20%26%20Differentiation.pdf) |
| **07** | **Royalty Captain UX & Implementation Roadmap** | [MD](docs/captain-experience/07-royalty-captain-ux-implementation-roadmap.md) | [PDF](docs/captain-experience/07%20%E2%80%94%20Royalty%20Captain%20UX%20%26%20Implementation%20Roadmap.pdf) |
| **08** | **Royalty Extra: Rider Experience & Careem Plus** *(Supplementary)* | [MD](docs/rider-experience/08-royalty-extra-rider-experience.md) | [PDF](docs/rider-experience/Royalty_Extra_Rider_Experience.pdf) |
| **09** | **Royalty Research Sources & Assumptions** | [MD](docs/research-sources/09-royalty-research-sources-assumptions.md) | [PDF](docs/research-sources/09%20%E2%80%94%20Royalty%20Research%20Sources%20%26%20Assumptions.pdf) |
| **10** | **Royalty Global Expansion, Lifestyle Intelligence & UI/UX** | [MD](docs/global-expansion/10-royalty-global-expansion-lifestyle-ui.md) | [PDF](docs/global-expansion/10%20%E2%80%94%20Royalty%20Global%20Expansion%2C%20Lifestyle%20Intelligence%20%26%20UI_UX.pdf) |
| **11** | **Partner Royalty — Careem Food (Restaurant & Merchant Side)** | [MD](docs/partner-royalty/Partner_Royalty_Careem_Food.md) | [PDF](docs/partner-royalty/Partner_Royalty_Careem_Food.pdf) |
| **12** | **Careem Wallet — Customer Adoption & Royalty Strategy** | [MD](docs/wallet-adoption/Careem_Wallet_Customer_Adoption_Strategy.md) | [PDF](docs/wallet-adoption/Careem_Wallet_Customer_Adoption_Strategy.pdf) |
| **13** | **Careem Wallet — Out-of-the-Box Moonshot Concepts** | [MD](docs/wallet-adoption/Careem_Wallet_Out_Of_The_Box_Ideas.md) | [PDF](docs/wallet-adoption/Careem_Wallet_Out_Of_The_Box_Ideas.pdf) |

- **Interactive UI/UX Prototype (No Backend):** [docs/ui-prototype/index.html](docs/ui-prototype/index.html) — Clickable Careem-branded mobile mockup (Hub, Battle Pass, For You Lifestyle Deals, and Beit Careem Family Vault).
- **Complete Software Engineering Documentation (10 Engineering PDFs + OpenAPI 3.1 + SQL + Diagrams + ADRs):** [docs/README.md](docs/README.md)

---

## Implementation Status (Documented vs. Implemented)

- **Implemented (Prototype Core Only):** `src/royalty/algorithm.py`, `src/royalty/mcp_server.py`, and `tests/test_royalty.py` (`5/5` unit tests passing).
- **Documented for Engineering Implementation (Not Yet Built):** Production modular monolith backend, PostgreSQL schema (`001_initial_schema.sql`), OpenAPI 3.1 endpoints (`openapi.yaml`), OAuth 2.0 PKCE Careem MCP client bridge, and production mobile/web frontend.

---

## Code & Verification (`src/` & `tests/`)

- `src/royalty/algorithm.py` — Config-driven tier split calculator (`DEFAULT_FLEET_TIERS` 60/40→40/60 & `INDEPENDENT_JORDAN_TIERS` 28/72→14/86), fatigue-safe XP engine, soft reset, Legacy floor, and `remaining_reward_budget_jod` cap guard.
- `src/royalty/mcp_server.py` — JSON-RPC 2.0 stdio MCP server exposing `royalty_get_captain_status`, `royalty_calculate_trip_split`, `royalty_get_missions`, and `royalty_issue_family_promo`.
- `tests/test_royalty.py` — Unit tests verifying split caps, budget-cap enforcement, fatigue/wash-trip guards, soft reset, and MCP tools.

```bash
python3 -m unittest discover -s tests -v
```
