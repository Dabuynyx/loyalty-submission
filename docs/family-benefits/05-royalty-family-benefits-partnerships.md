# 05 — Royalty Family Benefits & Partnerships ("Beit Careem")

**Why Family Benefits?** Competitors in Jordan (Jeeny, Petra Ride) only reward the *driver's phone*. Careem is a **Super App** (Rides + Food + Quik Groceries + Box + DineOut). Extending Royalty to the Captain's **household** creates an emotional and financial moat no single-vertical ride app can match.

---

## 1. Realistic, High-Value Family Benefits for Jordan

| Benefit Category | Funding Model | Tier Unlock | How It Works in Jordan |
| :--- | :--- | :---: | :--- |
| **1. Family Ride & School-Run Codes** | Careem-Funded (within Budget Cap) | **T3+** | Monthly JOD 3–5 promo codes usable by spouse/children for safe, tracked Careem rides. |
| **2. Careem Quik Household Grocery Credits** | Hybrid (Careem + FMCG Brand Sponsors) | **T5+** | JOD 5–8 monthly grocery credit for essentials (milk, bread, olive oil, diapers) via Careem Quik. |
| **3. Careem Plus Family Gift** | Careem Subscription Marginal Cost | **T6** | 1 free **Careem Plus** membership (worth JOD 2.99/mo in Jordan) gifted to a designated family member. |
| **4. Fuel & Auto-Care Network** | **100% Partner-Funded** | **T2+** | Negotiated discounts at Jordanian fuel stations (e.g., Manaseer / JoPetrol / TotalEnergies) & local tire/oil shops in exchange for Captain foot traffic. |
| **5. Healthcare & Pharmacy Discounts** | **100% Partner-Funded** | **T4+** | 15%–25% family discount at partner clinics/pharmacies in Amman, Irbid, and Zarqa. |
| **6. Education & Tech Upskilling** | Partner-Funded / CSR | **T6 / Legacy** | Discounted English, coding, or vocational courses for Captains' children (inspired by Uber's ASU model, localized for Jordan). |

---

## 2. MCP Verification & Required Integrations

We checked Careem's official MCP Server (`https://mcp.careemapis.com/mcp`) for family-benefit support:
- **What Careem MCP DOES Support Today:**
  - `apply_promotion_code` ⚠️ (Rides domain — applies a valid promo code string to a signed-in user's Careem account).
  - `cart_get_checkout_promos` & `cart_get_basket_price` (auto-evaluates best available promo on Food/Quik/Shops baskets).
  - `create_grocery_cart_with_quantities` ⚠️ & `cart_grocery_checkout` ⚠️ (allows a family member's AI assistant to build and check out a Quik grocery basket).
- **What Careem MCP Does NOT Support (Requires Royalty Backend + Careem Promo API):**
  - **Family Account Linking:** Careem MCP has no `link_family_member` tool. Royalty maintains a `FamilyBeneficiary` table (max **3 verified household members** per Captain, verified via OTP).
  - **Dynamic Promo Code Minting:** Careem MCP cannot *create* new promo codes. Royalty's `royalty_issue_family_promo` generates a single-use, user-bound code and (in production) registers it with Careem's internal Promo Service.

---

## 3. End-to-End Example: Earning, Assigning & Redeeming a Family Benefit

1. **Earn:** Captain Ahmad hits **Tier 5 (Elite)** in Amman. `Royalty` unlocks a **JOD 5.00 Family Careem Quik Code**.
2. **Assign:** In the Captain App (or via Royalty MCP), Ahmad selects his registered beneficiary **Fatima (Spouse)** and taps *"Send Family Benefit"*.
3. **Budget Check & Mint:** `royalty_verify_budget_cap` confirms the JOD 5.00 cost fits inside Ahmad's remaining Season Reward Budget. Royalty mints single-use code `BEIT-AHM-502` bound strictly to Fatima's Careem account ID.
4. **Redeem (via Careem MCP):** Fatima opens her Careem app (or AI assistant connected to Careem MCP), builds her weekly grocery basket with `create_grocery_cart_with_quantities` ⚠️, sees `BEIT-AHM-502` applied in `cart_get_basket_price`, confirms the final JOD total, and checks out via `cart_grocery_checkout` ⚠️.

---

## 4. Anti-Misuse & Fraud Prevention

- **Account-Bound Codes:** Promo codes are locked to the designated family member's `user_id` / phone number—preventing resale on WhatsApp/Facebook groups.
- **Household Cap:** Maximum **3 family beneficiaries** per Captain, changeable only once per 90 days.
- **No Self-Dealing:** A Captain cannot redeem their own Family Ride Code on a trip they themselves accept as the driver.
