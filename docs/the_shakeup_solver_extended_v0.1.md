# The Shakeup — Extended Solver Specification
### Party Integrity, Party Assembly & Venue Inventory Shaping (Tetris)
### Version 0.2 | 2026-05-27

> **Changes from v0.1:** Unified AllDifferent formulation replaces CUCR pre-processing;
> chains emerge naturally from constraint propagation. Section 0 added. Sections 2, 3, 5,
> and 7 updated accordingly.

---

## Overview of Three New Constraint Layers

The original solver treated seats as independent scalar quantities — bid b gets seat s.
Reality is 2-dimensional: seats have physical positions, parties have group sizes, and
the residual inventory after upgrades has commercial value that must be preserved.

```
Layer 1: Party Integrity   — patrons who booked together must sit together
Layer 2: Party Assembly    — separately-booked patrons can opt into shared seating
Layer 3: Inventory Shaping — venue controls the residual configuration post-upgrade
                             (the "Tetris" problem)
```

These three layers interact. They share a common foundation: the seat map must be
modelled as a **spatial graph** with adjacency data, and the solver's assignment
variables must operate on **seat blocks** (contiguous sets of seats), not individual seats.

---

## 0. Architectural Foundation: The Unified AllDifferent Formulation

### 0.1 Key Insight — Model All Patrons, Not Just Bidders

The previous architecture used a two-phase approach: a **CUCR** (Cascading Upgrade Chain
Resolver) pre-processed the bid graph via DFS to discover upgrade chains, then injected
chain constraints into the CP-SAT solver. This imposed an artificial chain-length cap
(k ≤ 4), required complex DFS traversal logic, and was a source of subtle bugs.

The new architecture eliminates CUCR entirely by modelling **every seated patron** as a
CP-SAT variable — not just the patrons who submitted bids. This enables a single
`AddAllDifferent` constraint to simultaneously enforce no-double-booking AND discover
arbitrarily long upgrade chains.

### 0.2 Variable Domains

Every patron who holds a seat in the performance is assigned a CP-SAT variable:

- **Non-bidding patrons:** Domain is pinned to `{current_seat}` only. They are not
  moving. CP-SAT's pre-solver eliminates these fixed-domain variables in microseconds
  during preprocessing — a 1,000-seat venue with 50 bidders has ~950 trivially
  propagated variables, leaving an effective search space of ~50 variables.

- **Bidding patrons (party_size = 1):** Domain = `{current_seat} ∪ {eligible target
  seats}`. If the solver assigns them to a target seat, they have moved (upgrade
  accepted). If it assigns them to their current seat, they stay put (bid not accepted).

- **Bidding patrons (party_size > 1):** Domain is expressed at the **block level**.
  Each party member's domain = `{current_seat} ∪ {seats in eligible target blocks}`,
  with intra-party linking constraints ensuring the party moves as a unit to a
  contiguous block (see Section 2 — Party Integrity). The `AllDifferent` constraint
  operates at the individual seat level, ensuring no two patrons (from any party) are
  assigned to the same physical seat.

### 0.3 How AllDifferent Enables Chain Discovery

`AddAllDifferent` enforces that every patron's assigned seat is unique. This single
constraint achieves two things simultaneously:

1. **No double-booking:** Two patrons cannot occupy the same seat.
2. **Chain emergence:** When Patron A moves from seat X to seat Y, seat X becomes
   available. If Patron B's domain includes seat X, the solver can assign B → X.
   If Patron C's domain includes B's vacated seat, the chain extends further.
   Chains of arbitrary length emerge naturally — no DFS, no chain detection, no k ≤ 4
   cap.

**Example:** A 3-link chain emerges without any explicit chain logic:
```
Patron C (Circle Side, Row A-5)  →  moves to Circle Centre, Row B-12
Patron B (Stalls Side, Row D-3)  →  moves to Circle Side, Row A-5 (C's vacated seat)
Patron A (Stalls Rear, Row H-8)  →  moves to Stalls Side, Row D-3 (B's vacated seat)
```
All three moves are discovered simultaneously by the AllDifferent solver.

### 0.4 Revenue Maximisation Objective

The solver's **primary objective** is to maximise total upgrade revenue — the sum of
accepted bid amounts:

```
Maximise  Σ (bid_amount_pence × party_size × moved[p])  for all bidding patrons p
```

Where `moved[p]` is 1 iff patron p is assigned to a seat other than their current seat.

Inventory shaping (SCOS) contributes a **secondary weighted bonus term** to the
objective, rewarding configurations that leave commercially valuable residual seat
blocks (see Section 4). The bonus weight is tuned so that revenue always dominates
unless two solutions have near-identical revenue.

### 0.5 Unified Formulation — Pseudocode

