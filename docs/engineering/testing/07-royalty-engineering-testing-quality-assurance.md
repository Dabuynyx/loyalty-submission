# 07 — Royalty Engineering Testing & Quality Assurance

**Test Catalog Reference:** [`docs/testing/test-catalog.md`](../../testing/test-catalog.md)  
**Existing Prototype Tests:** [`tests/test_royalty.py`](../../../tests/test_royalty.py) (`5/5` passing)

---

## 1. Test Pyramid & Strategy

| Layer | Scope & Tools | Mandatory Gates |
| :--- | :--- | :--- |
| **Unit Tests** | `algorithm.py` (tier resolution, 60% cap, XP fatigue cap, wash-trip guard, soft reset, budget math) | 100% pass on every commit; ≥ 95% branch coverage on `reward_engine` |
| **DB & Concurrency Tests** | PostgreSQL `SELECT ... FOR UPDATE`, `UNIQUE(idempotency_key)`, outbox atomicity | Parallel thread stress test (10 concurrent redeems → exactly 1 succeeds) |
| **API & OpenAPI Contract Tests** | Schemathesis / OpenAPI 3.1 validation against `docs/api/openapi.yaml` | Zero schema drift; `401`/`403`/`409` verified |
| **MCP Contract Tests** | Careem Local Sandbox (error injection: empty, validation error, outage) + `src/royalty/mcp_server.py` | Verify ⚠️ mutating tools **never** auto-retry on timeout |
| **Security & Privacy Tests** | OWASP API checks, cross-country IDOR, opt-out (`consent=false`) data-leakage test | Zero PII in logs; zero Careem MCP calls when opted out |
| **Localization & Accessibility** | Arabic RTL / English LTR layout + WCAG 2.1 AA contrast & screen-reader labels | No clipped Arabic text; touch targets ≥ 44×44px |

---

## 2. Critical Test Scenarios Summary (Full Matrix in `test-catalog.md`)

- **TC-01 Duplicate `TripCompleted`:** Same `idempotency_key` → 1 `progression_history` row, zero double XP.
- **TC-02 Concurrent Redemption:** 2 simultaneous requests for last JOD 5 → 1× `201`, 1× `409 Conflict`.
- **TC-03 / TC-04 / TC-05:** Insufficient budget, expired `BEIT-*` code, and >3 family beneficiaries all fail closed cleanly.
- **TC-08 / TC-09 MCP Failures:** Timeout on `cart_grocery_checkout` ⚠️ never retries; expired OAuth token triggers single refresh then re-auth prompt.
- **TC-10 Partial Partner Failure:** Partner 503 triggers compensating `REFUND` transaction restoring `reward_budgets`.
