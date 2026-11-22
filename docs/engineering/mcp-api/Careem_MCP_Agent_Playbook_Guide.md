# Careem MCP Agent Playbook — Complete Deep-Dive Developer Handbook

**Authoritative Source:** Careem Builders Documentation (`builders.careem.com`)  
**Production MCP Endpoint:** `https://mcp.careemapis.com/mcp` (Streamable HTTP)  
**QA / Sandbox Endpoint:** `https://mcp.sandbox.careemapis.com/mcp` & Local No-Code Markdown Sandbox  
**Scope:** Verbatim System Prompt, OAuth 2.0 PKCE Connection, Local Sandbox vs. Production, 4 End-to-End Multi-Step Walkthroughs, Critical Domain Gotchas, Error/SSE Handling, and Complete 50+ Tool Reference Catalog.

---

## 1. Official Paste-Able System Prompt (Verbatim)

Paste this block directly into your LLM agent’s system prompt (Claude, ChatGPT, AWS Bedrock, Kiro, Cursor, or custom MCP orchestrator):

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

## 2. Authentication, OAuth 2.0 PKCE & Environment Setup

### 2.1 Production OAuth 2.0 Discovery & Connection Sequence
1. **Protected Resource Metadata (RFC 9728):**
   `GET https://mcp.careemapis.com/.well-known/oauth-protected-resource`
   Returns `resource`, `authorization_servers`, and `scopes_supported` (`openid`, `xcma`, `profile`).
2. **Careem Identity OpenID Config:**
   `GET https://identity.careem.com/.well-known/openid-configuration`
   Returns `authorization_endpoint` (`/authorize`) and `token_endpoint` (`/token`).
3. **Authorization Code + Mandatory PKCE (`S256` only):**
   - **Hackathon Public Client ID (no client secret):** `1790a895-9cef-48b7-9a57-ec5670d50c41`
   - **Required Scopes:** `openid profile offline_access` (`offline_access` enables refresh tokens)
   - **Registered Callback URLs:** `http://localhost/callback`, `http://localhost:8080/callback`, `http://localhost:3000/callback`, `http://127.0.0.1/callback`
4. **MCP Client Config (Streamable HTTP):**
   ```json
   {
     "mcpServers": {
       "careem": {
         "type": "streamable_http",
         "url": "https://mcp.careemapis.com/mcp",
         "headers": {
           "Authorization": "Bearer ${CAREEM_ACCESS_TOKEN}"
         }
       }
     }
   }
   ```

### 2.2 Local Sandbox vs. Production Comparison

| Dimension | Local Sandbox (Practice Mode) | Production (`mcp.careemapis.com/mcp`) |
| :--- | :--- | :--- |
| **Auth / Login** | None required (no token, no client ID) | OAuth 2.0 Authorization Code + PKCE (`S256`) |
| **Statefulness** | **Stateless (no memory)** — adding items to a basket does not persist across calls | Fully stateful — real orders, real charges, real Captains |
| **Test World** | *Leonardo DiCappuccino* (Dubai, `AED`), `Home`/`Work`/`Gym`, 5 restaurants (*Morning Syrniki Café*), Careem Quik Dubai Marina | Real signed-in Careem account & live city coverage |
| **Rides Domain** | **Not available** in Local Sandbox | Early Access for Hackathon Client (always stop before `create_ride` ⚠️) |
| **Error Testing** | Built-in scenarios (empty search `"xyz"`, restaurant `39999` outage, validation errors) | Live errors; never test failures with mutating tools |

---

## 3. Four End-to-End Multi-Step Walkthroughs

### Walkthrough A — Customized Food Order (7 Sequential Steps)
1. `user_info()` → Resolve `Home` coordinates (`latitude`, `longitude`) and `city_id`.
2. `get_activities(activity_status="past", activity_type="food")` or `food_personalized_search` → Check user favorites first (Rule 5).
3. `food_merchant_search(query, coords)` → Obtain `restaurant_id`.
4. `food_get_restaurant_menu(restaurant_id, coords)` → Obtain `item_id` (e.g., *Burger* or *Cappuccino*).
5. `food_get_item_options(restaurant_id, item_id, coords)` (or `food_get_items_options` for batch) → Obtain required `catalog_option_id`s (e.g., *Oat Milk*, *No Onions*).
6. `cart_add_item(merchant_id, catalog_item_id, count, options, coords, domain="food")` ⚠️ *(confirm before modifying basket)*.
7. `cart_get_basket_price(merchant_id, coords, business_type="food")` → Returns exact `total_price` with best promo auto-applied.
8. **STOP & CONFIRM:** Show items, delivery address, promo savings, and exact `total_price`. Only after explicit user **"Yes"**, call `cart_checkout(basket_id, total_price, coords, domain="food")` ⚠️.

