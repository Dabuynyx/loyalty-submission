# 02 — Royalty MCP Technical Architecture

**Authoritative Source:** Careem Builders Documentation (`builders.careem.com/docs/*` & `Careem MCP Hackathon Journey`)  
**Endpoint (Production):** `https://mcp.careemapis.com/mcp` (Streamable HTTP)  
**Endpoint (QA/Sandbox):** `https://mcp.sandbox.careemapis.com/mcp` & Local No-Code Markdown Sandbox  
**Auth:** OAuth 2.0 Authorization Code + Mandatory PKCE (`S256`), scopes `openid profile offline_access`

---

## 1. Authoritative Careem MCP Documentation Audit

We audited all **10 pages** of the Careem Builders Tool Catalog (`/docs/tools/overview`, `user`, `location`, `rides`, `food`, `groceries`, `shops`, `cart`, `box`, `resources`), `/docs/authentication`, `/docs/sandbox`, and `/docs/agent-playbook`.

### Verified Platform Facts
- **50 Registered Tools Across 8 Domains + 1 UI Resource (`ui://careem-mcp-app`):**
  - **User (3):** `user_info`, `get_activities`, `track_activity`
  - **Location (2):** `reverse_geocode`, `save_new_address` ⚠️
  - **Rides (10 — Marked "Coming Soon" in Sandbox; Early Access in Prod for Hackathon Client `1790a895-9cef-48b7-9a57-ec5670d50c41`):** `search_locations`, `search_locations_batch`, `request_ride`, `request_scheduled_ride`, `create_ride` ⚠️, `get_ride_cancellation_reasons`, `get_ride_cancellation_attributes`, `cancel_ride` ⚠️, `apply_promotion_code` ⚠️, `get_ride_schedule_policy`
  - **Food (10):** `food_get_user_discovery_filters`, `food_search_restaurant_items`, `food_get_restaurant_menu`, `food_get_item_options`, `food_get_items_options`, `food_dish_search`, `food_merchant_search`, `food_personalized_search`, `food_get_scheduling_slots`, `food_check_slot_availability`
  - **Groceries / Careem Quik (5):** `search_groceries_items`, `search_groceries_get_top_user_items`, `search_groceries_get_all_deals`, `create_grocery_cart_with_quantities` ⚠️, `is_grocery_area_serviceable`
  - **Shops (1):** `global_search`
  - **Cart & Checkout (14):** `cart_get_global_view`, `cart_get_basket`, `cart_get_quik_basket`, `cart_add_item` ⚠️, `cart_add_items` ⚠️, `cart_update_item` ⚠️, `cart_delete_items` ⚠️, `cart_delete_basket` ⚠️, `cart_get_basket_price`, `cart_get_checkout_promos`, `cart_reschedule_basket` ⚠️, `cart_reorder` ⚠️, `cart_checkout` ⚠️, `cart_grocery_checkout` ⚠️
  - **Box (5):** `box_get_vehicle_types`, `box_pre_checkout`, `box_get_config`, `box_get_categories`, `box_create_order` ⚠️
- **Golden Rule:** Any tool marked ⚠️ **mutating** MUST pause and obtain explicit user confirmation with exact item/price details before execution. Never blindly retry a timed-out mutating tool.

### Critical Gap Discovered (No Captain-Side Tools)
> **Unverified / Missing in Careem MCP:**  
> The official Careem MCP server exposes **zero Captain (Driver)-side tools**. There are no tools for reading Captain earnings, trip counts, acceptance/cancellation rates, tier splits, creating new promo codes, or managing family accounts.

---

## 2. Dual-Layer Royalty MCP Architecture

To build a real, working product around Careem's actual MCP server without inventing fake Careem endpoints, Royalty uses a **Two-Layer MCP Architecture**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AI Client (Claude / ChatGPT / Custom)                │
└───────────────┬─────────────────────────────────────┬───────────────────┘
                │ Streamable HTTP (OAuth 2.0 PKCE)    │ Stdio / HTTP
                ▼                                     ▼
