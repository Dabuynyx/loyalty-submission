# ADR-0002: PostgreSQL Row-Level Locking & Transactional Outbox

- **Status:** Accepted
- **Decision:** Use PostgreSQL `SELECT ... FOR UPDATE` on `reward_budgets` combined with a `UNIQUE(idempotency_key)` constraint and a **Transactional Outbox** (`outbox_events` table) for all financial/reward state changes.
- **Context:** Concurrent reward claims or duplicate `TripCompleted` webhooks must never exceed `max_reward_budget_pct` or lose downstream notifications.
- **Alternatives Considered:** (1) Redis distributed locks + fire-and-forget Kafka; (2) Eventual consistency without budget locking.
- **Rationale:** Redis locks can expire mid-flight; eventual consistency risks budget overruns. PostgreSQL ACID transactions + outbox guarantee zero lost events and zero double-spends.
- **Consequences:** Slight write serialization per individual Captain's `reward_budgets` row (negligible at 1 Captain = ~15–20 trips/day).
- **Risks:** Outbox poller lag if background worker stalls (mitigated by health alerts on `unpublished` row age > 30s).
- **Revisit When:** Multi-region active-active writes are required per country (partitioned by `country_code`).
