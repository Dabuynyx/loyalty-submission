# 10 — Royalty Engineering Roadmap & Implementation Plan

**Note on Estimates:** Complexity is rated (`S / M / L`) rather than inventing calendar dates, as actual velocity depends on team size and Careem internal API approval timelines.

---

## Phased Implementation Plan (Phases 1–11)

| Phase | Objectives | Dependencies | Complexity | Acceptance Criteria |
| :--- | :--- | :--- | :---: | :--- |
| **1. Repo & Arch Prep** | Set up modular monolith skeleton, CI/CD, PostgreSQL + Alembic | None (Current docs ready) | **S** | CI green; `001_initial_schema.sql` applies cleanly |
| **2. Core Captain Account** | `captain_refs`, `loyalty_accounts`, `country_configs`, OAuth JWT guard | Phase 1, Careem Identity JWKS | **M** | Captain status endpoint returns `200` with `401` on bad JWT |
| **3. Eligibility & Algorithm** | Port `algorithm.py` to DB-backed `reward_engine` + `SELECT FOR UPDATE` | Phase 2, Careem Finance `R_cap` sign-off | **M** | All concurrency & budget-cap tests (`TC-01`–`TC-03`, `TC-11`) pass |
| **4. MCP Integration** | OAuth PKCE client for `mcp.careemapis.com/mcp` + circuit breaker | Careem Hackathon/Prod Client | **M** | Sandbox contract tests pass; mutating tools never auto-retry |
| **5. Catalog & Redemption** | `reward_catalog`, `reward_inventory`, `reward_transactions`, partner webhooks | Phase 3 | **M** | Atomic redeem + `REFUND` compensation on partner 503 (`TC-10`) |
| **6. Personalization** | `consent_records`, `captain_preferences`, 9-stage ranking + cold-start | Phase 4, Phase 5 | **M** | Zero lifestyle queries when `consent=false` (`TC-07`) |
| **7. Family Benefits** | `family_beneficiaries`, `promotional_codes`, Careem Promo API bridge | Phase 3, Careem Promo API | **L** | `BEIT-*` code bound to spouse & redeemable via Careem MCP |
| **8. UI Integration** | Connect mobile/web Captain UI (`docs/ui-prototype`) to REST API | Phases 2–7 | **M** | Arabic RTL + WCAG AA verified; all 4 tabs live |
| **9. Regional Config** | Parameterize `JO` (`FLEET` + `INDEPENDENT`), `AE`, `SA`, `EG` configs | Phase 2, Ops Partner Onboarding | **S** | Switching `country_code` loads isolated currency & verticals (`TC-12`) |
| **10. Testing & Pilot** | Full E2E, load test, security audit, 200-Captain Amman pilot | Phases 1–9 | **L** | Zero P0/P1 bugs; budget-cap invariant holds 100% |
| **11. Regional Expansion** | Phased rollout to UAE, KSA, Egypt, Iraq, Morocco via country checklist | Phase 10 Pilot Sign-Off | **M/Market** | Each country passes Country Onboarding Checklist |

**Critical Path:** Careem Finance confirmation of `max_reward_budget_pct` (Phase 3) → Careem Dispatch `TripCompleted` webhook & Promo Minting API approval (Phases 3 & 7) → Amman Pilot (Phase 10).
