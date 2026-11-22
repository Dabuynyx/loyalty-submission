# ADR-0001: Modular Monolith for MVP Architecture

- **Status:** Accepted
- **Decision:** Start Royalty as a **Modular Monolith** (single deployable Python/FastAPI or equivalent service with strict internal module boundaries: `reward_engine`, `catalog`, `family`, `personalization`, `mcp_bridge`, `regional_config`) backed by a single PostgreSQL database.
- **Context:** Initial launch targets ~200 pilot Captains in Amman before scaling across Jordan and MENA.
- **Alternatives Considered:** (1) Microservices per domain (10+ services + Kafka + service mesh); (2) Serverless functions per endpoint.
- **Rationale:** Microservices add distributed-transaction complexity, network latency, and DevOps overhead that slow down a small team. A modular monolith guarantees **ACID row-level locking** on `reward_budgets` and keeps deployment simple while allowing any module to be extracted later.
- **Consequences:** All modules share one DB transaction boundary; strict module interfaces must be enforced in code reviews.
- **Risks:** Tight coupling if developers bypass module boundaries and query each other's tables directly.
- **Revisit When:** Daily active trips in Royalty exceed 500k/day across 3+ countries or independent scaling of `personalization` vs. `reward_engine` becomes a bottleneck.