```python
from ortools.sat.python import cp_model

def build_unified_model(
    all_patrons:       List[Patron],       # every seated patron
    bids:              List[Bid],           # submitted bids (subset of patrons)
    seat_map:          Dict[str, Seat],     # all seats in venue
    blocks:            Dict[str, Dict[int, List[FrozenSet[str]]]],  # pre-computed
    inventory_targets: Dict[str, Dict[int, int]],
) -> cp_model.CpModel:

    model = cp_model.CpModel()
    bidder_ids = {b.patron_id for b in bids}

    # ── Per-patron seat assignment variable ────────────────────────────────
    seat_to_idx = {s: i for i, s in enumerate(seat_map.keys())}
    assign = {}  # patron_id → IntVar (seat index)

    for patron in all_patrons:
        current_idx = seat_to_idx[patron.current_seat_id]

        if patron.patron_id not in bidder_ids:
            # Non-bidder: domain pinned to current seat
            assign[patron.patron_id] = model.NewConstant(current_idx)
        else:
            bid = bids_by_patron[patron.patron_id]
            eligible_idxs = [current_idx]  # can always stay
            for blk in blocks[bid.target_section].get(bid.party_size, []):
                eligible_idxs.extend(seat_to_idx[s] for s in blk)
            eligible_idxs = list(set(eligible_idxs))
            assign[patron.patron_id] = model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(eligible_idxs),
                f"assign_{patron.patron_id}"
            )

    # ── AllDifferent — the core constraint ─────────────────────────────────
    model.AddAllDifferent(list(assign.values()))

    # ── Party integrity — block linking (see Section 2) ────────────────────
    # ... block variables y[bid][block] link party members to move as a unit

    # ── moved[p] indicator ─────────────────────────────────────────────────
    moved = {}
    for bid in bids:
        current_idx = seat_to_idx[bid.patron.current_seat_id]
        moved[bid.bid_id] = model.NewBoolVar(f"moved_{bid.bid_id}")
        model.Add(assign[bid.patron_id] != current_idx).OnlyEnforceIf(moved[bid.bid_id])
        model.Add(assign[bid.patron_id] == current_idx).OnlyEnforceIf(moved[bid.bid_id].Not())

    # ── Objective: maximise revenue + shaping bonus ────────────────────────
    revenue_terms = []
    for bid in bids:
        bid_revenue = bid.amount_pence * bid.party_size
        revenue_terms.append(bid_revenue * moved[bid.bid_id])

    shaping_bonus_terms = []  # populated by Section 4 (inventory shaping)
    # ... intact[] variables and bonus terms added here ...

    model.Maximize(sum(revenue_terms) + sum(shaping_bonus_terms))

    return model, assign, moved
```

### 0.6 Why CUCR Is Eliminated

| Aspect | Old (CUCR + CP-SAT) | New (Unified AllDifferent) |
|--------|--------------------|--------------------------|
| Chain discovery | DFS traversal, explicit chain objects | Emergent from AllDifferent |
| Chain length limit | Capped at k ≤ 4 | Unlimited — any length |
| Pre-processing step | Required before solver | Eliminated |
| Code complexity | ~500 lines of DFS/chain logic | 0 — AllDifferent is one line |
| Correctness | Manual chain validation | Provably correct by construction |
| Performance | DFS O(V+E) + solver | Solver only (pre-solver handles pinned vars) |

CP-SAT's `AddAllDifferent` is one of its most optimised global constraints, implemented
with arc-consistency propagation and domain-wiping. It outperforms hand-rolled chain
logic in both correctness and speed.

---

## 1. Foundational Change: Seat Map as a Spatial Graph

### 1.1 Extended Seat Data Model

The seat map previously stored: `{seat_id, section, row, number, desirability_score}`

It now requires: `{seat_id, section, row, number, x, y, adjacent_seat_ids, row_position}`

```python
@dataclass
class Seat:
    seat_id:           str
    section:           str         # e.g. "STALLS_CTR"
    row:               str         # e.g. "F"
    number:            int         # seat number within row
    x:                 float       # physical x coordinate (for rendering)
    y:                 float       # physical y coordinate (for rendering)
    adjacent_seat_ids: List[str]   # [left_neighbour, right_neighbour]
                                   # pre-computed at seat map upload time
    row_position:      int         # index within row (left=0, right=n)
    desirability_score: int        # 1–10; used in objective weighting
    is_accessible:     bool        # accessibility seat — excluded from upgrade pool
    is_aisle:          bool        # aisle seat — important for party block formation
```

**Adjacency rules:**
- Two seats are adjacent iff they share the same row AND their seat numbers differ by 1
- Exception: some theatre rows have gaps (e.g., missing seat 13 for superstition, or aisle gaps). These must be encoded during seat map upload.
- Cross-row adjacency is NOT used for party blocks — parties must sit in the same row.
  (Exception: a special `row_pair` mode for venues with 2-seat rows like box seating — MVP ignores this.)

### 1.2 Block Pre-Computation

Before the solver runs, pre-compute all valid contiguous seat blocks of each size
within each section, considering only AVAILABLE seats.

