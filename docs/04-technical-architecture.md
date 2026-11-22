# 04 — Technical Architecture & Data Model (Planning)

> **Scope:** Planning & architecture specification only. No application code is included in this phase.

---

## 1. High-Level Architecture (Event-Driven Loyalty Engine)

The Loyalty & Battle Pass Engine sits alongside Careem's existing Ride, Payment, and Careem Plus services as an **event-driven microservice** so it never blocks trip dispatch or checkout.

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────────┐
│  Ride Service   │────▶│                  │────▶│   XP & Quest Engine   │
└─────────────────┘     │   Event Bus      │     └───────────┬───────────┘
                        │  (Kafka / SQS)   │                 │
┌─────────────────┐     │                  │     ┌───────────▼───────────┐
│ Careem Food/Pay │────▶│                  │────▶│  Tier & Split Engine  │
└─────────────────┘     └──────────────────┘     └───────────┬───────────┘
                                                             │
┌─────────────────┐     ┌──────────────────┐                 │
│  Payout Ledger  │◀────│  Ride Settlement │◀────────────────┘
└─────────────────┘     └──────────────────┘
```

### Key Architectural Principles
- **Idempotency:** Every `RideCompleted` event carries a unique `ride_id` + `idempotency_key` so retries never double-award XP or double-pay bonuses.
- **Snapshot at Ride Start:** A driver's commission split (e.g., 52% Driver / 48% Careem) is locked at **trip acceptance/start** and stored on the trip settlement record for full financial auditability.
- **Config-Driven Curves:** Season dates, XP thresholds, and commission percentages live in a versioned `SeasonConfig` table—allowing A/B testing or Fleet vs. Independent calibration without code deploys.

---

## 2. Core Domain Data Model

### 2.1 `Season`
- `season_id` (UUID), `name` (e.g., `"Amman-2026-S11"`), `start_at`, `end_at`, `status` (`ACTIVE | ENDED`)
- `driver_tier_config` (JSON/Relational: T1–T6 XP thresholds, `careem_pct`, `driver_pct`, min rating, max cancel rate)
- `rider_tier_config` (JSON/Relational: R1–R5 XP thresholds, cashback caps, perks)

### 2.2 `DriverSeasonProgress`
- `driver_id`, `season_id`
- `current_xp` (int), `current_tier` (`T1`–`T6`)
- `has_pro_pass` (bool), `tier_shields_remaining` (int)
- `rolling_rating` (decimal), `rolling_cancel_rate` (decimal), `streak_days` (int)
- `last_active_at` (timestamp)

### 2.3 `RiderSeasonProgress`
- `rider_id`, `season_id`
- `current_xp` (int), `current_tier` (`R1`–`R5`)
- `is_careem_plus` (bool), `xp_multiplier` (`1.0` or `2.0`)
- `surge_shields_remaining` (int), `monthly_cashback_used_rides` (int)

### 2.4 `Quest` & `QuestProgress`
- `quest_id`, `audience` (`DRIVER | RIDER`), `cadence` (`DAILY | WEEKLY | SEASON`)
- `rule_expression` (e.g., `rides_in_window >= 3 AND cancel_count == 0`)
- `reward_xp` (int), `reward_voucher_id` (nullable)

### 2.5 `SplitLedger` (Financial Audit Trail)
- `ledger_id`, `ride_id`, `driver_id`, `season_id`
- `gross_fare_jod`, `tier_applied`, `careem_pct`, `driver_pct`
- `careem_amount_jod`, `driver_amount_jod`, `payment_method` (`CASH | CAREEM_PAY | CARD`)
- `created_at`

---

## 3. Real-Time Ride Settlement Flow

1. **Trip Requested:** Rider's `RiderSeasonProgress` is checked (`R4+` Careem Plus gets priority matching flag; `SurgeShield` token can be applied if surge > 1.0x).
2. **Trip Accepted:** Driver's current eligible tier is resolved (`T1`–`T6`, verifying quality gates: rating & cancel rate) and cached on the trip context.
3. **Trip Completed:**
   - `RideSettlement` reads the locked `driver_pct` / `careem_pct` and writes an immutable `SplitLedger` entry.
   - `RideCompleted` event is published to the Event Bus.
4. **Async XP & Tier Evaluation:**
   - `XP & Quest Engine` computes `Ride XP` (base + fare + zone + streak + Pro Pass / Careem Plus multiplier).
   - `QuestProgress` updates any active Daily/Weekly quests.
   - If `current_xp` crosses the next tier threshold **and** quality gates pass, `current_tier` upgrades immediately and a push notification is sent (*"Level Up! You unlocked Tier 4 — 52% Driver Split!"*).

---

## 4. Anti-Fraud & Anti-Gaming Controls

| Abuse Vector | Mitigation |
| :--- | :--- |
| **Fake short rides / self-booking** | Minimum fare (e.g., JOD 1.50) & minimum distance/duration (≥ 1.0 km, ≥ 3 min) required to earn XP; device/IP/GPS-proximity graph flags repeated driver-rider pairs. |
| **GPS spoofing for zone multipliers** | Cross-check pickup/dropoff coordinates against actual route telemetry and cell-tower/speed sanity checks. |
| **Cancel-and-rebook farming** | Driver cancellations directly penalize `rolling_cancel_rate`, blocking tier upgrades even if XP is high. |
| **Cash-commission evasion** | Drivers with overdue cash-settlement balances have tier split upgrades paused until settled via Careem Pay or agent office. |

---

## 5. Planned API Surface (Phase 2)

- **Driver App:**
  - `GET /v1/drivers/{id}/loyalty/season` — Current tier, split %, XP progress bar, active quests, Pro Pass status.
  - `POST /v1/drivers/{id}/loyalty/pro-pass/subscribe` — Activate Captain Pro Pass.
  - `POST /v1/drivers/{id}/loyalty/rewards/{reward_id}/claim` — Claim unlocked vouchers/bonuses.
- **Rider App:**
  - `GET /v1/riders/{id}/loyalty/season` — Current tier, 2x Careem Plus status, Surge Shields, cashback cap usage.
  - `POST /v1/riders/{id}/loyalty/surge-shield/apply` — Apply Surge Shield token to trip quote.
- **Admin / Ops:**
  - `POST /v1/admin/seasons` — Create/configure season curves (Fleet vs. Independent) and quests.
