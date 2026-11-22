# Royalty Software Engineering Documentation

Complete, implementation-ready engineering specification for **Royalty** (Careem Builders ’26).

## Engineering PDFs & Source Documents

| # | Document | Markdown | PDF |
| :---: | :--- | :---: | :---: |
| **01** | **Royalty Software Architecture & System Design** | [MD](engineering/architecture/01-royalty-software-architecture-system-design.md) | [PDF](engineering/architecture/01%20%E2%80%94%20Royalty%20Software%20Architecture%20%26%20System%20Design.pdf) |
| **02** | **Royalty Database Design & Data Dictionary** | [MD](engineering/database/02-royalty-database-design-data-dictionary.md) | [PDF](engineering/database/02%20%E2%80%94%20Royalty%20Database%20Design%20%26%20Data%20Dictionary.pdf) |
| **03** | **Royalty Algorithm & Reward Engine Technical Specification** | [MD](engineering/reward-engine/03-royalty-algorithm-reward-engine-technical-specification.md) | [PDF](engineering/reward-engine/03%20%E2%80%94%20Royalty%20Algorithm%20%26%20Reward%20Engine%20Technical%20Specification.pdf) |
| **04** | **Royalty MCP Integration & API Specification** | [MD](engineering/mcp-api/04-royalty-mcp-integration-api-specification.md) | [PDF](engineering/mcp-api/04%20%E2%80%94%20Royalty%20MCP%20Integration%20%26%20API%20Specification.pdf) |
| **04b** | **Careem MCP Agent Playbook — Complete Usage Guide** | [MD](engineering/mcp-api/Careem_MCP_Agent_Playbook_Guide.md) | [PDF](engineering/mcp-api/Careem_MCP_Agent_Playbook_Guide.pdf) |
| **05** | **Royalty Security, Privacy & Threat Model** | [MD](engineering/security-privacy/05-royalty-security-privacy-threat-model.md) | [PDF](engineering/security-privacy/05%20%E2%80%94%20Royalty%20Security%2C%20Privacy%20%26%20Threat%20Model.pdf) |
| **06** | **Royalty Personalization & Regional Data Architecture** | [MD](engineering/personalization/06-royalty-personalization-regional-data-architecture.md) | [PDF](engineering/personalization/06%20%E2%80%94%20Royalty%20Personalization%20%26%20Regional%20Data%20Architecture.pdf) |
| **07** | **Royalty Engineering Testing & Quality Assurance** | [MD](engineering/testing/07-royalty-engineering-testing-quality-assurance.md) | [PDF](engineering/testing/07%20%E2%80%94%20Royalty%20Engineering%20Testing%20%26%20Quality%20Assurance.pdf) |
| **08** | **Royalty Deployment, Operations & Reliability** | [MD](engineering/deployment/08-royalty-deployment-operations-reliability.md) | [PDF](engineering/deployment/08%20%E2%80%94%20Royalty%20Deployment%2C%20Operations%20%26%20Reliability.pdf) |
| **09** | **Royalty Frontend Engineering Handoff** | [MD](engineering/frontend-handoff/09-royalty-frontend-engineering-handoff.md) | [PDF](engineering/frontend-handoff/09%20%E2%80%94%20Royalty%20Frontend%20Engineering%20Handoff.pdf) |
| **10** | **Royalty Engineering Roadmap & Implementation Plan** | [MD](engineering/roadmap/10-royalty-engineering-roadmap-implementation-plan.md) | [PDF](engineering/roadmap/10%20%E2%80%94%20Royalty%20Engineering%20Roadmap%20%26%20Implementation%20Plan.pdf) |
| **11** | **Royalty Beginner-to-End Code Implementation Guide** | [MD](engineering/roadmap/11-royalty-beginner-to-end-implementation-guide.md) | [PDF](engineering/roadmap/11%20%E2%80%94%20Royalty%20Beginner-to-End%20Code%20Implementation%20Guide.pdf) |
| **12** | **Royalty Technical Intensification Blueprint (6 Core Upgrades)** | [MD](engineering/12-royalty-technical-intensification-blueprint.md) | [PDF](engineering/12%20%E2%80%94%20Royalty%20Technical%20Intensification%20Blueprint.pdf) |
| **13** | **Suggestions — Deep Research on Unexplored Opportunities** | [MD](suggestions/Suggestions.md) | [PDF](suggestions/Suggestions.pdf) |

## Machine-Readable Artifacts

- **OpenAPI 3.1 Spec:** [`docs/api/openapi.yaml`](api/openapi.yaml)
- **PostgreSQL Schema:** [`docs/schemas/database/001_initial_schema.sql`](schemas/database/001_initial_schema.sql)
- **Event Schemas:** [`docs/schemas/events/royalty-events.json`](schemas/events/royalty-events.json)
- **Mermaid Diagrams:** [`system-architecture.mmd`](diagrams/architecture/system-architecture.mmd) · [`er-diagram.mmd`](diagrams/database/er-diagram.mmd) · [`mcp-and-redemption-sequence.mmd`](diagrams/workflows/mcp-and-redemption-sequence.mmd)
- **ADRs:** [`0001`](adr/0001-modular-monolith-mvp.md) · [`0002`](adr/0002-postgresql-transactional-outbox.md) · [`0003`](adr/0003-dual-layer-mcp-architecture.md)
- **Test Catalog & Glossary:** [`test-catalog.md`](testing/test-catalog.md) · [`glossary-and-env.md`](engineering/glossary-and-env.md)
