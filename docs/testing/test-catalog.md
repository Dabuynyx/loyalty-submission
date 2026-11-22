# Royalty Test Case Catalog

| ID | Scenario | Input / Precondition | Expected Outcome | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Duplicate `TripCompleted` event | Same `idempotency_key` sent twice | 2nd call returns cached 202; XP & budget unchanged | `progression_history` has 1 row |
| **TC-02** | Concurrent reward redemption | 2 simultaneous `POST /redeem` for last JOD 5 budget | 1 succeeds (201), 1 fails (409 Conflict) | `used_budget <= max_allowed` |
| **TC-03** | Insufficient reward budget | Remaining budget JOD 2.00; request JOD 5.00 promo | Rejected (409); suggests partner-funded perk | Budget untouched |
| **TC-04** | Invalid / expired promo code | Expired `BEIT-*` code applied via Careem MCP | Careem MCP returns structured promo error | Clear UI message, no crash |
| **TC-05** | Unauthorized family assignment | Non-owner or 4th beneficiary (> max 3) | Rejected (403 / 400) | `family_beneficiaries <= 3` |
| **TC-06** | Unsupported country | `country_code = "XX"` or `is_active = false` | Rejected (404 / 422) | No cross-country fallback |
| **TC-07** | Disabled personalization | `personalization_opt_in = false` | Generic cold-start quests only; 0 lifestyle queries | Zero `get_activities` calls |
| **TC-08** | Careem MCP timeout (mutating) | `cart_grocery_checkout` times out after 10s | **No automatic retry**; calm error + status check | Zero duplicate orders |
| **TC-09** | Careem MCP auth failure | Expired OAuth PKCE token (401) | Refresh token attempted once; else prompt re-login | No raw token logged |
| **TC-10** | Partial partner failure | Royalty reserves budget, partner API returns 503 | Compensating `REFUND` tx restores budget | `reward_budgets` reconciled |
| **TC-11** | Boundary conditions | Fare JOD 1.49 (wash guard); 10.0h active (fatigue cap) | 0 XP awarded; fare still paid | Hard cap 60% never exceeded |
| **TC-12** | Country config change | Switch `JO` `FLEET` (60/40) vs `INDEPENDENT` (28/72) | Split updates deterministically per config | Existing locked trips unchanged |
