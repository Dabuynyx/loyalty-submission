# 05 — Royalty Security, Privacy & Threat Model

**Methodology:** STRIDE Threat Modeling + OWASP ASVS Level 2 & OWASP API Security Top 10.

---

## 1. STRIDE Threat Model

| Threat | Category | Attack Vector | Mitigation (MVP & Production) |
| :--- | :---: | :--- | :--- |
| **Account Compromise** | Spoofing | Stolen JWT or phishing Captain login | Careem OAuth 2.0 + PKCE (`S256`); short-lived JWTs (15m) + audience validation. |
| **Reward Replay / Double Spend** | Tampering / Repudiation | Replaying `TripCompleted` webhook or double-clicking `Redeem` | `UNIQUE(idempotency_key)` + `SELECT ... FOR UPDATE` on `reward_budgets`. |
| **Family Promo Abuse / Resale** | Elevation / Fraud | Selling `BEIT-*` codes on social media or linking fake accounts | Codes bound to `careem_consumer_ref`; max 3 beneficiaries; 90-day cooldown on beneficiary swaps; self-ride check blocks Captain driving own family code. |
| **MCP Tool Misuse** | Tampering | Prompt injection tricks AI into calling `cart_checkout` ⚠️ or `create_ride` ⚠️ | Playbook enforces mandatory human-in-the-loop confirmation before any ⚠️ mutating tool; strict JSON schema validation. |
| **Budget Manipulation / Insider Abuse** | Elevation | Admin raising `max_reward_budget_pct` silently | Dual-control approval for budget changes > 25%; immutable `audit_events` log. |
| **Sensitive Preference Exposure** | Info Disclosure | Leaking Captain food/location habits or cross-country data | Opt-in `consent_records` gate; `country_code` tenant isolation on every query; TLS 1.3 + AES-256 at rest. |
| **Partner Integration Compromise** | Spoofing / Tampering | Forged partner redemption callbacks | HMAC-SHA256 signed partner webhooks + IP allowlist + per-partner API keys. |

---

## 2. MVP vs. Production Security Controls

- **Required for MVP / Pilot:**
  - OAuth 2.0 / JWT verification on every API route (`401`/`403` fail-closed).
  - Row-level locking + idempotency keys on all budget/promo mutations.
  - Zero secrets in git (`.env.example` placeholders only); explicit `consent_records` check before calling Careem MCP `get_activities`.
- **Required Before Full Production:**
  - Careem WAF / mTLS between Careem Dispatch and Royalty `POST /events/trips/completed`.
  - Automated fraud-graph anomaly detection (wash-trip ring detection).
  - KMS-managed envelope encryption for `captain_preferences` and automated GDPR/local-law data deletion pipeline.
