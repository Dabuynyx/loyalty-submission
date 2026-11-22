# 04 — Royalty Incentive Economics & Reward Algorithm

**Constraint Foundation:** Every reward, split uplift, cash bonus, and Careem-funded family promo code must obey a strict mathematical **Reward Budget Cap** so overlapping incentives never erode unit economics.

---

## 1. Existing Algorithm Audit & Percentage Constraints

### 1.1 Split Curve Constraint (Verified from Project Specification)
- **Entry Split (Tier 1):** `60% Careem / 40% Driver`
- **Maximum Driver Split (Tier 6):** `40% Careem / 60% Driver` (hard cap: `driver_pct <= 0.60`)
- **Uplift Range:** `+0%` (T1) to `+20%` (T6) of **Gross Trip Fare** above the T1 baseline.

### 1.2 Jordan Market Calibration Note (Unverified Production Parameter)
In Jordan's independent car-owner market, standard commissions are ~20%–25% (drivers keep 75%–80%). The **60/40 → 40/60** split applies directly to a **Careem-Managed / Financed Fleet** (where Careem or a fleet partner funds the vehicle, insurance, and LTRC licensing). Because the Royalty algorithm is **config-driven**, the exact same math supports an **Independent Driver Curve** (e.g., `28% → 14%` Careem cut) without changing a single line of core logic.

---

## 2. Mathematical Framework & Budget Cap Guard

To guarantee that **split uplifts + mission bonuses + overflow credits + Careem-funded family promos** never exceed Careem's permitted reward budget:

### 2.1 Core Formulas
Let:
- $G$ = Captain's Gross Fares in a Season (JOD)
- $b_{\text{base}} = 0.40$ = Baseline Tier-1 Driver Share
- $b_t \in [0.40, 0.60]$ = Tier-$t$ Driver Share
- $U = \sum_{\text{trips}} (b_t - b_{\text{base}}) \cdot \text{fare}_i$ = Total Split Uplift Paid (JOD)
- $M$ = Direct Cash / Mission Bonuses Paid (JOD)
- $F_{\text{cost}}$ = **Careem's Net Direct Cost** of Family Promo Redemptions (excluding partner-funded discounts!)
- $R_{\text{cap}} \in (0, 1]$ = Maximum Permitted Total Reward Budget % of Gross Fares (e.g., **22.0% of $G$** in the Fleet model, meaning total effective driver+family payout never exceeds $40\% + 22\% = 62\%$ of $G$, leaving Careem $\ge 38\%$ gross margin before partner subsidies).

**Hard Invariant (Enforced by `verify_budget_cap` in `src/royalty/algorithm.py`):**

$$\text{Total Direct Reward Liability} = U + M + F_{\text{cost}} \le R_{\text{cap}} \cdot G$$

If a Captain's split uplift $U$ already consumes 20% of $G$ (at Tier 6), the remaining direct budget for cash bonuses and Careem-funded family promos is automatically capped at $(R_{\text{cap}} - 0.20) \cdot G = 2.0\% \cdot G$—and any additional rewards shift to **Partner-Funded Benefits** (zero direct cost to Careem!).

---

## 3. Financial Scenarios (Illustrative Jordan Fleet Model, Per Active Captain / Month)

> **Disclaimer:** All figures below are **illustrative planning assumptions** for a 30-day season in Amman (average fare JOD 4.50). They are not actual Careem financial statements.

| Metric | Conservative (High Churn) | Moderate (Target Base Case) | Optimistic (Full Flywheel) |
| :--- | :---: | :---: | :---: |
| Monthly Trips / Captain | 180 | 260 | 340 |
| Gross Fares $G$ (JOD) | JOD 810 | JOD 1,170 | JOD 1,530 |
| Avg. Blended Driver Tier | T2.5 (46% Driver) | T4.0 (52% Driver) | T5.2 (56.8% Driver) |
| Careem Gross Commission | 54.0% (JOD 437) | 48.0% (JOD 562) | 43.2% (JOD 661) |
| Direct Bonus + Careem-Funded Family Cost | JOD 12 (1.5%) | JOD 18 (1.5%) | JOD 24 (1.6%) |
| **Partner-Funded Reward Value** *(Zero Careem Cost)* | JOD 10 | JOD 22 | JOD 35 |
| **Captain Pro Pass Subscription** *(25% adoption @ JOD 9.99)* | +JOD 1.50 avg | +JOD 2.50 avg | +JOD 3.50 avg |
| **Net Careem Margin / Captain / Month** | **JOD 426.50** | **JOD 546.50** | **JOD 640.50** |
| Estimated Monthly Retention Rate | 78% | 88% | 94% |
| Avoided Replacement CAC (~JOD 90/churned driver) | Baseline | +JOD 9.00 saved | +JOD 14.40 saved |

### Key Economic Insight
Even though Careem's percentage drops from **54% → 43.2%** between Conservative and Optimistic, **Net Careem Margin per Captain rises +50% (JOD 426.50 → JOD 640.50)** because retained Captains complete nearly double the monthly trips and partner-funded perks absorb most of the extra reward value!

---

## 4. Abuse & Leakage Controls

1. **Redemption & Expiration:** Unclaimed Family Promo Codes expire at Season End + 15 days, keeping unredeemed liability bounded (assumed 75%–85% redemption rate).
2. **Minimum Trip Guard:** Trips under JOD 1.50 or < 1.0 km earn **0 XP** and **0 Split Uplift** to block self-booking wash trips.
3. **Cash-Settlement Lock:** Captains with overdue cash-commission balances have split uplifts held in escrow until settled.
