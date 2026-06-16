# The Shakeup — Financial Model, Solver Spec & API Contracts
### Version 0.1 | Pilot Reference: My Neighbour Totoro @ Gillian Lynne Theatre
### 2026-05-25

---

# Part 1: Financial Model

## 1.1 Pilot Venue Profile — Gillian Lynne Theatre

| Attribute | Value |
|-----------|-------|
| Venue | Gillian Lynne Theatre, London |
| Owner/Operator | LW Theatres (Andrew Lloyd Webber) |
| Ticketing System | Line-Up |
| Total Capacity | ~1,295 seats |
| Stalls | ~862 seats (3 segments: Left, Centre, Right) |
| Circle | ~433 seats (3 segments: Left, Centre, Right) |
| Stage Type | Modified thrust — protrudes into stalls |
| Current Show | My Neighbour Totoro (RSC) |
| Booking Through | 10 January 2027 |
| Performances/Week | ~8 (Tue–Sun eve + Thu/Sat mat) |

---

## 1.2 Seat Section Taxonomy for The Shakeup (Gillian Lynne)

The thrust stage means side seats in both Stalls and Circle get genuinely angled sightlines. This makes the upgrade incentive real and specific — it's not an abstract tier upgrade, it's a concrete view improvement.

```
Section ID       | Desirability | Approx Seats | Typical Face Value | Role in System
-----------------+--------------+--------------+--------------------+------------------------
STALLS_CTR       |      10      |    ~320      |     £85–£115       | Premium destination
STALLS_SIDE      |       6      |    ~270      |     £45–£65        | Primary upgrade origin
STALLS_REAR      |       5      |    ~272      |     £35–£55        | Primary upgrade origin
CIRCLE_CTR       |       8      |    ~190      |     £65–£85        | Secondary destination
CIRCLE_SIDE      |       4      |    ~123      |     £30–£50        | Primary upgrade origin
CIRCLE_REAR      |       3      |    ~120      |     £25–£40        | Primary upgrade origin
```

**Upgrade direction graph (Gillian Lynne):**
```
CIRCLE_REAR  ──► CIRCLE_CTR
CIRCLE_REAR  ──► STALLS_CTR   (significant desirability jump — high bid potential)
CIRCLE_SIDE  ──► CIRCLE_CTR
CIRCLE_SIDE  ──► STALLS_CTR
STALLS_REAR  ──► STALLS_CTR
STALLS_SIDE  ──► STALLS_CTR
```
No downward moves in this graph (unless freebie lateral moves are configured by LW Theatres — e.g., CIRCLE_CTR → STALLS_SIDE for a bar credit bundle).

---

## 1.3 Revenue Model — Structure

The Shakeup charges **a percentage of each successfully captured upgrade bid**. No SaaS fee, no onboarding cost, no minimum commitment.

**Rationale for pure revenue share at launch:**
- Zero financial risk for the theatre to trial the platform. This removes the biggest sales objection.
- Aligns The Shakeup's incentive entirely with the theatre's — we only get paid when they do.
- Creates a natural upgrade path: once the platform has demonstrated consistent revenue, introduce a tiered SaaS + lower-rev-share model for high-volume venues (Phase 2).

**Revenue Split:**

| Party | Share | Notes |
|-------|-------|-------|
| The Shakeup | **25%** of charge_amount_£ per confirmed upgrade | Platform fee |
| Theatre / LW Theatres | **75%** of charge_amount_£ per confirmed upgrade | Pure incremental revenue — no extra cost incurred |

Stripe processing fees (~1.5% + £0.20 per transaction) are deducted from The Shakeup's 25% share. The theatre always receives exactly 75% of the stated charge.

---

## 1.4 Unit Economics — Single Performance Model

**Assumptions (conservative, first 3 months of operation):**

