# 08 — Royalty Deployment, Operations & Reliability

**Infrastructure Note:** Because Careem's internal cloud/Kubernetes standards are not publicly documented, this specification defines a **cloud-agnostic containerized deployment** (Docker + PostgreSQL + Worker) adaptable to Careem's AWS/GCP environment.

---

## 1. Environments & CI/CD Pipeline

- **Environments:** `dev` (local Docker + Careem Local Sandbox MCP) → `test` (ephemeral DB in CI) → `staging` (Careem QA `mcp.sandbox.careemapis.com/mcp`) → `prod` (`mcp.careemapis.com/mcp`).
- **CI/CD Gates:** Lint + Typecheck → Unit & Concurrency Tests → OpenAPI 3.1 Lint → Secret Scan (block if any token/key detected) → Container Build → Expand-Only DB Migration → Canary Deploy (5% traffic) → Full Rollout.
- **Feature Flags:** `ENABLE_LIFESTYLE_PERSONALIZATION`, `ENABLE_FAMILY_BENEFITS`, and per-country `country_configs.is_active` allow instant kill-switch without redeployment.
- **Secrets:** Managed via cloud KMS / Secrets Manager (never `.env` files in production or git).

---

## 2. Observability, Dashboards & SLOs

- **Structured JSON Logging:** `timestamp`, `level`, `trace_id`, `captain_id` (pseudonymous UUID), `country_code`, `event_type`, `latency_ms`. Never log OAuth tokens, promo codes in plain text, or PII.
- **Core SLOs:** API `p99 < 250ms`; `TripCompleted` processing `< 2s`; Availability `99.9%`.
- **Key Dashboards & Alerts:**
  1. **Financial & Budget Guard:** Real-time `used_budget / max_allowed` per country (Alert if any account > 100% — should be mathematically impossible).
  2. **Outbox & Partner Health:** Alert if `outbox_events` unpublished age > 30s or partner API 5xx > 2%.
  3. **MCP Circuit Breaker:** Track Careem MCP latency, 401 refresh rate, and circuit-open events.

---

## 3. Backup, DR & Incident Response

- **Backup & DR:** PostgreSQL automated daily snapshots + continuous WAL archiving (**RPO ≤ 5 min, RTO ≤ 30 min**).
- **Incident Runbooks:**
  - *Budget Overrun / Calculation Bug:* Flip `ENABLE_FAMILY_BENEFITS=false`, run `reward_transactions` vs `reward_budgets` reconciliation query, issue compensating adjustments.
  - *Careem MCP Outage:* Circuit breaker opens automatically; core Captain tier/split/receipt features stay 100% online.
  - *Data Exposure:* Revoke OAuth refresh tokens, rotate signing keys, audit `audit_events`, notify Careem Security within SLA.
