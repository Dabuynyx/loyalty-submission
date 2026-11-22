# Technical Glossary & Example Environment Configuration

## Glossary
- **Captain:** Careem driver-partner.
- **Careem MCP:** Careem's Model Context Protocol server (`https://mcp.careemapis.com/mcp`, 50 consumer tools).
- **Reward Budget Cap (`R_cap`):** Maximum % of gross fares that Careem-funded uplifts, bonuses, and family promos may consume.
- **Soft Reset:** End-of-season drop of at most 2 tiers (never to zero), bounded by the Captain Legacy floor.
- **Beit Careem:** Royalty's household-bound family benefit & promo sharing module.
- **Transactional Outbox:** DB pattern writing domain events to `outbox_events` in the same ACID transaction as state updates.

## Example Environment Configuration (`.env.example` — Non-Production Placeholders Only)

```ini
# Application
ROYALTY_ENV=development
ROYALTY_LOG_LEVEL=INFO
ROYALTY_DEFAULT_COUNTRY=JO

# Database (PostgreSQL)
DATABASE_URL=postgresql://royalty_user:CHANGE_ME_LOCAL@localhost:5432/royalty_dev

# Careem Identity & Official MCP (Public Client PKCE - No Secret)
CAREEM_IDENTITY_ISSUER=https://identity.careem.com/
CAREEM_MCP_ENDPOINT=https://mcp.careemapis.com/mcp
CAREEM_SANDBOX_MCP_URL=http://localhost:3001/mcp
CAREEM_HACKATHON_CLIENT_ID=1790a895-9cef-48b7-9a57-ec5670d50c41
CAREEM_OAUTH_REDIRECT_URI=http://localhost:8080/callback

# Security & Feature Flags
JWT_AUDIENCE=royalty-api
ENABLE_LIFESTYLE_PERSONALIZATION=true
ENABLE_FAMILY_BENEFITS=true

# AWS Bedrock (PII-Free Co-Pilot Explanations)
AWS_REGION=me-south-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
```
