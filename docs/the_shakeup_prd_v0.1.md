# The Shakeup — PRD & Technical Feature Manifest
### Version 0.1 | Living Document | Started: 2026-05-25

---

## Executive Summary

**The Shakeup** is a B2B2C yield management platform for live events — beginning with West End theatre — that converts the structural inefficiency of unsold premium inventory in the final days before curtain into a revenue-generating, satisfaction-increasing upgrade marketplace. 

It does not compete with primary ticketing (Ticketmaster, ATG, See Tickets). It operates *after* the ticket is already sold, in the underserved "last mile" window between purchase and performance.

The core mechanic is a **sealed-bid upgrade auction** triggered 7 days out, resolved by a constrained optimization solver 3 days out, with automatic ticket reissuance upon successful payment capture.

---

## Part 1: Core User Personas & Primary Workflows

### Persona A — The Theatre Patron (Consumer / "Bidder")

**Profile:**  
- Age 28–65. Regular attender (2–8 shows/year). Bought tickets 2–6 months in advance, likely in the dress circle or upper circle for a popular West End production. Feels the mild injustice of rush-ticket buyers potentially sitting better than them.
- Is familiar with hotel/airline upgrade systems and finds the concept immediately intuitive.
- Technically comfortable: uses mobile apps, online banking, digital ticketing.

**Primary Workflow:**
1. Receives branded upgrade-offer email from the theatre (white-labelled, The Shakeup powered) **7 days before** their performance.
2. Clicks through to The Shakeup web app, authenticated via a magic link tied to their booking reference.
3. Sees an interactive seat map of the theatre. Their current seat(s) are highlighted. Available upgrade zones are colour-coded by desirability and price band.
4. Places **one or more bids** — each bid is a (target zone/seat, max bid price £, willingness flags) tuple. They will only ever be moved once and only upward in desirability (or laterally if they accept freebies for moving to a more split/less central position).
5. Enters card details. Card is **pre-authorised** (not charged) at this stage.
6. Receives a confirmation email with a "bid receipt" and waits for the **3-day resolution event**.
7. At T–3 days: receives one of three outcomes —  
   - ✅ **Upgrade confirmed**: New e-ticket issued, card charged, original seat released back to theatre inventory.  
   - ⚠️ **Partial match**: Offered a secondary option (if they set one up).  
   - ❌ **No match**: Pre-authorisation released, original seat retained, no charge.

**Key Pain Points Solved:**
- Removes the psychological sting of "worse seat for more money than a day-of buyer."
- Low-friction: one email, one session, one decision — no daily monitoring required.
- No financial risk until T–3.

---

### Persona B — The Theatre/Venue Manager (B2B / "Operator")

**Profile:**  
- Box office manager, Head of Sales, or Revenue Manager at a West End production (e.g., an ATG or Nimax venue, or an independent producer). Has access to sales data. Cares about per-show revenue, occupancy optics, sponsor/ancillary revenue, and audience satisfaction scores.

**Primary Workflow:**

**Onboarding (one-time per production):**
1. Uploads historical sales data (CSV/API): seat-level, timestamped, priced. This feeds the demand forecasting model.
2. Configures the seat map for their specific theatre (or selects from a pre-built library of West End venues).
3. Defines **upgrade eligibility rules**:
   - Which sections are "upgradeable-from" (e.g., Upper Circle → Dress Circle is valid; Stalls Row A → Row B is not).
   - Blackout seats (wheelchair spaces, comp seats, press holds).
   - Whether to offer "lateral move with freebie" bundles (and what those freebies are: bar credit £, ice cream + programme, etc.).
4. Sets **inventory hold parameters**: how many seats to reserve from the upgrade pool for late walk-in sales vs. releasing to the auction.
5. Configures revenue share / per-upgrade fee with The Shakeup platform.

