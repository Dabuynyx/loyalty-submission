# Careem Loyalty & Battle Pass System — Planning & Documentation

> **Status:** Planning & Documentation Phase (No application code yet)  
> **Target Market:** Jordan Ride-Hailing Ecosystem (Amman & Governorates)  
> **Repository:** `loyalty-submission`

---

## Executive Summary

Jordan's ride-hailing market is intensely competitive, with **Careem**, **Uber**, **Jeeny**, **Petra Ride**, and newer entrants competing for the same pool of drivers ("Captains") and riders. Because switching apps has near-zero friction, drivers multi-home across apps and chase short-term promos, driving up acquisition costs and hurting reliability during peak hours.

This project designs a **Fortnite Battle Pass–inspired Loyalty & Progression System** for Careem in Jordan across three pillars:

1. **Driver Tier & Dynamic Split System ("Captain Battle Pass"):** Drivers start at a **60% Careem / 40% Driver** earnings split (Tier 1) and progress through seasonal tiers up to a capped **40% Careem / 60% Driver** split (Tier 6). Leaving Careem for a competitor means sacrificing hard-earned progression and a higher take-home percentage.
2. **Rider & Careem Plus Progression System:** Everyday riders earn XP and seasonal rewards, while **Careem Plus** subscribers (JOD 2.99/month in Jordan) unlock a **2x XP multiplier**, an **exclusive Premium Reward Track**, Surge Shield tokens, priority matching, and enhanced Careem Pay cashback.
3. **Sustainable Monetization:** Careem funds lower top-tier commissions through higher driver utilization and retention, recurring subscription revenue (**Captain Pro Pass** + **Careem Plus**), blended portfolio margins, Careem Pay wallet adoption, and merchant-sponsored rewards.

---

## Documentation Index

| Document | Audience | Description | PDF |
| :--- | :--- | :--- | :--- |
| [01 — Driver Tier & Battle Pass System](docs/01-driver-tier-system.md) | Product, Operations, Engineering | The 6-tier progression curve (60/40 → 40/60), XP formulas, quests, Captain Pro Pass, anti-gaming gates, and JOD worked examples. | [PDF](docs/pdf/01-driver-tier-system.pdf) |
| [02 — Rider & Careem Plus System](docs/02-rider-and-careem-plus-system.md) | Product, Growth, Marketing | Standard Rider Battle Pass vs. Careem Plus Enhanced Track, XP mechanics, and cross-ecosystem perks (Rides + Food + Pay). | [PDF](docs/pdf/02-rider-and-careem-plus-system.pdf) |
| [03 — Business Model & Jordan Strategy](docs/03-business-model-and-jordan-market.md) | Executives, Investors, Judges | Jordan competitive analysis, Win-Win-Win value proposition, unit economics, monetization streams, and commission calibration note. | [PDF](docs/pdf/03-business-model-and-jordan-market.pdf) |
| [04 — Technical Architecture & Data Model](docs/04-technical-architecture.md) | Engineering, Architects | Event-driven loyalty engine, domain schema, real-time split calculation, anti-fraud controls, and API surface. | [PDF](docs/pdf/04-technical-architecture.pdf) |

---

## Quick Overview: The Driver Split Curve

| Tier | Name | Careem Share | Driver Share | Season XP Required | Key Unlock |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **T1** | Rookie | **60%** | **40%** | 0 XP | Base access & Daily Quests |
| **T2** | Challenger | **56%** | **44%** | 1,000 XP | +4% Driver Split, Fuel Voucher |
| **T3** | Contender | **52%** | **48%** | 2,500 XP | +8% Driver Split, Priority Airport Queue |
| **T4** | Pro | **48%** | **52%** | 5,000 XP | +12% Driver Split, Instant Payouts |
| **T5** | Elite | **44%** | **56%** | 8,500 XP | +16% Driver Split, Peak Surge Multiplier |
| **T6** | Legend | **40%** | **60%** | 13,000 XP | Max 60% Driver Split, VIP Support & Tier Shield |

---

## Next Steps

1. Review the four planning documents and PDFs.
2. Finalize key business parameters (season length, fleet vs. independent driver commission calibration, Captain Pro Pass pricing).
3. Move to Phase 2: Implementation (Backend Loyalty Engine, Driver/Rider UI mockups, and Simulation Dashboard).
