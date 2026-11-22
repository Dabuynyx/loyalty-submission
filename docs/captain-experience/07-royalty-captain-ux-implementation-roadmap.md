# 07 — Royalty Captain UX & Implementation Roadmap

**UX Principle:** The Captain must always see six things at a glance: *(1) What they earned, (2) Why they earned it, (3) What they can redeem, (4) What it costs (if anything), (5) What to do next, and (6) Whether a reward is guaranteed or conditional.*

---

## 1. End-to-End Captain User Experience

### 1.1 Discovery & Onboarding ("Endowed Progress")
- Upon opening the Captain App, new and existing Captains see the **Royalty Season Hub** already pre-seeded with **100 Welcome XP** (leveraging the *Endowed Progress Effect* so the progress bar is never empty at 0%).
- Clear visual banner: *"You are at Tier 1 (40% Split). Complete 8 rides this week to unlock Tier 2 (44% Split) + Car-Wash Discount."*

### 1.2 Home Hub & Live Trip Receipt
- **Top Card:** Current Tier Badge (e.g., `T4 PRO · 52% Driver Split`), XP Progress Bar (`5,240 / 8,500 XP to T5 Elite`), and active Quality Gate indicators (`Rating: 4.82 ✓ | Cancel: 3.1% ✓`).
- **Post-Trip Transparent Receipt:**
  - Gross Fare: `JOD 6.00`
  - Locked Tier Split (T4 · 52%): **`JOD 3.12` to Captain** / `JOD 2.88` to Careem
  - XP Earned: `+110 Base/Fare XP × 1.5x Peak = +165 XP` *(Guaranteed)*
- **Missions & Family Vault Tabs:**
  - *Missions:* Daily & Weekly Flex Quests with clear condition badges (`Guaranteed upon completion`).
  - *Beit Careem (Family Vault):* Manage up to 3 family beneficiaries and 1-tap generate/send unlocked promo codes.

### 1.3 Recovery & Support
- If a promo redemption fails or a quality gate drops (e.g., cancellation rate rises to 6.5%), the UI shows an **exact recovery path** (*"Complete 4 rides without canceling to restore T4 eligibility"*) plus a 1-tap **"Ask Co-Pilot / Support"** button.

---

## 2. Phased Implementation Roadmap

| Phase | Scope | Key Deliverables | Success Metrics (KPIs) |
| :--- | :--- | :--- | :--- |
| **Phase 1: Hackathon Prototype (Now)** | Deterministic Royalty Algorithm + Captain MCP Extension + Documentation | `src/royalty/algorithm.py`, `src/royalty/mcp_server.py`, Unit Tests, 9 Strategy/Tech PDFs | 100% test pass on budget-cap & tier-split invariants |
| **Phase 2: Amman Closed Pilot (Weeks 1–6)** | 200 Amman Captains (100 Fleet + 100 Independent), Manual Partner Vouchers, Family Quik Codes | Captain App Hub UI, Telemetry Pipeline, Pilot Survey | +12% 30-day Captain retention; ≥ 60% Family Code redemption |
| **Phase 3: Careem Production Integration (Months 2–4)** | OAuth 2.0 PKCE + Careem Internal Promo Minting API + Careem Pay Instant Cashout + Full Jordan Launch | Production MCP Bridge, Anti-Fraud Graph, Partner Portal | -20% Driver CAC; +15% Amman peak-hour supply fulfillment |
