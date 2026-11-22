# 09 — Royalty Frontend Engineering Handoff

**Visual Prototype Reference:** [`docs/ui-prototype/index.html`](../../ui-prototype/index.html)  
**Target UX:** Simple, Careem-branded, 4-tab mobile experience (`Hub`, `Pass`, `For You`, `Family`) built for quick glances between rides.

---

## 1. Design Tokens & Accessibility

| Token | Value | Usage |
| :--- | :--- | :--- |
| `--green-dark` | `#007A3D` | Primary headers, active nav, Careem brand anchor |
| `--green` | `#00A859` | Primary CTA buttons, progress bar fill, active tier border |
| `--mint` | `#ECFDF5` | Success pills, current tier highlight, secondary CTA |
| `--gold` | `#F59E0B` | Tier badges (`TIER 4 · PRO`), partner-funded lifestyle accent |
| **Typography** | System Sans / Cairo (Arabic) | Minimum `12px` body, `28px` bold hero split |
| **Accessibility** | WCAG 2.1 AA | ≥ 4.5:1 text contrast, ≥ 44×44px tap targets, full Arabic **RTL** (`dir="rtl"`) mirror support |

---

## 2. Screen-to-API Mapping & State Handling

| Screen | Primary API Calls | User Actions | States Required |
| :--- | :--- | :--- | :--- |
| **1. Hub (Home)** | `GET /captains/{id}/loyalty/status` | View current split %, Safe-Shift hours, last trip receipt | Skeleton loader; **Degraded banner** if offline (shows last cached tier) |
| **2. Pass (Ladder)** | `GET /captains/{id}/loyalty/progression` | Inspect T1–T6 splits & quality gates | Empty/new-driver state shows **100 Endowed Welcome XP** |
| **3. For You (Lifestyle)** | `GET /captains/{id}/recommendations`, `PUT /captains/{id}/preferences` | Claim partner burger/fuel deal; toggle personalization opt-in | **Consent-off state** shows cold-start Safe-Shift & Flex quests |
| **4. Family (Beit Careem)** | `GET /captains/{id}/family-benefits`, `POST .../family-benefits/assign` | Select beneficiary; send `BEIT-*` code (with `Idempotency-Key`) | **409 Budget Cap state** gracefully recommends partner-funded perks |

**Analytics Events:** Emit `royalty_tab_viewed`, `royalty_offer_claimed`, `royalty_family_code_sent`, and `royalty_consent_toggled` (never include PII).