```python
from itertools import combinations
from collections import defaultdict
from typing import Dict, FrozenSet, List

def compute_available_blocks(
    section_seats: Dict[str, List[Seat]],   # section_id → list of Seat
    available_seat_ids: set,                 # seats with state AVAILABLE
    max_party_size: int = 6,
) -> Dict[str, Dict[int, List[FrozenSet[str]]]]:
    """
    Returns: blocks[section_id][size] = list of frozensets of seat_ids
    Each frozenset represents one valid contiguous block of that size.
    """
    blocks = defaultdict(lambda: defaultdict(list))

    for section_id, seats in section_seats.items():
        # Filter to available seats only
        avail = [s for s in seats if s.seat_id in available_seat_ids]

        # Group by row
        rows = defaultdict(list)
        for seat in avail:
            rows[seat.row].append(seat)

        # Within each row, find all contiguous runs
        for row_id, row_seats in rows.items():
            # Sort by seat number
            row_seats.sort(key=lambda s: s.number)

            # Build runs of consecutively numbered available seats
            runs = []
            current_run = [row_seats[0]]
            for seat in row_seats[1:]:
                prev = current_run[-1]
                if seat.seat_id in prev.adjacent_seat_ids:
                    current_run.append(seat)
                else:
                    runs.append(current_run)
                    current_run = [seat]
            runs.append(current_run)

            # Extract all contiguous sub-runs of length 1..max_party_size
            for run in runs:
                for size in range(1, min(max_party_size, len(run)) + 1):
                    for start in range(len(run) - size + 1):
                        block = frozenset(s.seat_id for s in run[start:start+size])
                        blocks[section_id][size].append(block)

    return blocks
```

**Performance note:** For a 1,300-seat venue with 400 available seats:
- Size-1 blocks: ~400
- Size-2 blocks: ~350 (most adjacent pairs)
- Size-3 blocks: ~280
- Size-4 blocks: ~210
- Total blocks across all sizes: ~1,500

This pre-computation runs in O(n) and takes <50ms. It is cached per `solver_run_id`.

---

## 2. Layer 1: Party Integrity (Keep Together)

### 2.1 Problem Statement

A booking of N seats must be upgraded atomically: all N seats move together to
N adjacent seats in the destination section. Partial upgrades are not permitted.

**Example:**
- Booking REF-001: 4 seats in Stalls Side, Row C, 14–17 (party of 4)
- Bid: Stalls Centre, max £12/person = £48 total
- Valid upgrade: assign seats F7, F8, F9, F10 (contiguous block of 4 in Stalls Centre)
- Invalid upgrade: assign F7, F9, G3, G4 (non-contiguous; party separated)

### 2.2 Integration with the Unified AllDifferent Formulation

Party integrity builds on top of the AllDifferent foundation (Section 0). The per-patron
`assign[patron_id]` variables from the unified formulation handle individual seat
assignment and chain emergence. For parties (party_size > 1), we add **block selection
variables** that link party members together:

```python
# From Section 0 (unified formulation):
# assign[patron_id] ∈ Domain  — per-patron seat assignment (AllDifferent enforced)
# moved[bid_id] ∈ {0,1}       — 1 iff patron moved from current seat

# Additional variables for party integrity:
# y[bid_id][block_idx] ∈ {0,1} — bid b assigned to contiguous seat block B
#   where block_idx indexes into pre-computed blocks for the bid's target section
#   and block size = bid.party_size
#
# When y[bid][block] = 1, each member of the party is constrained to occupy
# one seat from that block. The AllDifferent constraint on assign[] ensures
# no seat in the block is double-booked with any other patron.

# Derived variable (seat occupancy):
# z[seat_id] ∈ {0,1} — seat s is used by any upgrade assignment
#   z[s] = OR over all (bid, block) where s ∈ block and y[bid][block] = 1
#   Used by inventory shaping (Section 4) to track residual availability
```

### 2.3 Extended Constraint Set (Integrated with AllDifferent)

