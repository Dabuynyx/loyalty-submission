# Suggestions — Deep Research on Unexplored Opportunities & Next-Level Enhancements

**Purpose:** Deep-dive research into **7 high-impact areas** not yet covered in detail across the core Royalty business or engineering documents—combining verified Jordan/MENA market realities with concrete product and technical recommendations.

---

## 1. EV & Hybrid "Green Captain" Track (Jordan's EV Boom)

### Verified Market Context
- Jordan has become a regional leader in electric vehicle (EV) adoption due to high fuel prices and past tax incentives.
- Ride-hailing Captains in Amman have aggressively adopted EVs (BYD, MG, GAC, etc.) to cut daily operating costs, supported by fast-charging networks such as **ION (ION Microsystems)** and Greater Amman Municipality (GAM) charging initiatives. Careem Jordan has also actively expanded its EV fleet and financing partnerships (*Jordan News*).

### Suggestion for Royalty
- **ION / EV Charging Partner Tier:** Negotiate **10%–15% off-peak kWh charging discounts** with ION and local Amman fast-charging stations for **Tier 2+ EV Captains** (100% partner-funded for off-peak 01:00–06:00 or 11:00–14:00 grid balancing).
- **Green-Shift XP Bonus:** Award `+10% Eco-XP` on EV trips—giving EV Captains a faster climb to Tier 5–6 while helping Careem hit regional sustainability targets.

---

## 2. Central Bank of Jordan (CBJ) & JoMoPay Compliance for Wallets & Promos

### Verified Regulatory Context
- Jordan’s national interoperable mobile payment switch, **JoMoPay**, is overseen by the **Central Bank of Jordan (CBJ)** and operated by **JoPACC**, connecting licensed e-wallets (Zain Cash, Orange Money, UWallet, Dinarak). Any stored-value digital wallet or peer-to-peer transfer in Jordan falls under CBJ electronic payment bylaws.

### Suggestion for Royalty
- **Keep Royalty Closed-Loop:** Never store withdrawable cash balances inside Royalty's own database. Keep `BEIT-*` family codes strictly as **single-use merchant/vertical promotional discounts** (not transferable cash).
- **Route T4+ Instant Cashouts Through Licensed Rails:** Execute all real-money payouts and bonuses via **Careem Pay** or **JoMoPay-licensed wallets** so Royalty never triggers independent e-money licensing requirements.
- **Tax & GST Clarity:** Confirm with Careem Tax/Legal in Jordan whether commission uplifts (`60/40 → 40/60`) reduce Careem's taxable commission base cleanly compared to cash bonuses.

---

## 3. Female Captain ("Captainah") Loyalty & Daytime-Safety Track

### Verified Context
- Careem has a strong regional track record of recruiting and supporting female Captains (*Captainahs*) in Jordan, Saudi Arabia, and Egypt through flexible scheduling and safety tooling.

### Suggestion for Royalty
- **Daytime-Optimized Quests:** Standard rush-hour multipliers (16:00–19:00 or late-night burger perks) can inadvertently disadvantage female Captains who prefer daytime shifts (08:00–15:00). Add **School-Run & Midday Flex Quests** with equal XP value.
- **Safety-First Perks:** Unlock priority **Female-Preferred / Family-Ride Matching** (where permitted by local regulation) and 24/7 SOS priority response at **Tier 2** rather than gating safety behind Tier 5–6.

---

## 4. Hands-Free Arabic Voice & WhatsApp Co-Pilot (Low-Connectivity UX)

### The Gap
Our current UI prototype (`docs/ui-prototype/index.html`) assumes the Captain is parked and tapping a 4-tab mobile app. In reality, Captains in Amman's hilly terrain or tunnels face intermittent 4G and cannot safely read dashboards while driving.

### Suggestion for Royalty
- **Offline Tier Caching:** Cache `current_tier`, `driver_pct`, and `active_missions` locally in the Captain app with a stale-timestamp badge.
- **WhatsApp Business & Arabic Voice Digests:** Send a concise end-of-shift **Arabic WhatsApp summary** (*"أحسنت يا كابتن أحمد! ربحت اليوم 28 دينار (52%) وباقي لك 350 نقطة للوصول للمستوى الخامس"*) with 1-tap `Beit Careem` code sharing—zero in-car distraction.

---

## 5. Corporate (Careem for Business) & Jordan Tourism Corridor Unlocks

### The Gap
Once a Captain hits **Tier 6 (60% Driver Split)**, percentage uplift stops. How can Careem raise their **absolute JOD earnings** without raising the split above 60%?

### Suggestion for Royalty
- **High-Ticket Trip Access:** Gate pre-booked **Careem for Business** corporate rides and **Jordan Tourism Corridors** (Queen Alia Airport, Dead Sea, Petra, Wadi Rum) for **Tier 5–6 Legend Captains** with Rating ≥ 4.85.
- **Why It Works:** A JOD 35–60 airport/Dead Sea trip at a 60% split earns the Captain far more net JOD than five short city trips, while Careem's corporate clients get the most reliable, highest-rated Captains.

---

## 6. Game-Economy Balancing & A/B Experimentation Playbook

### The Gap
Our database schema includes `experiment_assignments`, but we have not yet defined how to prevent **XP inflation** (where too many Captains hit Tier 6 too easily, eroding blended margin) or **XP deflation** (where casual Captains quit).

### Suggestion for Royalty
- **Target Tier Distribution:** Calibrate seasonal XP thresholds so roughly **10%–15% reach T6 Legend**, **25% reach T4–T5**, and **60% sit in T1–T3** (preserving the ~48%–52% blended Careem margin).
- **Geo-Fenced A/B Cohorts:** Test new quest multipliers in 10% cohorts (e.g., Irbid or East Amman) for 14 days, measuring **Net Margin per Retained Captain** (not just trip count) before nationwide rollout.

---

## 7. Proactive Churn Prediction & Automated "Win-Back" Shield

### The Gap
Currently, **Tier Shields** are manually triggered or granted at Tier 6. If a Tier 4 Captain gets poached by a 0% Jeeny promo for 5 days, Careem only notices after they've churned.

### Suggestion for Royalty
- **Early-Warning Trigger:** If a Captain in **T3–T6** shows a **≥ 60% drop in 5-day rolling trips** compared to their 30-day baseline, automatically grant a **48-Hour Emergency Tier Shield + "Comeback Quest" (+300 XP for 3 rides)**—funded strictly within `remaining_reward_budget_jod`.
- **Psychology:** Combines loss aversion (*protecting their 52%–60% split*) with an immediate, achievable win.
