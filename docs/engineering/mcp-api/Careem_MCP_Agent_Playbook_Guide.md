# Careem MCP Agent Playbook — Complete Usage Guide

**Purpose:** Practical implementation and prompt-engineering guide showing exactly how to use every rule in Careem’s official **Agent Playbook** with **Careem MCP** (`https://mcp.careemapis.com/mcp`) and **Royalty** (Captain, Family & Food Partner workflows).

---

## 1. The Official Paste-Able System Prompt (Verbatim)

Paste the following rules directly into your LLM agent’s system prompt (Claude, ChatGPT, AWS Bedrock, Kiro, or custom MCP client):

> **The Golden Rule:** Read-only tools are free to call while reasoning. **Mutating tools spend the user's money or change their real-world state** — always confirm first, and never retry them blindly after a timeout.

1. **Always pass the user's coordinates** (`latitude`/`longitude`) — nearly every tool is location-scoped. Get saved addresses from `user_info` if the user says "home" or "work".
2. **Respect chain dependencies**: `context_blob` from `request_ride` must be passed verbatim to `create_ride` and expires quickly; `pricingId` from `get_ride_cancellation_attributes` is required by `cancel_ride`; `catalog_option_id`s from `food_get_item_options` are required to add customizable food items.
3. **Never checkout blind**: call `cart_get_basket_price` first and pass its total as `total_price` to checkout. Confirm order contents, address, and price with the user before any mutating tool.
4. **Payment** defaults are auto-resolved (working card → wallet → cash); only pass `payment_type` if the user asks.
5. **Personalize** with `get_activities(past)` — prefer the user's known favourites over cold search.
6. **Budget for multi-step journeys**: a full food order is ~6+ sequential tool calls; keep your agent's tool-loop limits generous.
7. **Errors** come back as an `error` string field in the tool's structured output, or as MCP tool errors (e.g. a missing `Authorization` header is rejected). Retry idempotent reads; never blind-retry mutating tools.
8. **Long streams**: keepalive comments (`: keepalive`) arrive every 15 s on SSE streams — ignore them.

---

## 2. Rule-by-Rule Practical Guide (How to Use Every Rule)

### Rule 1 — Always Pass Coordinates (`latitude` / `longitude`)
- **Why:** Careem MCP tools filter restaurants, Careem Quik dark stores, ride pricing, and Box delivery coverage by exact coordinates.
- **How to use it:**
  - Start every session with `user_info()` to retrieve saved bookmarks (`Home`, `Work`, `Gym`) and `service_area_id` / `city_id`.
  - If the user gives a new map pin, call `reverse_geocode(latitude, longitude)` first to get `location.providerId` before `save_new_address` ⚠️.
- **Don’t:** Never guess coordinates or call `food_merchant_search` without `coords`.

### Rule 2 — Respect Strict Tool Chain Dependencies
Every Careem domain requires passing exact IDs from Step `N` into Step `N+1`:

| Journey | Mandatory Tool Chain (Exact Order) | Critical Token / ID Passed |
| :--- | :--- | :--- |
| **Food Order** | `user_info` → `food_merchant_search` → `food_get_restaurant_menu` → `food_get_item_options` → `cart_add_item` ⚠️ → `cart_get_basket_price` → `cart_checkout` ⚠️ | `restaurant_id`, `item_id`, `catalog_option_id`, `basket_id`, `total_price` |
| **Groceries (Quik)** | `user_info` → `is_grocery_area_serviceable` → `search_groceries_items` → `create_grocery_cart_with_quantities` ⚠️ → `cart_get_basket_price` → `cart_grocery_checkout` ⚠️ | `catalog_item_id`, `merchant_id`, `basket_id`, `total_price` |
| **Book a Ride** | `search_locations` → `request_ride` → *(optional `apply_promotion_code` ⚠️)* → `create_ride` ⚠️ | Short-lived **`context_blob`** (pass **verbatim**; book promptly before expiry!) |
| **Cancel a Ride** | `get_ride_cancellation_reasons` → `get_ride_cancellation_attributes` → `cancel_ride` ⚠️ | **`pricingId`** (from attributes) + `rideId` |
| **Send a Parcel (Box)** | `box_get_config` → `box_get_vehicle_types` → `box_pre_checkout` → `box_create_order` ⚠️ | **`cct_id`**, `pickup_location_id`, `dropoff_location_id` |

