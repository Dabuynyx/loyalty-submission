# ADR-0003: Dual-Layer MCP Architecture

- **Status:** Accepted
- **Decision:** Keep Careem's official Consumer MCP (`https://mcp.careemapis.com/mcp`) strictly for consumer/household actions (`user_info`, `get_activities`, `apply_promotion_code`, `create_grocery_cart_with_quantities`, `cart_checkout`) and isolate all Captain-side loyalty, split, and family-promo logic in Royalty's backend / Captain MCP Extension.
- **Context:** Audit of `builders.careem.com` confirmed 50 consumer tools and **0 Captain-side tools**.
- **Alternatives Considered:** Waiting for Careem to add Captain tools to public MCP; scraping or mocking Careem internal APIs.
- **Rationale:** Zero dependency on unverified Careem MCP extensions; cleanly separates consumer OAuth PKCE sessions from Captain loyalty state.
- **Consequences:** Production promo-code minting requires a Careem internal Promo Service integration (currently simulated in `src/royalty/mcp_server.py`).
- **Revisit When:** Careem publishes official Captain-domain tools on `mcp.careemapis.com/mcp`.
