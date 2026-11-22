-- Royalty Initial PostgreSQL Schema (Reference Migration 001)
-- Separates Royalty-owned state from Careem-owned identity/dispatch via opaque external IDs.

CREATE TABLE country_configs (
    country_code CHAR(2) PRIMARY KEY,
    currency_code CHAR(3) NOT NULL,
    default_language VARCHAR(10) NOT NULL DEFAULT 'ar',
    timezone VARCHAR(64) NOT NULL,
    max_reward_budget_pct NUMERIC(5,4) NOT NULL CHECK (max_reward_budget_pct > 0 AND max_reward_budget_pct <= 0.50),
    active_verticals JSONB NOT NULL DEFAULT '["rides"]',
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE city_configs (
    city_id VARCHAR(32) PRIMARY KEY,
    country_code CHAR(2) NOT NULL REFERENCES country_configs(country_code),
    name VARCHAR(100) NOT NULL,
    high_demand_zones JSONB NOT NULL DEFAULT '[]',
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE captain_refs (
    captain_id UUID PRIMARY KEY,
    careem_captain_ref VARCHAR(128) UNIQUE NOT NULL, -- Opaque Careem ID (never phone/email)
    country_code CHAR(2) NOT NULL REFERENCES country_configs(country_code),
    city_id VARCHAR(32) REFERENCES city_configs(city_id),
    fleet_type VARCHAR(20) NOT NULL CHECK (fleet_type IN ('FLEET', 'INDEPENDENT')),
    lifetime_trips INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE loyalty_seasons (
    season_id UUID PRIMARY KEY,
    country_code CHAR(2) NOT NULL REFERENCES country_configs(country_code),
    name VARCHAR(80) NOT NULL,
    starts_at TIMESTAMPTZ NOT NULL,
    ends_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(16) NOT NULL CHECK (status IN ('PLANNED', 'ACTIVE', 'ENDED'))
);

CREATE TABLE loyalty_tiers (
    tier_id SERIAL PRIMARY KEY,
    season_id UUID NOT NULL REFERENCES loyalty_seasons(season_id),
    fleet_type VARCHAR(20) NOT NULL,
    tier_number SMALLINT NOT NULL CHECK (tier_number BETWEEN 1 AND 6),
    name VARCHAR(40) NOT NULL,
    careem_pct NUMERIC(5,4) NOT NULL,
    driver_pct NUMERIC(5,4) NOT NULL,
    min_xp INT NOT NULL,
    min_rating NUMERIC(3,2) NOT NULL,
    max_cancel_rate NUMERIC(4,3) NOT NULL,
    UNIQUE (season_id, fleet_type, tier_number)
);

CREATE TABLE loyalty_accounts (
    account_id UUID PRIMARY KEY,
    captain_id UUID NOT NULL REFERENCES captain_refs(captain_id),
    season_id UUID NOT NULL REFERENCES loyalty_seasons(season_id),
    current_xp INT NOT NULL DEFAULT 100,
    current_tier SMALLINT NOT NULL DEFAULT 1,
    rolling_rating NUMERIC(3,2) NOT NULL DEFAULT 5.00,
    rolling_cancel_rate NUMERIC(4,3) NOT NULL DEFAULT 0.000,
    active_hours_today NUMERIC(4,2) NOT NULL DEFAULT 0.00,
    tier_shields_remaining SMALLINT NOT NULL DEFAULT 1,
    cash_settlement_overdue BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (captain_id, season_id)
);

CREATE TABLE reward_budgets (
    budget_id UUID PRIMARY KEY,
    account_id UUID NOT NULL UNIQUE REFERENCES loyalty_accounts(account_id),
    gross_fares_local NUMERIC(12,3) NOT NULL DEFAULT 0,
    uplift_paid_local NUMERIC(12,3) NOT NULL DEFAULT 0,
    direct_bonuses_local NUMERIC(12,3) NOT NULL DEFAULT 0,
    family_promo_cost_local NUMERIC(12,3) NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE progression_history (
    history_id UUID PRIMARY KEY,
    account_id UUID NOT NULL REFERENCES loyalty_accounts(account_id),
    idempotency_key VARCHAR(128) UNIQUE NOT NULL,
    source_trip_id VARCHAR(128),
    xp_delta INT NOT NULL,
    tier_before SMALLINT NOT NULL,
    tier_after SMALLINT NOT NULL,
    reason VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE partner_organizations (
    partner_id UUID PRIMARY KEY,
    country_code CHAR(2) NOT NULL REFERENCES country_configs(country_code),
    name VARCHAR(120) NOT NULL,
    category VARCHAR(40) NOT NULL, -- FUEL, FOOD, AUTO, HEALTH, EDU
    settlement_model VARCHAR(32) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE reward_catalog (
    reward_id UUID PRIMARY KEY,
    country_code CHAR(2) NOT NULL REFERENCES country_configs(country_code),
    partner_id UUID REFERENCES partner_organizations(partner_id),
    title VARCHAR(120) NOT NULL,
    funding_type VARCHAR(24) NOT NULL CHECK (funding_type IN ('CAREEM_FUNDED', 'PARTNER_FUNDED', 'HYBRID')),
    min_tier SMALLINT NOT NULL DEFAULT 1,
    direct_cost_local NUMERIC(10,3) NOT NULL DEFAULT 0,
    perceived_value_local NUMERIC(10,3) NOT NULL,
    vertical VARCHAR(24) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE reward_inventory (
    reward_id UUID PRIMARY KEY REFERENCES reward_catalog(reward_id),
    total_quota INT,
    remaining_quota INT,
    expires_at TIMESTAMPTZ
);

CREATE TABLE family_beneficiaries (
    beneficiary_id UUID PRIMARY KEY,
    captain_id UUID NOT NULL REFERENCES captain_refs(captain_id),
    careem_consumer_ref VARCHAR(128) NOT NULL,
    relationship VARCHAR(32) NOT NULL,
    verified_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (captain_id, careem_consumer_ref)
);

CREATE TABLE promotional_codes (
    promo_id UUID PRIMARY KEY,
    code VARCHAR(40) UNIQUE NOT NULL,
    captain_id UUID NOT NULL REFERENCES captain_refs(captain_id),
    bound_consumer_ref VARCHAR(128) NOT NULL,
    reward_id UUID NOT NULL REFERENCES reward_catalog(reward_id),
    amount_local NUMERIC(10,3) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ISSUED', 'REDEEMED', 'EXPIRED', 'REVOKED')),
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE reward_transactions (
    tx_id UUID PRIMARY KEY,
    account_id UUID NOT NULL REFERENCES loyalty_accounts(account_id),
    reward_id UUID REFERENCES reward_catalog(reward_id),
    idempotency_key VARCHAR(128) UNIQUE NOT NULL,
    tx_type VARCHAR(24) NOT NULL CHECK (tx_type IN ('RESERVE', 'ISSUE', 'REDEEM', 'REFUND', 'EXPIRE')),
    direct_cost_local NUMERIC(10,3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE consent_records (
    consent_id UUID PRIMARY KEY,
    captain_id UUID NOT NULL REFERENCES captain_refs(captain_id),
    purpose VARCHAR(40) NOT NULL, -- LIFESTYLE_PERSONALIZATION, FAMILY_SHARING
    granted BOOLEAN NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (captain_id, purpose)
);

CREATE TABLE captain_preferences (
    captain_id UUID PRIMARY KEY REFERENCES captain_refs(captain_id),
    preferred_categories JSONB NOT NULL DEFAULT '[]',
    preferred_shift_window VARCHAR(32),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE personalized_recommendations (
    rec_id UUID PRIMARY KEY,
    captain_id UUID NOT NULL REFERENCES captain_refs(captain_id),
    reward_id UUID NOT NULL REFERENCES reward_catalog(reward_id),
    rank_score NUMERIC(6,4) NOT NULL,
    explanation_text VARCHAR(255) NOT NULL,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE outbox_events (
    event_id UUID PRIMARY KEY,
    event_type VARCHAR(64) NOT NULL,
    aggregate_id UUID NOT NULL,
    payload JSONB NOT NULL,
    published BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE audit_events (
    audit_id UUID PRIMARY KEY,
    actor_type VARCHAR(24) NOT NULL,
    actor_id VARCHAR(128) NOT NULL,
    action VARCHAR(80) NOT NULL,
    target_id VARCHAR(128),
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_loyalty_accounts_captain ON loyalty_accounts(captain_id);
CREATE INDEX idx_outbox_unpublished ON outbox_events(published, created_at) WHERE published = FALSE;
CREATE INDEX idx_audit_actor_time ON audit_events(actor_id, created_at DESC);
