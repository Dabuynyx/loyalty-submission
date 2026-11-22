# 04 — Royalty MCP Integration & API Specification

**Authoritative Careem MCP Docs:** `builders.careem.com/docs/getting-started`, `/docs/sandbox`, `/docs/tools/*`  
**Machine-Readable API Spec:** [`docs/api/openapi.yaml`](../../api/openapi.yaml)  
**Sequence Diagram:** [`docs/diagrams/workflows/mcp-and-redemption-sequence.mmd`](../../diagrams/workflows/mcp-and-redemption-sequence.mmd)

---

## 1. Verified Careem MCP Tool Inventory (50 Tools Across 8 Domains)

| Domain | Count | Verified Exact Tool Names | Mutating (⚠️) | Sandbox | Prod | Royalty Use Case |
| :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| **User** | 3 | `user_info`, `get_activities`, `track_activity` | Read-Only | Yes | Yes | Resolve saved `Home` coords; read opt-in lifestyle signals (`food`/`groceries`) |
| **Location** | 2 | `reverse_geocode`, `save_new_address` ⚠️ | `save_new_address` | Yes | Yes | Resolve Captain/family coordinates |
| **Rides** | 10 | `search_locations`, `search_locations_batch`, `request_ride`, `request_scheduled_ride`, `create_ride` ⚠️, `get_ride_cancellation_reasons`, `get_ride_cancellation_attributes`, `cancel_ride` ⚠️, `apply_promotion_code` ⚠️, `get_ride_schedule_policy` | `create_ride`, `cancel_ride`, `apply_promotion_code` | **No** ("Coming soon") | Early Access (Hackathon Client) | Family member applies `BEIT-*` ride promo code (`apply_promotion_code` ⚠️) |
| **Food** | 10 | `food_get_user_discovery_filters`, `food_search_restaurant_items`, `food_get_restaurant_menu`, `food_get_item_options`, `food_get_items_options`, `food_dish_search`, `food_merchant_search`, `food_personalized_search`, `food_get_scheduling_slots`, `food_check_slot_availability` | Read-Only | Yes | Yes | Lifestyle meal discovery (e.g., post-shift burger deals) |
| **Groceries** | 5 | `search_groceries_items`, `search_groceries_get_top_user_items`, `search_groceries_get_all_deals`, `create_grocery_cart_with_quantities` ⚠️, `is_grocery_area_serviceable` | `create_grocery_cart_with_quantities` | Yes | Yes | Household weekly Quik basket creation |
| **Shops** | 1 | `global_search` | Read-Only | Yes | Yes | Specialty retail deal discovery |
| **Cart** | 14 | `cart_get_global_view`, `cart_get_basket`, `cart_get_quik_basket`, `cart_add_item` ⚠️, `cart_add_items` ⚠️, `cart_update_item` ⚠️, `cart_delete_items` ⚠️, `cart_delete_basket` ⚠️, `cart_get_basket_price`, `cart_get_checkout_promos`, `cart_reschedule_basket` ⚠️, `cart_reorder` ⚠️, `cart_checkout` ⚠️, `cart_grocery_checkout` ⚠️ | 10 Mutating | Yes | Yes | Evaluate promos (`cart_get_basket_price`) & checkout after explicit user confirmation |
| **Box** | 5 | `box_get_vehicle_types`, `box_pre_checkout`, `box_get_config`, `box_get_categories`, `box_create_order` ⚠️ | `box_create_order` | Yes | Yes | Family parcel delivery quotes & orders |

**UI Resource:** `ui://careem-mcp-app` (optional embedded widget; text-only clients ignore it).

---

## 2. MCP Integration Layer & Safety Rules

- **Connection:** Streamable HTTP to `https://mcp.careemapis.com/mcp` with `Authorization: Bearer <access_token>` obtained via **OAuth 2.0 Authorization Code + PKCE (`S256`)** against `https://identity.careem.com/`.
- **Timeouts & Retries:** 8s connect/read timeout. Read-only tools retry up to 2× with exponential backoff; **mutating tools (⚠️) NEVER auto-retry** on timeout to prevent duplicate charges or dispatches.
- **Circuit Breaker:** Opens for 30s after 5 consecutive 5xx/timeout errors from Careem MCP; Royalty degrades gracefully to core tier/split/catalog features.
- **Royalty Captain MCP Extension (`src/royalty/mcp_server.py`):** Exposes `royalty_get_captain_status`, `royalty_calculate_trip_split`, `royalty_get_missions`, and `royalty_issue_family_promo` ⚠️ because Careem MCP has zero Captain-side tools.

---

## 3. Royalty HTTP API Summary (OpenAPI 3.1.0)

All 16 endpoints are formally defined in `docs/api/openapi.yaml`, including:
- **Captain:** `GET /captains/{id}/loyalty/status`, `GET .../progression`, `GET .../rewards/available`, `GET .../recommendations`, `PUT .../preferences`, `POST .../rewards/{reward_id}/redeem` (requires `Idempotency-Key`), `POST .../family-benefits/assign`.
- **Internal/Admin:** `POST /events/trips/completed`, `POST /admin/catalog`, `PUT /admin/budgets/{country_code}`, `POST /admin/partners/offers`.
