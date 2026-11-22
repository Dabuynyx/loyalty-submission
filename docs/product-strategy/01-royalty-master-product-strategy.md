# 01 — Royalty Master Product Strategy

**Project:** Royalty — Next-Generation Captain Loyalty & Engagement System  
**Event:** Careem Builders ’26 · Amman, Jordan  
**Primary Focus:** Careem Captains (Drivers) · *Supplementary Rider Strategy in Deliverable 08*  
**Classification:** Verified Facts, Research-Backed Conclusions & Original Product Proposals

---

## 1. Executive Summary & Vision

Jordan’s ride-hailing market is one of the most competitive in MENA. Under the **Land Transport Regulatory Commission (LTRC)**, licensed platforms—**Careem, Uber, Jeeny, Petra Ride, and Gojo**—compete for the exact same pool of drivers ("Captains"). Because multi-homing across apps has near-zero switching cost, Captains routinely chase short-term 0% commission promos on Jeeny or local apps, causing peak-hour supply shortages and high Driver Acquisition Cost (CAC) for Careem.

**Royalty** transforms Careem from a transactional dispatch app into a **long-term Captain career & household support ecosystem**:
1. **Builds on the Existing Royalty Percentage-Split Algorithm:** Captains start at **60% Careem / 40% Driver (Tier 1)** and progress through seasonal tiers up to a hard cap of **40% Careem / 60% Driver (Tier 6)**—with a **strict mathematical Reward Budget Guard** ensuring overlapping bonuses, family codes, and perks never breach the platform's percentage limit.
2. **Solves the "Cap Problem" Without Margin Collapse:** Once a Captain hits the 60% driver split cap, Royalty shifts motivation from raw commission cuts to **high-perceived-value, low-direct-cost** levers: **Family Benefits** (transferable Careem promo codes for household rides/groceries/food), **Partner-Funded Fuel & Maintenance**, **Tier Shields**, and **Captain Legacy** status.
3. **Bridges Careem's Official MCP Server with a Custom Captain MCP Extension:** After auditing all **50 tools across 8 domains** on `https://mcp.careemapis.com/mcp`, we verified that Careem MCP is currently **consumer-facing** (Food, Groceries/Quik, Shops, Cart, Box, User, Location, and Coming-Soon Rides). Royalty leverages Careem MCP for **Captain household & family redemption** (`apply_promotion_code`, `create_grocery_cart_with_quantities`, `cart_get_basket_price`, `box_create_order`) while adding a lightweight **Captain Royalty MCP Extension** for Captain-side progression, split calculation, and family promo issuance.

---

## 2. Captain-First Problem Discovery (Jordan Market)

| Verified Fact / Industry Pain Point | Source & Evidence Level | How Royalty Solves It |
| :--- | :--- | :--- |
| **High Fuel & Maintenance Burden:** Fuel prices, 7-year vehicle age limits (LTRC), commercial insurance, and frequent servicing squeeze net Captain take-home pay. | Verified (LTRC regulations & Jordan market reporting) | Tier-unlocked **partner-funded** fuel rebates (Manaseer / JoPetrol / TotalEnergies) and garage/oil-change discounts. |
| **Multi-Homing & Zero Switching Cost:** Jeeny offers 0% introductory commission windows and rapid daily payouts; Petra Ride markets local fixed-cost fairness. | Verified (Jeeny & Petra Ride public driver portals) | **Captain Legacy & Soft-Reset Tiers** create earned switching costs—leaving Careem forfeits a 56%–60% split and family perks. |
| **Cash-Dominated Settlement Friction:** High cash trip share in Jordan forces Captains to settle platform commissions manually or via offices. | Verified (POMEPS / MIT Jordan ride-hailing studies) | **+25% XP Bonus** for Careem Pay / digital trips + instant wallet cashout unlocked at Tier 4. |
| **Gamification Burnout & Safety Risk:** Aggressive "midnight deadline" quests in gig apps encourage fatigued driving and rushing. | Research-backed (CMU / behavioral economics literature) | **Fatigue-Safe Daily XP Caps** (max 10h/day XP-eligible), **Part-Time Friendly Weekly Quests**, and **Zero-Punishment Tier Shields**. |
| **Household & Family Pressure:** Most Captains drive to support a household; standard driver apps ignore the Captain's family. | Research-backed hypothesis (requires Jordan Captain pilot validation) | **Family Careem Wallet & Promo Codes**—Captains gift earned ride, Quik grocery, and Careem Food codes to spouse/children. |

---

## 3. Five Original Differentiated Feature Concepts (Top 3 Selected)

We evaluated five original concepts tailored to Jordan and Careem's super-app capabilities:

1. **★ SELECTED #1 — "Beit Careem" (Family Loyalty Pass & Promo Sharing):** Captains earn monthly **Family Careem Codes** (usable on Careem Rides, Careem Food, and Careem Quik groceries via `apply_promotion_code` and `cart_get_checkout_promos`). Careem is the *only* player in Jordan with Rides + Food + Quik + Box in one super-app—making family codes impossible for Jeeny or Petra Ride to replicate.
2. **★ SELECTED #2 — "Captain Legacy" & Soft-Reset Battle Pass:** A 30-day seasonal progression (inspired by Fortnite Battle Pass, adapted for professional dignity). Unlike Uber Pro's 3-month cliff, Captains never drop to zero—end-of-season **Soft Reset (-2 tiers)** + **Lifetime Legacy Badges** (1,000 / 5,000 / 10,000 trips) preserve permanent floor perks.
3. **★ SELECTED #3 — "Co-Pilot AI" (MCP-Powered Personalized Captain & Household Assistant):** Uses Careem MCP + Royalty MCP to recommend optimal shifts without fatigue, explain exact earnings breakdowns transparently, and auto-build the Captain's household Careem Quik grocery basket using earned family credits (`create_grocery_cart_with_quantities`).
4. **Concept #4 — "Captain Circles" (Neighborhood Micro-Squads):** Small groups of 5–8 Amman Captains earn a collective +5% XP boost for covering underserved neighborhoods (e.g., Zarqa, Russeifa, East Amman) during morning commutes. *(Deferred to Phase 2 due to collusion/gaming risk).*
5. **Concept #5 — "Vehicle Upgrade Escrow":** Micro-savings matched 5% by Careem toward a newer LTRC-compliant hybrid/EV. *(Deferred to Phase 3 due to fintech/banking licensing).*

---

## 4. Strategic Guardrails

- **Hard Percentage Cap Compliance:** Total direct financial rewards (split uplift + cash bonuses + Careem-funded promo cost) are mathematically bounded by the `max_reward_budget_pct` constraint.
- **Transparency & Dignity:** Every trip summary shows *Gross Fare → Tier Split Applied → Careem Share → Captain Share → XP Earned → Next Milestone*. No hidden deductions.
- **Safety Over Hustle:** No XP is awarded beyond 10 active driving hours/day, and rest breaks are rewarded with a **"Safe Shift" +50 XP bonus**.
