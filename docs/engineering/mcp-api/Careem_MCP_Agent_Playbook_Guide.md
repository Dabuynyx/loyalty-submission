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

## 3. Quick-Reference: Read-Only vs. Mutating (⚠️) Tools

| Safe to Call Freely (Read-Only) | MUST Confirm First & Never Blind-Retry (⚠️ Mutating) |
| :--- | :--- |
| `user_info`, `get_activities`, `track_activity`, `reverse_geocode`, `search_locations`, `request_ride`, `food_*`, `search_groceries_*`, `global_search`, `cart_get_basket_price`, `cart_get_checkout_promos`, `box_pre_checkout` | `save_new_address`, `create_ride`, `cancel_ride`, `apply_promotion_code`, `create_grocery_cart_with_quantities`, `cart_add_item`, `cart_add_items`, `cart_update_item`, `cart_delete_items`, `cart_delete_basket`, `cart_reschedule_basket`, `cart_reorder`, `cart_checkout`, `cart_grocery_checkout`, `box_create_order` |
