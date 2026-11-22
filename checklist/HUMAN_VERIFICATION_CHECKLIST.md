# ROYALTY — Human-Only Master Verification Checklist

<!--
  AI-LOCK: STRICTLY READ-ONLY FOR ALL AI AGENTS & VIBE-CODING TOOLS.
  NO AI TOOL MAY CHECK BOXES ([x]) OR EDIT THIS FILE.
  HUMAN VERIFICATION REQUIRED BY: @Dabuynyx, @YousefHaymour1, @farescodex
-->

> **Rule:** Every box below must be verified and checked **manually by a human**. Do not allow any AI tool to auto-check items.

---

## 1. Documentation & Artifacts Audit
- [ ] Opened and visually inspected all Strategy/Business PDFs (`docs/product-strategy/`, `docs/incentive-economics/`, `docs/family-benefits/`, `docs/competitive-research/`, `docs/rider-experience/Royalty_Extra_Rider_Experience.pdf`, `docs/global-expansion/`) *(Sign-off: _______)*
- [ ] Opened and visually inspected all 12 Engineering PDFs (`docs/engineering/`) including Arabic text rendering in `Suggestions.pdf` *(Sign-off: _______)*
- [ ] Verified `docs/api/openapi.yaml` in Swagger Editor / Redocly with zero errors *(Sign-off: _______)*
- [ ] Rendered all 3 Mermaid `.mmd` diagrams (`docs/diagrams/`) in Mermaid Live Editor to confirm clean rendering *(Sign-off: _______)*
- [ ] Verified `docs/schemas/database/001_initial_schema.sql` executes cleanly in PostgreSQL 16 *(Sign-off: _______)*

---

## 2. Core Algorithm & Financial Safety
- [ ] Manually ran `python3 -m unittest discover -s tests -v` and observed all tests pass *(Sign-off: _______)*
- [ ] Verified `60/40 → 40/60` Fleet split curve and `28/72 → 14/86` Independent Jordan curve match business expectations *(Sign-off: _______)*
- [ ] Verified hard `60%` driver cap cannot be exceeded at any XP level *(Sign-off: _______)*
- [ ] Verified `remaining_reward_budget_jod` blocks stacked promos/bonuses from exceeding `max_reward_budget_pct` *(Sign-off: _______)*
- [ ] Verified `10h` daily fatigue XP cap and `JOD 1.50 / 1.0 km` wash-trip guard *(Sign-off: _______)*

---

## 3. Backend API, Database & Concurrency (Doc 12 Upgrades)
- [ ] FastAPI server starts cleanly locally (`uvicorn`) and serves `/v1/*` endpoints *(Sign-off: _______)*
- [ ] `POST /v1/events/trips/completed` with duplicate `Idempotency-Key` returns `202` without double-awarding XP *(Sign-off: _______)*
- [ ] Concurrent redemption test (`10` parallel requests for last JOD 5 budget) allows **only 1** success (`201`) and rejects **9** (`409`) *(Sign-off: _______)*
- [ ] Partner 503 failure triggers compensating `REFUND` transaction restoring `reward_budgets` *(Sign-off: _______)*
- [ ] `outbox_events` records `TierUpgraded` and `FamilyBenefitAssigned` in the same ACID transaction *(Sign-off: _______)*

---

## 4. Careem MCP, AWS Bedrock & Kiro Integration
- [ ] Connected to Careem Local Sandbox and verified `user_info`, `search_groceries_items`, `cart_get_basket_price` *(Sign-off: _______)*
- [ ] Verified OAuth 2.0 + PKCE (`S256`) login against Careem Production/QA MCP (`mcp.careemapis.com/mcp`) *(Sign-off: _______)*
- [ ] Confirmed ⚠️ mutating tools (`cart_grocery_checkout`, `apply_promotion_code`, `create_ride`) **always** pause for human confirmation and **never** auto-retry on timeout *(Sign-off: _______)*
- [ ] Verified AWS Bedrock `copilot.py` returns Arabic/English explanations with **zero PII** in prompts and falls back cleanly when offline *(Sign-off: _______)*
- [ ] Verified `.kiro/specs/royalty/` (`requirements.md`, `design.md`, `tasks.md`) exists and matches the codebase *(Sign-off: _______)*

---

## 5. UI/UX, RTL & Accessibility
- [ ] Opened `docs/ui-prototype/index.html` in Chrome/Safari and tested all 4 tabs (`Hub`, `Pass`, `For You`, `Family`) *(Sign-off: _______)*
- [ ] Verified live API connection (Trip Simulator updates XP/Split %; Family Code decrements Remaining Budget) *(Sign-off: _______)*
- [ ] Tested 1-click **Arabic (`العربية`) RTL** layout with zero text clipping or broken alignment *(Sign-off: _______)*

---

## 6. Security, Privacy & Final Repo Sign-Off
- [ ] Confirmed zero real secrets, tokens, passwords, or `.env` files exist anywhere in git history (`gitleaks` / manual check) *(Sign-off: _______)*
- [ ] Verified `personalization_opt_in = false` blocks all lifestyle queries and Careem MCP `get_activities` calls *(Sign-off: _______)*
- [ ] Verified `BEIT-*` family codes are bound to a single Careem consumer account (max 3 beneficiaries) *(Sign-off: _______)*
- [ ] Final human sign-off by all collaborators before Careem Builders ’26 submission *(Sign-off: _______)*
