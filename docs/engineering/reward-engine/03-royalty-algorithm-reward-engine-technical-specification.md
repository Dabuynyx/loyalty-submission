# 03 — Royalty Algorithm & Reward Engine Technical Specification

**Verified Code Reference:** [`src/royalty/algorithm.py`](../../../src/royalty/algorithm.py)  
**Test Reference:** [`tests/test_royalty.py`](../../../tests/test_royalty.py)

---

## 1. Exact Specification of Implemented Algorithm

### 1.1 Tier Curves (Config-Driven)
- **Fleet Curve (`DEFAULT_FLEET_TIERS`):**
  - T1 Rookie: `60% Careem / 40% Driver` (`0 XP`)
  - T2 Challenger: `56% / 44%` (`1,000 XP`, Rating ≥ `4.50`, Cancel ≤ `10%`)
  - T3 Contender: `52% / 48%` (`2,500 XP`, Rating ≥ `4.60`, Cancel ≤ `8%`)
  - T4 Pro: `48% / 52%` (`5,000 XP`, Rating ≥ `4.70`, Cancel ≤ `6%`)
  - T5 Elite: `44% / 56%` (`8,500 XP`, Rating ≥ `4.80`, Cancel ≤ `5%`)
  - T6 Legend: `40% / 60%` (`13,000 XP`, Rating ≥ `4.85`, Cancel ≤ `4%`)
- **Independent Curve (`INDEPENDENT_JORDAN_TIERS`):** `28/72 → 25/75 → 22/78 → 19/81 → 16/84 → 14/86` with identical XP & quality gates.
- **Unverified Production Guard:** Exact `max_reward_budget_pct` (currently `0.22` default in prototype) and financial base (Gross Fare vs. Net Commission) **must be confirmed by Careem Finance** before enabling production payouts.

### 1.2 XP & Anti-Abuse Formulas (`calculate_trip_xp`)
1. **Wash-Trip Guard:** If `fare_jod < 1.50` OR `distance_km < 1.0` → return `0 XP`.
2. **Fatigue-Safe Cap:** If `active_hours_today >= 10.0` → return `0 XP` (fare is still paid normally).
3. **XP Formula:** `round((50 + 10 * fare_jod) * (1.5 if is_peak else 1.0) * (1.25 if is_cashless else 1.0))`.

### 1.3 Tier Resolution & Legacy Floor (`resolve_tier`)
- If `cash_settlement_overdue == True` → forced to **T1**.
- `legacy_floor_tier(lifetime_trips)`: `≥7500 → T4`, `≥3000 → T3`, `≥1000 → T2`, else `T1`.
- Otherwise, highest tier where `season_xp >= min_xp`, `rating >= min_rating`, and `cancel_rate <= max_cancel_rate`.

---

## 2. Budget Cap Invariant & Transaction Safety

**Hard Invariant (`remaining_reward_budget_jod`):**

$$\text{Remaining} = \max\Big(0,\ (\text{gross\_fares} \times R_{\text{cap}}) - (\text{uplift\_paid} + \text{direct\_bonuses} + \text{family\_promo\_cost})\Big)$$

- **Concurrency Control:** Every `RESERVE` / `ISSUE` / `REDEEM` executes inside a PostgreSQL transaction acquiring `SELECT ... FOR UPDATE` on `reward_budgets`.
- **Duplicate Events:** `progression_history.idempotency_key` and `reward_transactions.idempotency_key` have `UNIQUE` constraints; duplicate webhooks return `202` / `200` without mutating balances.
- **Refunds & Cancellations:** If a partner redemption fails after budget reservation, a compensating `REFUND` transaction credits back `direct_cost_local` to `reward_budgets`.
- **Partner-Funded Rewards:** Have `direct_cost_local = 0`, so they **never** consume `reward_budgets` and remain available even when a Captain hits T6's 60% cap.
