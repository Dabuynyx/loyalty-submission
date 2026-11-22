# 06 — Royalty Personalization & Regional Data Architecture

**Core Rule:** The Personalization Engine **cannot** override `reward_budgets` or `max_reward_budget_pct`. Every recommended offer passes through the independent `Reward Eligibility` filter before reaching the Captain.

---

## 1. Nine-Stage Separated Personalization Pipeline

1. **Preference Collection:** Explicit opt-in tags (`PUT /captains/{id}/preferences`, e.g., `burgers`, `coffee`, `groceries`) + authorized Careem MCP `get_activities` signals.
2. **Consent Management:** `consent_records` (`LIFESTYLE_PERSONALIZATION`). If `granted = false`, Stages 1, 3, and 6 are bypassed immediately.
3. **Preference Storage:** Coarse category tags only (`captain_preferences`); deleted immediately upon opt-out.
4. **Reward Eligibility Filter:** Checks Captain's `current_tier`, `country_code`, `city_id`, and `remaining_reward_budget_local`.
5. **Reward Discovery:** Queries `reward_catalog` + `partner_organizations` (prioritizing **partner-funded** zero-cost deals when direct budget is tight).
6. **Recommendation Generation:** Ranks eligible offers by category match + time-of-day shift fit (e.g., 22:00 post-shift burger deal).
7. **Cold-Start Fallback:** If the Captain shared zero preferences, ranks **generic high-utility offers** (fuel rebates, Safe-Shift tea, Weekly Flex quests) so Royalty works 100% out of the box.
8. **Recommendation Explanation:** Every card includes a transparent `explanation_text` (e.g., *"Matched because you opted into Food perks · Funded by Partner"*).
9. **Measurement:** Tracks click-to-redeem conversion without storing sensitive raw behavioral logs.

---

## 2. Multi-Country & Regional Configuration Architecture

- **Global Identity vs. Local Balances:** `captain_refs.careem_captain_ref` is global, while `loyalty_accounts`, `reward_budgets`, and `promotional_codes` are **strictly scoped by `country_code`**. Balances and codes are **never transferable** across borders.
- **Configuration-Driven Expansion (`country_configs` + `city_configs`):**
  - `JO` (`JOD`, `ar/en`, `Asia/Amman`, verticals: `rides, food, quik, box`)
  - `AE` (`AED`, `ar/en`, `Asia/Dubai`, verticals: `rides, food, quik, box, pay`)
  - `SA` (`SAR`, `ar/en`, `Asia/Riyadh`, verticals: `rides, food, pay`)
  - `EG` (`EGP`, `ar/en`, `Africa/Cairo`, verticals: `rides, food`)
  - `IQ` / `MA` (`IQD`/`MAD`, verticals: `rides` only → partner fuel/telecom catalog)

### New Country Onboarding Checklist
1. Confirm Careem Finance `max_reward_budget_pct` & Fleet vs. Independent `loyalty_tiers` curve.
2. Insert `country_configs` + `city_configs` (with `is_active = false` initially).
3. Onboard ≥ 3 local `partner_organizations` (fuel, auto-care, food/grocery).
4. Verify local data-residency & consent wording with Legal.
5. Enable `is_active = true` for pilot cohort via feature flag.
