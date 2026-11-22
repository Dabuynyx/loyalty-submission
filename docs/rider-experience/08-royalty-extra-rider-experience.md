# 08 — Royalty Extra: Rider Experience & Careem Plus Extension

> **Supplementary Document:** The primary Royalty product is **Captain-first**. This document explores how Royalty can extend to **Riders (Customers)**—especially **Careem Plus** subscribers (JOD 2.99/month in Jordan)—**without** ever reducing Captain earnings or breaching the Captain reward budget.

---

## 1. Core Principle: Strict Financial Ring-Fencing

- **Zero Hidden Captain Deductions:** Rider discounts, cashback, and Surge Shields are funded **exclusively** from Careem's marketing/subscription budget (`Careem Plus` MRR and Careem's platform share)—**never** deducted from the Captain's trip fare or split percentage.
- **Calculated on Gross Fare:** Even when a Rider uses a 10% Careem Plus cashback or a JOD 2.00 Rider Royalty voucher, the Captain's 40%–60% split is computed on the **full gross fare** before rider promos.

---

## 2. Rider Battle Pass & Careem Plus Enhanced Track

### 2.1 How Riders Earn XP (Cross-Ecosystem)
- **Complete a Ride:** `100 XP + 15 XP/JOD` (`+25%` bonus for Careem Pay/Card).
- **Off-Peak Commute (10:00–15:00):** `+50 XP` (shifts rider demand to quiet hours, helping Captains stay busy).
- **Careem Food / Quik Order:** `+75 XP` (already supported via Careem MCP `get_activities`).

### 2.2 Standard Rider vs. Careem Plus (JOD 2.99/mo in Jordan)

| Rider Tier | Season XP | Free Rider Track | **Careem Plus Track (2x XP Multiplier)** |
| :---: | :---: | :--- | :--- |
| **R1 Explorer** | 0 XP | Access to Rider Quests | **2x XP**, Priority Support, 10% cashback (10 rides/mo) |
| **R2 Commuter** | 500 XP | JOD 1.00 Ride Voucher | **+ 1× Surge Shield Token** |
| **R3 Regular** | 1,200 XP | 5% off 2 rides | **+ Cashback upgraded to 12% on 14 rides/mo** |
| **R4 VIP** | 2,500 XP | 1× Cancel Fee Waiver | **+ Priority Matching with T4–T6 Top Captains** |
| **R5 Ambassador** | 4,500 XP | JOD 3.00 Ride Credit | **+ 15% cashback (20 rides/mo) + JOD 5 DineOut Credit** |

---

## 3. How Rider Loyalty Helps Captains (Two-Sided Flywheel)

1. **Priority Matching Benefits Both Sides:** Matching `R4–R5 Careem Plus` riders first with `T4–T6 Legend` Captains pairs Careem's highest-frequency, digital-paying customers with its most reliable, highest-rated drivers.
2. **Off-Peak XP Quests:** Encouraging Riders to book between 10:00 and 15:00 increases Captain utilization during Amman's midday lull.
3. **Careem MCP Readiness:** Every Rider-side food, grocery, and ride-pricing flow (`food_*`, `search_groceries_*`, `cart_get_checkout_promos`, `apply_promotion_code`, `request_ride`) is **already designed for Careem's Consumer MCP**, making Phase 2 Rider rollout straightforward.
