"""Core Royalty incentive algorithm with strict percentage-budget cap enforcement."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class TierRule:
    tier: int
    name: str
    careem_pct: float
    driver_pct: float
    min_xp: int
    min_rating: float
    max_cancel_rate: float


# Default Fleet Curve: 60% Careem / 40% Driver (T1) -> 40% Careem / 60% Driver (T6)
DEFAULT_FLEET_TIERS: List[TierRule] = [
    TierRule(1, "Rookie", 0.60, 0.40, 0, 0.0, 1.00),
    TierRule(2, "Challenger", 0.56, 0.44, 1000, 4.50, 0.10),
    TierRule(3, "Contender", 0.52, 0.48, 2500, 4.60, 0.08),
    TierRule(4, "Pro", 0.48, 0.52, 5000, 4.70, 0.06),
    TierRule(5, "Elite", 0.44, 0.56, 8500, 4.80, 0.05),
    TierRule(6, "Legend", 0.40, 0.60, 13000, 4.85, 0.04),
]

# Optional Independent Car-Owner Calibration for Jordan market (~28% -> 14% Careem cut)
INDEPENDENT_JORDAN_TIERS: List[TierRule] = [
    TierRule(1, "Rookie", 0.28, 0.72, 0, 0.0, 1.00),
    TierRule(2, "Challenger", 0.25, 0.75, 1000, 4.50, 0.10),
    TierRule(3, "Contender", 0.22, 0.78, 2500, 4.60, 0.08),
    TierRule(4, "Pro", 0.19, 0.81, 5000, 4.70, 0.06),
    TierRule(5, "Elite", 0.16, 0.84, 8500, 4.80, 0.05),
    TierRule(6, "Legend", 0.14, 0.86, 13000, 4.85, 0.04),
]


@dataclass
class CaptainState:
    captain_id: str
    season_xp: int = 100  # Endowed Progress start
    rating: float = 4.85
    cancel_rate: float = 0.02
    active_hours_today: float = 0.0
    lifetime_trips: int = 0
    gross_fares_jod: float = 0.0
    uplift_paid_jod: float = 0.0
    direct_bonuses_jod: float = 0.0
    family_promo_cost_jod: float = 0.0
    tier_shields: int = 1
    cash_settlement_overdue: bool = False
    family_beneficiaries: List[str] = field(default_factory=list)


def legacy_floor_tier(lifetime_trips: int) -> int:
    """Permanent floor tier earned from lifetime trips (Captain Legacy)."""
    if lifetime_trips >= 7500:
        return 4
    if lifetime_trips >= 3000:
        return 3
    if lifetime_trips >= 1000:
        return 2
    return 1


def resolve_tier(
    captain: CaptainState, tiers: List[TierRule] = DEFAULT_FLEET_TIERS
) -> TierRule:
    """Return highest TierRule whose XP and quality gates are met (or legacy floor)."""
    if captain.cash_settlement_overdue:
        return tiers[0]

    floor = legacy_floor_tier(captain.lifetime_trips)
    eligible = tiers[0]
    for rule in tiers:
        if rule.tier <= floor:
            eligible = rule
            continue
        if (
            captain.season_xp >= rule.min_xp
            and captain.rating >= rule.min_rating
            and captain.cancel_rate <= rule.max_cancel_rate
        ):
            eligible = rule
    return eligible


def calculate_trip_xp(
    fare_jod: float,
    distance_km: float,
    active_hours_today: float,
    is_peak: bool = False,
    is_cashless: bool = False,
    max_daily_xp_hours: float = 10.0,
) -> int:
    """Compute fatigue-safe, anti-wash-trip XP for a completed ride."""
    if fare_jod < 1.50 or distance_km < 1.0:
        return 0
    if active_hours_today >= max_daily_xp_hours:
        return 0  # Fatigue-safe cap: fare still paid, XP pauses

    base = 50.0 + 10.0 * fare_jod
    mult = (1.5 if is_peak else 1.0) * (1.25 if is_cashless else 1.0)
    return int(round(base * mult))


def calculate_trip_split(
    captain: CaptainState,
    fare_jod: float,
    tiers: List[TierRule] = DEFAULT_FLEET_TIERS,
) -> Dict[str, float]:
    """Calculate deterministic Careem/Driver split and uplift vs. Tier 1 baseline."""
    if fare_jod <= 0:
        raise ValueError("fare_jod must be positive")
    tier = resolve_tier(captain, tiers)
    base_driver_pct = tiers[0].driver_pct
    driver_jod = round(fare_jod * tier.driver_pct, 3)
    careem_jod = round(fare_jod - driver_jod, 3)
    uplift_jod = round(fare_jod * (tier.driver_pct - base_driver_pct), 3)
    return {
        "tier": tier.tier,
        "tier_name": tier.name,
        "careem_pct": tier.careem_pct,
        "driver_pct": tier.driver_pct,
        "careem_jod": careem_jod,
        "driver_jod": driver_jod,
        "uplift_jod": uplift_jod,
    }


def remaining_reward_budget_jod(
    captain: CaptainState, max_reward_budget_pct: float = 0.22
) -> float:
    """Return remaining direct reward budget (JOD) allowed under the percentage cap."""
    max_allowed = captain.gross_fares_jod * max_reward_budget_pct
    used = (
        captain.uplift_paid_jod
        + captain.direct_bonuses_jod
        + captain.family_promo_cost_jod
    )
    return round(max(0.0, max_allowed - used), 3)


def issue_family_promo(
    captain: CaptainState,
    beneficiary_id: str,
    amount_jod: float,
    vertical: str = "QUIK",
    max_reward_budget_pct: float = 0.22,
    tiers: List[TierRule] = DEFAULT_FLEET_TIERS,
) -> Dict[str, object]:
    """Issue a household-bound Careem promo code if tier and budget cap permit."""
    tier = resolve_tier(captain, tiers)
    if tier.tier < 3:
        return {"ok": False, "reason": "Requires Tier 3 (Contender) or higher."}
    if beneficiary_id not in captain.family_beneficiaries:
        if len(captain.family_beneficiaries) >= 3:
            return {"ok": False, "reason": "Max 3 family beneficiaries allowed."}
        captain.family_beneficiaries.append(beneficiary_id)

    rem = remaining_reward_budget_jod(captain, max_reward_budget_pct)
    if amount_jod > rem:
        return {
            "ok": False,
            "reason": f"Exceeds reward budget cap (remaining: JOD {rem:.2f}). Use partner-funded perk instead.",
        }

    captain.family_promo_cost_jod = round(captain.family_promo_cost_jod + amount_jod, 3)
    code = f"BEIT-{captain.captain_id[:4].upper()}-{vertical[:3].upper()}-{int(amount_jod * 100)}"
    return {
        "ok": True,
        "promo_code": code,
        "bound_to_user": beneficiary_id,
        "vertical": vertical,
        "amount_jod": amount_jod,
        "remaining_budget_jod": round(rem - amount_jod, 3),
    }


def apply_season_soft_reset(
    captain: CaptainState,
    use_tier_shield: bool = False,
    tiers: List[TierRule] = DEFAULT_FLEET_TIERS,
) -> TierRule:
    """Soft-reset at season end: drop at most 2 tiers (0 if shielded), respecting Legacy floor."""
    current = resolve_tier(captain, tiers)
    floor = legacy_floor_tier(captain.lifetime_trips)
    if use_tier_shield and captain.tier_shields > 0:
        captain.tier_shields -= 1
        new_tier_num = current.tier
    else:
        new_tier_num = max(floor, current.tier - 2)

    target_rule = tiers[new_tier_num - 1]
    captain.season_xp = max(100, target_rule.min_xp)
    return target_rule