### Walkthrough B — Careem Quik Grocery List in One Call (6 Steps)
1. `user_info()` → Resolve `Home` coordinates.
2. `is_grocery_area_serviceable(coords)` → Verify Careem Quik dark-store coverage.
3. `search_groceries_items(search_terms=["milk", "eggs", "bread"], coords)` → Omit `merchant_id` for Quik (nearest dark store auto-resolves and returns `merchant_id` + each `catalog_item_id`).
4. `create_grocery_cart_with_quantities(items, merchant_id, coords)` ⚠️ *(confirm before mutating)*.
5. `cart_get_basket_price(merchant_id, coords, business_type="quik")` → Get exact `total_price` and fees.
6. **STOP & CONFIRM:** Present basket + address + `total_price` → call `cart_grocery_checkout(basket_id, total_price, coords)` ⚠️ only after user says **"Yes"**.

### Walkthrough C — Ride Quote, Promo Code & Safe Cancellation
- **Booking Chain:**
  1. `search_locations(query, lat, lng)` (or `search_locations_batch` with up to 5 landmark/spelling variations).
  2. `request_ride(pickup, dropoff, lat, lng)` (or `request_scheduled_ride` + `get_ride_schedule_policy`) → Returns ride tiers, prices, and short-lived **`context_blob`**.
  3. *(Optional)* `apply_promotion_code(code, lat, lng)` ⚠️ *(confirm first — e.g., Royalty family code)*.
  4. **STOP & CONFIRM:** Present pickup, dropoff, vehicle tier, and fare. Only on explicit **"Yes"**, call `create_ride(selectedProduct, context_blob, pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)` ⚠️ promptly before `context_blob` expires.
- **Cancellation Chain:**
  `get_ride_cancellation_reasons(rideId)` → `get_ride_cancellation_attributes(rideId, cancellationReasonId)` *(extract **`pricingId`** and fee)* → **Confirm fee with user** → `cancel_ride(rideId, pricingId, answer)` ⚠️.

### Walkthrough D — Careem Box Parcel Delivery
1. `box_get_config(lat, lng, business_type="send")` → Confirm `service_status == "AVAILABLE"`.
2. `box_get_vehicle_types(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, business_type="send")` → Get **`cct_id`** (e.g., motorbike vs. car).
3. *(Optional)* `box_get_categories(lat, lng, business_type="send")` → Get `package_category_id`.
4. `box_pre_checkout(pickup/dropoff coords, cct_id, package_category_id?)` → Returns price range + `user_available_payment_methods`.
5. **STOP & CONFIRM:** User **must explicitly choose** `payment_type` (`cash | card | wallet`, plus `payment_id` if card) — **never auto-select** for Box → call `box_create_order(...)` ⚠️.

---

## 4. Critical Engineering Gotchas, Error Recovery & SSE Handling

| Gotcha / Pitfall | Exact Verified Behavior | Required Agent / Code Handling |
| :--- | :--- | :--- |
| **`domain` vs. `business_type` on Cart** | `domain` only accepts `shops` (default — covers **both** Quik & Shops!) or `food`. `business_type` accepts granular values (`food`, `restaurants`, `quik`). | Never pass `domain="quik"`; pass `domain="shops"` and `business_type="quik"`. |
| **`cart_delete_items` format** | `item_uuids` is a **comma-separated string**, NOT a JSON array. | Serialize as `"uuid1,uuid2"`. |
| **`cart_add_items` partial failure** | Batch add has **partial success per item with no rollback**. | Inspect every item result in response; inform user which items succeeded vs. failed. |
| **`get_activities` pagination cap** | Max **35** past activities per call; max **3 calls (105 total)** via `next_cursor`. | Stop paging after 3 cursors; do not infinite-loop. |
| **`search_groceries_items` ETA filter** | Passing `max_delivery_minutes` returns an **ETA error instead of items** if exceeded. | Catch ETA error and retry without `max_delivery_minutes` or inform user. |
| **Multi-step loop budget (Rule 6)** | Food/Quik flows take 6–8 sequential tool calls. | Set agent `max_tool_steps >= 15`. |
| **Timeout on Mutating Tool (Rule 7)** | Checkout/booking may have succeeded server-side before timeout. | **NEVER auto-retry.** Call `get_activities(activity_status="ongoing")` to verify state first. |
| **SSE `: keepalive` (Rule 8)** | Streamable HTTP / SSE emits `: keepalive` every **15 seconds**. | Strip lines beginning with `:` before JSON parsing. |

---

## 5. Complete Catalog of All 50 Official Careem MCP Tools (+ UI Resource & Royalty Extension)

