"""Royalty Captain MCP Extension Server (JSON-RPC 2.0 over stdio + Python tool registry).

Bridges the gap in Careem's Consumer MCP (mcp.careemapis.com/mcp) by providing
Captain-side loyalty, split calculation, mission discovery, and family promo tools.
"""

import json
import sys
from typing import Any, Callable, Dict

from .algorithm import (
    DEFAULT_FLEET_TIERS,
    CaptainState,
    calculate_trip_split,
    calculate_trip_xp,
    issue_family_promo,
    remaining_reward_budget_jod,
    resolve_tier,
)

# In-memory demo store for hackathon/sandbox verification
DEMO_CAPTAINS: Dict[str, CaptainState] = {
    "cap_ahmad": CaptainState(
        captain_id="cap_ahmad",
        season_xp=5400,
        rating=4.84,
        cancel_rate=0.03,
        active_hours_today=5.5,
        lifetime_trips=3200,
        gross_fares_jod=1200.0,
        uplift_paid_jod=144.0,
        direct_bonuses_jod=10.0,
        family_promo_cost_jod=5.0,
        family_beneficiaries=["usr_fatima_spouse"],
    )
}


def _get_captain(captain_id: str) -> CaptainState:
    if captain_id not in DEMO_CAPTAINS:
        DEMO_CAPTAINS[captain_id] = CaptainState(captain_id=captain_id)
    return DEMO_CAPTAINS[captain_id]


def royalty_get_captain_status(captain_id: str) -> Dict[str, Any]:
    cap = _get_captain(captain_id)
    tier = resolve_tier(cap)
    next_tier = DEFAULT_FLEET_TIERS[min(tier.tier, len(DEFAULT_FLEET_TIERS) - 1)]
    return {
        "captain_id": cap.captain_id,
        "tier": tier.tier,
        "tier_name": tier.name,
        "careem_pct": tier.careem_pct,
        "driver_pct": tier.driver_pct,
        "season_xp": cap.season_xp,
        "xp_to_next_tier": max(0, next_tier.min_xp - cap.season_xp),
        "remaining_reward_budget_jod": remaining_reward_budget_jod(cap),
        "tier_shields": cap.tier_shields,
    }


def royalty_calculate_trip_split(
    captain_id: str,
    fare_jod: float,
    distance_km: float = 5.0,
    is_peak: bool = False,
    is_cashless: bool = True,
) -> Dict[str, Any]:
    cap = _get_captain(captain_id)
    split = calculate_trip_split(cap, fare_jod)
    xp = calculate_trip_xp(
        fare_jod, distance_km, cap.active_hours_today, is_peak=is_peak, is_cashless=is_cashless
    )
    return {**split, "xp_earned": xp, "fatigue_cap_reached": cap.active_hours_today >= 10.0}


def royalty_get_missions(captain_id: str) -> Dict[str, Any]:
    cap = _get_captain(captain_id)
    return {
        "captain_id": cap.captain_id,
        "missions": [
            {"id": "safe_shift", "title": "Take a 30-min break after 4h driving", "xp": 50, "guaranteed": True},
            {"id": "cashless_4", "title": "Complete 4 Careem Pay / Card rides", "xp": 100, "guaranteed": True},
            {"id": "flex_15", "title": "Weekly Flex: 15 rides (Part-time friendly)", "xp": 350, "guaranteed": True},
        ],
    }


def royalty_issue_family_promo_tool(
    captain_id: str, beneficiary_id: str, amount_jod: float, vertical: str = "QUIK"
) -> Dict[str, Any]:
    """Mutating tool (⚠️): caller must confirm with Captain before invoking."""
    cap = _get_captain(captain_id)
    return issue_family_promo(cap, beneficiary_id, amount_jod, vertical=vertical)


TOOLS: Dict[str, Callable[..., Dict[str, Any]]] = {
    "royalty_get_captain_status": royalty_get_captain_status,
    "royalty_calculate_trip_split": royalty_calculate_trip_split,
    "royalty_get_missions": royalty_get_missions,
    "royalty_issue_family_promo": royalty_issue_family_promo_tool,
}


def serve_stdio() -> None:
    """Minimal MCP-compatible JSON-RPC 2.0 stdio loop."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params") or {}

        if method == "initialize":
            res = {"protocolVersion": "2024-11-05", "serverInfo": {"name": "royalty-captain-mcp", "version": "0.1.0"}, "capabilities": {"tools": {}}}
        elif method == "tools/list":
            res = {"tools": [{"name": name, "description": fn.__doc__ or ""} for name, fn in TOOLS.items()]}
        elif method == "tools/call":
            name = params.get("name")
            args = params.get("arguments") or {}
            fn = TOOLS.get(name)
            data = fn(**args) if fn else {"error": f"Unknown tool: {name}"}
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"error": f"Unsupported method: {method}"}

        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": res}) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    serve_stdio()
