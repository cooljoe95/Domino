# The Shakeup
## Master Product Requirements Document
### Version 1.1 | 2026-05-29 | Confidential

---

> This document is the single authoritative source for The Shakeup product, technical
> architecture, and business model. It synthesises nine prior specification documents
> into one coherent reference. Detailed technical appendices are available separately.

---

## Table of Contents

1. [[#1. Executive Summary|Executive Summary]]
2. [[#2. The Problem & Market Opportunity|The Problem & Market Opportunity]]
3. [[#3. The Solution — Product Overview|Product Overview]]
4. [[#4. Core Personas|Core Personas]]
5. [[#5. The Bid Lifecycle — End to End|The Bid Lifecycle]]
6. [[#6. Product Feature Set|Product Feature Set]]
7. [[#7. The Proprietary Algorithmic Core|The Proprietary Algorithmic Core]]
8. [[#8. Business Model & Financial Projections|Business Model & Financial Projections]]
9. [[#9. Go-To-Market Strategy|Go-To-Market Strategy]]
10. [[#10. Legal & Regulatory Compliance|Legal & Regulatory Compliance]]
11. [[#11. Risk Register Summary|Risk Register Summary]]
12. [[#12. Technology Stack & Architecture|Technolgy Stack & Architecture]]
13. [[#13. Data Model|Data Model]]
14. [[#14. Product Roadmap|Product Roadmap]]

---

## 1. Executive Summary

**The Shakeup** is a B2B2C yield management platform for live theatre. It converts the
structural inefficiency of unsold premium inventory in the final days before curtain into
a revenue-generating, satisfaction-increasing seat upgrade marketplace.

The core mechanic %% mechanic?, probably mechanism%%: advance-booking theatre patrons receive a personalised upgrade offer **7 days before their performance** %%It isn't personalized to them... the email might be in name, but the offer is standard for them to make a bid, we wouldn't have predisposed the amount for them to bid%%, place sealed bids for better seats, and receive resolution — with automatic ticket reissuance — **3 days before curtain**. Venue partners receive 80% of all upgrade revenue. The Shakeup takes 20%.

**The platform operates entirely after the primary ticket is sold.** It does not compete
with Ticketmaster, See Tickets %%Should this probably be TodayTix?, I don't know what See Tickets are.. %%, or ATG. It monetises inventory that would otherwise
generate £0 (unsold premium seats) or £25 (day seats) — for patrons who paid full
price and deserve a better path to a better seat.

---

**Pilot target:** My Neighbour Totoro, Gillian Lynne Theatre (LW Theatres estate) %%New Wimbledon Theatre might also be good as they have a rotation of shows and we can see how different audiences act in that one pilot%%
**Target pilot launch:** October 2026
**Self-funded:** Founder holds >£1,000,000 in liquid assets. No external investment required.
**UK break-even:** 5 venues (~12 months post-pilot)
**"Very profitable" threshold:** 42 venues (~24–36 months post-pilot) → £2.65M/year

---

## 2. The Problem & Market Opportunity

### 2.1 The West End Inventory Problem

West End theatre operates with a structural inventory paradox:

**The seats that are hardest to sell are the ones people most want.** %%Citation needed... Potentially build web scraper to verify day of sales... won't know how much they paid though%% 
Premium central seats (Stalls Centre, Dress Circle Centre) carry the highest face values
and attract the most demand — but they also attract buyers who plan far in advance. Once
the advance-sale window passes, these seats sit unsold until box-office-morning day
seats are released at heavily discounted prices. %%Can be sold as a way to make theatre more affordable for some folks who are able to spread out the cost into two different pay cycles%%

Meanwhile, the patrons who *did* plan far in advance — who bought restricted-view or
peripheral seats months ago at full price — sit with the mild injustice of watching
late buyers potentially sit better than them, for less.

```
The result:
  ┌──────────────────────────────────────────────────────┐
  │  Advance buyer (booked 4 months ago)                 │
  │  Paid: £65 for Stalls Side                           │
  │  Is sitting in a restricted-view position            │
  │                                                      │
  │  Day-seat buyer (queued this morning)                │
  │  Paid: £25 for Stalls Centre                         │
  │  Has a better view for £40 less                      │
  └──────────────────────────────────────────────────────┘
```

No platform exists to capture the latent willingness-to-pay between these two groups.

### 2.2 Market Size
> [!NOTE]
> Need to confirm these numbers as they appear as if out of nowhere

**West End (primary market):**
- ~50 major productions running simultaneously
- ~50,000 seats per night × 8 performances/week = 400,000 seat-nights/week
- Average occupancy: 78% → ~88,000 unsold seat-nights/week
- Premium (Stalls/Dress Circle) occupancy lower than average in off-peak periods
- Day seat sell-through: low (confirmed anecdotally by venue managers)

**UK National:**
- ~1,400 professional theatre venues
- ~250 active (5+ shows/week) at any time
- Serviceable addressable market: ~150 venues

**International (long-term):**
- Broadway: 40+ productions, ~1,700 seats avg, higher price tolerance
- Global live theatre: ~5,000 professional venues with reserved seating
> [!NOTE]
> Maybe add expansion into Events/Concerts as well as sporting
### 2.3 Competitive Landscape

**No direct competitor exists.** Seat upgrade bidding in adjacent sectors:
> [!NOTE]
> Add UP and TodayTix

| Sector   | Platform              | Why it doesn't apply to theatre                        |
| -------- | --------------------- | ------------------------------------------------------ |
| Hotels   | Nor1, Plusgrade       | Room upgrade = category change, not spatial assignment |
| Airlines | Various               | Zone-based, not reserved-seat; no party integrity      |
| Sports   | Dynamic pricing tools | General admission or season-ticket specific            |

Theatre reserved-seat management requires combinatorial optimisation across a physical
seat graph, with party integrity, chain effects, and inventory shaping constraints that
do not exist in any other upgrade bidding context. This is not an adjacent solution;
it is a net-new problem requiring net-new technology.

---

## 3. The Solution — Product Overview

The Shakeup is a three-phase platform operating in the window between ticket purchase
and performance:

```
T–7 days:  Upgrade offer emails sent to eligible patrons %%Potentially not eligible, just everyone, and also initial email, so they are able to do so at teh onset%%
           ↓
T–7 to T–3: Patron bid collection window
           ↓
T–3 days:  Pre-authorisation run → Solver → Resolution → Reissuance
           ↓
Show day:  Patrons arrive at new seats; venue has clean inventory
```

**What the patron experiences:**
1. White-labelled email from the show, personalised to their specific seats
2. Interactive seat map: their current seats highlighted, eligible upgrade zones colour-coded %%Maybe not just zones, they can deselect seats with restricted views and deselect/select specific seats within a zone%%
3. Place one or more bids for different sections; card stored but not charged
4. Three days before: confirmation of upgrade (with new ticket) or notification of no match
5. No financial risk until confirmation; original seat guaranteed regardless

**What the venue gets:**
- Incremental revenue on seats that would otherwise generate day-seat prices or nothing
- No change to their primary ticketing workflow
- A real-time dashboard showing bid volume, heatmap, and projected revenue %%Can we promise this and next in V1? or subsequent Vs?%%
- Post-show analytics: participation funnel, section performance, satisfaction ratings %%We can ask what they thought of it, but without an incentive, I don't foresee many responses%%
- Commercially shaped residual inventory (the solver protects day-of sale configurations) %%Using the likeliness of sale from manager.... We will need past sales data to train their model on%%

---

## 4. Core Personas

### Persona A — The Theatre Patron

**Profile:** Age 28–65. Plans ahead: booked 2–6 months in advance. Familiar with
hotel/airline upgrade systems; finds the concept immediately intuitive. Mobile-first.
Cares about the experience, not just the price.

**Journey trigger:** White-labelled upgrade offer email from the production, 7 days out.

**Pain points solved:**
- The psychological sting of the day-seat buyer sitting better for less
- The friction of monitoring availability and acting day-of
- No financial risk: card not charged until upgrade is confirmed

**Key UX requirements:**
- Magic link authentication — no account creation
- Three taps from email to bid submitted %%Not sure this can be guaranteed maybe prefilled with sections better than his with blanket bid (or bids) but if they want to get rid of individual seats or add a section (such as going higher and center) they can%%
- Live match probability updates as bid amount is typed %%might get rid of, can't really know, I know the airlines do this, but think it's just psychological and not based in reality%%
- Explicit, plain-English disclosure before card is stored
- Outcome email with full transparency (bid rank shown for unmatched bids)

---

### Persona B — The Venue/Theatre Manager

**Profile:** Box office manager, Head of Sales, or Revenue Manager at a West End
production. Has access to sales data. Cares about per-show revenue, occupancy,
audience satisfaction, and ancillary revenue.

**Journey trigger:** New production setup; ongoing per-show monitoring.

**Key workflows:**
1. **Onboarding (one-time):** Upload seat map, configure upgrade ruleset, set inventory hold parameters, upload historical sales data %%minimum upgrade amount?%%
2. **Per-show:** Monitor live bid dashboard; optionally review solver output before execution %%Maybe don't allow as we plan on it running at 4am to avoid race conditions (but we also know that isn't possible, so possibly not allow new sales during the meantime?)%%
3. **Post-show:** Review analytics report, download CSV of outcomes

**Key dashboard requirements:**
- Real-time KPIs: bid count, bid value, projected upgrades, projected revenue
- Bid heatmap %%where they are coming from and how much? %% overlaid on venue seat map 
- Solver countdown with "run early" and "pause" controls %%do we really want it to run early?%%
- Optional solver approval gate with auto-approve timer (30 minutes)
- Resolution monitoring with alert on any payment/reissuance failure
- Post-show funnel: eligible → opened → bid → pre-auth → matched → confirmed %%post show??%%

---

### Persona C — The Platform Operator (Internal)

**Profile:** The Shakeup engineering/operations team.

**Key functions:**
- Venue onboarding pipeline management
- Solver job monitoring across all concurrent performances
- Financial settlement oversight (Stripe Connect)
- DBIE model retraining and SCOS calibration %%definitions please, this is the first time they are being used in this doc%%
- Incident response for payment or reissuance failures

---

## 5. The Bid Lifecycle — End to End

### 5.1 Phase Timeline
> [!NOTE]
> Need to fix phase 1, we may want to incorporate with their booking system to know how many seats are available, the performance wont be from T-14, but rather from when booking begins, and bids can be done then... The email 7 days before will act as a reminder.

> [!NOTE]
> Phase 4 abbreviations need definitions

> [!NOTE]
> Find way to avoid race conditions... maybe add all of the seats to the cart to prevent people buying them at 4 am, and if it runs in two minutes, that should be fine?
```
PHASE 0 — Venue onboarding (one-time per venue)
  └─ Seat map upload → ruleset config → sales history → VDF fingerprint

PHASE 1 — Performance setup (T–14 to T–7)
  └─ Booking sync from ticketing system
  └─ Seat state initialised (SOLD / AVAILABLE / HELD)
  └─ Offer email job scheduled at T–7
  └─ Solver job scheduled at T–3

PHASE 2 — Bid collection (T–7 to T–3)
  └─ Magic link email sent
  └─ Patron visits portal → browses seat map → places bid(s)
  └─ Card stored via Stripe SetupIntent (no charge)
  └─ Bid receipt email sent

PHASE 3 — Pre-auth run (T–3, before solver)
  └─ PaymentIntent created for each PENDING bid
  └─ Failed pre-auths → PRE_AUTH_FAILED → excluded from solver
  └─ Passed bids → PRE_AUTH_OK → solver input

PHASE 4 — Solver execution (T–3, immediately after pre-auth)
  └─ AllDifferent CP-SAT model: all patrons modelled; non-bidders pinned
  └─ Chains emerge naturally from constraint propagation
  └─ Objective: maximise revenue + residual inventory value
  └─ Output: upgrade_assignments[] + unmatched_bids[]

PHASE 5 — Resolution & reissuance (T–3, immediately after solver)
  └─ MATCHED: compute second-price charge → capture at charge amount → reissue ticket → notify patron
  └─ UNMATCHED: cancel pre-auth → notify patron (with bid rank + winning price)
  └─ CAPTURE_FAILED: cancel pre-auth → revert seat state → notify patron

PHASE 6 — Show cancellation (if triggered by venue at any time)
  └─ All PENDING/PRE_AUTH_OK bids → CANCELLED_SHOW
  └─ All CONFIRMED bids → full refund via Stripe Refund API → REFUNDED
  └─ Patrons revert to original seats (original tickets remain valid)
  └─ Venue dashboard shows cancellation summary
```

### 5.2 Bid State Machine
> [!NOTE]
> Need to ensure that the user only gets matched once if there are multiple bids to their name
```
[*] → DRAFT (patron starts form)
DRAFT → PENDING (card stored via SetupIntent)
DRAFT → ABANDONED (patron exits)

PENDING → PRE_AUTH_FAILED (T–3 pre-auth declined)
PENDING → PRE_AUTH_OK (T–3 pre-auth succeeded)

PRE_AUTH_OK → MATCHED (solver assigns a seat)
PRE_AUTH_OK → UNMATCHED (solver finds no feasible assignment)

MATCHED → CONFIRMED (second-price payment captured ✅)
MATCHED → CAPTURE_FAILED (capture fails after one retry ❌)

Any non-terminal → CANCELLED_SHOW (venue cancels performance)
CONFIRMED → REFUNDED (venue cancels after upgrades were confirmed)

Terminal states: CONFIRMED, REFUNDED, UNMATCHED, CAPTURE_FAILED, PRE_AUTH_FAILED, ABANDONED, CANCELLED_SHOW
```

### 5.3 Seat State Machine

```
[*] → AVAILABLE (performance created)
AVAILABLE → SOLD (booking from ticketing system)
AVAILABLE → HELD (manager inventory hold)
SOLD → BID_VACATING (patron has a PENDING or PRE_AUTH_OK bid)
BID_VACATING → SOLD (all patron bids reach terminal state without CONFIRMED)
BID_VACATING → VACATED (one of patron's bids = CONFIRMED)
VACATED → AVAILABLE (released to venue inventory for day-of sales)
HELD → AVAILABLE (hold removed by manager)
```

### 5.4 The Deferred Pre-Auth Pattern

The platform uses a **deferred pre-auth saga** — the single most important payment
architecture decision:

- **At bid placement (T–7 to T–3):** `Stripe SetupIntent` stores the card as a reusable
  `PaymentMethod`. Zero financial commitment. SCA-compliant %%What is SCA compliancy?%%.
  Patron does not need to be present at T–3.
- **At T–3 (Phase 3):** Fresh `PaymentIntent` created using stored PaymentMethod with
  `capture_method: manual`. Pre-auth amount = patron's full bid (their maximum).
- **Immediately after solver (second-price resolution):**
  - For each MATCHED bid: compute the **second price** (highest losing bid for that
    section + £1, floored at £8/seat). Capture at this lower amount. Stripe natively
    supports partial capture — the remaining hold is released automatically.
  - For each UNMATCHED bid: cancel PaymentIntent.

**Why this design:** Stripe card pre-authorisations carry a 7-day guaranteed validity
window (varies by card network and issuing bank). Pre-authing at T–7 and capturing at
T–3 sits exactly at this limit. The deferred pattern eliminates this entirely — pre-auth
and capture occur within minutes of each other at T–3, with zero expiry risk.

### 5.5 Show Cancellation & Refund Handling

If a venue cancels a performance, all upgrade activity must unwind cleanly:

**Before solver has run (T–7 to T–3):**
- All PENDING bids → CANCELLED_SHOW. No payment was taken (only SetupIntent stored).
  PaymentMethod can be detached. Patron notified: "The performance has been cancelled.
  Your upgrade bid has been withdrawn. No charge was made."

**After solver has run (T–3 onwards, upgrades confirmed):**
- All CONFIRMED bids → full refund via `Stripe Refund API` → REFUNDED.
  Refund amount = the second-price charge that was captured, not the original bid.
- Patrons revert to original seats. The venue's ticketing system handles original
  ticket refunds separately — The Shakeup only refunds the upgrade charge.
- Venue dashboard shows cancellation summary with total refunds issued.

**Key principle:** The Shakeup never holds patron money for a cancelled show. Refunds
are processed within 24 hours of the cancellation event. Stripe refunds typically
appear on the patron's statement within 5–10 business days.

---

## 6. Product Feature Set

### 6.1 MVP (Pilot — October 2026)
>[!NOTE]
>Heatmap should be V1
>Need inventory shaping
>Probably don't need at T-4 reminder too
>Reissuance should at least be one API integration and add more later
>

| Feature | Description |
|---------|-------------|
| Patron bid portal | Magic-link authenticated web app. Seat map, bid entry, basket, card storage, confirmation |
| Manager dashboard | Venue setup wizard, live bid KPIs, solver controls, resolution monitoring |
| Solver (AllDifferent) | CP-SAT solver: AllDifferent formulation, party integrity (aisle-aware blocks), hard inventory shaping, revenue maximisation |
| Second-price auction | Winners pay £1 above the highest losing bid (floored at £8/seat). Patrons bid their true max, pay the competitive price |
| Payment pipeline | Stripe SetupIntent → PaymentIntent (pre-auth at full bid) → capture at second price / cancel |
| Email system | White-labelled transactional emails: T–7 offer, bid receipt, 3× outcome variants |
| Reissuance (MVP) | Manual: venue box office receives CSV of new seat assignments; reissues tickets manually |
| Cancellation handling | Show cancellation triggers automatic refund of all confirmed upgrade charges |
| Reporting | Post-show analytics: participation funnel, section performance, revenue summary |

**MVP deliberately excludes:** ML bid guidance (rule-based at MVP), API-based reissuance,
party assembly (linked bookings), upgrade eligibility rules (all booked patrons eligible),
inventory shaping soft objective (hard hold constraints only), heatmap visualisation.

### 6.2 V1 (Months 8–18)

| Feature | Description |
|---------|-------------|
| Spektrix API integration | Automated booking sync + programmatic ticket reissuance |
| Line-Up API integration | Same, for LW Theatres estate |
| DBIE (ML bid intelligence) | Trained on pilot data; per-patron, per-zone bid recommendations with match probability |
| Party assembly | Linked bid groups — separately-booked patrons can opt into shared seating |
| Upgrade eligibility rules | Venue-configurable: minimum tier gap, section restrictions, patron filters |
| Inventory shaping (soft) | Soft objective bonus for over-delivering on intact residual blocks |
| Bid heatmap | Visual overlay on seat map showing bid origin/destination patterns |
| Manager mobile view | Key dashboard metrics and solver approval on mobile |

### 6.3 V2 (Months 18–36)

| Feature | Description |
|---------|-------------|
| Tessitura + TixTrack integration | UK regional and Nimax venue coverage |
| Fringe simplified mode | Zone-only bidding; no seat-level optimisation; freebie-lateral move mechanic |
| DBIE v2 | Per-venue fine-tuning after ≥20 shows; weather + competition signals |
| Multi-venue solver | Coordinated scheduling across 10+ concurrent venues |
| Patron account | Optional repeat-user profile; bid history; upgrade preference learning |
| Revenue share analytics | Venue-level P&L reporting; show-over-show trend analysis |

### 6.4 V3 (Year 3+)

| Feature | Description |
|---------|-------------|
| Broadway mode | USD pricing, US payment compliance, OvationTix/Telecharge integration |
| Concert/sports mode | Zone-only (no individual seat); general admission overlay |
| ATG commercial partnership | Enterprise deal; proprietary ATG system integration |
| Real-time market pricing | Dynamic seat pricing during the bid window based on live demand signals |

---

## 7. The Proprietary Algorithmic Core

These four engines constitute The Shakeup's defensible competitive moat. They become
more valuable with every additional show run through the platform.

### 7.1 Unified AllDifferent Solver (replaces CUCR)

**The problem it solves:** When patron A upgrades from Stalls Side to Stalls Centre,
their vacated seat becomes available — which could satisfy patron B's bid to move from
Upper Circle to Stalls Side. A naïve solver that only considers currently-empty seats
misses these "upgrade chains" entirely.

The original architecture used a separate pre-processing step (CUCR — Cascading Upgrade
Chain Resolver) to detect chains via DFS traversal before the solver ran. This has been
replaced by a fundamentally cleaner approach: **model every seated patron as a CP-SAT
variable and let chains emerge naturally from constraint propagation.**

**The unified formulation:**
>[!NOTE]
>Need to ensure people are seated together
>Does this actually maximizer revenue?
```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Every patron in the theatre gets a variable: which seat are they in after resolution?
seat_of = {}
for patron in all_patrons:
    if patron.has_bid:
        # Bidder: can stay put OR move to any eligible target seat
        domain = [patron.current_seat] + patron.eligible_target_seats
    else:
        # Non-bidder: pinned to their current seat (domain of 1)
        domain = [patron.current_seat]
    seat_of[patron] = model.NewIntVarFromDomain(
        cp_model.Domain.FromValues(domain), f'seat_{patron.id}'
    )

# No two patrons can end up in the same seat — AND chains emerge from this
model.AddAllDifferent(list(seat_of.values()))

# Track who moved (for revenue calculation)
moved = {}
for patron in bidding_patrons:
    moved[patron] = model.NewBoolVar(f'moved_{patron.id}')
    model.Add(seat_of[patron] != patron.current_seat).OnlyEnforceIf(moved[patron])
    model.Add(seat_of[patron] == patron.current_seat).OnlyEnforceIf(moved[patron].Not())

# PRIMARY OBJECTIVE: maximise total upgrade revenue
model.Maximize(sum(
    patron.bid_amount_pence * moved[patron]
    for patron in bidding_patrons
))
```

**Why chains emerge naturally:** `AllDifferent` means if patron A moves from seat 5 to
seat 10, no other patron can claim seat 10 — but seat 5 is now free. If patron B's
domain includes seat 5, the solver will discover this opportunity automatically through
constraint propagation. No DFS, no chain detection, no chain-length cap.

**Why it's efficient:** A 1,300-seat venue with 950 non-bidders creates 950 pinned
variables (domain = {current_seat}). CP-SAT's pre-solver eliminates these in
microseconds — they're trivially propagated. The effective search space is just the
~50 bidders, with domains correctly pruned to account for cascaded vacancies.

**What this eliminates vs. the old CUCR:**
- DFS chain detection pre-processing → eliminated
- Artificial chain-length cap (k ≤ 4) → eliminated (solver explores any length)
- Chain-level atomic constraints → eliminated (`AllDifferent` handles it)
- Chain unwind logic → simplified (revert individual assignments)

**Impact:** Same 40–80% chain revenue lift as the old CUCR, but simpler architecture,
fewer failure modes, and no artificial limits on chain length.

**Patent status:** Provisional UK patent application planned for unified AllDifferent
solver + SCOS combination applied to reserved-seat venue upgrade management.

---

### 7.2 Seat Chain Opportunity Scorer (SCOS)

**The problem it solves:** When patron A vacates seats 14C–14D, these may combine with
the already-vacant 14E to create a contiguous triple — which the venue can sell as a
day-of group. This latent option value should influence the solver's assignment choices.

**Algorithm:** For each candidate bid assignment, simulate the post-solver vacancy map.
For each contiguous vacant run in each row, compute:
`P(sell) × avg_last_72h_price × chain_length_multiplier`
This `chain_opportunity_score` enters the solver objective as a weighted bonus term
(configurable per venue via `chain_weight` parameter).

---

### 7.3 Dynamic Bid Intelligence Engine (DBIE)

**The problem it solves:** Without guidance, patrons don't know what to bid. Without
ML-calibrated guidance, The Shakeup can't give patrons confidence in the match
probability their bid generates.

**Feature space (inputs):**
- Show genre, production age, day/time, occupancy at T–7
- Origin zone → destination zone pair
- Historical sell-through of destination zone for this production
- Patron lead time (months since original purchase)
- Repeat user flag
- Weather forecast, local event competition

**Outputs:**
- `recommended_bid_£` with confidence band
- `predicted_match_probability_%` at specific bid amounts (displayed live to patron)

**Training:** Weekly retraining on outcome data (which bids won, at what price, for
what zone pair). Per-venue fine-tuning after ≥20 shows. Training data is anonymised
aggregates — no individual patron data used in model training (GDPR compliance).

**MVP alternative:** Rule-based formula using face value differential × occupancy
multiplier until DBIE training data is sufficient (estimated: after 3–4 pilot shows).

---

### 7.4 Venue Demand Fingerprint (VDF)

**The problem it solves:** The inventory hold decision (how many seats to withhold
from the upgrade pool for day-of sales) is currently made by gut feel. VDF makes it
a data-driven recommendation.

**Staged Roadmap:**
- **V0 (MVP Stage — Hardcoded Targets):** To handle the cold-start problem (lack of historical data during initial pilot shows), the venue manager manually inputs target counts for different group sizes up to size six per section (e.g., "preserve exactly 4 singles, 3 pairs, and 1 quad in Stalls Centre"). The solver enforces these targets as hard constraints.
- **V1/V2 (Data-Driven Stage — Poisson Dynamic Reserve Pricing):** Transition to a fully automated, probabilistic approach. The system models the number of groups sold in the last 72 hours per group size (1 to 6) as independent Poisson distributions per section.

**Poisson Modeling Pipeline (V1/V2):**
1. Historical sales records bucketed by time-to-curtain (8 buckets: >90d, 60–90d, ... day-of).
2. Model day-of sales per group size $g \in \{1, \dots, 6\}$ per section as an independent Poisson process with expected sale rate $\lambda_{section, g}$ estimated from the last 10–20 shows.
3. Compute the **marginal probability** $P(\text{sale} \ge k)$ of selling the $k$-th group of size $g$ on the day of the show based on the estimated $\lambda_{section, g}$.
4. Multiply this marginal probability by the target group's discount ticket price to compute the **opportunity cost** (expected value) of occupying a block of size $g$ with an upgrade.
5. Ingest these opportunity costs directly into the solver's objective function as negative-weight "phantom bids" competing with actual patron upgrade bids, replacing manual inputs and hard constraints.

**Output:** `demand_fingerprint` JSON stored per (venue, production). Surfaces in dashboard as:
- *V0:* "Manager-specified targets active. Enforcing 4 singles, 3 pairs, 1 family group."
- *V1/V2:* *"Based on past shows, there is a 95% likelihood of needing 3 pairs in Stalls Centre. Seeding opportunity cost of £24 per pair preserved."*

---

### 7.5 Extended Solver Constraints

**Party Integrity — V0 (keep together):**
Solver variables change from per-seat `x[bid, seat]` to per-block `y[bid, block]`,
where a block is a pre-computed contiguous set of N adjacent seats in the same row.
A party of 4 is assigned atomically to a contiguous 4-seat block or not at all.
Block pre-computation runs in O(n) from the seat adjacency graph before each solver run.
Blocks never cross aisles — aisle gaps break contiguous runs during pre-computation.

**Inventory Shaping (hard constraints) — V0 (the Tetris constraint):**
Venue manager manually inputs expected day-of demand by section for discrete group sizes up to six (e.g., "preserve 4 singles, 3 pairs, and 1 quad in Stalls Centre"). The solver adds `intact[block]` binary variables: after all upgrade assignments, the remaining unassigned seats must contain at least the hardcoded count of valid contiguous blocks of each size. This is a hard constraint at V0 to guarantee inventory safety during cold start.

**Inventory Shaping (soft objective / Dynamic Reserve Pricing) — V1/V2:**
Replaces the hardcoded minimum targets and hard constraints with a probabilistic **opportunity cost** framework powered by the Poisson demand model.
For each group size $g \in \{1, \dots, 6\}$, we represent the expected day-of sales as independent Poisson distributions. The solver objective function is augmented with **negative-weight "phantom bids"** that represent the opportunity cost of losing an intact seat block of size $g$:
$$\text{PhantomBid}(section, g, k) = P(X_{section, g} \ge k) \times \text{Price}(g)$$
where $k$ is the $k$-th block of size $g$ in the section, and $X_{section, g} \sim \text{Poisson}(\lambda_{section, g})$.
This creates a dynamic reserve price where upgrades are only granted if the actual patron's upgrade bid exceeds the expected revenue of keeping that seat block available for last-minute buyers, trading off sure revenue against probabilistic demand organically.

**Party Assembly — V1 (bring together):**
Separately-booked patrons can link their bids in the portal. Linked bids are merged
into a synthetic combined bid with `party_size = sum of all parties`. The solver
finds a contiguous block for the combined group.

**Upgrade Eligibility Rules — V1:**
Venue-configurable rules that filter which patrons receive upgrade offers. Examples:
minimum tier gap between current and target section, section-specific restrictions,
patron category filters. At MVP, all booked patrons are eligible.

---

## 8. Business Model & Financial Projections

### 8.1 Revenue Mechanics

- **Revenue model:** Pure revenue share. No setup fee, no SaaS subscription.
- **Split:** 80% to venue, 20% to The Shakeup
- **Auction mechanism:** Second-price sealed bid with £1 increment. Patrons enter their
  maximum bid. Winners pay £1 above the highest losing bid for their target section,
  floored at £8/seat. Patrons never pay more than they bid.
- **Why second-price:** Incentivises truthful bidding (patrons bid their true maximum
  because they know they'll only pay the competitive price). Generates better price
  discovery data for DBIE training. Every winner feels they got a deal.
- **Bid floor:** £8/seat (operational minimum — covers Stripe fees + platform costs)
- **Bid ceiling:** Uncapped. Market-determined. Day-seat price (~£25) is the rational
  ceiling for patrons who know about day seats; higher for patrons who don't.
- **Bid structure:** No guidance initially (MVP — price discovery). After 3–4 shows,
  DBIE introduces calibrated guidance ranges.
- **Original ticket price:** NOT included in the solver objective. The market self-
  corrects — patrons in better seats bid less (smaller jump), patrons in worse seats
  bid more (larger jump). SCOS already captures vacancy value. Adding ticket price
  to the objective would distort the auction and undermine strategy-proofness.

### 8.2 The Per-Person Pricing Advantage

Unlike hotel upgrade bidding (flat-rate per room regardless of occupancy), theatre
bids are per seat. A family of 4 bidding £10/person generates £40 per upgrade booking.

**Weighted average party size:** 2.6 seats per upgrade booking
**Average upgrade transaction value (£10/seat):** £26
**The Shakeup's take per transaction (20%):** £5.20

### 8.3 Revenue by Venue Tier

**Scenario A — No guidance, £10/seat avg, 8% participation:**

| Tier | Capacity | Chain mult | Upgrade bookings/show | TS/show | TS/week |
|------|---------|------------|----------------------|--------|--------|
| Studio (250) | 250 | 1.2× | 1.7 | £9 | £69 |
| Mid (500) | 500 | 1.3× | 3.5 | £18 | £147 |
| Standard WE (800) | 800 | 1.4× | 6.1 | £32 | £253 |
| Large WE (1,300) | 1,300 | 1.6× | 11.4 | £59 | £472 |
| Major (2,300) | 2,300 | 1.8× | 22.6 | £118 | £706 |

**Scenario B — Calibrated guidance, £18/seat avg, 15% participation:**

| Tier | TS/show | TS/week | TS/year |
|------|--------|--------|--------|
| Studio (250) | £30 | £242 | £12,600 |
| Mid (500) | £65 | £524 | £27,200 |
| Standard WE (800) | £113 | £902 | £46,900 |
| Large WE (1,300) | £210 | £1,678 | £87,300 |
| Major (2,300) | £416 | £2,499 | £130,000 |

### 8.4 Profitability Milestones

**Operating costs by stage:**
| Stage | Team | Annual | Weekly |
|-------|------|--------|--------|
| Founder-only | 1 | £70k | £1,350 |
| Early team | 3 | £250k | £4,800 |
| Growth | 7 | £600k | £11,500 |
| Scaled | 15 | £1.4M | £26,900 |

**Venues to break even (Scenario B, West End portfolio mix):**

| Stage | Target/week | Venues needed |
|-------|------------|--------------|
| Founder viable | £1,350 | **2 venues** |
| Early team | £4,800 | **5 venues** |
| Growth | £11,500 | **10 venues** |
| Scaled | £26,900 | **23 venues** |
| **"Very profitable"** | **£50,000+** | **42 venues → £2.65M/year** |

**5-year projection:**
| Year | Venues | TS Revenue |
|------|--------|-----------|
| 1 (post-pilot) | 5 | £252k |
| 2 | 20 | £1.0M |
| 3 | 42 | £2.65M |
| 4 | 80 UK | £5.2M |
| 5 | 100 UK + 20 Broadway | £7.2M |

---

## 9. Go-To-Market Strategy

### 9.1 The Two-Party Problem

Every venue deal requires sign-off from two distinct organisations:

**The Production** (e.g., RSC + Nippon TV for Totoro) controls the IP, brand, and
patron communications. They care about audience satisfaction and show reputation.

**The Venue Operator** (e.g., LW Theatres) controls ticketing, box office, and the
physical reissuance process. They care about incremental revenue and operational simplicity.

Both must agree. The venue operator is typically easier to reach first and can brief
the production separately.

### 9.2 Primary Pilot Target

**Show:** My Neighbour Totoro
**Venue:** Gillian Lynne Theatre (1,295 seats, 6 sections)
**Operator:** LW Theatres
**Primary contact:** Martin Crosier, Managing Director — LW Tickets (appointed 2025
specifically to own ticketing, box office, and data operations)
**Secondary contact:** Matt Simkin, Head of Commercial

**Why Totoro is ideal:**
- Totoro audiences are brand-loyal and digitally engaged — high email open rates
- Family bookings (avg party 3.2) produce higher per-booking upgrade revenue
- Premium sections (Stalls Centre) typically have 15–25% day-of vacancy
- The show runs October 2026 – January 2027, giving a 100-show pilot window
- Cultural resonance makes a successful case study highly transferable

**IP note:** The show involves RSC + Nippon TV + LW Theatres. Nippon TV is a Studio
Ghibli board member company — any patron email using Ghibli characters requires Nippon
TV sign-off. Recommended approach: use only the "My Neighbour Totoro" wordmark and LW
Theatres venue branding. No Ghibli characters, no Ghibli logo. Eliminates IP clearance
risk entirely.

### 9.3 The Three-Meeting Sales Process

**Meeting 1 — The Problem Frame (30 min):**
Agenda: "Do you have this problem?" Walk through the Totoro day-seat occupancy data
and the 78% average occupancy headline. Do not pitch the solution in meeting 1.
Target outcome: agreement that the problem exists and is worth solving.

**Meeting 2 — The Solution Demo (60 min):**
Agenda: Live demo of the patron portal (using test data for Gillian Lynne seat map).
Show the solver running. Show the manager dashboard. Show the post-show report.
Target outcome: agreement on pilot terms and hand-off to legal/commercial.

**Meeting 3 — Pilot Terms (45 min):**
Agenda: LOI terms, DPA structure, pilot success metrics, timeline.
Target outcome: signed LOI.

### 9.4 Pilot LOI Terms

| Term | Proposed |
|------|---------|
| Duration | 100 performances (~3 months) |
| Revenue split | 80/20 (venue/TS) |
| Setup fee | Zero |
| Data rights | Venue retains booking data; The Shakeup retains anonymised aggregate bid data |
| Renegotiation trigger | 3-month review; target move to 75/25 for continuing agreement |
| Exclusivity | None — The Shakeup retains right to approach other venues concurrently |

### 9.5 Timeline

```
Mid-June 2026   First LinkedIn message to Martin Crosier / Matt Simkin
July 2026       Meeting 1 with LW Theatres
                Endorsing body (UKES) application submitted
August 2026     Meeting 2 — demo
                LOI signed
                Endorsement letter received
September 2026  IFV visa application submitted
                DPA drafted and reviewed
October 2026    Visa granted
                MVP deployed to staging
                First T–7 email sent to Totoro patrons
November 2026   First live upgrades processed ✅
```

---

## 10. Legal & Regulatory Compliance

### 10.1 Key Frameworks

| Framework | Requirement | The Shakeup's approach |
|-----------|------------|----------------------|
| Consumer Rights Act 2015 | 14-day cancellation right for digitally-delivered services | Bid cancellation allowed up to T–3 at no cost. CRA 2015 §37 exemption: time-limited event service. |
| DMCC Act 2024 | Drip pricing prohibited. All fees must be shown upfront | Bid amount = total price. Platform fee is backend revenue share only, never shown to patron. |
| UK GDPR | Lawful basis for processing; patron consent for marketing; data minimisation | Legitimate interest for upgrade processing; explicit PECR consent for email. Minimal PII stored. |
| PCI DSS | Card data must not touch The Shakeup's servers | Stripe Elements (SAQ A scope). Card number never reaches The Shakeup's database. |
| PSR 2017 / SCA | Strong Customer Authentication required for payment initiation | SetupIntent with MIT (Merchant-Initiated Transaction) flag. SCA triggered at SetupIntent; exempt at capture. |
| PECR 2003 | Consent required for marketing emails | White-labelled upgrade offer emails are not The Shakeup's marketing. Venue's own PECR consent applies. Separate unsubscribe from upgrade offers only. |

### 10.2 Critical UX/Legal Requirements

These must be implemented exactly as specified — they are not suggestions:

1. **Pre-bid disclosure checkbox:** Must be unchecked by default. Must name the exact
   charge amount, the exact date, and "without further confirmation from me." The card
   entry fields must be disabled until checkbox is ticked.

2. **Cancel bid:** Freely accessible from confirmation email and bid management page
   until T–3 (10:00am). No cancellation fee. CRA 2015 compliance.

3. **Bid guidance labelled "guidance":** Not "price," not "typical price." CMA guidance
   on drip pricing requires clarity that this is guidance, not a commitment.

4. **Unmatched email shows bid rank:** "You placed 4th for 3 available seats." This is
   not just good UX — it is the defence against a "why was I charged?"-style complaint
   (even though no charge occurs — the rank explanation builds trust).

5. **GDPR consent record:** Server must record `{patron_id, consent_timestamp,
   ip_address, user_agent, bid_amounts[], performance_id}` before the SetupIntent
   is confirmed. This is the timestamped consent evidence for any dispute.

### 10.3 Joint Controller Risk

If The Shakeup and the venue jointly determine the purposes and means of patron data
processing, GDPR Article 26 requires a documented Joint Controller Agreement. This
must be reviewed by a solicitor with data privacy expertise before the pilot launch.
The DPA template should be drafted alongside the LOI.

---

## 11. Risk Register Summary

**Full risk register: 28 risks across 6 categories. Top 10 by priority:**

| # | Risk | Likelihood | Impact | Key Mitigation |
|---|------|-----------|--------|---------------|
| R01 | LW Theatres declines pilot | Medium | Critical | Spektrix network as backup; parallel outreach |
| R02 | Production company (RSC/Nippon) blocks email | Low-Med | High | Use wordmark only; no Ghibli assets |
| R03 | Stripe pre-auth fail rate >15% | Low | High | Pre-auth at T–3, not T–7; eliminates expiry risk |
| R04 | Patron participation rate <5% | Medium | High | Totoro's brand loyalty and family demographic |
| R05 | Solver chain failure | Low | Medium | AllDifferent handles chains natively; individual revert on capture failure |
| R06 | DMCC Act enforcement on pricing | Low | Critical | Zero drip pricing; bid = total price |
| R07 | Solver timeout on large venue | Low-Med | Medium | 120s limit; FEASIBLE accepted if gap <20% |
| R08 | Ticketing API reissuance fails | Medium | High | Manual CSV fallback at MVP |
| R09 | Competitor enters market | Low | Medium | 2–3 year data moat; provisional patent filing |
| R10 | Ghibli IP clearance issue | Low | High | Wordmark-only approach; no characters |

---

## 12. Technology Stack & Architecture

### 12.1 Core Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| API | FastAPI (Python) | Founder's primary language; async-native; OpenAPI auto-generation |
| Database | PostgreSQL 16 | ACID compliance for financial records; performance-level partitioning |
| Job queue | Celery + Redis | T–3 batch jobs; scheduled via Celery Beat |
| Solver | Google OR-Tools CP-SAT | Open source; proven at scale; Python bindings |
| Payment | Stripe Connect | SAQ A PCI scope; SetupIntent + PaymentIntent; Connect for revenue split |
| Email | SendGrid / Postmark | Transactional delivery; white-labelled SMTP domain per venue |
| Frontend | Next.js (patron portal + manager dashboard) | SSR for magic-link landing; React component reuse |
| Infrastructure | AWS (ECS + RDS + ElastiCache) | Mature managed services; EU-West-2 (London) for UK data residency |
| Monitoring | Datadog / Grafana + PagerDuty | Solver job alerting; payment failure alerting |

### 12.2 Scalability Design

The solver is **per-performance-scoped**: each performance's T–3 job is entirely
independent. At 50 venues × 2 shows/day = 100 solver runs/day, each taking 30–90
seconds on 8 cores. A Kubernetes cluster with 20 workers handles this comfortably.
No shared solver state; horizontal scaling is trivially parallelisable.

### 12.3 T–3 Job Sequence

```
[Celery Beat] → preauth_job(performance_id)
    → For each PENDING bid: create PaymentIntent (capture_method=manual)
    → Mark PRE_AUTH_OK or PRE_AUTH_FAILED
    → Enqueue solver_job(performance_id)

[Celery Worker] → solver_job(performance_id)
    → Fetch PRE_AUTH_OK bids + all seated non-bidders (pinned)
    → Compute seat blocks (block pre-computation)
    → Build AllDifferent CP-SAT model (all patrons; non-bidders pinned)
    → Objective: maximise Σ(bid_amount × moved[patron])
    → Solve (120s wall-clock limit)
    → Write bid_outcome[], update bid statuses
    → Enqueue resolution_job(solver_run_id)

[Celery Worker] → resolution_job(solver_run_id)
    → For each MATCHED bid:
        → Compute second price (highest losing bid for section + £1, floor £8)
        → Capture PaymentIntent at second-price amount (partial capture)
        → Reissue ticket → notify patron ("You bid £X, you paid £Y — saved £Z!")
    → For each UNMATCHED bid: cancel PaymentIntent, notify patron (with bid rank + winning price)
    → Push dashboard notification to manager
    → Write post-show analytics record
```

---

## 13. Data Model

### 13.1 Core Entity Catalogue

| Entity | Key Fields | Notes |
|--------|-----------|-------|
| `venue` | venue_id, name, address, ticketing_system_type | One per theatre building |
| `venue_layout` | layout_id, venue_id, name, total_capacity | e.g. "Standard Proscenium 1,295 seats" |
| `section` | section_id, layout_id, name, face_value_pence, desirability_rank, is_upgradeable_from, is_upgradeable_to | Tied to layout |
| `seat` | seat_id, layout_id, section_id, row, number, x, y, adjacent_seat_ids[], accessibility_flag, desirability_score | Includes adjacency for party integrity |
| `production` | production_id, venue_id, layout_id, show_title, genre, start_date, end_date | References specific layout |
| `performance` | performance_id, production_id, curtain_datetime, status, solver_run_at | One per show date/time |
| `seat_state` | performance_id, seat_id, status, assigned_patron_id, hold_type | Dynamic; one row per seat per performance |
| `booking` | booking_id, performance_id, patron_id, seat_ids[], ticketing_ref, sale_price_pence | From ticketing system |
| `patron` | patron_id, email, stripe_customer_id, stripe_payment_method_id | Minimal PII |
| `bid` | bid_id, booking_id, patron_id, performance_id, target_section_id, amount_pence, party_size, willingness_flags, status, stripe_payment_intent_id | Core transactional record |
| `bid_group` | group_id, performance_id, total_party_size, target_section, status | Party assembly |
| `bid_group_member` | group_id, bid_id, booking_ref, party_size | Party assembly |
| `bid_outcome` | outcome_id, bid_id, assigned_seat_ids[], charge_amount_pence, freebie_bundle_id, solver_run_id | Post-solver |
| `solver_run` | solver_run_id, performance_id, triggered_at, completed_at, objective_value_pence, runtime_ms, status, bids_matched_count | Audit per execution |
| `demand_fingerprint` | fingerprint_id, layout_id, production_id, section_id, time_bucket, p_late_sale, avg_late_price_pence | VDF output |
| `inventory_target` | performance_id, section, group_size, min_blocks, shaping_weight_pence | Tetris constraint inputs |
| `seat_block_cache` | solver_run_id, section, block_size, block_idx, seat_ids[] | Pre-computed blocks |
| `payment_event` | event_id, bid_id, stripe_event_type, amount_pence, status, occurred_at | Append-only; 7-year retention |
| `freebie_bundle` | bundle_id, venue_id, description, monetary_value_pence, fulfilment_type | e.g. "Bar credit £10" |
| `sales_history` | venue_id, production_id, seat_id, sale_datetime, sale_price_pence | VDF training data |

### 13.2 Key Design Decisions

- **All money in pence (integer).** No floating point in the financial layer.
- **Venue layout, not venue, is the seat map anchor.** Same building can have multiple
  configurations for different productions.
- **Seat adjacency stored as an array on the seat record.** Pre-computed at upload time;
  used by the block pre-computation algorithm at solver time.
- **payment_event is append-only.** No UPDATE on financial records. Full audit trail.
- **PII minimisation.** `patron` stores email + Stripe token only. Historical bid analytics
  are anonymised before the 2-year retention window expires.

---

## 14. Product Roadmap

### 14.1 Phase Map

```
PHASE 0 — Foundation (Months 1–4, pre-pilot)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Company incorporation
  • ICO data controller registration
  • Stripe Connect account + KYC
  • IP solicitor: AllDifferent solver + SCOS provisional patent application
  • LW Theatres outreach and meeting 1
  • MVP development (incl. hardcoded inventory targets up to group size 6)
  • DPA + LOI legal review

PHASE 1 — Pilot (Months 5–7, Oct–Jan 2026/27)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Gillian Lynne / Totoro: 100 performances
  • Manual CSV reissuance (MVP with hardcoded inventory targets)
  • Data collection: bids, amounts, chains, participation
  • DBIE training data generation
  • Second venue LOI outreach (in parallel, from month 6)
  • Endorsing body / IFV visa process

PHASE 2 — Early Scale (Months 8–18)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Spektrix API integration (automated reissuance)
  • Line-Up API integration (LW Theatres estate)
  • DBIE v1 deployment (guided bid ranges)
  • Party assembly (linked bids)
  • Poisson-driven Dynamic Reserve Pricing (inventory shaping via phantom bids)
  • Upgrade eligibility rules (venue-configurable)
  • 5 venues total → team break-even
  • First hire: backend engineer

PHASE 3 — UK Dominance (Months 18–36)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Tessitura + TixTrack integrations
  • 20+ UK venues
  • DBIE v2 (per-venue fine-tuning)
  • Team: 6–10 people
  • Revenue: £1.0M–£2.65M/year

PHASE 4 — International (Year 3–5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Broadway pilot: 1–2 productions
  • ATG commercial partnership (enterprise)
  • Concert/sports mode
  • Revenue: £5M–£10M+/year
```

### 14.2 Innovation Expansion Opportunities

| Area | Description | Timeline |
|------|-------------|---------|
| Dynamic reserve pricing | Venue sets dynamic floor prices per section based on demand signals. Experimental. | V3 |
| Real-time pricing | Dynamic seat pricing during the bid window based on live demand signals | V3 |
| Fringe simplified | Zone-only bidding; freebie-lateral mechanic; no seat optimisation | V2 |
| NPS integration | Link post-show satisfaction surveys to upgrade status; feed DBIE | V1 |
| Accessibility preferences | Ensure accessibility-seat patrons are never disrupted; allow upgrade bids from standard to accessible where desired | V1 |

---

## Document Inventory

| Document | Version | Purpose |
|----------|---------|---------|
| This document (Master PRD) | 1.0 | Single authoritative source |
| [PRD v0.1](./the_shakeup_prd_v0.1.md) | 0.1 | Original feature manifest |
| [Dataflow v0.2](./the_shakeup_dataflow_v0.2.md) | 0.2 | State machines, phase dataflows, sequence diagrams |
| [Financial, Solver & API v0.1](./the_shakeup_financial_solver_api_v0.1.md) | 0.1 | CP-SAT formulation, API contracts |
| [Extended Solver v0.2](./the_shakeup_solver_extended_v0.1.md) | 0.2 | AllDifferent formulation, party integrity, assembly, Tetris constraints |
| [Scaling Model v0.1](./the_shakeup_scaling_model_v0.1.md) | 0.1 | Per-person pricing, venue count to profit |
| [Legal & Compliance v0.1](./the_shakeup_legal_compliance_v0.1.md) | 0.1 | CRA, DMCC, GDPR, PCI, PSR analysis |
| [Risk Register v0.1](./the_shakeup_risk_register_v0.1.md) | 0.1 | 28 risks, mitigations, prioritisation |
| [GTM Playbook v0.1](./the_shakeup_gtm_playbook_v0.1.md) | 0.1 | Pitch narrative, LOI terms, contacts |
| [UX Flows v0.1](./the_shakeup_ux_flows_v0.1.md) | 0.1 | Patron portal and manager dashboard UX |
| [IFV Narrative v0.1](./the_shakeup_ifv_narrative_v0.1.md) | 0.1 | Innovator Founder Visa endorsement document |

---

*The Shakeup | Confidential | Version 1.0 | 2026-05-26*
*For enquiries: [founder contact details]*