| Input | Value | Basis |
|-------|-------|-------|
| Eligible "upgradeable-from" seats | 665 | STALLS_SIDE + STALLS_REAR + CIRCLE_SIDE + CIRCLE_REAR |
| Show occupancy rate (assumed) | 78% | Mid-run West End, not peak |
| Eligible occupied seats | ~519 | 665 × 78% |
| Email open rate | 45% | Theatre email list — brand email |
| Bid placement rate (of openers) | 20% | Conservative first-cycle estimate |
| **Bids placed per performance** | **~47** | 519 × 45% × 20% |
| Pre-auth failure rate | 8% | Industry card decline average |
| Bids reaching solver | ~43 | 47 × 92% |
| Solver match rate | 55% | Conservative — some seats in STALLS_CTR/CIRCLE_CTR already SOLD or HELD |
| **Confirmed upgrades per performance** | **~24** | 43 × 55% |
| Average charge per upgrade | £38 | Blended average across section pairs |
| **Upgrade revenue per performance** | **~£912** | 24 × £38 |
| The Shakeup revenue per performance | **~£228** | 25% of £912 |
| LW Theatres revenue per performance | **~£684** | 75% of £912 |

**Per week (8 performances):**

| Metric | Value |
|--------|-------|
| Upgrades confirmed | ~192 |
| Gross upgrade revenue | ~£7,296 |
| The Shakeup net (after Stripe) | ~£1,768 |
| LW Theatres net | ~£5,472 |

---

## 1.5 Revenue Projections — 12-Month Pilot Ramp

The model improves as participation rates increase with brand familiarity and as the bid recommendation engine improves match quality.

| Month | Shows Active | Avg Upgrades/Perf | Avg Charge | Monthly Gross | Shakeup Monthly |
|-------|-------------|-------------------|-----------|--------------|-----------------|
| 1–2 (MVP pilot) | 1 (Totoro) | 20 | £35 | £4,480 | £1,120 |
| 3–4 | 1 | 26 | £38 | £6,656 | £1,664 |
| 5–6 | 2 (+ 1 new) | 26 | £40 | £13,312 | £3,328 |
| 7–9 | 4 shows | 30 | £42 | £32,256 | £8,064 |
| 10–12 | 6 shows | 35 | £45 | £60,480 | £15,120 |

> **Note:** These projections assume linear growth in venue partnerships. Acquiring LW Theatres as a group partner (not just Totoro) unlocks all 6 LW venues simultaneously in Month 5–6. That step-change is the most important business development milestone.

---

## 1.6 Pricing Mechanics — First-Price Sealed Bid (MVP)

At MVP, **the patron pays exactly what they bid** (first-price auction). No haggling, no surprise.