```python
from ortools.sat.python import cp_model

def build_party_integrity_layer(
    model:       cp_model.CpModel,
    assign:      Dict[str, IntVar],         # from unified formulation (Section 0)
    moved:       Dict[str, BoolVar],         # from unified formulation (Section 0)
    bids:        List[Bid],
    blocks:      Dict[str, Dict[int, List[FrozenSet[str]]]],   # pre-computed
    seat_to_idx: Dict[str, int],
    patrons:     Dict[str, List[str]],       # patron_id → list of bid_ids
    inventory_targets: Dict[str, Dict[int, int]],  # section → {size: min_count}
) -> Tuple[Dict, Dict]:
    """
    Adds party integrity constraints on top of the unified AllDifferent model.
    Returns block variables y and seat occupancy variables z.
    
    NOTE: The AllDifferent constraint on assign[] (Section 0) handles
    no-double-booking globally. This layer adds block-linking constraints
    to ensure parties move as a unit to contiguous seats.
    """

    # ── Block selection variables ──────────────────────────────────────────────

    # y[bid_id][block_idx] — bid b wins block B
    y = {}
    for bid in bids:
        eligible_blocks = blocks[bid.target_section].get(bid.party_size, [])
        y[bid.bid_id] = [
            model.NewBoolVar(f"y_{bid.bid_id}_{i}")
            for i, _ in enumerate(eligible_blocks)
        ]

    # z[seat_id] — seat s is consumed by an upgrade
    all_involved_seats = set()
    for bid in bids:
        for blk in blocks[bid.target_section].get(bid.party_size, []):
            all_involved_seats |= blk
    z = {s: model.NewBoolVar(f"z_{s}") for s in all_involved_seats}

    # ── Constraints ────────────────────────────────────────────────────────────

    # C1: Each bid wins at most one block
    for bid in bids:
        model.Add(sum(y[bid.bid_id]) <= 1)

    # C2: Each seat consumed by at most one upgrade
    #     (This is also enforced by AllDifferent on assign[], but the explicit
    #      constraint on z[] helps propagation and is needed for inventory shaping)
    for seat_id in all_involved_seats:
        consuming_vars = []
        for bid in bids:
            eligible_blocks = blocks[bid.target_section].get(bid.party_size, [])
            for i, blk in enumerate(eligible_blocks):
                if seat_id in blk:
                    consuming_vars.append(y[bid.bid_id][i])
        model.Add(sum(consuming_vars) <= 1)

    # C3: Link z[seat] to y[bid][block] assignments
    for seat_id in all_involved_seats:
        consuming_vars = []
        for bid in bids:
            eligible_blocks = blocks[bid.target_section].get(bid.party_size, [])
            for i, blk in enumerate(eligible_blocks):
                if seat_id in blk:
                    consuming_vars.append(y[bid.bid_id][i])
        # z[s] = 1 iff any consuming var is 1
        model.AddMaxEquality(z[seat_id], consuming_vars if consuming_vars else [model.NewConstant(0)])

    # C4: Link block variables to per-patron assign[] variables
    #     When y[bid][block] = 1, each party member's assign[] must be a seat in that block
    for bid in bids:
        if bid.party_size > 1:
            eligible_blocks = blocks[bid.target_section].get(bid.party_size, [])
            for i, blk in enumerate(eligible_blocks):
                block_seat_idxs = [seat_to_idx[s] for s in blk]
                for member_id in bid.party_member_ids:
                    # If this block is selected, member must be in one of its seats
                    model.AddLinearExpressionInDomain(
                        assign[member_id],
                        cp_model.Domain.FromValues(block_seat_idxs)
                    ).OnlyEnforceIf(y[bid.bid_id][i])

    # C5: Each patron's bookings: at most one bid satisfied
    for patron_id, bid_ids in patrons.items():
        patron_bids = [b for b in bids if b.bid_id in bid_ids]
        satisfied = [sum(y[b.bid_id]) for b in patron_bids]
        model.Add(sum(satisfied) <= 1)

    # C6: Inventory shaping — Layer 3 (see Section 4 below)
    # ... (added below)

    # ── Objective ──────────────────────────────────────────────────────────────
    # PRIMARY: Maximise total upgrade revenue
    # Revenue for bid b = bid.amount_pence × bid.party_size (total booking revenue)
    # moved[bid_id] comes from the unified formulation (Section 0)
    revenue_terms = []
    for bid in bids:
        bid_revenue = bid.amount_pence * bid.party_size
        revenue_terms.append(bid_revenue * moved[bid.bid_id])

    # SECONDARY: Inventory shaping bonus (added in Section 4)
    shaping_bonus_terms = []  # populated by add_inventory_shaping()

    model.Maximize(sum(revenue_terms) + sum(shaping_bonus_terms))

    return y, z
```

> **Note on AllDifferent interaction:** Constraint C2 (seat consumed at most once) is
> technically redundant with the global `AllDifferent` on `assign[]`, but serves two
> purposes: (1) it aids CP-SAT's constraint propagation by providing a local view, and
> (2) the `z[seat]` variables are required by the inventory shaping layer (Section 4)
> to determine which seats remain intact.

### 2.4 Impact on UX