**Per-Show Management:**
1. Dashboard shows real-time bid volume, bid value distribution, projected upgrade revenue, and occupancy forecast.
2. At T–3, the optimization solver runs. Manager can review the proposed seating rearrangement before it executes (optional approval gate, or auto-approve).
3. Post-show: receives analytics report — revenue delta from upgrades, NPS correlation (if integrated), ancillary uplift from freebies.

---

### Persona C — The Platform Operator (Internal / The Shakeup Team)

This persona is internal but architecturally significant. They:
- Manage the venue onboarding pipeline (seat map ingestion, API credential management).
- Monitor solver job execution (T–3 batch jobs across all concurrent productions).
- Manage the financial settlement layer (Stripe Connect or equivalent).
- Tune the bid recommendation model across theatres and over time.

---

## Part 2: MVP Feature Set

> MVP scope = West End theatre only. Covers the core bid-place → optimize → reissue loop. No ML model at MVP — rule-based bid recommendations only.

---

### MVP Feature 1: Patron Bid Portal (Web App)

**Entry Point:** Magic-link email (no account creation required at MVP).

**Inputs:**
- `booking_reference` (validated against theatre's ticketing API or uploaded manifest)
- `seat_id[]` (patron's current seat(s))
- `target_zone_id` (the zone they are bidding for — not a specific seat at this stage)
- `max_bid_amount` (£, decimal, min floor price set by venue config)
- `willingness_flags`: `{ accept_split_party: bool, accept_lateral_move: bool, accept_freebie_bundle: bool }`
- `payment_method` (card pre-auth via Stripe PaymentIntent with `capture_method: manual`)

**Processing Logic:**
- Validate booking_reference is for the correct performance_id.
- Validate patron's current seat is in an "upgradeable-from" zone.
- Validate bid amount ≥ zone floor price.
- Create `bid` record with status = `PENDING`.
- Initiate Stripe PaymentIntent, store `payment_intent_id` on the bid record.
- Confirm pre-auth to patron; DO NOT capture funds.

**Outputs:**
- `bid_id` (UUID)
- Bid receipt email with summary and T–3 resolution datetime.
- Bid status: `PENDING`.

---

### MVP Feature 2: Theatre Manager Dashboard

**Inputs:**
- Historical sales CSV (seat_id, sale_datetime, sale_price, performance_id)
- Venue seat map (JSON schema: seat_id, section_id, row, number, x/y coordinates, accessibility_flag)
- Upgrade eligibility ruleset (JSON config)
- Inventory hold count per zone (integer)

**Processing Logic:**
- Parse and store historical sales data into `sales_history` table keyed by `venue_id + performance_id + seat_id`.
- Ingest seat map and build the venue graph (used by the solver).
- Validate ruleset (no circular upgrade chains, no blackout seat conflicts).

**Real-Time Dashboard Displays:**
- Total bids placed (count)
- Total bid value (£) — sum of `max_bid_amount` across `PENDING` bids
- Bid distribution by target zone (heatmap overlay on seat map)
- Occupancy forecast pre/post upgrade (bar chart)
- T–3 countdown timer

---

### MVP Feature 3: Upgrade Optimization Solver (T–3 Batch Job)

This is the architectural centrepiece of the platform.

**Trigger:** Scheduled job runs at exactly T–72h before curtain for each active `performance_id`.

**Inputs:**
- All `PENDING` bids for this `performance_id`
- Current seat occupancy map (seats already sold, seats confirmed for upgrade, seats held)
- Venue upgrade eligibility graph (directed graph: `from_zone → to_zone`)
- `seat_chain` data: sequences of adjacent single seats (from historical analysis) that when combined form a sellable pair/group

**Algorithm (MVP — rule-based, no ML):**
This is the Google OR-Tools CP-SAT / linear solver invocation:

**Objective function:** Maximise `Σ (accepted_bid_amount_i)` subject to:
1. **Capacity constraint**: No seat can be assigned to more than one patron.
2. **Upgrade direction constraint**: Patron can only move to a zone with a higher desirability score than their current zone.
3. **Party integrity constraint**: If `accept_split_party = false`, all seats in a party must move to seats in the same zone (not necessarily adjacent at MVP).
4. **Occupancy neutrality constraint**: Total occupied seats after solver ≥ total occupied seats before (no net seat losses — the theatre does not lose revenue from this operation).
5. **Inventory hold constraint**: Seats in the hold pool are unavailable to the solver.
6. **Freebie constraint**: If a patron accepted a lateral/downward move, apply the `freebie_bundle` and include that bundle's cost in the objective function (deducted from the bid value).
7. **Chain unlock constraint**: If a patron's original seat, when vacated, creates a completed adjacent pair that has a `seat_chain` probability × expected_value exceeding a configured threshold, the chain-unlock value is added to the objective as a bonus term.

**Output:**
- `upgrade_assignment[]`: list of `{ bid_id, new_seat_id, charge_amount, freebie_bundle_id | null }`
- `unmatched_bids[]`: list of bid_ids where no feasible assignment was found
- Solver run metadata: runtime_ms, objective_value, constraint_violations (should be 0)

---

### MVP Feature 4: Resolution & Ticket Reissuance

**Trigger:** Fired immediately after solver produces `upgrade_assignment[]`.

**For each matched bid:**
1. Capture Stripe PaymentIntent (`payment_intent_id`) for `charge_amount`.
2. If capture succeeds:
   - Update `seat_assignments` table: `patron_id → new_seat_id`, release `original_seat_id` back to venue inventory.
   - Call venue ticketing API (or generate a reissuance webhook payload) to void old ticket and issue new e-ticket to patron email.
   - Send patron confirmation email with new seat details, QR code, and "Your upgrade is confirmed" messaging.
   - Update bid status: `CONFIRMED`.
3. If capture fails:
   - Retry once (30s delay).
   - If still fails: cancel bid, retain original seat, notify patron.
   - Update bid status: `PAYMENT_FAILED`.

**For each unmatched bid:**
1. Cancel Stripe PaymentIntent (release pre-auth).
2. Send patron "no upgrade available" email.
3. Update bid status: `UNMATCHED`.

---

### MVP Feature 5: Static Rule-Based Bid Recommendation Engine

At MVP, bid recommendations are computed from a simple pricing model rather than a trained ML model.

**Inputs per zone:**
- `zone_desirability_score` (set by venue manager, 1–10)
- `current_occupancy_rate` for the performance (% of seats sold)
- `historical_avg_upgrade_premium` for this zone-pair (from past shows, or seeded manually by venue)
- `days_to_show` (always 7 at display time)

**Logic (rule-based formula):**
```
base_recommendation = (destination_zone_face_value - origin_zone_face_value) × occupancy_multiplier
occupancy_multiplier = 1.0 + (current_occupancy_rate - 0.6) × 1.5   # scales with demand
recommended_min = base_recommendation × 0.6
recommended_max = base_recommendation × 1.2
```

Displayed to patron as: *"Patrons in similar seats typically bid between £X and £Y for this upgrade."*

---

## Part 3: Proprietary Core Features (Competitive Moat)

These are the features that, once built, create a defensible advantage. Each requires significant data, domain expertise, or algorithmic sophistication to replicate.

---

### Proprietary Core 1: Dynamic Bid Intelligence Engine (DBIE) — ML-Powered Upgrade Pricing Model

**What it does:**  
Replaces the static rule-based recommender with a trained regression/ensemble model that produces real-time, per-patron, per-zone bid recommendations. Over time this becomes The Shakeup's most valuable proprietary asset — a living dataset of what theatre audiences actually pay to move seats.

**Why it's a moat:**  
The model only improves as more shows run through the platform. A new entrant would need years of outcome data to replicate it. The feature space is highly specific to live entertainment and not easily sourced elsewhere.

**Feature Space (input variables):**
- Show genre (musical, play, opera, ballet)
- Production age (premiere week vs. 18 months in)
- Show day of week + time (Wed matinée vs. Sat evening)
- Current occupancy rate at T–7 (%)
- Weather forecast for performance day (precipitation probability, temperature delta from seasonal norm)
- Origin zone → destination zone pair (zone-to-zone premium index)
- Historical sell-through rate of destination zone for this production
- Patron's lead time (how far in advance they originally bought)
- Whether the patron has used The Shakeup before (repeat user signal)
- Local event competition (sports fixtures, other major West End openings on same night)

**Output:**
- `recommended_bid_£` (point estimate)
- `confidence_band_low`, `confidence_band_high`
- `predicted_match_probability` (%) — i.e. "at this bid, you have an ~70% chance of being upgraded"

**Data Pipeline:**
- Outcome data (which bids won, at what price, for what zone pair) is collected post-resolution and fed back into the training pipeline.
- Model retrained weekly (or triggered by N new outcome records).
- Per-venue fine-tuning after sufficient volume (≥ 20 shows).

---

### Proprietary Core 2: Seat Chain Opportunity Scorer (SCOS)

**What it does:**  
Quantifies the hidden option value embedded in a patron's original seat. When Patron A vacates Seat 14D, if Seat 14C is also occupied by a willing bidder and Seat 14E is empty, the chain is: [13D, 14C, 14D, 14E] — potentially creating a "row of four" which historically sells at a premium in the last 72 hours.

This converts isolated seat vacancies into a combinatorial marketplace where the *vacated seat chain* has a calculable expected revenue contribution to the theatre, independent of the upgrade bid itself.

**Inputs:**
- Theatre seat adjacency graph (pre-computed at venue onboarding)
- Historical last-72h single/pair/group sell-through rates by zone and row (uploaded by venue manager)
- Current seat occupancy state for this performance
- Set of seats that would be vacated if a given set of bids were accepted

**Algorithm:**
1. For each candidate bid assignment, simulate the post-solver vacancy map.
2. For each contiguous vacant run in each row, query the `seat_chain_value_table`: `P(sell) × avg_last_72h_price × chain_length_multiplier`.
3. Sum all chain values across the vacancy map → `chain_opportunity_score`.
4. Feed `chain_opportunity_score` as a bonus term into the solver objective function (weighted by venue-configurable `chain_weight` parameter).

**Why it's a moat:**  
No existing ticketing platform models the downstream seat-chain option value when making upgrade decisions. This makes The Shakeup's optimization strictly superior to any greedy approach a theatre could run manually.

---

### Proprietary Core 3: Venue Demand Fingerprinting (VDF) — Production-Level Demand Curve Modelling

**What it does:**  
When a venue uploads historical sales data (seat-level, timestamped, priced), The Shakeup constructs a **demand curve per production** — not just aggregate occupancy, but *when* specific seat zones fill up, at what price, and with what velocity. This fingerprint drives the inventory hold strategy, telling the manager how many seats to withhold from the upgrade pool because they have a high late-sale probability.

**Inputs:**
- Historical sales records: `(performance_id, seat_id, sale_datetime, sale_price)`
- Production metadata: (show title, genre, start_date, is_touring)
- Performance metadata: (day_of_week, matinée_flag, special_event_flag)

**Processing Pipeline:**
1. **Time-to-curtain bucketing**: Classify each historical sale into one of 8 time buckets (e.g., >90 days, 60–90, 30–60, 14–30, 7–14, 3–7, 1–3, day-of).
2. **Zone sell-through matrix**: For each `zone_id × time_bucket`, compute `mean_occupancy_delta`, `sell_price_distribution`, and `velocity_coefficient`.
3. **Late-sale demand score**: For each zone, compute `P(at_least_one_sale_in_last_72h)` — the metric that directly informs inventory hold decisions.
4. **Seat-level anomaly detection**: Flag individual seats that consistently sell late (e.g., a specific aisle seat popular with mobility-limited patrons) for exclusion from the upgrade pool.

**Output:**
- `demand_fingerprint` JSON document stored per `(venue_id, production_id)`.
- Surfaced in the Manager Dashboard as: "Based on past shows, Zone B typically sells 3.2 additional seats in the final 3 days. We recommend holding 4 seats from the upgrade pool."
- Feeds the solver's `inventory_hold_count` automatically rather than relying on manager intuition.

---

### Proprietary Core 4: Cascading Upgrade Chain Resolver (CUCR)

**What it does:**  
Solves the structural complexity that arises when Patron A's upgrade into Zone B frees a Zone B seat, which then becomes a valid upgrade target for Patron B who was already in Zone C — creating a **multi-hop upgrade chain**. This is not natively supported by a simple bin-packing formulation and requires a chain-decomposition pre-processing step.

**Why it matters:**  
Without CUCR, the solver can only move patrons into *currently empty* premium seats. With CUCR, the solver can construct upgrade chains where Patron A → Seat X (was Patron B's), Patron B → Seat Y (was empty), and both pay. This materially increases both revenue and the number of patrons successfully upgraded.

**Algorithm:**
1. **Graph Construction**: Build a directed bipartite graph: left nodes = bids (patron wants to move FROM zone_i TO zone_j), right nodes = seats in each zone.
2. **Chain Detection**: Use a depth-first traversal to identify chains of length k where the "freed" seat at each hop is a valid assignment for the next bid in the chain.
3. **Chain Value Computation**: For a chain of length k, total value = `Σ bid_amounts_i`. This chain competes with individual assignments in the solver's objective.
4. **Constraint propagation**: Add chain-level constraints to the CP-SAT model — if chain C is selected, all k assignments in C must be activated together (atomic commitment).
5. **Fallback**: If a chain breaks (e.g., one patron's payment fails at capture), the entire chain is unwound and each patron retains their original seat.

**Complexity consideration:** Chain length should be capped at k ≤ 4 to maintain polynomial solve time for typical venue sizes (≤ 2,500 seats). Beyond k=4, the marginal revenue gain is negligible and the failure cascade risk increases.

---

## Open Questions / Items for Next Iteration

1. **Ticketing API integration strategy**: Will The Shakeup integrate directly with primary ticketing platforms (Spektrix, Tessitura, ATG's proprietary system) via their APIs, or will the MVP rely on a venue-uploaded seat manifest CSV + manual ticket reissuance workflow? This has major implications for MVP complexity.

2. **Payment pre-authorisation window**: Stripe card pre-auths are only guaranteed for 7 days (varies by card type/bank). Since we pre-auth at T–7 and capture at T–3, this is exactly at the edge. Do we accept the risk of pre-auth expiry, or do we push the bid window to T–5 for safety?

3. **Freebie fulfilment logistics**: Bar credits and merchandise bundles require the theatre's POS system to honour them. Is this a manual process (email voucher code) at MVP, or does it require POS integration?

4. **Regulatory / consumer rights**: In the UK, pre-authorised card charges for bids that are then captured without a second explicit confirmation may have implications under the Consumer Rights Act 2015. Legal review recommended before launch.

5. **Solver runtime budget**: For a full West End house (2,400 seats, potentially hundreds of bids), what is the acceptable wall-clock runtime for the T–3 solver job? CP-SAT with chain constraints and chain-of-chains up to k=4 may require time limits. Need to benchmark.

6. **Fringe viability**: Fringe venues often do not have reserved seating, making the upgrade mechanic inapplicable. However, "freebie bundles for moving to a less busy section" could still apply in a simplified form. Defer to Phase 2 assessment.

---

## Expansion Roadmap (Post-MVP Signal)

| Phase | Market | Key Unlock |
|-------|--------|------------|
| 1 | West End (MVP) | Core bid→optimize→reissue loop |
| 2 | UK Regional Theatres | Multi-venue solver, Spektrix/Tessitura API integrations |
| 3 | Broadway | USD pricing, US consumer protection compliance, Telecharge/TDF integration |
| 4 | Fringe | Simplified "freebie lateral move" mechanic without seat optimization |
| 5 | Concerts / Sports | General event mode; zone-only (no individual seat) bidding |
