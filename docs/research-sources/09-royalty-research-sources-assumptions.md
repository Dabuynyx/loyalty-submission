# 09 — Royalty Research Sources & Assumptions Register

**Research Standard:** Every major claim in the Royalty package is classified as **(A) Verified Fact**, **(B) Research-Backed Conclusion**, **(C) Illustrative Assumption**, or **(D) Unverified / Requires Careem Production Confirmation**.

---

## 1. Authoritative Technical Sources (Careem MCP)

| Source | Claim Supported | Status |
| :--- | :--- | :---: |
| `https://builders.careem.com/docs/tools/overview` (+ 9 subpages) | 50 consumer MCP tools across 8 domains + `ui://careem-mcp-app`; Rides marked "Coming soon"; zero Captain-side tools exist. | **Verified** |
| `https://builders.careem.com/docs/getting-started` & `authentication` | Prod endpoint `https://mcp.careemapis.com/mcp`, OAuth 2.0 + PKCE (`S256`), scopes `openid profile offline_access`. | **Verified** |
| `https://builders.careem.com/docs/sandbox` & `Careem MCP Hackathon Journey` PDF | Local sandbox is stateless (Leonardo DiCappuccino, Dubai, AED); Hackathon Client ID `1790a895-9cef-48b7-9a57-ec5670d50c41` enables early Rides pricing in prod. | **Verified** |

---

## 2. Jordan Market & Competitor Sources

| Source | Claim Supported | Status |
| :--- | :--- | :---: |
| LTRC / Jaradat Law / Jordan News / Petra News | Jordan ride-hailing regulated by LTRC; licensed apps include Careem, Uber, Jeeny, Petra Ride, Gojo; max 7-year vehicle age & permit rules. | **Verified** |
| POMEPS / MIT Jordan Ride-Hailing Studies | Standard Jordan app commissions ~20%–25%; high cash-payment usage creates commission-settlement friction. | **Verified** |
| Jordan Times / Careem.com (`Careem Plus Jordan`) | Careem Plus in Jordan costs **JOD 2.99/month** (10% credit back on up to 10 economy rides/mo, free food delivery > JOD 5, DineOut, priority support). | **Verified** |
| Careem Captain Portal (`careem.com`) | Careem Captain Rewards/Club in Jordan offers Silver/Gold/Platinum tiers, fuel (e.g., Manaseer) & maintenance discounts, in-ride insurance. | **Verified** |
| Jeeny (`jeeny.me`) & Petra Ride (`petraride.com`) | Jeeny offers 0% intro commission promos & daily/weekly ride-count bonuses; Petra Ride positions as local Jordanian fixed-cost alternative. | **Verified** |
| Uber Pro (`uber.com`, `asu.edu`) & GrabBenefits (`grab.com`) | Uber Pro 3-month tiers + transferable ASU tuition (2,000 trips, US/select markets); GrabBenefits healthcare, fuel, and Indonesian family scholarships. | **Verified** |
| Nunes & Drèze (*Endowed Progress Effect*); Kim (CMU *Workplace Gamification*) | Pre-seeded progress boosts completion; unchecked gamification causes extrinsic crowding-out and fatigued driving. | **Research-Backed** |

---

## 3. Explicit Assumptions & Unverified Items Requiring Pilot Validation

1. **Unverified Production Parameter — Exact Reward Budget Cap (`R_cap`):** Because Careem's internal Jordan P&L and fleet financing terms are private, we modeled an illustrative `22%` total reward cap on top of the `40%` T1 baseline (`src/royalty/algorithm.py` makes `R_cap` and the tier curve 100% configurable).
2. **Fleet vs. Independent Split:** The `60/40 → 40/60` split assumes a Careem-financed/managed fleet; independent car-owners in Jordan require the configurable `28% → 14%` Careem commission calibration.
3. **Captain Family Preferences:** Whether Amman Captains value Careem Quik grocery codes more than fuel vouchers is a **hypothesis** to be tested in the Phase 2 200-Captain Amman pilot.
4. **Internal Careem APIs:** Live Captain telemetry ingestion and programmatic promo code minting require Careem internal API approval beyond the public Consumer MCP server.