┌───────────────────────────────┐     ┌───────────────────────────────────┐
│  Layer A: Official Careem MCP │     │  Layer B: Royalty Captain MCP     │
│  (mcp.careemapis.com/mcp)     │     │  (Custom Extension — src/royalty) │
├───────────────────────────────┤     ├───────────────────────────────────┤
│ • user_info (Captain/Family)  │     │ • royalty_get_captain_status      │
│ • get_activities (cross-app)  │     │ • royalty_calculate_trip_split    │
│ • apply_promotion_code ⚠️     │     │ • royalty_get_missions            │
│ • cart_get_checkout_promos    │     │ • royalty_issue_family_promo ⚠️   │
│ • search_groceries_get_all_   │     │ • royalty_verify_budget_cap       │
│   deals                       │     │ • royalty_recommend_next_action   │
│ • create_grocery_cart_with_   │     └─────────────────┬─────────────────┘
│   quantities ⚠️               │                       │
│ • cart_get_basket_price       │                       ▼
│ • cart_checkout ⚠️            │     ┌───────────────────────────────────┐
│ • box_pre_checkout / create⚠️ │     │   Royalty Incentive & Cap Engine  │
└───────────────────────────────┘     └───────────────────────────────────┘
```

---

## 3. Capability Classification Matrix

| Capability | Category | Tools / Components Used |
| :--- | :--- | :--- |
| **A. Immediate (Verified Careem MCP)** | Household grocery/food redemption, deal discovery, applying existing promo codes, cross-vertical activity lookup | `user_info`, `get_activities`, `search_groceries_get_all_deals`, `create_grocery_cart_with_quantities` ⚠️, `cart_get_basket_price`, `cart_get_checkout_promos`, `apply_promotion_code` ⚠️, `cart_checkout` ⚠️ |
| **B. Royalty Custom MCP + Backend** | Captain tier/XP tracking, 60/40→40/60 split calculation, budget-cap enforcement, personalized mission generation, family promo code generation | `royalty_get_captain_status`, `royalty_calculate_trip_split`, `royalty_get_missions`, `royalty_issue_family_promo` ⚠️, `royalty_verify_budget_cap` |
| **C. Requires Careem Production Approval** | Live Captain telemetry ingestion (trips, ratings, LTRC status), real-time dispatch priority flag, wallet payout settlement, dynamic promo code minting in Careem Promo Service | Careem Captain Dispatch API, Careem Pay Ledger API, Careem Promo Minting API |
| **D. Currently Infeasible via MCP Alone** | Direct Captain commission override inside Careem's production settlement without Careem internal APIs; automated ride booking without user confirmation | Blocked by Careem MCP consumer-only scope & Playbook mutating-tool rule |

---

## 4. End-to-End MCP Workflow: "Captain Earns & Redeems Family Grocery Benefit"

1. **Check Captain Status (Layer B):** `royalty_get_captain_status(captain_id)` → Returns Tier 4 (52% Driver Split), 5,200 XP, and 1 unclaimed **Family Quik Voucher (JOD 5)**.
2. **Issue Family Promo (Layer B — Mutating ⚠️):** After Captain confirms, `royalty_issue_family_promo(captain_id, family_member_id, benefit_type="QUIK")` checks `royalty_verify_budget_cap` and mints code `FAM-AMM-9421`.
3. **Family Member Redeems via Careem MCP (Layer A):**
   - `user_info()` → Resolves family member's `Home` address in Amman.
   - `is_grocery_area_serviceable(coords)` → Confirms Careem Quik coverage.
   - `search_groceries_get_all_deals(coords)` + `search_groceries_items(terms)` → Finds milk, bread, eggs, olive oil.
   - `create_grocery_cart_with_quantities(items, merchant_id, coords)` ⚠️ *(after user confirmation)*.
   - `cart_get_basket_price(merchant_id, coords, use_wallet=True)` → Auto-applies best promo and shows exact total.
   - **Stop & Confirm:** Agent displays full basket, address, and final discounted JOD total, then calls `cart_grocery_checkout` ⚠️ only after explicit user "yes".

---

## 5. Sandbox vs. Production Constraints

- **Local Sandbox:** Stateless (no persistent cart memory), uses Dubai test user *Leonardo DiCappuccino* (`AED`), no Rides tools, supports error-injection scenarios (empty results, validation errors, outages).
- **Production (`mcp.careemapis.com/mcp`):** Requires OAuth 2.0 PKCE login with a real Careem account; Hackathon Client ID `1790a895-9cef-48b7-9a57-ec5670d50c41` unlocks Rides pricing (`request_ride`) but agents **must never auto-confirm `create_ride` ⚠️**.