### 5.1 User (3 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 1 | `user_info` | Read-Only | Profile + saved bookmarks (`Home`/`Work`) + routines (`coords?`, `service_area_id?`) |
| 2 | `get_activities` | Read-Only | Cross-vertical orders/rides (`activity_status?`, `activity_type?`, `next_cursor?`) |
| 3 | `track_activity` | Read-Only | Live tracking & ETA (`activity_type`, `reference_id`) |

### 5.2 Location (2 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 4 | `reverse_geocode` | Read-Only | Coordinates → address + `location.providerId` (`latitude`, `longitude`) |
| 5 | `save_new_address` | ⚠️ Mutating | Save address bookmark (`saved_name`, `provider_id`, `latitude`, `longitude`, `building_type`) |

### 5.3 Rides — Coming Soon in Sandbox / Early Access in Prod (10 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 6 | `search_locations` | Read-Only | Search locations / POIs (`query`, `latitude`, `longitude`) |
| 7 | `search_locations_batch` | Read-Only | Up to 5 location variations in one call (`locationTerms[]`, `latitude`, `longitude`) |
| 8 | `request_ride` | Read-Only | Ride options + prices + short-lived `context_blob` (`pickup`, `dropoff`, `latitude`, `longitude`) |
| 9 | `request_scheduled_ride` | Read-Only | Future ride options + prices (`+ pickupTime` RFC3339) |
| 10 | `create_ride` | ⚠️ Mutating | Book ride (`selectedProduct`, verbatim `context_blob`, pickup/dropoff coords, `payment_type?`) |
| 11 | `get_ride_cancellation_reasons` | Read-Only | List cancellation reasons (`rideId`) |
| 12 | `get_ride_cancellation_attributes` | Read-Only | Cancellation fee details + `pricingId` (`rideId`, `cancellationReasonId?`) |
| 13 | `cancel_ride` | ⚠️ Mutating | Cancel a ride (`rideId`, `pricingId`, `answer?`) |
| 14 | `apply_promotion_code` | ⚠️ Mutating | Apply promo code to account (`code`, `latitude`, `longitude`) |
| 15 | `get_ride_schedule_policy` | Read-Only | Ride scheduling policy & windows (`latitude`, `longitude`) |

### 5.4 Food (10 Tools)
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

### 5.5 Groceries / Careem Quik (5 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 26 | `search_groceries_items` | Read-Only | Multi-term search in nearest Quik store or Shops merchant (`search_terms[]`, `coords`, `merchant_id?`) |
| 27 | `search_groceries_get_top_user_items` | Read-Only | User's frequently ordered grocery items (`coords`) |
| 28 | `search_groceries_get_all_deals` | Read-Only | All active Careem Quik deals (`coords`) |
| 29 | `create_grocery_cart_with_quantities` | ⚠️ Mutating | Build entire shopping-list basket in one call (`items[]`, `merchant_id`, `coords`) |
| 30 | `is_grocery_area_serviceable` | Read-Only | Confirm Careem Quik delivery coverage (`coords`) |

### 5.6 Shops — Specialty Retail (1 Tool)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 31 | `global_search` | Read-Only | Search specialty retail merchants & items across brands (`query`, `coords`, `location?`) |

### 5.7 Cart & Checkout (14 Tools)
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

### 5.8 Box — Package & Parcel Delivery (5 Tools)
| # | Tool Name | Type | Purpose & Key Parameters |
| :---: | :--- | :---: | :--- |
| 46 | `box_get_vehicle_types` | Read-Only | Available courier vehicles + `cct_id` (pickup/dropoff coords, `business_type=send`) |
| 47 | `box_pre_checkout` | Read-Only | Validation, pricing & `user_available_payment_methods` (`cct_id`, coords, `package_category_id?`) |
| 48 | `box_get_config` | Read-Only | Confirm `service_status = AVAILABLE` (`latitude`, `longitude`, `business_type=send`) |
| 49 | `box_get_categories` | Read-Only | Available parcel categories + `package_category_id` (`latitude`, `longitude`, `business_type=send`) |
| 50 | `box_create_order` | ⚠️ Mutating | Create parcel delivery order (`cct_id`, pickup/dropoff location IDs, `payment_type`) |

### 5.9 Embedded UI Resource & Royalty Extension (5 Additional Capabilities)
- **Official Careem UI Resource:** `ui://careem-mcp-app` (`text/html;profile=mcp-app`) — Optional interactive widget for MCP-Apps clients (text-only agents ignore it; no MCP prompts are exposed).
- **Royalty Captain MCP Extension (`src/royalty/mcp_server.py`):**
  - `royalty_get_captain_status` (Read-Only) — Current progress %, split, XP & remaining reward budget.
  - `royalty_calculate_trip_split` (Read-Only) — Deterministic split & fatigue-safe XP preview.
  - `royalty_get_missions` (Read-Only) — Active guaranteed & part-time flex missions.
  - `royalty_issue_family_promo` (⚠️ Mutating) — Budget-capped household promo code issuance.