### Rule 3 — Never Checkout Blind (Human-in-the-Loop Confirmation)
- **Before calling `cart_checkout` ⚠️ or `cart_grocery_checkout` ⚠️:**
  1. Always call `cart_get_basket_price` (which auto-applies the best valid promo) to obtain the exact `total_price`.
  2. Display a clear confirmation summary to the user: **Items + Delivery Address + Applied Promo + Exact Final Total**.
  3. Wait for an explicit **"Yes"** before invoking the checkout tool with that exact `total_price`.
- **Same rule for Rides & Box:** Stop at `request_ride` / `box_pre_checkout` and wait for explicit user approval before calling `create_ride` ⚠️ or `box_create_order` ⚠️.

### Rule 4 — Let Payment Auto-Resolve
- Careem automatically picks the best available payment method in priority order: **Working Card → Careem Pay Wallet → Cash**.
- **How to use it:** Omit `payment_type` by default. Only pass `payment_type` (`cash | card | wallet`) if the user explicitly says *"pay with cash"* or *"use my Careem wallet"*. (Exception: `box_create_order` requires an explicit user-chosen `payment_type` from `box_pre_checkout`'s `user_available_payment_methods`).

### Rule 5 — Personalize with `get_activities(past)`
- **How to use it:** Before doing a cold search, call `get_activities(activity_status="past", activity_type="food")` (paginates up to 35/call, max 3 calls / 105 activities via `next_cursor`) or `search_groceries_get_top_user_items(coords)` and `food_personalized_search`.
- **In Royalty:** Only call this when the user has opted into lifestyle personalization (`personalization_opt_in = true`)—e.g., to surface a Captain’s favorite post-shift burger spot or weekly household groceries.

### Rule 6 — Budget for Multi-Step Tool Loops
- A single customized food order takes **6–8 sequential tool calls** (`user_info` → search → menu → options → add → price → confirm → checkout).
- **Engineering Setting:** Configure your agent framework (Claude, Bedrock, LangGraph, Kiro) with `max_tool_steps >= 15` so the agent never stops halfway through a basket chain.

### Rule 7 — Error Handling & Zero Blind Retries
- **Two Error Shapes:**
  1. Structured tool JSON containing an `"error"` string (e.g., store closed, ETA exceeded, invalid promo code).
  2. Protocol-level MCP error (e.g., `401 Unauthorized` due to missing/expired `Authorization: Bearer <token>`).
- **Recovery Policy:**
  - **Read-only tools:** Safe to retry up to **2×** with exponential backoff.
  - **Mutating tools (⚠️):** **NEVER blindly retry on timeout.** If `cart_checkout` or `create_ride` times out, check `get_activities(activity_status="ongoing")` first and explain the state calmly to the user so you never double-charge or dispatch two Captains.

### Rule 8 — Ignore SSE Keepalive Comments (`: keepalive`)
- Careem’s Streamable HTTP / SSE endpoint emits `: keepalive` comments every **15 seconds** on long-lived streams.
- **Engineering Setting:** Ensure your HTTP/SSE parser strips/ignores comment lines starting with `:` rather than throwing a JSON parse error or resetting the connection.

---

## 3. Complete Catalog of All 50 Official Careem MCP Tools (+ UI Resource)

Every tool below is verified directly against `builders.careem.com/docs/tools/*`. Tools marked **⚠️ Mutating** require explicit user confirmation and must **never** be blind-retried on timeout.

### 3.1 User (3 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 1 | `user_info` | Read-Only | Profile + saved bookmarks (`Home`/`Work`) + routines (`coords?`, `service_area_id?`) |
| 2 | `get_activities` | Read-Only | Cross-vertical orders/rides (`activity_status?`, `activity_type?`, `next_cursor?`) |
| 3 | `track_activity` | Read-Only | Live tracking & ETA (`activity_type`, `reference_id`) |

### 3.2 Location (2 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 4 | `reverse_geocode` | Read-Only | Coordinates → address + `location.providerId` (`latitude`, `longitude`) |
| 5 | `save_new_address` | ⚠️ Mutating | Save address bookmark (`saved_name`, `provider_id`, `latitude`, `longitude`, `building_type`) |

### 3.3 Rides — Coming Soon in Sandbox / Early Access in Prod (10 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 6 | `search_locations` | Read-Only | Search locations / POIs (`query`, `latitude`, `longitude`) |
| 7 | `search_locations_batch` | Read-Only | Up to 5 location spelling/landmark variations in one call (`locationTerms[]`, `latitude`, `longitude`) |
| 8 | `request_ride` | Read-Only | Ride options + prices + short-lived `context_blob` (`pickup`, `dropoff`, `latitude`, `longitude`) |
| 9 | `request_scheduled_ride` | Read-Only | Future ride options + prices (`+ pickupTime` RFC3339) |
| 10 | `create_ride` | ⚠️ Mutating | Book ride (`selectedProduct`, verbatim `context_blob`, pickup/dropoff coords, `payment_type?`) |
| 11 | `get_ride_cancellation_reasons` | Read-Only | List cancellation reasons (`rideId`) |
| 12 | `get_ride_cancellation_attributes` | Read-Only | Cancellation fee details + `pricingId` (`rideId`, `cancellationReasonId?`) |
| 13 | `cancel_ride` | ⚠️ Mutating | Cancel a ride (`rideId`, `pricingId`, `answer?`) |
| 14 | `apply_promotion_code` | ⚠️ Mutating | Apply promo code to account (`code`, `latitude`, `longitude`) |
| 15 | `get_ride_schedule_policy` | Read-Only | Ride scheduling policy & windows (`latitude`, `longitude`) |

### 3.4 Food (10 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 16 | `food_get_user_discovery_filters` | Read-Only | Available filters & sorts at location (`latitude`, `longitude`) |
| 17 | `food_search_restaurant_items` | Read-Only | Search dishes inside one restaurant (`restaurant_id`, `query`, `coords`, `domain?`) |
| 18 | `food_get_restaurant_menu` | Read-Only | Full restaurant menu (`restaurant_id`, `coords`) |
| 19 | `food_get_item_options` | Read-Only | Customization choices + `catalog_option_ids` (`restaurant_id`, `item_id`, `coords`, `domain?`) |
| 20 | `food_get_items_options` | Read-Only | Batch customization choices for multiple items (`restaurant_id`, `item_ids[]`, `coords`) |
| 21 | `food_dish_search` | Read-Only | Search dishes across restaurants (`query`, `coords`, filters) |
| 22 | `food_merchant_search` | Read-Only | Search restaurants/merchants (`query`, `coords`, filters) |
| 23 | `food_personalized_search` | Read-Only | Recommendations from user's usual restaurants (`merchant_names[]` up to 3, `coords`) |
| 24 | `food_get_scheduling_slots` | Read-Only | Available delivery/pickup time slots (`restaurant_id`, `coords`) |
| 25 | `food_check_slot_availability` | Read-Only | Confirm specific slot (`restaurant_id`, `coords`, `slot_start`, `slot_end`) |

### 3.5 Groceries / Careem Quik (5 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 26 | `search_groceries_items` | Read-Only | Multi-term search in nearest Quik store or Shops merchant (`search_terms[]`, `coords`, `merchant_id?`) |
| 27 | `search_groceries_get_top_user_items` | Read-Only | User's frequently ordered grocery items (`coords`) |
| 28 | `search_groceries_get_all_deals` | Read-Only | All active Careem Quik deals (`coords`) |
| 29 | `create_grocery_cart_with_quantities` | ⚠️ Mutating | Build entire shopping-list basket in one call (`items[]`, `merchant_id`, `coords`) |
| 30 | `is_grocery_area_serviceable` | Read-Only | Confirm Careem Quik delivery coverage (`coords`) |

### 3.6 Shops — Specialty Retail (1 Tool)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 31 | `global_search` | Read-Only | Search specialty retail merchants & items across brands (`query`, `coords`, `location?`) |

### 3.7 Cart & Checkout (14 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 32 | `cart_get_global_view` | Read-Only | All open baskets with item details (`coords`, `merchant_id?`) |
| 33 | `cart_get_basket` | Read-Only | Open basket for one merchant (`merchant_id`, `coords`) |
| 34 | `cart_get_quik_basket` | Read-Only | Open Careem Quik grocery basket (`coords`, `city_id?`) |
| 35 | `cart_add_item` | ⚠️ Mutating | Add one item / count 0 removes (`merchant_id`, `catalog_item_id`, `count`, `options[]`, `coords`) |
| 36 | `cart_add_items` | ⚠️ Mutating | Batch add items to one merchant (`items[]`, partial success, no rollback) |
| 37 | `cart_update_item` | ⚠️ Mutating | Update line item quantity (`item_uuid`, `count`) |
| 38 | `cart_delete_items` | ⚠️ Mutating | Delete lines by UUID (`merchant_id`, comma-separated `item_uuids`, `coords`) |
| 39 | `cart_delete_basket` | ⚠️ Mutating | Delete entire merchant basket (`merchant_id`, `coords`) |
| 40 | `cart_get_basket_price` | Read-Only | Exact final total with best promo auto-applied (`merchant_id`, `coords`, `payment_type?`, `use_wallet?`) |
| 41 | `cart_get_checkout_promos` | Read-Only | List available promos with `is_best_saving` flag (`merchant_id`, `coords`, `business_type`, `payment_type`) |
| 42 | `cart_reschedule_basket` | ⚠️ Mutating | Reschedule delivery/pickup slot (`merchant_id`, `coords`, `scheduled_slot_start?`, `scheduled_slot_end?`) |
| 43 | `cart_reorder` | ⚠️ Mutating | Create draft basket from a past order (`order_id`, `coords`) |
| 44 | `cart_checkout` | ⚠️ Mutating | Place Food or Shops order (`basket_id`, `total_price`, `coords`, `domain?`) |
| 45 | `cart_grocery_checkout` | ⚠️ Mutating | Place Careem Quik order — auto-resolves address & payment (`basket_id`, `total_price`, `coords`) |

### 3.8 Box — Package & Parcel Delivery (5 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 46 | `box_get_vehicle_types` | Read-Only | Available courier vehicles + `cct_id` (pickup/dropoff coords, `business_type=send`) |
| 47 | `box_pre_checkout` | Read-Only | Validation, pricing & `user_available_payment_methods` (`cct_id`, coords, `package_category_id?`) |
| 48 | `box_get_config` | Read-Only | Confirm `service_status = AVAILABLE` (`latitude`, `longitude`, `business_type=send`) |
| 49 | `box_get_categories` | Read-Only | Available parcel categories + `package_category_id` (`latitude`, `longitude`, `business_type=send`) |
| 50 | `box_create_order` | ⚠️ Mutating | Create parcel delivery order (`cct_id`, pickup/dropoff location IDs, `payment_type`) |

### 3.9 Embedded UI Resource & Royalty Custom Extension (5 Additional Capabilities)
- **Official Careem UI Resource:** `ui://careem-mcp-app` (`text/html;profile=mcp-app`) — Optional interactive widget for MCP-Apps clients (text-only agents ignore it).
- **Royalty Captain MCP Extension (`src/royalty/mcp_server.py`):**
  - `royalty_get_captain_status` (Read-Only) — Current progress %, split, XP & remaining reward budget.
  - `royalty_calculate_trip_split` (Read-Only) — Deterministic split & fatigue-safe XP preview.
  - `royalty_get_missions` (Read-Only) — Active guaranteed & part-time flex missions.
  - `royalty_issue_family_promo` (⚠️ Mutating) — Budget-capped household promo code issuance.