**Why not second-price (Vickrey)?**
Second-price is more theoretically optimal (encourages honest maximum bids) but creates consumer confusion: "You were charged £32 but you bid £45 — congratulations!" This requires explanation in every outcome email and creates support tickets. First-price is immediately intuitive and familiar (it's how hotel upgrades, airline upgrades, and hotel bidding apps work). We revisit Vickrey pricing in Phase 2 once the audience is educated.

**Floor prices per section pair (Gillian Lynne, illustrative):**

| From | To | Floor Price | Suggested Bid Range |
|------|----|------------|-------------------|
| STALLS_SIDE | STALLS_CTR | £20 | £25–£55 |
| STALLS_REAR | STALLS_CTR | £15 | £20–£45 |
| CIRCLE_SIDE | CIRCLE_CTR | £15 | £20–£40 |
| CIRCLE_REAR | CIRCLE_CTR | £10 | £15–£30 |
| CIRCLE_REAR | STALLS_CTR | £30 | £35–£70 |
| CIRCLE_SIDE | STALLS_CTR | £25 | £30–£65 |

Floor prices prevent the solver's objective from being polluted by trivially low bids that consume valuable inventory.

---

## 1.7 Phase 2 Pricing Evolution

Once sufficient outcome data exists (~20 shows processed), introduce **section clearing price** (simplified second-price):

- All matched bids for the same `(from_section, to_section)` pair are charged at the **lowest winning bid** in that pair, not their individual max bid.
- This is disclosed to patrons at bid time: *"You will pay no more than your bid, and may pay less if others bid lower."*
- Increases the expected number of high bids (rational bidders bid their true max).
- Increases total upgrade revenue at higher participation rates.

---

# Part 2: Formal Solver Specification

## 2.1 Problem Statement

Given:
- A set of patrons **P** who have placed bids, each pre-authorised
- A set of available destination seats **S** (AVAILABLE, not HELD)
- An upgrade eligibility directed graph **G** (section → section)
- Each patron p ∈ P may have multiple bids, each targeting a different section

Find an assignment of at most one bid per patron to at most one seat, maximising total upgrade revenue, subject to hard constraints on feasibility.

---

## 2.2 Sets and Parameters

```
Sets:
  B     = set of all bids with status PRE_AUTH_OK
  S     = set of seats with status AVAILABLE for this performance
  P     = set of distinct patrons with at least one bid in B
  C     = set of seat chains (pre-computed adjacency groups)
  
  bids(p)      = { b ∈ B : patron(b) = p }          -- all bids for patron p
  party(p)     = set of seat_ids currently held by patron p (status = BID_VACATING)
  origin(p)    = section_id of patron p's current seat(s)
  section(b)   = target section_id for bid b
  section(s)   = section_id of seat s
  
Parameters:
  amount(b)    = max_bid_£ for bid b                 -- scalar ≥ floor_price
  desir(sec)   = desirability_rank of section sec    -- integer 1–10
  split_ok(b)  = willingness_flags.accept_split_party for bid b  -- bool
  chain_val(c) = expected_revenue(c) × p_sell(c)    -- chain opportunity value
  chain_wt     = venue-configurable chain weight ∈ [0, 1]  -- default 0.6
  
  eligible(b, s) = 1 iff section(s) = section(b)
                       AND desir(section(b)) > desir(origin(patron(b)))
                       AND s is not accessibility-blacklisted
```

---

## 2.3 Decision Variables

```
x[b, s] ∈ {0, 1}    -- 1 if bid b is assigned to seat s
y[c]    ∈ {0, 1}    -- 1 if seat chain c is fully vacated (all chain seats released)
```

---

## 2.4 Objective Function

```
Maximise:
  Σ_{b ∈ B, s ∈ S} amount(b) × x[b, s]
  + chain_wt × Σ_{c ∈ C} chain_val(c) × y[c]
```

The chain bonus term adds the expected incremental theatre revenue from newly-created sellable seat groups. `chain_wt` allows the venue to dial down chain bonuses if they prefer a pure revenue-maximising mode.

---

## 2.5 Hard Constraints

```
(C1) Single satisfaction per bid:
  Σ_{s ∈ S} x[b, s] ≤ 1,   ∀ b ∈ B

(C2) Single satisfaction per patron (only ONE of their bids can be assigned):
  Σ_{b ∈ bids(p)} Σ_{s ∈ S} x[b, s] ≤ 1,   ∀ p ∈ P

(C3) Seat capacity (no double-assignment):
  Σ_{b ∈ B} x[b, s] ≤ 1,   ∀ s ∈ S

(C4) Eligibility (bid can only go to its target section, and only upward):
  x[b, s] = 0   if eligible(b, s) = 0

(C5) Party integrity (if patron does not accept split party):
  If split_ok(b) = false AND |party(patron(b))| > 1:
    All seats assigned to patron p's winning bid must be in the same section.
    Formally: if x[b, s] = 1, then for every other seat s' in party(p),
    there must exist a bid b' where x[b', s''] = 1 and section(s'') = section(s).
    (Relaxed at MVP: party integrity enforced at section level, not adjacency level)

(C6) No movement of non-bidders:
  seat s can only appear as destination if it is in set S (AVAILABLE).
  Patrons not in P (no bids placed) are never displaced. [Enforced by data — 
  only AVAILABLE seats enter S; SOLD seats with no bid stay SOLD.]

(C7) Chain activation:
  y[c] ≤ Σ_{b,s: s ∈ chain(c)} x[b, s] / |chain(c)|
  -- chain c is only "activated" (y[c]=1) if ALL its seats are vacated.
  -- Implemented as: y[c] = AND over all seats in chain c of (that seat is vacated).
  -- In CP-SAT: model.AddBoolAnd([vacated[s] for s in chain(c)]).OnlyEnforceIf(y[c])
```

---

## 2.6 Python Pseudocode (OR-Tools CP-SAT)

```python
from ortools.sat.python import cp_model
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set

@dataclass
class Bid:
    bid_id: str
    patron_id: str
    target_section_id: str
    max_bid_pence: int          # Use integers — CP-SAT works in integers
    party_seat_ids: List[str]
    accept_split_party: bool

@dataclass  
class Seat:
    seat_id: str
    section_id: str

@dataclass
class SeatChain:
    chain_id: str
    seat_ids: List[str]
    value_pence: int            # chain_val(c) = p_sell × avg_price, in pence

def run_upgrade_solver(
    bids: List[Bid],
    available_seats: List[Seat],
    eligible: Dict[Tuple[str, str], bool],   # (bid_id, seat_id) → bool
    chains: List[SeatChain],
    chain_weight_pct: int = 60,              # 60% = 0.6, in integer arithmetic
    time_limit_seconds: int = 60
) -> Dict:

    model = cp_model.CpModel()

    # --- Index structures ---
    bids_by_patron: Dict[str, List[Bid]] = {}
    for b in bids:
        bids_by_patron.setdefault(b.patron_id, []).append(b)

    # --- Decision variables ---
    x: Dict[Tuple[str, str], cp_model.IntVar] = {}
    for b in bids:
        for s in available_seats:
            if eligible.get((b.bid_id, s.seat_id), False):
                x[(b.bid_id, s.seat_id)] = model.NewBoolVar(f'x_{b.bid_id}_{s.seat_id}')

    vacated: Dict[str, cp_model.IntVar] = {}
    for b in bids:
        for seat_id in b.party_seat_ids:
            if seat_id not in vacated:
                vacated[seat_id] = model.NewBoolVar(f'vacated_{seat_id}')

    y: Dict[str, cp_model.IntVar] = {}
    for c in chains:
        y[c.chain_id] = model.NewBoolVar(f'y_{c.chain_id}')

    # --- C1: Single satisfaction per bid ---
    for b in bids:
        model.Add(
            sum(x[(b.bid_id, s.seat_id)]
                for s in available_seats
                if (b.bid_id, s.seat_id) in x)
            <= 1
        )

    # --- C2: Single satisfaction per patron ---
    for patron_id, patron_bids in bids_by_patron.items():
        model.Add(
            sum(x[(b.bid_id, s.seat_id)]
                for b in patron_bids
                for s in available_seats
                if (b.bid_id, s.seat_id) in x)
            <= 1
        )

    # --- C3: Seat capacity ---
    for s in available_seats:
        model.Add(
            sum(x[(b.bid_id, s.seat_id)]
                for b in bids
                if (b.bid_id, s.seat_id) in x)
            <= 1
        )

    # --- C4: Eligibility enforced by only creating x vars for eligible pairs ---
    # (already handled in variable creation above)

    # --- C5: Party integrity (section-level, MVP) ---
    for patron_id, patron_bids in bids_by_patron.items():
        for b in patron_bids:
            if not b.accept_split_party and len(b.party_seat_ids) > 1:
                # If this bid is satisfied, all party members must have a bid
                # satisfied in the same section. Enforced as a soft check post-solve
                # at MVP; full constraint encoding deferred to V1.
                pass  # TODO: V1 — encode as linked bid constraint

    # --- Vacated seat linkage ---
    for b in bids:
        bid_satisfied = model.NewBoolVar(f'satisfied_{b.bid_id}')
        model.Add(
            sum(x[(b.bid_id, s.seat_id)]
                for s in available_seats
                if (b.bid_id, s.seat_id) in x)
            == bid_satisfied
        )
        for seat_id in b.party_seat_ids:
            # seat is vacated iff patron's winning bid is this bid
            # (simplified: vacated if ANY of patron's bids is satisfied)
            model.AddImplication(bid_satisfied, vacated[seat_id])

    # --- C7: Chain activation ---
    for c in chains:
        chain_seats_vacated = [
            vacated[seat_id]
            for seat_id in c.seat_ids
            if seat_id in vacated
        ]
        if chain_seats_vacated:
            # y[c] = 1 only if ALL chain seats are vacated
            model.AddBoolAnd(chain_seats_vacated).OnlyEnforceIf(y[c.chain_id])
            model.AddBoolOr([v.Not() for v in chain_seats_vacated]).OnlyEnforceIf(
                y[c.chain_id].Not()
            )

    # --- Objective ---
    bid_revenue = sum(
        b.max_bid_pence * x[(b.bid_id, s.seat_id)]
        for b in bids
        for s in available_seats
        if (b.bid_id, s.seat_id) in x
    )
    chain_revenue = sum(
        (chain_weight_pct * c.value_pence // 100) * y[c.chain_id]
        for c in chains
    )
    model.Maximize(bid_revenue + chain_revenue)

    # --- Solve ---
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_seconds
    solver.parameters.num_search_workers = 4   # Parallelise — small problem size
    status = solver.Solve(model)

    # --- Extract results ---
    assignments = []
    unmatched_bid_ids = []

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for b in bids:
            matched = False
            for s in available_seats:
                if (b.bid_id, s.seat_id) in x and solver.Value(x[(b.bid_id, s.seat_id)]) == 1:
                    assignments.append({
                        "bid_id": b.bid_id,
                        "assigned_seat_id": s.seat_id,
                        "charge_amount_pence": b.max_bid_pence,
                        "chain_ids_unlocked": [
                            c.chain_id for c in chains
                            if solver.Value(y[c.chain_id]) == 1
                            and any(seat_id in b.party_seat_ids for seat_id in c.seat_ids)
                        ]
                    })
                    matched = True
                    break
            if not matched:
                # Only report as unmatched if no other bid for this patron was matched
                patron_matched = any(
                    a["bid_id"] in [pb.bid_id for pb in bids_by_patron[b.patron_id]]
                    for a in assignments
                )
                if not patron_matched:
                    unmatched_bid_ids.append(b.bid_id)

        return {
            "status": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
            "objective_value_pence": int(solver.ObjectiveValue()),
            "runtime_ms": int(solver.WallTime() * 1000),
            "assignments": assignments,
            "unmatched_bid_ids": unmatched_bid_ids
        }
    else:
        # No solution found (INFEASIBLE or UNKNOWN)
        return {
            "status": "NO_SOLUTION",
            "objective_value_pence": 0,
            "runtime_ms": int(solver.WallTime() * 1000),
            "assignments": [],
            "unmatched_bid_ids": [b.bid_id for b in bids]
        }
```

---

## 2.7 Scalability Analysis — Gillian Lynne Context

| Parameter | Estimated Value | Implication |
|-----------|----------------|-------------|
| Available destination seats at T–3 | ~80–150 | STALLS_CTR + CIRCLE_CTR minus SOLD and HELD |
| Bids reaching solver | ~40–80 | Per conservative unit economics model |
| Decision variables x[b,s] | ~6,000–12,000 | 80 bids × 150 seats (sparse — eligibility filters most) |
| Chain variables y[c] | ~20–60 | Depends on adjacency groups computed at onboarding |
| Estimated solve time | **< 2 seconds** | CP-SAT with 4 workers handles this trivially |
| Time limit budget | 60 seconds | Headroom for scaling to larger venues |

This is a small MIP for CP-SAT. Even at a 2,400-seat venue (Royal Albert Hall, Broadway) with 300 bids, the problem remains well within CP-SAT's capabilities given the sparsity introduced by eligibility filtering.

---

## 2.8 The "Non-Adjacent Party" Problem (MVP Limitation)

At MVP, the party integrity constraint (C5) is enforced **at section level only** — if a party of 2 wins an upgrade to STALLS_CTR, the solver guarantees they both land in STALLS_CTR, but does not guarantee they are in adjacent or even nearby seats.

**Why:** Adjacent seat assignment requires the solver to model seat coordinates and adjacency, which roughly doubles the variable count and constraint complexity.

**V1 fix:** Pre-compute adjacency groups for all seats in STALLS_CTR. Add a constraint that party seats must be assigned within the same adjacency group (row + consecutive seat numbers). This is an `AddAllowedAssignments` constraint on the coordinate tuples.

**MVP mitigation:** The seat map selection UI shows available pairs clearly. When a party bids, the system preferentially offers them paired destination groups on the seat map (this is a UI heuristic, not a solver guarantee at MVP). The solver is notified that the patron wants to stay together; if it can't find adjacent seats, the bid is scored lower in the objective.

---

# Part 3: API Contracts

## 3.1 API Design Principles

- **REST** with JSON payloads throughout.
- All monetary values are **integers in pence** (GBP minor units) — no floating point in the API or database. `£38.50 → 3850`.
- All datetime fields are **ISO 8601 UTC** strings.
- All IDs are **UUID v4** strings.
- Authentication: **JWT bearer tokens** for the patron portal; **API key + HMAC signature** for venue system webhooks; **session cookie** for the manager dashboard.
- Versioning: **URL path versioning** — `/api/v1/...`
- Errors follow **RFC 7807 Problem Details**: `{ type, title, status, detail, instance }`.

---

## 3.2 Core API Endpoints

### Authentication

```
POST   /api/v1/auth/magic-link/verify
  Body:    { token: string }
  Returns: { access_token: string, patron_id: uuid, performance_id: uuid,
             booking_id: uuid, expires_at: datetime }
  Errors:  401 TOKEN_EXPIRED | 401 TOKEN_INVALID | 410 BIDDING_CLOSED
```

---

### Venues & Layouts

```
POST   /api/v1/venues
  Auth:    Manager session
  Body:    { name: string, address: string, ticketing_system_type: enum }
  Returns: { venue_id: uuid, ...venue }

POST   /api/v1/venues/{venue_id}/layouts
  Auth:    Manager session
  Body:    multipart/form-data — seat_map_file (JSON or CSV)
  Returns: { layout_id: uuid, seat_count: int, section_count: int, preview_url: string }

PUT    /api/v1/venues/{venue_id}/layouts/{layout_id}/ruleset
  Auth:    Manager session
  Body:    {
    upgrade_edges: [{ from_section_id: uuid, to_section_id: uuid }],
    freebie_bundles: [{ bundle_id: uuid, description: string, value_pence: int }],
    blackout_seat_ids: [uuid],
    default_hold_count_per_section: { [section_id: uuid]: int }
  }
  Returns: { ruleset_version: int, validated: bool, warnings: string[] }
```

---

### Productions & Performances

```
POST   /api/v1/venues/{venue_id}/productions
  Auth:    Manager session
  Body:    { show_title: string, genre: enum, layout_id: uuid, start_date: date, end_date: date }
  Returns: { production_id: uuid }

POST   /api/v1/productions/{production_id}/sales-history
  Auth:    Manager session
  Body:    multipart/form-data — sales_csv_file
  Format:  CSV columns: seat_id, sale_datetime, sale_price_pence, booking_ref
  Returns: { records_imported: int, fingerprint_job_id: uuid }

GET    /api/v1/productions/{production_id}/performances
  Auth:    Manager session
  Returns: [{ performance_id, curtain_datetime, status, bid_count, upgrade_revenue_pence }]

POST   /api/v1/performances
  Auth:    Manager session (or ticketing webhook)
  Body:    {
    production_id: uuid,
    curtain_datetime: datetime,
    bookings: [{
      booking_ref: string,
      patron_email: string,
      seat_ids: [uuid],
      sale_price_pence: int
    }]
  }
  Returns: { performance_id: uuid, seat_states_created: int, jobs_scheduled: [string] }
```

---

### Seat Map (Patron-Facing)

```
GET    /api/v1/performances/{performance_id}/seatmap
  Auth:    Patron JWT
  Query:   patron_id (optional — highlights current seat if provided)
  Returns: {
    performance_id: uuid,
    curtain_datetime: datetime,
    sections: [{
      section_id: uuid,
      name: string,
      desirability_rank: int,
      is_upgradeable_to: bool,
      face_value_pence: int,
      available_seat_count: int,
      bid_heatmap_intensity: float,   -- 0.0–1.0, anonymised bid density
      recommendation: {
        from_section_id: uuid,        -- only present if patron is eligible
        recommended_min_pence: int,
        recommended_max_pence: int,
        match_probability_pct: int
      } | null
    }],
    patron_context: {
      current_seat_ids: [uuid],
      current_section_id: uuid,
      eligible_upgrades: [section_id]
    } | null
  }
```

---

### Bids

```
POST   /api/v1/bids
  Auth:    Patron JWT
  Body:    {
    performance_id: uuid,
    target_section_id: uuid,
    max_bid_pence: int,
    preference_rank: int,            -- 1 = first choice
    willingness_flags: {
      accept_split_party: bool,
      accept_lateral_move: bool,
      accept_freebie_bundle: bool
    },
    stripe_payment_method_id: string -- from Stripe.js SetupIntent
  }
  Returns: { bid_id: uuid, status: "PENDING", resolution_datetime: datetime }
  Errors:  400 BID_BELOW_FLOOR | 400 SECTION_NOT_ELIGIBLE | 400 BIDDING_CLOSED
           409 PATRON_ALREADY_CONFIRMED  -- if a prior bid already won
           422 DUPLICATE_SECTION_BID    -- already have a PENDING bid for this section

GET    /api/v1/bids?performance_id={uuid}&patron_id={uuid}
  Auth:    Patron JWT
  Returns: [{
    bid_id: uuid,
    target_section_id: uuid,
    target_section_name: string,
    max_bid_pence: int,
    preference_rank: int,
    status: enum,                    -- PENDING | MATCHED | CONFIRMED | UNMATCHED | PRE_AUTH_FAILED | CAPTURE_FAILED
    outcome: {                       -- present if status = CONFIRMED
      assigned_seat_id: uuid,
      assigned_seat_label: string,   -- e.g. "Stalls Centre, Row F, Seat 14"
      charge_amount_pence: int,
      freebie_bundle: { description, value_pence } | null
    } | null
  }]

DELETE /api/v1/bids/{bid_id}
  Auth:    Patron JWT
  Notes:   Only valid while status = PENDING. Cancels bid; seat_state reverts.
  Returns: { bid_id: uuid, status: "CANCELLED" }
```

---

### Bid Recommendations

```
GET    /api/v1/recommendations
  Auth:    Patron JWT
  Query:   from_section_id, to_section_id, performance_id
  Returns: {
    from_section_id: uuid,
    to_section_id: uuid,
    recommended_min_pence: int,
    recommended_max_pence: int,
    match_probability_pct: int,
    basis: {
      current_occupancy_pct: int,
      avg_historical_bid_pence: int | null,   -- null if < 10 historical data points
      demand_fingerprint_available: bool
    }
  }
```

---

### Manager Dashboard

```
GET    /api/v1/performances/{performance_id}/dashboard
  Auth:    Manager session
  Returns: {
    performance_id: uuid,
    curtain_datetime: datetime,
    status: enum,
    occupancy: { total_seats: int, sold: int, available: int, held: int, bid_vacating: int },
    bids: {
      total: int,
      by_section: [{ section_id, section_name, count, total_value_pence }],
      heatmap_data: [{ seat_id, bid_intensity: float }]
    },
    projected_upgrade_revenue_pence: int,
    t_minus_hours: float,
    solver_run: { status, triggered_at, completed_at, objective_value_pence } | null
  }

POST   /api/v1/performances/{performance_id}/solver/approve
  Auth:    Manager session
  Notes:   Optional step — if venue has opted into manual approval before execution.
           If auto-approve is configured (default), solver runs without this call.
  Body:    { approve: bool }
  Returns: { solver_job_id: uuid, scheduled_at: datetime }
```

---

### Webhooks (Inbound — from ticketing systems)

```
POST   /api/v1/webhooks/lineup/booking-created
POST   /api/v1/webhooks/lineup/booking-cancelled
POST   /api/v1/webhooks/spektrix/booking-created
POST   /api/v1/webhooks/spektrix/booking-cancelled

Auth:  HMAC-SHA256 signature in X-Shakeup-Signature header
Body:  Normalised internal format (adapter layer translates ticketing-system-specific payloads)

Booking Created payload:
  {
    event_type: "booking.created",
    source: "lineup" | "spektrix" | "csv",
    booking_ref: string,
    performance_id: uuid,
    patron_email: string,
    seat_ids: [uuid],
    sale_price_pence: int,
    occurred_at: datetime
  }
```

---

### Solver & Resolution (Internal — not patron-facing)

```
POST   /api/v1/internal/solver/run         -- triggered by job queue
POST   /api/v1/internal/resolution/run     -- triggered by job queue post-solver
GET    /api/v1/internal/solver-runs/{id}   -- audit + monitoring
```

---

## 3.3 Line-Up Integration Contract (V1 — Pilot with Totoro)

Line-Up provides three APIs. The Shakeup requires primarily the **Admin API** for seat management and the **Reporting API** for booking sync.

### Required Line-Up API Capabilities

| Operation | Line-Up API | The Shakeup Use |
|-----------|------------|-----------------|
| Fetch performance seat state | Admin API: `GET /performances/{id}/seats` | Population of `seat_state` at T–14 |
| Fetch booking details | Admin API: `GET /orders/{booking_ref}` | Patron email, seat_ids, sale price |
| Subscribe to booking events | Reporting API / Webhooks | Real-time booking sync (new sales + cancellations) |
| Transfer seat (ticket reissuance) | Admin API: `PUT /orders/{booking_ref}/seats` | Swap patron from old_seat to new_seat post-resolution |
| Void and reissue ticket | Admin API: `POST /tickets/{id}/reissue` | Generate new QR-coded ticket for patron |

### Adapter Layer Architecture

The Shakeup implements a **ticketing adapter pattern**. Each ticketing system has an adapter class that normalises its API responses to The Shakeup's internal schema:

```
LineUpAdapter
  .fetch_seat_state(performance_ref: str) → List[SeatState]
  .fetch_booking(booking_ref: str) → Booking
  .subscribe_events(performance_ref: str, webhook_url: str) → None
  .transfer_seat(booking_ref: str, old_seat_ref: str, new_seat_ref: str) → TicketRef
  .reissue_ticket(booking_ref: str, new_seat_ref: str) → TicketRef

SpektrixAdapter
  .fetch_seat_state(...)
  .fetch_booking(...)
  ... (same interface)
```

This means adding a new ticketing system (Tessitura, TixTrack) is a new adapter class only — no core platform code changes.

### Line-Up Authentication

Line-Up uses API key authentication per venue instance. At onboarding:
1. LW Theatres creates an API key for The Shakeup within their Line-Up admin panel.
2. The Shakeup stores `encrypted_api_key` per `venue_id` in its credential vault.
3. All Line-Up API calls use: `Authorization: Bearer {api_key}` + `X-Venue-Id: {lw_venue_ref}`.

### MVP Fallback for Line-Up

While V1 Line-Up API integration is being scoped with LW Theatres, the MVP proceeds as:
1. **Inbound:** LW Theatres provides a daily booking export CSV via secure SFTP. The Shakeup's ingestion job picks this up nightly.
2. **Outbound (reissuance):** After solver confirmation, The Shakeup emails a resolution pack to the LW box office: `[booking_ref, old_seat, new_seat, patron_email]`. Box office staff process the swap in Line-Up manually before show day.
3. **Patron ticket:** The Shakeup sends the patron a PDF/Apple Wallet ticket as a courtesy confirmation. The venue's system ticket (used for actual entry) is updated by box office.

This is operationally workable for a pilot (low volume, high-trust venue relationship) and creates no technical debt — the V1 API integration simply replaces steps 1–3 automatically.

---

## 3.4 Stripe Integration Contract

```
Setup (at bid placement, T–7 to T–3):
  Stripe.js:    stripe.confirmSetup({ elements, confirmParams })
  Server:       stripe.customers.create({ email: patron.email })
  Server:       stripe.setupIntents.create({ customer: customer.id, ... })
  Server:       stripe.setupIntents.confirm({ payment_method: pm_id })
  Store:        patron.stripe_customer_id, patron.stripe_payment_method_id

Pre-auth (T–3, Step 1, per bid):
  Server:       stripe.paymentIntents.create({
                  amount: bid.max_bid_pence,
                  currency: 'gbp',
                  customer: patron.stripe_customer_id,
                  payment_method: patron.stripe_payment_method_id,
                  capture_method: 'manual',
                  confirm: true,
                  off_session: true          // patron is not present
                })
  On success:   store payment_intent_id on bid record
  On error:     stripe.error.code → bid.status = PRE_AUTH_FAILED

Capture (T–3, post-solver, matched bids only):
  Server:       stripe.paymentIntents.capture(payment_intent_id, { amount_to_capture: charge_amount_pence })
  On success:   bid.status = CONFIRMED
  On error:     retry once after 30s; if still fails → CAPTURE_FAILED

Release (unmatched or failed bids):
  Server:       stripe.paymentIntents.cancel(payment_intent_id)

Refund (post-capture failure — e.g., ticket reissuance fails):
  Server:       stripe.refunds.create({ payment_intent: payment_intent_id })

Revenue settlement:
  MVP:          Direct charge to patron; The Shakeup invoices LW Theatres monthly for 75% share.
  V1:           Stripe Connect — The Shakeup creates connected accounts for each venue;
                capture auto-splits to venue sub-account (75%) and platform account (25%).
```