The patron bid entry screen already has "keep us together" as a flag. This now has
a concrete solver effect: if `keep_together = True`, the solver only assigns the bid
to a contiguous block. If `keep_together = False` (or the patron ticks "happy to sit
nearby but not adjacent"), the solver can assign the booking to non-adjacent seats
across the section — represented as N separate size-1 block assignments linked to
the same booking.

**Implementation note:** Non-adjacent party placement (when patron opts in) requires
N individual assignments to be solved simultaneously with a shared constraint that
they cannot be re-distributed to OTHER patrons. This is handled by the C4 constraint
(only one bid satisfied per patron) — the single bid covers all N seats.

---

## 3. Layer 2: Party Assembly (Bring People Together)

### 3.1 Problem Statement

Patrons who booked separately (different booking references, potentially different
sections) want to sit together after upgrade. The solver must treat their linked bids
as a single super-party with a combined seat block requirement.

**Example:**
- Booking A: 2 seats in Stalls Side (Sarah + James)
- Booking B: 2 seats in Circle Side (Tom + Maria) — booked separately
- All four want to sit together after the upgrade
- Solver should find a block of 4 adjacent Stalls Centre seats and assign them all,
  capturing bids from both bookings

### 3.2 Patron-Facing Mechanism

A "Link with a friend" feature in the bid portal:

```
── Party assembly (optional) ──────────────────────────
 
 Want to sit with friends who have a separate booking?
 
 Enter their booking reference:  [BK-2847401  ] [Link]
 
 Linked party:
   ✓ James & Sarah (Booking BK-2847401)
     2 seats · Stalls Side
     Their bid: up to £X per person [set by them]
 
 Combined group: 4 seats
 You will all be assigned together or not at all.
 ─────────────────────────────────────────────────────
```

**Data model addition:**
```python
@dataclass  
class BidGroup:
    group_id:         str
    booking_refs:     List[str]      # bookings in this group
    total_party_size: int            # sum of all parties
    target_section:   str            # must be same for all linked bids
    min_bid_pence:    int            # minimum bid in the group (solver uses this as floor)
    # Each individual bid still has its own amount — solver revenue = sum of all bids in group
```

**Solver extension:**
BidGroups are resolved before the main solver runs. Each BidGroup is converted to a single
synthetic bid:

```python
def flatten_bid_groups(bids: List[Bid], groups: List[BidGroup]) -> List[Bid]:
    """Merge grouped bids into synthetic combined bids."""
    flat_bids = []
    grouped_bid_ids = {b for g in groups for ref in g.booking_refs for b in bids_by_booking[ref]}

    # Ungrouped bids pass through unchanged
    for bid in bids:
        if bid.bid_id not in grouped_bid_ids:
            flat_bids.append(bid)

    # Grouped bids become a single synthetic bid
    for group in groups:
        component_bids = [b for b in bids if b.booking_ref in group.booking_refs]
        synthetic = Bid(
            bid_id=f"GROUP_{group.group_id}",
            party_size=group.total_party_size,
            target_section=group.target_section,
            amount_pence=sum(b.amount_pence for b in component_bids),  # total revenue
            booking_refs=group.booking_refs,       # all constituent bookings
            is_synthetic_group=True,
        )
        flat_bids.append(synthetic)

    return flat_bids
```

The solver then handles the synthetic bid exactly like any other bid — it needs a contiguous
block of `total_party_size` seats. The origin seats to be vacated are the union of all
component bookings' current seats.

### 3.3 Complexity Note

Party assembly adds an interesting chain consideration: if Bookings A and B are linked
and both currently sit in different sections, the vacated origin seats are in two different
sections. This creates multi-origin vacancies.

The unified AllDifferent formulation handles this naturally. When the synthetic group bid
is accepted, all constituent patrons vacate their original seats. Because every patron
(including those in other sections) has an `assign[]` variable in the AllDifferent
constraint, those vacated seats immediately become available domains for other bidders.
No special multi-origin logic is needed — the AllDifferent propagator discovers these
opportunities automatically during constraint propagation.

---

## 4. Layer 3: Venue Inventory Shaping (The Tetris Problem)

### 4.1 Problem Statement

After the solver assigns upgrades, the remaining AVAILABLE seats in each section have
a commercial value to the venue — some configurations are easier to sell than others:

- A pair of adjacent seats sells quickly to couples/friends
- A block of 4 adjacent seats sells to families
- An isolated single surrounded by CONFIRMED seats is hardest to sell
- A single at an aisle position is easier than a single in the middle of a row

The venue manager knows from historical data roughly how many seats of each configuration
they expect to sell in the last 72 hours. The solver should respect this when choosing
WHICH seats to use for upgrades — preferring configurations that leave commercially
useful residual inventory.

### 4.2 Manager Input: Expected Day-Of Demand

In the venue ruleset configuration (Tab B, already partially designed):

```
Expected day-of sales (seats you expect to sell after T-3):

Section          Singles  Pairs  3-groups  4-groups  5+
──────────────────────────────────────────────────────
Stalls Centre:      2       6        1         1       0
Circle Centre:      1       3        0         0       0
Stalls Side:        3       2        0         0       0

[ ℹ️  Based on your last 12 shows, we pre-populate these.
  Adjust if this week is different (school holiday, etc.) ]

[ Save targets ]
```

This input defines `inventory_targets[section][size] = min_blocks_required`.

### 4.3 Residual Block Constraint

After all upgrade assignments, the remaining (unassigned) available seats in each section
must contain at least `inventory_targets[s][k]` valid contiguous blocks of size k.

**Mathematical formulation:**

Let `B_sk` = set of all pre-computed blocks of size k in section s.
Let `intact[block]` = 1 iff no seat in `block` is used by any upgrade.

```python
# intact[B] = 1 iff no upgrade assignment touches any seat in B
# intact[B] = product of (1 - z[seat]) for all seats in B
# In CP-SAT: intact[B] = 1 iff sum(z[s] for s in B) == 0

intact = {}
for section_id, size_map in blocks.items():
    for size, block_list in size_map.items():
        # Only track sizes that have inventory targets
        if inventory_targets.get(section_id, {}).get(size, 0) == 0:
            continue
        for i, blk in enumerate(block_list):
            var = model.NewBoolVar(f"intact_{section_id}_{size}_{i}")
            # intact = 1 iff ALL seats in blk are unoccupied (z[s] = 0)
            model.AddBoolAnd([z[s].Not() for s in blk if s in z]).OnlyEnforceIf(var)
            model.AddBoolOr([z[s] for s in blk if s in z]).OnlyEnforceIf(var.Not())
            intact[(section_id, size, i)] = var

# Inventory shaping constraint: require minimum intact blocks per section/size
for section_id, size_targets in inventory_targets.items():
    for size, min_blocks in size_targets.items():
        relevant_intact = [
            intact[(section_id, size, i)]
            for i in range(len(blocks[section_id].get(size, [])))
            if (section_id, size, i) in intact
        ]
        if relevant_intact:
            model.Add(sum(relevant_intact) >= min_blocks)
```

### 4.4 Objective Function Extension

Pure revenue maximisation can conflict with inventory shaping: the solver might want to
use a pair of seats for an upgrade, but the venue needs that pair to remain intact for
a day-of sale.

The inventory shaping constraints (C5) make this a hard constraint — the solver must
satisfy them. But we can also add a soft objective term that rewards leaving EXTRA
intact blocks beyond the minimum:

```python
# Soft reward for over-delivering on intact inventory
shaping_bonus_terms = []
shaping_weight = 50  # pence — tune this; determines how aggressively solver protects inventory

for (section_id, size, i), intact_var in intact.items():
    # Bonus is proportional to block size (pairs worth more than singles)
    bonus = shaping_weight * size
    shaping_bonus_terms.append(bonus * intact_var)

# Combined objective: revenue + inventory shaping bonus
model.Maximize(sum(objective_terms) + sum(shaping_bonus_terms))
```

**Tuning `shaping_weight`:**
- Too low: solver ignores residual inventory, maximises upgrade revenue at the expense of day-of sales
- Too high: solver refuses to use premium seats for upgrades because it wants to preserve pairs
- The right value: approximately (expected day-of revenue per seat) × (probability of selling) 
  For Stalls Centre at £25/day seat with 60% sell-through: 2500p × 0.6 = 1500p per seat
  For a pair: 3000p — so `shaping_weight ≈ 1500` (pence per seat preserved)

This is a venue-configurable parameter per section, seeded by the VDF demand model and editable
in the manager dashboard.

### 4.5 Staged Evolution: Poisson Dynamic Reserve Pricing (V1/V2)

To move beyond the static, manual targets of V0 (where venue managers manually hardcode intact group targets from 1 to 6), the V1/V2 system introduces a probabilistic dynamic reserve pricing mechanism based on separate **Poisson demand distributions per group size**.

Instead of treating inventory targets as a hard constraint or tuning a generic `shaping_weight` manually, the system estimates the expected day-of sale rate $\lambda_{section, g}$ per section and group size $g \in \{1, \dots, 6\}$ from historical show data.

#### Mathematical Formulation

For a given section and group size $g$, let the initial available number of intact blocks of size $g$ before running the solver be $N_{section, g}$.
Let $X_{section, g}$ be the random variable representing the number of blocks of size $g$ sold in the final 72 hours. We assume:
$$X_{section, g} \sim \text{Poisson}(\lambda_{section, g})$$

For the $k$-th intact block of size $g$ (indexed from 1 to $N_{section, g}$), the **marginal probability** that this specific block will be needed for a day-of sale is the probability that demand $X_{section, g}$ is at least $k$:
$$P(X_{section, g} \ge k) = 1 - \sum_{i=0}^{k-1} \frac{e^{-\lambda} \lambda^i}{i!}$$

This marginal probability decreases as $k$ increases, reflecting diminishing marginal returns (the first pair has a very high probability of selling, whereas the 6th pair has a much lower probability).

The **opportunity cost** (expected value) of breaking the $k$-th block of size $g$ is its marginal probability multiplied by the commercial ticket price for that group size:
$$\text{PhantomBid}(section, g, k) = P(X_{section, g} \ge k) \times g \times \text{seat\_price}$$

#### CP-SAT Objective Integration

The solver integrates these opportunity costs directly into the objective function as **negative-weight phantom bids** associated with the `intact[block]` variables. The hard constraint $\sum \text{intact\_var} \ge \text{min\_blocks}$ is removed entirely. The new objective becomes:

```python
# Unified CP-SAT Objective: Maximise upgrade revenue + expected residual value
objective_terms = []

# 1. Actual patron upgrade bids (second-price payment values)
for patron_id, bid_var in bid_assignments.items():
    objective_terms.append(payment_amounts[patron_id] * bid_var)

# 2. Dynamic Poisson-driven phantom bids (residual inventory opportunity cost)
for (section_id, size, k), intact_var in intact.items():
    # Compute marginal probability of needing the k-th block of this size
    lmbda = lambda_estimates[section_id][size]
    # P(X >= k)
    marginal_prob = 1.0 - poisson_cdf(k - 1, lmbda)
    
    # Expected value = probability * group size * seat price
    seat_price = discount_seat_prices[section_id]
    phantom_bid = int(marginal_prob * size * seat_price * 100) # in pence
    
    objective_terms.append(phantom_bid * intact_var)

model.Maximize(sum(objective_terms))
```

#### Why This is Superior:
1. **Self-Regulating:** If the venue has 8 open pairs but historically only sells 2 day-of ($\lambda = 2.0$), the first two pairs will have high phantom bids (e.g., 86% and 59% of ticket price), making them hard to break. The remaining 6 pairs will have very low phantom bids, allowing the solver to break them freely for any upgrade bids that yield higher revenue.
2. **Cold-Start Compatibility:** In V0/MVP, we bypass this complex estimation by hardcoding the number of intact blocks of sizes 1 to 6 as a hard constraint. In V1/V2, once historical data is accumulated, the system automatically transitions to these dynamic phantom bids, eliminating the manual overhead and potential for deadlocks.

### 4.6 The Tetris Visualisation

Post-solve, the manager's "Solver Review" screen gets a new visualisation mode:

```
[ Before ]  [ After — Upgrades ]  [ After — Residual ]

In "After — Residual" view:
  ■ Dark green:  Confirmed upgrade assignment
  ░ Light green: Intact pair (commercial)
  ▓ Gold:        Intact quad (commercial)
  □ Grey:        Isolated single (harder to sell)
  ─ Black:       SOLD (original booking)

Residual inventory check:
  Stalls Centre:  6 intact pairs ✓ (target: 6)
                  1 intact quad  ✓ (target: 1)
                  2 isolated singles ⚠️
  Circle Centre:  3 intact pairs ✓ (target: 3)
```

This visualisation gives the venue manager immediate confidence that the upgrade
programme is not damaging their day-of sales prospects.

---

## 5. Interaction Between Layers

The three layers interact in important ways, unified under the AllDifferent formulation:

```
Party Assembly
    │
    ▼
 flatten_bid_groups()           ← merges groups into synthetic bids
    │                              sets party_size = combined group size
    ▼
Block Pre-computation
    │                           ← computes valid blocks of all sizes
    ▼
Unified AllDifferent Model (Section 0)
    │
    ├── assign[patron] for ALL patrons (non-bidders pinned)
    ├── AddAllDifferent(assign[])   ← no-double-booking + chain emergence
    ├── moved[bid] indicators       ← tracks which bids are accepted
    │
    ├── Layer 1: Block variables y[bid][block]    (party integrity)
    │            + linking to assign[] per party member
    ├── Layer 2: Group bids treated as single bid (party assembly)
    ├── Layer 3: Residual intact[] constraints    (inventory shaping)
    │
    └── Maximise: Σ(bid_revenue × moved[bid]) + Σ(shaping_bonus)
    │
    ▼
Post-solve Validation
    ├── Verify: each patron assigned exactly one seat (AllDifferent)
    ├── Verify: all assigned blocks are contiguous and available
    ├── Verify: intact block targets met
    ├── Verify: no group bid partially satisfied
    └── Verify: total revenue matches expected sum of accepted bids
```

> **Note:** CUCR (Cascading Upgrade Chain Resolver) has been eliminated from this
> pipeline. Chains are discovered by the AllDifferent solver during constraint
> propagation — no separate DFS pre-processing step is needed.

**Edge case — group bid impossible:**
If a BidGroup requests 5 adjacent seats in Stalls Centre but only 3 contiguous available
seats exist, the synthetic bid has no valid block and receives no upgrade. The unmatched
email explains this:

> "Your linked group of 5 could not be seated together in Stalls Centre — the largest
> available contiguous block was 3 seats. Your original seats are confirmed."

**Edge case — inventory constraint makes solver infeasible:**
If inventory targets are so aggressive they leave no seats available for upgrades, the
solver returns with 0 upgrades and no revenue. The manager dashboard warns:

> "⚠️ Your day-of demand targets for this performance leave insufficient inventory
> for upgrades. Reduce your pair/quad targets or increase the upgrade pool."

---

## 6. Implementation Complexity Assessment

| Feature | CP-SAT complexity | Dev effort | Priority |
|---------|------------------|-----------|---------|
| Party integrity | Medium — block variables | 1–2 weeks | MVP* |
| Party assembly | Low-medium — bid merging | 1 week | V1 |
| Inventory shaping (hard constraints) | High — intact[] variables | 2–3 weeks | V1 |
| Inventory shaping (soft objective) | Low — weight tuning | 3 days | V1 |
| Tetris visualisation in dashboard | Medium — front-end | 1 week | V1 |
| VDF-seeded shaping targets | High — ML integration | 4–6 weeks | V2 |

*Party integrity is effectively MVP for any multi-seat booking to work correctly.
Without it, a party of 4 bidding together could theoretically be split into 4
different rows — which is obviously unacceptable and would generate immediate complaints.

---

## 7. Solver Performance with Extended Constraints

For a 1,300-seat venue (Gillian Lynne) with 47 active bids:

| Model version | Variables | Constraints | Solve time (est.) |
|--------------|-----------|-------------|------------------|
| Original (seat-level) | ~1,200 | ~300 | <1s |
| Unified AllDifferent (all patrons) | ~8,800 | ~3,200 | 5–30s |
| Unified + inventory shaping | ~10,500 | ~4,500 | 30–90s |

**Note on variable count:** The unified AllDifferent formulation creates a variable
for every seated patron (~1,300), not just bidders (~47). However, CP-SAT's pre-solver
eliminates fixed-domain variables (non-bidders pinned to their current seat) during
preprocessing in microseconds. The ~950 non-bidder variables are trivially propagated
away before the search begins, leaving an effective search space of ~50 bidder variables
plus block selection variables. The actual search complexity is similar to the old model,
but the formulation is simpler and provably correct.

90 seconds is acceptable for a T–3 batch job with no time pressure.
CP-SAT uses branch-and-bound with aggressive pruning — in practice, good solutions
are found in the first 10–20 seconds and the remaining time improves the objective marginally.

**Solver timeout strategy:**
```python
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 120.0    # 2-minute hard limit
solver.parameters.num_search_workers = 8          # parallelise on multi-core
solver.parameters.log_search_progress = True
status = solver.Solve(model)

# Status handling:
# OPTIMAL: best solution found — proceed
# FEASIBLE: good solution found (within time limit) — proceed if revenue > 0
# INFEASIBLE: constraints are contradictory — alert platform team, abort run
# UNKNOWN: timeout before any solution — alert platform team, abort run
```

For truly large venues (2,300+ seats, 100+ bids), consider a two-stage approach:
1. Solve the assignment problem at section level (which section gets which bid)
2. Solve the seat-level block assignment within each section independently
This reduces the search space dramatically at the cost of global optimality.

---

## 8. Data Model Additions

```sql
-- Seat map adjacency (new table)
CREATE TABLE seat_adjacency (
    seat_id         TEXT REFERENCES seat_map(seat_id),
    adjacent_seat_id TEXT REFERENCES seat_map(seat_id),
    direction       TEXT CHECK (direction IN ('LEFT', 'RIGHT')),
    PRIMARY KEY (seat_id, adjacent_seat_id)
);

-- Bid groups (new table)
CREATE TABLE bid_group (
    group_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    performance_id  UUID REFERENCES performance(performance_id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    total_party_size INTEGER NOT NULL,
    target_section  TEXT NOT NULL,
    status          TEXT CHECK (status IN ('PENDING', 'MATCHED', 'UNMATCHED'))
);

CREATE TABLE bid_group_member (
    group_id        UUID REFERENCES bid_group(group_id),
    bid_id          UUID REFERENCES bid(bid_id),
    booking_ref     TEXT NOT NULL,
    party_size      INTEGER NOT NULL,
    PRIMARY KEY (group_id, bid_id)
);

-- Inventory shaping targets (new table)
CREATE TABLE inventory_target (
    venue_id        UUID REFERENCES venue(venue_id),
    performance_id  UUID REFERENCES performance(performance_id),
    section         TEXT NOT NULL,
    group_size      INTEGER NOT NULL CHECK (group_size BETWEEN 1 AND 8),
    min_blocks      INTEGER NOT NULL DEFAULT 0,
    shaping_weight_pence INTEGER NOT NULL DEFAULT 1500,
    PRIMARY KEY (performance_id, section, group_size)
);

-- Pre-computed seat blocks (cached per solver_run)
CREATE TABLE seat_block_cache (
    solver_run_id   UUID REFERENCES solver_run(solver_run_id),
    section         TEXT NOT NULL,
    block_size      INTEGER NOT NULL,
    block_idx       INTEGER NOT NULL,
    seat_ids        TEXT[] NOT NULL,   -- array of seat_ids in this block
    PRIMARY KEY (solver_run_id, section, block_size, block_idx)
);
```
