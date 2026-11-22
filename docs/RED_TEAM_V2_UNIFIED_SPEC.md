# ROYALTY v2.0 — Unified, Red-Teamed Specification (Canonical Source of Truth)

> **Supersedes v1 (60/40 → 40/60 6-Tier Model):** All earlier v1 documents (`01`, `03`, `04`, and `src/royalty/algorithm.py` v1 prototype) are preserved as historical archive. **This document is the canonical v2.0 specification** aligned with the redesigned 3-range UI (`75% → 90%`), Jordan unit economics, CBJ/LTRC regulations, and verified Careem MCP capabilities.

---

## 1. Canonical Captain Royalty Model (Weekly Marginal Brackets)

### 1.1 Why Weekly Marginal Brackets Fix the v1 & Permanent-Split Leaks
- **The Problem with Permanent 90%:** A permanent 10% Careem take-rate across all future trips drops Careem's revenue per full-time Captain by ~60% (failing to cover card fees, insurance, support, and GST) and enables wash-trip farming.
- **The v2.0 Solution — Weekly Marginal Brackets (Resets Every Monday 04:00 AM):**
  - **Rides 1–30 / week:** **75% Captain** (25% Careem)
  - **Rides 31–55 / week:** **80% Captain** (20% Careem)
  - **Rides 56+ / week:** **85% Captain** (15% Careem)
  - **Peak / Hard-to-Serve Bonus Trips:** **90% Captain** (10% Careem — marginal peak-hour/zone trips only)
- **Blended Economics:** Averages **~21.5% Careem blended take-rate** across the week while ensuring the *next* ride pays **85%–90%**—the exact decision point where a multi-homing Captain would otherwise switch to Jeeny or Petra Ride.
- **Same-Day Digital Cashout for ALL Captains:** Same-day cashout of Card and Careem Wallet earnings is unlocked from **Ride 1** for every Captain (eliminating the #1 reason drivers ask riders to cancel and pay cash).
- **Inline Rewards (No Dummy Family Page):**
  - `75%–80%`: Partner Car Wash & Oil-Change Discount
  - `80%–85%`: 1 Family Ride + Food Promo Code (up to 3 JOD, single-use & account-bound)
  - `85%–90%`: Peak-Hour Priority & VIP Support

---

## 2. Canonical Food Partner Royalty (Incremental GMV Model)

- **Incremental GMV Commission Relief:** Lower commission (`25% → 15%`) applies **only on monthly GMV above each restaurant’s own trailing 8-week baseline**—preventing Careem from subsidizing baseline orders that high-volume chains would get anyway.
- **Anti-Spoofing Prep-Time Gate:** Kitchen prep time (`≤ 15 min`) is measured via **courier GPS arrival-to-pickup gap**, not the restaurant’s manual "Order Ready" tap.

---

## 3. Jordan Regulatory & Anti-Fraud Guardrails (CBJ / LTRC / PDPL)

Aligned with **Jordan Electronic Payment and Money Transfer Bylaw No. 111 of 2017**, **Personal Data Protection Law No. 24 of 2023**, and **LTRC Smart-App Rules**:
- **Deprecated Unlicensed Fintech Concepts:** *Reverse ATM (Captain cash-in)*, *Careem Flex (JOD 5 overdraft)*, *Qatta P2P Wallet Transfers*, and *Merchant-Locked Prepaid Vaults* are **removed from v2.0** to avoid unlicensed e-money/credit triggers.
- **Compliant Alternatives Retained:**
  1. **Beit Careem:** Single-use, account-bound promotional codes (not P2P cash transfers).
  2. **Ramadan & Eid Commitment Pots + Digital Eidiya:** User-labeled savings goals inside their own Wallet unlocking merchant-funded basket discounts (no interest, no P2P), plus closed-loop gift vouchers.
  3. **Transparent Behavior-Based Cashback (No Random Lottery):** Replaces chance-based Cashback Reveal (which raises *maysir*/prize-permit issues) with clear, deterministic rewards tied to vertical, time of day, and Wallet usage, with a **per-rider monthly cap**.
- **Day-1 Collusion Controls:** Graph-based ring detection, `JOD 1/day` cap on ride-change Wallet deposits, and **in-app Captain Meal redemption with selfie/liveness check**.

---

## 4. Super-App Differentiation ("Ride-to-Table" & "In-Sync Arrival")

1. **Ride-to-Table (Flagship Cross-Vertical Loop):** DineOut / Careem Food partners sponsor the customer’s Careem ride to their restaurant (*"Dinner at X — your ride is on us"*), funded from Partner Royalty incremental savings. Impossible for Talabat (no rides) or Jeeny/Petra Ride (no merchants).
2. **In-Sync Arrival:** Book a ride home and schedule your Careem Food / Quik basket (`food_get_scheduling_slots` + `cart_reschedule_basket`) to arrive within 5 minutes of your drop-off, paid in one confirmation.
3. **Back-Haul Delivery ("Patience Pricing"):** Non-urgent Box/Quik orders ride along with a Captain already heading that direction *(subject to LTRC passenger-vehicle goods-carriage verification)*.

---

## 5. Verified Careem MCP Demo Flow ("Thursday Restock" — Wallet-Aware Quik)

*(Uses only verified `builders.careem.com` parameters; treats all merchant text as untrusted data to prevent prompt injection).*
1. `user_info` → `is_grocery_area_serviceable` → `search_groceries_get_top_user_items` + `search_groceries_get_all_deals` (only after checking `consent`).
2. **⚠️ Gate 1 (Confirm Basket):** `create_grocery_cart_with_quantities`.
3. `cart_get_basket_price(business_type="quik", use_wallet=True)` vs. cash + `cart_get_checkout_promos` → *"Careem Wallet saves you JOD 0.65."*
4. **⚠️ Gate 2 (Confirm Total & Address):** `cart_grocery_checkout` (never auto-retry on timeout; verify via `get_activities(activity_status="ongoing")`).
