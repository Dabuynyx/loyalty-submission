# 01 — Driver Tier & Battle Pass System ("Captain Pass")

## 1. Core Concept

To combat driver churn to competing apps in Jordan (Uber, Jeeny, Petra Ride, Gojo), Careem introduces a **seasonal, Fortnite Battle Pass–style progression system** for drivers ("Captains").

Instead of a flat, static commission rate, a driver's earnings split is **dynamic and earned**:
- **Starting Split (Tier 1):** **60% Careem / 40% Driver**
- **Maximum Split (Tier 6):** **40% Careem / 60% Driver** (hard cap — drivers never reach 100%)

Every completed ride, peak-hour trip, and streak awards **Captain XP**. As XP accumulates during a **30-day Season**, the driver climbs tiers and immediately earns a higher share of every fare.

---

## 2. The 6-Tier Progression Table ("T System")

| Tier | Badge | Careem % | Driver % | Season XP Threshold | Quality Gate (Minimum) | Core Perks Unlocked |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| **T1** | Rookie | **60%** | **40%** | 0 XP | Active LTRC Permit | Base dispatch, Daily Quests |
| **T2** | Challenger | **56%** | **44%** | 1,000 XP | Rating ≥ 4.5, Cancel ≤ 10% | +4% split, Partner car-wash discount |
| **T3** | Contender | **52%** | **48%** | 2,500 XP | Rating ≥ 4.6, Cancel ≤ 8% | +8% split, Fuel voucher (JOD 5/mo) |
| **T4** | Pro | **48%** | **52%** | 5,000 XP | Rating ≥ 4.7, Cancel ≤ 6% | +12% split, Instant Careem Pay cashout |
| **T5** | Elite | **44%** | **56%** | 8,500 XP | Rating ≥ 4.8, Cancel ≤ 5% | +16% split, Priority Queen Alia Airport & peak matching |
| **T6** | Legend | **40%** | **60%** | 13,000 XP | Rating ≥ 4.85, Cancel ≤ 4% | Max 60% split, VIP support, 1 free Tier Shield/season |

> **Why a Quality Gate?**  
> Without rating and cancellation gates, drivers could grind short rides while cherry-picking or canceling cash trips. Quality gates ensure higher pay only goes to reliable, high-rated Captains.

---

## 3. How XP & Quests Work (The "Addictive" Loop)

### 3.1 Base XP Formula
Drivers earn XP on every completed ride:

`Ride XP = (50 Base XP + 10 XP × Fare in JOD) × Zone Multiplier × Streak Multiplier`

- **Base XP:** 50 XP per completed ride (rewards trip count).
- **Fare XP:** 10 XP per JOD of fare (rewards longer trips, e.g., Airport runs).
- **Peak / Zone Multiplier:**
  - Normal hours: `1.0x`
  - Amman Rush Hour (07:30–09:30, 16:00–19:00): `1.5x`
  - High-demand zones (Abdali, Sweifieh, Dabouq, Queen Alia Airport): `1.75x`
- **Streak Multiplier:**
  - 3 consecutive days with ≥ 5 rides/day: `1.1x`
  - 7 consecutive days: `1.25x`
  - 14+ consecutive days: `1.4x`

### 3.2 Daily & Weekly Quests (Battle Pass Missions)
Just like Fortnite's Battle Pass challenges, quests give bursts of XP to keep drivers logging in daily:
- **Daily Quests (Reset 04:00 AM):**
  - *Morning Rush:* Complete 3 rides between 07:00 and 10:00 → **+150 XP**
  - *Clean Sheet:* Complete 8 rides with 0 driver cancellations → **+200 XP**
  - *Digital First:* Accept 4 Careem Pay / Card rides → **+100 XP**
- **Weekly Quests:**
  - *Weekend Warrior:* Complete 25 rides Friday–Saturday → **+750 XP**
  - *Top Rated:* Maintain 4.9+ average across 40 rides → **+600 XP**

---

## 4. Free Track vs. Captain Pro Pass (Monetization)

Like Fortnite's Free vs. Paid Battle Pass, Careem offers two tracks each 30-day season:

| Feature | Free Track (All Drivers) | Captain Pro Pass (JOD 9.99 / Season) |
| :--- | :---: | :---: |
| Tier Split Progression (60/40 → 40/60) | Yes | Yes |
| XP Multiplier | 1.0x | **1.5x Boost** (reach T6 33% faster) |
| Season Head Start | Start at T1 (0 XP) | **Instant +1,000 XP** (Start at T2!) |
| Tier Shield (Inactivity Protection) | None (except T6) | **2 Tier Shields / Season** |
| Milestone Cash Bonuses | Partner vouchers only | **JOD 25+ in milestone cash bonuses** |
| Instant Payouts | T4+ only | **Unlocked from Day 1** |

**Why drivers buy it:** A driver doing 250+ rides/month easily recoups JOD 9.99 within days via the +4% head start at Tier 2 and the 1.5x XP boost to reach Tier 5–6 sooner.

---

## 5. Season Reset & Retention Mechanics

A **30-day Season** prevents drivers from hitting Tier 6 once and coasting:
- **Soft Reset (Not Full Reset):** At the end of a 30-day season, drivers do **not** drop all the way back to Tier 1. Instead, they drop **2 tiers** (e.g., T6 Legend → T4 Pro, T4 Pro → T2 Challenger) and keep a **Season Badge** on their profile.
- **Why Soft Reset Works:** Dropping 2 tiers gives drivers an immediate head start over brand-new drivers (protecting loyalty) while still giving them a reason to grind back to T6 every month.
- **Inactivity Decay Warning:** If a driver is inactive for 7+ days without a **Tier Shield**, they receive a push notification (*"Your 56% split expires in 48 hours — complete 3 rides to lock it in!"*), creating strong loss-aversion retention.

---

## 6. Worked Earnings Examples (JOD)

### Example A: Single JOD 5.00 Ride in Amman
| Driver Tier | Careem % | Driver % | Careem Earns | Driver Earns | Driver Gain vs. T1 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **T1 (Rookie)** | 60% | 40% | JOD 3.00 | **JOD 2.00** | — |
| **T3 (Contender)** | 52% | 48% | JOD 2.60 | **JOD 2.40** | +JOD 0.40 (+20%) |
| **T6 (Legend)** | 40% | 60% | JOD 2.00 | **JOD 3.00** | **+JOD 1.00 (+50%)** |

### Example B: Full-Time Driver (JOD 1,500 Gross Monthly Fares)
- **At T1 (40% Driver):** Driver takes home **JOD 600** | Careem takes **JOD 900**
- **At T4 (52% Driver):** Driver takes home **JOD 780** | Careem takes **JOD 720**
- **At T6 (60% Driver):** Driver takes home **JOD 900** (+JOD 300/month raise!) | Careem takes **JOD 600**

**Psychological Impact:** Every time a T5 or T6 driver considers switching to Jeeny or Petra Ride, they see they are earning **50% more per ride** than a rookie — making the switching cost feel huge.
