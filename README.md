# ROYALTY — Careem Builders ’26 (Amman, Jordan)

> **Captain-First Loyalty, Household Benefits & Dual-Layer MCP Ecosystem**  
> **Repository:** `Dabuynyx/loyalty-submission`

---

## Executive Summary

**Royalty** is a next-generation Captain loyalty and engagement platform built for **Careem Builders ’26** in Amman, Jordan. It solves Jordan's acute multi-homing problem (Careem vs. Uber, Jeeny, Petra Ride, Gojo) by combining:

1. **Dynamic 6-Tier Split & Battle Pass (`60/40 → 40/60`):** Captains progress from Tier 1 (**60% Careem / 40% Driver**) to a hard-capped Tier 6 (**40% Careem / 60% Driver**), with a deterministic **Reward Budget Cap Guard** (`src/royalty/algorithm.py`) ensuring overlapping bonuses and family promos never exceed Careem's permitted percentage limit.
2. **"Beit Careem" Family Benefits:** Captains unlock household-bound Careem promo codes for **Careem Rides, Careem Quik groceries, Careem Food, and Careem Plus**—leveraging Careem's super-app moat that single-vertical competitors (Jeeny, Petra Ride) cannot match.
3. **Ethical, Fatigue-Safe Progression:** 10-hour daily XP caps, Safe-Shift break bonuses, part-time friendly Weekly Flex Quests, Tier Shields, and **Captain Legacy** permanent floor tiers.
4. **Dual-Layer Careem MCP Architecture:** Audited all **50 tools across 8 domains** on `https://mcp.careemapis.com/mcp`. Because Careem's official MCP is consumer-only, Royalty pairs **Careem MCP** (for household promo redemption, Quik grocery baskets, and Box deliveries) with a custom **Royalty Captain MCP Extension** (`src/royalty/mcp_server.py`).

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

---

## Code & Verification (`src/` & `tests/`)

- `src/royalty/algorithm.py` — Config-driven tier split calculator (`DEFAULT_FLEET_TIERS` 60/40→40/60 & `INDEPENDENT_JORDAN_TIERS` 28/72→14/86), fatigue-safe XP engine, soft reset, Legacy floor, and `remaining_reward_budget_jod` cap guard.
- `src/royalty/mcp_server.py` — JSON-RPC 2.0 stdio MCP server exposing `royalty_get_captain_status`, `royalty_calculate_trip_split`, `royalty_get_missions`, and `royalty_issue_family_promo`.
- `tests/test_royalty.py` — Unit tests verifying split caps, budget-cap enforcement, fatigue/wash-trip guards, soft reset, and MCP tools.

```bash
python3 -m unittest discover -s tests -v
```
