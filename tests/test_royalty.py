"""Unit tests for Royalty incentive algorithm, budget cap, and MCP tools."""

import unittest

from src.royalty.algorithm import (
    DEFAULT_FLEET_TIERS,
    INDEPENDENT_JORDAN_TIERS,
    CaptainState,
    apply_season_soft_reset,
    calculate_trip_split,
    calculate_trip_xp,
    issue_family_promo,
    resolve_tier,
)
from src.royalty.mcp_server import royalty_get_captain_status


class TestRoyaltyAlgorithm(unittest.TestCase):
    def test_tier_progression_and_hard_60_cap(self) -> None:
        cap = CaptainState("c1", season_xp=20000, rating=4.95, cancel_rate=0.01)
        split = calculate_trip_split(cap, fare_jod=10.0)
        self.assertEqual(split["tier"], 6)
        self.assertEqual(split["driver_pct"], 0.60)
        self.assertEqual(split["careem_pct"], 0.40)
        self.assertEqual(split["driver_jod"], 6.0)

    def test_budget_cap_blocks_excess_family_promo(self) -> None:
        cap = CaptainState(
            "ahmad",
            season_xp=6000,
            gross_fares_jod=1000.0,
            uplift_paid_jod=215.0,  # 21.5% already used of 22% cap
            family_beneficiaries=["spouse_1"],
        )
        blocked = issue_family_promo(cap, "spouse_1", amount_jod=10.0)
        self.assertFalse(blocked["ok"])
        allowed = issue_family_promo(cap, "spouse_1", amount_jod=5.0)
        self.assertTrue(allowed["ok"])
        self.assertEqual(allowed["remaining_budget_jod"], 0.0)

    def test_fatigue_cap_and_wash_trip_guard(self) -> None:
        self.assertEqual(calculate_trip_xp(1.0, 0.5, active_hours_today=2.0), 0)
        self.assertEqual(calculate_trip_xp(6.0, 5.0, active_hours_today=10.0), 0)
        self.assertGreater(calculate_trip_xp(6.0, 5.0, active_hours_today=4.0, is_peak=True), 0)

    def test_soft_reset_and_independent_calibration(self) -> None:
        cap = CaptainState("vet", season_xp=14000, lifetime_trips=3500)
        new_rule = apply_season_soft_reset(cap, use_tier_shield=False)
        self.assertEqual(new_rule.tier, 4)  # T6 - 2 = T4
        ind_tier = resolve_tier(cap, INDEPENDENT_JORDAN_TIERS)
        self.assertEqual(ind_tier.driver_pct, 0.81)

    def test_mcp_status_tool(self) -> None:
        res = royalty_get_captain_status("cap_ahmad")
        self.assertEqual(res["tier_name"], "Pro")
        self.assertEqual(res["driver_pct"], 0.52)


if __name__ == "__main__":
    unittest.main()
