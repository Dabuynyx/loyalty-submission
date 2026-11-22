# Careem Wallet (Careem Pay) — Customer Adoption & Royalty Strategy

**Scope:** Research & Strategy Documentation (Jordan & MENA — No application code)  
**Core Question:** *Why do Careem customers in Jordan barely use Careem Wallet today, and how can Royalty transform it into their #1 preferred payment method?*

---

## 1. How Careem Wallet Currently Works (Verified)

In Jordan, **Careem Pay / Careem Wallet** stores digital credit inside the Careem app to pay for Rides, Careem Food, Careem Quik, and Careem Box:
- **Priority Auto-Spend:** When enabled, Careem deducts from the Wallet balance first and charges the remainder to a saved card or cash.
- **Top-Up Methods:**
  1. **Debit / Credit Card:** Via `Pay → Balance → Top-up wallet` (note: Careem warns that some banks charge cash-advance/processing fees on credit card top-ups).
  2. **Cash Ride Change:** When paying a Captain in cash, the rider can ask the Captain to deposit the change into their Careem Wallet.
  3. **Instant Refunds:** Cancelled orders or fare adjustments refund to Careem Wallet almost immediately (vs. 3–14 business days to a bank card).
- **Local Infrastructure Context:** Jordan’s national instant payment rails (**CliQ** for banks and **JoMoPay** for wallets like Zain Cash, Orange Money, UWallet, Dinarak) are overseen by the **Central Bank of Jordan (CBJ)** and **JoPACC**. Careem Wallet in Jordan operates primarily as a **closed-loop service wallet** rather than a standalone bank-transferring JoMoPay wallet.

---

## 2. Why Customers Barely Use Careem Wallet (5 Root Causes)

| # | Barrier | What Actually Happens in Jordan |
| :---: | :--- | :--- |
| **1** | **The "Trapped Money" Problem** | Because Careem Wallet is closed-loop, pre-loading JOD 20 feels risky—users cannot easily send unused funds back to CliQ/bank if they need cash. |
| **2** | **Zero Advantage Over Cash or Card** | Paying with Wallet costs the exact same JOD 5.00 as paying Cash or Visa—there is no immediate reward for locking money inside Careem. |
| **3** | **Driver Pushback on Digital Rides** | Captains need daily cash for fuel and expenses. Some ask digital-paying riders to cancel and pay cash, training customers to just pick Cash. |
| **4** | **Top-Up Friction (Card Entry & Fees)** | Typing 16-digit card numbers (or risking bank credit-card fees) is far harder than handing over a JOD 5 note—especially for unbanked/debit-hesitant users. |
| **5** | **Group & Family Cash Culture** | Friends/coworkers ordering Careem Food or sharing rides pool cash easily at the door; paying from one person's wallet creates bill-splitting friction. |

---

## 3. How Royalty Completely Changes Careem Wallet (6 Breakthrough Mechanics)

To beat cash in Jordan, Careem Wallet must be **cheaper, faster, and socially effortless**—and **Royalty** solves *both* the customer side and the driver pushback simultaneously:

### 3.1 Turn Cash Into Wallet: "Change Booster" (+10% Bonus)
- **Current:** Riders awkwardly wait for coins or let the Captain deposit exact change into Careem Wallet.
- **Royalty Upgrade:** Every time a cash rider puts their **ride change into Careem Wallet**, Royalty adds a **+10% Change Bonus** (e.g., JOD 1.50 change becomes **JOD 1.65** in Wallet) + **+25% Rider Progress**. This turns Jordan's cash habit into Careem’s #1 free wallet acquisition channel!

### 3.2 Fix Driver Resistance via Captain Royalty (`85%–90%` Instant Cashout)
- **Why drivers hated digital/wallet rides:** Delayed corporate payouts.
- **Royalty Fix:** Because Captains in our `85%–90%` range unlock **Instant Careem Cashout** (and earn faster progress on cashless rides), Captains **actively prefer** Careem Wallet riders—eliminating driver cancellation pressure.

### 3.3 "Wallet-First" Instant Value (Make Wallet Visibly Cheaper Than Cash)
- **Cashless Discount / Credit-Back:** Wallet payments automatically unlock **3%–5% instant credit-back** (stacked cleanly with **Careem Plus's 10% ride cashback** in Jordan) + **2× Rider Royalty Progress**.
- **Exact-Change Elimination:** Zero doorstep coin arguments on Careem Food and Rides.

### 3.4 1-Tap CliQ & JoMoPay Top-Up (Zero Card Friction)
- Integrate **CliQ** and **JoMoPay** (Zain Cash / Orange Money / UWallet) as 1-tap instant top-up sources—allowing unbanked users to load exact trip/order amounts in 3 seconds with **zero credit-card fees**.

### 3.5 "Beit Careem" Shared Family Wallet & Allowances
- Parents or **Tier 3+ Royalty Captains** can allocate a **closed-loop Family Allowance** (e.g., JOD 15/mo for school rides or Careem Quik groceries) to spouse/children accounts—creating recurring household wallet usage without bank cards.

### 3.6 1-Tap Group Bill Split ("Qatta" Mode)
- Solve Jordan's office/family food-ordering barrier: when ordering Careem Food, the payer taps **"Split via Careem Wallet / CliQ Link"**, and friends reimburse their share directly into the payer's Careem Wallet in 1 tap.

---

## 4. Careem MCP Readiness (`use_wallet` Already Supported!)

Careem’s official Consumer MCP (`https://mcp.careemapis.com/mcp`) **already exposes wallet parameters** across its checkout and ride tools:
- `cart_get_basket_price(..., use_wallet=True)` — Previews exact savings and net total when paying with Wallet.
- `cart_get_checkout_promos(..., use_wallet=True)` — Surfaces Wallet-exclusive promos (`is_best_saving`).
- `cart_checkout(..., use_wallet_balance=True)` & `cart_grocery_checkout(..., use_wallet_balance=True)` — Executes Food/Quik/Shops checkout using Careem Wallet (always after explicit user confirmation).
- `create_ride(..., payment_type="wallet")` & `box_create_order(..., payment_type="wallet")` — Pays for Rides and Careem Box parcels via Careem Wallet.

**Agent UX Opportunity:** When a user checks out via Careem MCP, the AI assistant automatically checks `cart_get_basket_price(use_wallet=True)` vs. `cash` and shows: *"Pay with Careem Wallet to save JOD 0.65 and earn 2× Royalty Progress!"*

---

## 5. Economics: Why Careem Wins When Customers Use Wallet

1. **Higher Order Frequency (Pre-Loaded Commitment):** Users with even JOD 3–5 sitting in Careem Wallet open Careem first instead of Talabat, Jeeny, or Petra Ride.
2. **Lower Cash-Settlement & Fraud Losses:** Fewer cash trips mean less uncollected commission debt from Captains and zero fake-cash cancellations.
3. **Working Capital Float & Lower Card Fees:** Wallet-funded internal ledger transfers avoid repeated 1.5%–2.5% Visa/Mastercard acquiring fees on every small JOD 2.50 ride.
