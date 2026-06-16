# The Shakeup — IFV Strategy, Patent Analysis & V0 Build Order

---

## Part 1: Innovator Founder Visa — Application Strategy

### 1.1 The Three Tests

Every sentence in your application maps to one of these Home Office criteria. The endorsing body (UKES recommended, Innovator International as backup) will assess you against all three in a 45–60 minute video interview.

| Test | What They're Really Asking | Your Strongest Evidence |
|------|---------------------------|----------------------|
| **Innovation** | "Is this genuinely new, or a rebrand of something that exists?" | No one runs a constrained-optimisation auction for reserved-seat upgrades. Airlines do it — theatres don't. The AllDifferent + SCOS + Poisson phantom bid formulation has no known prior art. |
| **Viability** | "Can this person actually execute within 2 years?" | Self-funded (>£1M liquid). Zero external dependency. Pilot venue identified (LW Theatres / Totoro). Full technical architecture designed. Founder is the engineer. |
| **Scalability** | "Will this create UK jobs and economic value?" | £2.65M revenue at 42 venues (Year 3). Broadway expansion planned. 15-person team at scale. Pure SaaS economics — each new venue is marginal cost only. |

### 1.2 What to Highlight — Innovation

The assessor is typically non-technical. Frame innovation in layers, from accessible to deep:

**Layer 1 — The Problem (30 seconds):**
> "Every night in the West End, 200–400 premium seats sit empty while people in cheaper seats would happily pay more to move up. The venue has already lost that revenue. There's no system to capture it."

**Layer 2 — Why Nobody Has Solved It (60 seconds):**
> "Airlines solved this with overbooking and yield management. Theatres can't — because theatre seats are *reserved and named on tickets*. Moving person A to a better seat means person A's old seat must become available for person B, whose old seat must work for person C. It's a cascading chain that must resolve simultaneously, respecting party sizes, aisle boundaries, and the venue's need to keep sellable inventory intact."

**Layer 3 — The Technical Innovation (90 seconds):**
> "We model every patron in the theatre as a variable in a constraint-satisfaction solver. A single mathematical constraint — AllDifferent — ensures no seat is double-booked and chains of any length resolve automatically. The solver then maximises total upgrade revenue subject to party integrity (families stay together), aisle constraints, and inventory shaping. No one has applied this class of algorithm to live entertainment seating."

**Layer 4 — The Evolving IP (only if they dig deeper):**
> "In V0, venue managers manually set aside seats for late sales. By V1, we fit Poisson distributions to historical group-size sales and generate 'phantom bids' — the expected revenue from keeping a seat block intact — that compete directly against real patron bids in the solver's objective function. The system self-tunes."

### 1.3 What to Highlight — Viability

Endorsing bodies want *specificity*, not optimism. Prepare:

| Evidence | What to Show |
|----------|-------------|
| **Named pilot venue** | LW Theatres, Gillian Lynne Theatre, *My Neighbour Totoro*. Name the people you'll contact (Martin Crosier, Matt Simkin). |
| **LOI** (if obtained) | Worth more than any financial projection. Even a non-binding letter from a venue transforms the application. |
| **Unit economics** | Per-show revenue of £912 gross → £228 TS take (conservative). 8 shows/week = £1,768/week TS net from *one* venue. |
| **Self-funding** | >£1M liquid assets. Year 1 total cost: £87k. No dependency on fundraising. |
| **Founder-engineer** | You are the builder. No outsourcing risk. FastAPI/Python, OR-Tools, Next.js — all in your stack. |
| **Risk awareness** | Reference your risk register. They want to hear you say "here's what could go wrong and here's how I mitigate it." |
| **Regulatory homework** | GDPR compliance plan, Consumer Rights Act 2015 analysis, PCI DSS (SAQ A via Stripe). Show you've done the legal work. |

### 1.4 What to Highlight — Scalability

| Argument | Evidence |
|----------|---------|
| **TAM** | UK: 300+ venues, £60M+ addressable. Broadway: 41 houses, £25M+. Global: sports, concerts, opera. |
| **SaaS economics** | Zero setup fee → zero barrier. Each new venue adds ~£50k/year TS revenue at negligible marginal cost. |
| **Job creation** | Hiring plan: first backend engineer at 5 venues, 6–10 people at 20 venues, 15+ at 42 venues. |
| **Ticketing adapter pattern** | Adding a new ticketing system (Spektrix, Tessitura, TixTrack) requires only a new adapter class — weeks, not months. |
| **International** | Broadway pilot planned Year 3. Same solver, same UX, new Stripe region. |
| **Data flywheel** | Each show generates training data for DBIE and VDF. After 100+ shows, the demand model and bid guidance become a moat that takes competitors 2+ years to replicate even if they had the algorithm. |

### 1.5 The Interview

Based on what endorsing bodies typically probe:

| Question Pattern | How to Answer |
|-----------------|---------------|
| *"Can you explain your innovation to me simply?"* | Use Layer 1 + Layer 2 above. Do NOT start with "AllDifferent formulation." Start with empty premium seats. |
| *"Why the UK specifically?"* | West End is the world's second-largest theatre market. LW Theatres operates 8 venues. Concentrated geography = fast iteration. Broadway comes after UK proof. |
| *"What if a ticketing company just adds this?"* | They've had 20+ years and haven't. Their architecture is transactional, not optimisation-based. Adding a constraint solver to Spektrix is a ground-up rewrite, not a feature. Plus — our provisional patent. |
| *"How will you fund this?"* | Self-funded. £87k Year 1. No dilution, no dependency on VCs. Revenue-positive by venue 2. |
| *"What are the risks?"* | Lead with your top 3: venue adoption speed, pre-auth friction reducing bids, and ticketing API access. Then explain each mitigation. |
| *"When will you hire?"* | First hire at 5 venues (~Month 8). Show a chart mapping headcount to venue count. |

### 1.6 Timeline

```
June 2026       LW Theatres outreach begins (cannot slip — Totoro ends Jan 2027)
July 2026       Meeting 1 with LW Theatres
                Endorsing body application submitted to UKES (in parallel — don't wait for LOI)
July–Aug 2026   UKES assessment period (4–8 weeks)
August 2026     Endorsement letter received
                LOI signed with LW Theatres (strengthens but not required for endorsement)
September 2026  IFV visa application submitted
                (3 weeks if applying out-of-country; 8 weeks in-UK)
October 2026    Visa granted → MVP finalised → First T-7 email
November 2026   First real upgrades processed (visa milestone evidence)
```

> [!IMPORTANT]
> **Do NOT apply to two endorsing bodies simultaneously.** They can see duplicate applications and it signals uncertainty. UKES first; Innovator International only if UKES declines.

> [!TIP]
> **The LOI and the endorsement application should run in parallel.** You do not need the LOI to apply. But if you can get even a non-binding LOI from LW Theatres before the interview, it is the single most powerful piece of evidence you can present.

### 1.7 Application Documents to Prepare

| Document | Pages | Status |
|----------|-------|--------|
| Business plan (Innovation / Viability / Scalability structure) | 20–30 | Draft from existing PRD |
| Financial model (5-year P&L, unit economics) | 3–5 | Exists in master PRD §8 |
| Architecture diagram | 1 | Exists in dataflow v0.2 |
| Solver pseudocode | 2–3 | Exists in solver spec |
| Risk register summary | 2 | Exists |
| LOI from LW Theatres | 1 | Not yet obtained |
| Founder CV | 2 | Prepare |
| Market research (West End capacity data) | 2 | Partially in GTM playbook |
| Legal compliance summary (GDPR, CRA 2015) | 2 | Exists in legal doc |

---

## Part 2: Patent & IP Analysis

### 2.1 What's Genuinely Patentable (UK Context)

UK software patents require demonstrating a **"technical effect"** — the algorithm must produce a result that goes beyond a pure business method or mathematical abstraction. Here's the honest assessment:

| Component | Patentable? | Strength | Technical Effect Argument |
|-----------|------------|----------|--------------------------|
| **AllDifferent solver for reserved-seat upgrades** | ✅ Yes — strongest candidate | **Strong** | A constraint-satisfaction formulation applied to a *physical system* (reserved seats in a venue) that produces a provably optimal assignment while preserving party integrity and spatial constraints (aisle boundaries). This isn't generic scheduling — it's a specific application to physical seat reassignment with chain resolution. |
| **SCOS (Seat Chain Opportunity Scorer)** | ✅ Yes — file with AllDifferent | **Medium-Strong** | Vacancy valuation that quantifies the commercial value of residual seat configurations using spatial adjacency analysis. The "technical effect" is computing a measurable physical property (sellability of seat clusters) from graph topology. |
| **Poisson phantom bid mechanism** | ✅ Yes — file separately or as continuation | **Medium** | Per-group-size Poisson demand estimation generating opportunity-cost weights that compete in a unified optimisation objective. The technical effect argument: this is a feedback control system where historical sales data dynamically adjusts constraint weights in a physical seat assignment problem. |
| **DBIE (bid guidance model)** | ❌ Trade secret | — | Pure ML/statistical model. No technical effect argument beyond "we trained a model." Protect as trade secret — the training data is the moat, not the architecture. |
| **VDF (demand fingerprint)** | ❌ Trade secret | — | Statistical pipeline on sales data. Same issue. The value is in the *data*, not the method. |

### 2.2 Recommended Patent Strategy

```
                    ┌─────────────────────────────────────┐
PROVISIONAL FILING  │  AllDifferent Solver + SCOS          │
(before pilot)      │  "Constraint-satisfaction method     │
£170 + agent fees   │   for optimising reserved-seat       │
~£2–3k with IP      │   upgrades in live entertainment     │
solicitor opinion   │   venues with chain resolution"      │
                    └─────────────────────────────────────┘
                                    │
                          12-month priority window
                                    │
                    ┌─────────────────────────────────────┐
CONTINUATION or     │  + Poisson Dynamic Reserve Pricing   │
PCT FILING          │  "Probabilistic inventory shaping    │
(after pilot data)  │   using per-group-size demand        │
                    │   estimation in seat assignment      │
                    │   optimisation"                      │
                    └─────────────────────────────────────┘
```

> [!IMPORTANT]
> **File the provisional BEFORE any public announcement, pilot press, or conference presentation.** UK patent law allows a 12-month priority window from provisional filing. The provisional costs ~£170 in official fees; budget £2–3k total for an IP solicitor to draft claims properly.

> [!WARNING]
> **The IFV narrative doc and legal compliance doc still reference "CUCR + SCOS" as the patent subject.** The master PRD has been updated to "AllDifferent solver + SCOS." These need reconciling before the endorsing body application — the assessor may read all your supporting documents.

### 2.3 The Real Moat (Beyond Patents)

Patents are a speed bump, not a wall — especially in UK software. Your actual defensibility stack:

| Layer | Time to Replicate | Notes |
|-------|-------------------|-------|
| **Provisional patent** | 12–18 months (to design around) | Buys you a head start |
| **Data flywheel** | 2+ years | 100+ shows of bid data, outcome data, demand curves. A competitor starting from zero has nothing to train DBIE or VDF on. |
| **Venue relationships** | 12–18 months | LOIs, DPAs, trust with box office teams. Theatre is a relationship business. |
| **Ticketing integrations** | 6–12 months per system | Each adapter (LineUp, Spektrix, Tessitura) takes weeks to build but months to negotiate API access. |
| **Regulatory compliance** | 3–6 months | GDPR DPA, Consumer Rights Act analysis, PCI DSS scope — a competitor must redo all of this. |

### 2.4 Inconsistencies to Fix Before Filing

The research surfaced these cross-document conflicts that need resolving:

| Issue | Where | Resolution Needed |
|-------|-------|-------------------|
| Revenue split: 80/20 vs 75/25 | Master PRD (80/20) vs Financial Solver API & GTM (75/25) | Decide on one. The LOI terms may differ from general pricing. |
| Patent subject: CUCR vs AllDifferent | IFV narrative & legal doc (CUCR) vs Master PRD (AllDifferent) | Update IFV narrative and legal doc to AllDifferent |
| Auction type: first-price vs second-price at MVP | Financial Solver API (first-price at MVP) vs Master PRD (second-price) | Decide. Second-price is better for bid truthfulness but slightly harder to implement. |
| Pre-auth timing | Original PRD (instant at T-7) vs all later docs (deferred, SetupIntent at bid time) | Later docs are correct. Original PRD is superseded. |

---

## Part 3: V0 Build Order for AI-Assisted Development

### 3.0 Philosophy

The ordering principle is: **build the thing the next thing depends on, and validate it before moving on.** Each phase produces a testable artifact. Don't build the frontend until the API works. Don't build the API until the solver works. Don't build the solver until the data model exists.

### Build Sequence

```
Phase 1   Database Schema + Migrations          ← everything depends on this
  │
Phase 2   Seat Map & Adjacency Graph Engine      ← solver needs spatial data
  │
Phase 3   Core Solver (AllDifferent + Revenue)   ← the product's heart
  │
Phase 4   Inventory Shaping (Hard Constraints)   ← V0 Tetris layer
  │
Phase 5   Party Integrity (Block Variables)      ← groups must stay together
  │
Phase 6   Second-Price Auction Calculation       ← payment amount logic
  │
Phase 7   API Layer (FastAPI)                    ← endpoints for everything above
  │
Phase 8   Stripe Payment Pipeline               ← SetupIntent / PaymentIntent
  │
Phase 9   Email System                           ← T-7, T-4, outcome emails
  │
Phase 10  Patron Portal Frontend (Next.js)       ← seat map, bid entry, basket
  │
Phase 11  Manager Dashboard Frontend (Next.js)   ← setup wizard, solver controls
  │
Phase 12  Integration Testing & Dry Run          ← end-to-end with test data
```

---

### Phase 1: Database Schema + Migrations

**What to build:** PostgreSQL schema for all 16 core entities.

**Key entities (in dependency order):**
1. `venue` → `venue_layout` → `section` → `seat` (with adjacency data)
2. `production` → `performance`
3. `seat_state` (per performance × seat: AVAILABLE, SOLD, UPGRADE_POOL, INVENTORY_HOLD)
4. `booking` → `patron`
5. `bid` (patron_id, performance_id, current_seat_id, target_section_id, max_bid_pence, party_size)
6. `bid_outcome`, `solver_run`, `payment_event`
7. `inventory_target` (section × group_size × min_blocks — the V0 hardcoded targets)
8. `demand_fingerprint`, `sales_history` (empty at V0, but schema should exist)

**Why first:** Every other component reads from or writes to these tables. Getting the schema wrong means rewriting everything downstream.

**Validate by:** Write seed data for Gillian Lynne Theatre (1,300 seats, ~8 sections). Verify you can represent the full seat map with adjacency relationships.

---

### Phase 2: Seat Map & Adjacency Graph Engine

**What to build:**
- Seat adjacency graph construction from layout data
- Aisle boundary detection (seats adjacent by number but separated by an aisle are NOT adjacent)
- Contiguous block pre-computation: enumerate all valid blocks of size 1–6 per row per section
- Block validity: blocks never cross aisles

**Why second:** The solver operates on blocks, not individual seats. Block pre-computation is the bridge between the raw seat map and the solver's variable space.

**Validate by:** Load Gillian Lynne seat data. Print all valid 4-seat blocks in Stalls Centre. Manually verify none cross aisles. Verify block count is reasonable (~50–100 blocks per section per size).

```python
# Expected output format:
# Section: Stalls Centre
#   2-seat blocks: 142
#   3-seat blocks: 98
#   4-seat blocks: 67
#   5-seat blocks: 41
#   6-seat blocks: 22
# No blocks cross aisle boundaries: ✓
```

---

### Phase 3: Core Solver (AllDifferent + Revenue Maximisation)

**What to build:**
- CP-SAT model using Google OR-Tools
- One variable per seated patron (not just bidders)
- Non-bidders: domain = {current_seat} (pinned)
- Bidders: domain = {current_seat} ∪ {eligible target seats}
- `AddAllDifferent` constraint on all patron seat assignments
- `moved[p]` indicator variables (1 if patron moved from current seat)
- Objective: `Maximize Σ(bid_amount × moved[p])` for bidding patrons
- Solver time limit: 120 seconds

**Why third:** This is the product. If the solver doesn't work, nothing else matters.

**Validate by:** Create a test scenario with 50 seated patrons, 10 bidders, known optimal solution. Verify solver finds it. Then scale to 1,300 patrons with 47 bidders (Gillian Lynne scale). Verify it solves in <30 seconds.

---

### Phase 4: Inventory Shaping (Hard Constraints)

**What to build:**
- `intact[block]` binary variables: 1 iff no seat in block is used by an upgrade
- Hard constraint: `Σ intact[section, size, i] >= min_blocks[section][size]`
- Manager-configured targets for group sizes 1–6 per section
- Infeasibility detection: if targets are too aggressive, solver returns 0 upgrades with a diagnostic message

**Why fourth:** Depends on Phase 2 (block pre-computation) and Phase 3 (solver foundation). This adds the Tetris layer that protects day-of sales inventory.

**Validate by:** Set targets (e.g., "preserve 4 pairs in Stalls Centre"). Run solver. Count residual intact pairs. Verify ≥ 4. Then set impossibly high targets and verify graceful failure with diagnostic output.

---

### Phase 5: Party Integrity (Block Variables)

**What to build:**
- For bidders with party_size > 1: replace individual seat variables with block assignment variables `y[bid][block]`
- Constraint: at most one block selected per bid
- When a block is selected, all seats in that block are marked as occupied (linked to `z[seat]` variables)
- Blocks must match party size exactly
- Blocks never cross aisles (already enforced by Phase 2)

**Why fifth:** This is the most complex solver extension. Build it after the core solver and inventory shaping work independently, then integrate.

**Validate by:** Create a party of 4 bidding for Stalls Centre. Verify they're assigned to a contiguous 4-seat block. Verify they're never split. Create a scenario where the only available 4-block crosses an aisle — verify the party is NOT assigned there (stays in current seats).

---

### Phase 6: Second-Price Auction Calculation

**What to build:**
- Post-solve payment calculation:
  - For each target section, rank all bids (winners and losers)
  - Winner pays: max(£8 floor, second-highest bid + £1)
  - If only one bidder for a section: they pay the £8 floor
- Payment amount stored on `bid_outcome`
- Patron notification: "You bid £25. You'll be charged £14." (savings message)

**Why sixth:** Pure business logic that sits between the solver output and payment capture. Depends on solver results but not on the API or frontend.

**Validate by:** Create scenarios with multiple bidders for the same section. Verify payment amounts match second-price rules. Verify no one pays more than their bid. Verify the £8 floor applies correctly.

---

### Phase 7: API Layer (FastAPI)

**What to build (in endpoint groups):**
1. **Auth:** `POST /auth/magic-link/request`, `POST /auth/magic-link/verify`
2. **Venue management:** `POST /venues`, `POST /venues/{id}/layouts`, `PUT /venues/{id}/layouts/{id}/ruleset`
3. **Performance management:** `POST /performances` (with booking data import)
4. **Patron-facing:** `GET /performances/{id}/seatmap`, `POST /bids`, `GET /bids`, `DELETE /bids/{id}`
5. **Manager-facing:** `GET /performances/{id}/dashboard`, `POST /performances/{id}/solver/approve`
6. **Internal:** `POST /internal/solver/run`, `POST /internal/resolution/run`
7. **Webhooks:** Booking created/cancelled from ticketing systems

**Why seventh:** The API is a thin layer over the business logic built in Phases 1–6. Don't build it earlier — you'd be writing endpoints against a moving target.

**Validate by:** Run the full API test suite. Hit every endpoint with test data. Verify the solver endpoint returns correct assignments. Verify bid CRUD works. Verify auth flow works.

---

### Phase 8: Stripe Payment Pipeline

**What to build:**
- `SetupIntent` creation at bid time (stores card, no charge)
- `PaymentIntent` creation at T-3 resolution (pre-auth for max bid amount)
- Capture at second-price amount (partial capture of pre-auth)
- Cancel for losing bids (release pre-auth)
- Refund flow for show cancellations (reverse captured amounts)
- Webhook handlers for Stripe events (payment_intent.succeeded, etc.)
- Error handling: card declined, insufficient funds, expired card

**Why eighth:** Payment is critical but depends on the bid and resolution flow being stable. Don't integrate Stripe until the bid lifecycle is solid.

**Validate by:** Use Stripe test mode. Create a bid, run the solver, verify pre-auth appears on test card, verify capture at correct (second-price) amount, verify losing bids are released. Test card decline scenarios.

---

### Phase 9: Email System

**What to build:**
- SendGrid/Postmark integration with white-label per-venue sender
- Email templates (all white-labelled with venue branding):
  1. **T-7 Offer email:** "You're seeing [show]. Want a better seat?"
  2. **Bid receipt:** "Your bid of £X for [section] has been placed"
  3. **T-4 Reminder:** "Bidding closes in 24 hours"
  4. **Outcome — Won:** "You've been upgraded! New seat: [X]. Charged: £Y (you saved £Z)"
  5. **Outcome — Lost:** "Your bid wasn't selected. No charge."
  6. **Outcome — Card Failed:** "We tried to process your upgrade but your card was declined."
  7. **Show Cancelled:** "The show has been cancelled. Your upgrade bid has been refunded."
- Celery Beat scheduled jobs for T-7 and T-4 triggers

**Why ninth:** Emails are the patron's primary interface with the system. They depend on the bid lifecycle, payment pipeline, and solver results all working correctly.

**Validate by:** Send all 7 email types to a test inbox. Verify rendering, links, white-label branding. Verify Celery Beat triggers at correct times relative to performance datetime.

---

### Phase 10: Patron Portal Frontend (Next.js)

**What to build (screens):**
- A1: Magic link landing page
- A2: Interactive seat map (current seat highlighted, target sections shown, colour-coded by price tier)
- A3: Bid entry (amount input with guidance text, section selector)
- A4: Bid basket (review all bids, edit, delete)
- A5: Pre-bid disclosure + Stripe card entry (legally mandated T&C acceptance)
- A6: Bid confirmation page
- A7: "My bids" status page (shows current bid status)

**Why tenth:** The frontend consumes the API built in Phase 7. Building it earlier means mocking everything — slow and error-prone.

**Validate by:** Full user flow test: receive magic link → view seat map → place bid → store card → confirm → view status. Test on mobile (most patrons will use phones).

---

### Phase 11: Manager Dashboard Frontend (Next.js)

**What to build (screens):**
- B1: Venue onboarding wizard (4 steps: venue details → seat map upload → section config → inventory targets)
- B2: Per-show live dashboard (bid count, bid amounts, participation rate, revenue projection)
- B3: Solver review screen (approve/reject solver output, view seat assignments)
- B4: Resolution monitoring (payment capture progress, failures, retry actions)
- B5: Post-show analytics report (funnel: emails sent → opened → bids placed → upgrades confirmed → revenue)

**Why eleventh:** The manager dashboard is important but not on the critical path for the *patron* experience. A venue manager can operate V0 with API calls and CSV exports if the dashboard slips.

**Validate by:** Full manager flow: create venue → upload seat map → configure sections → set inventory targets → view live bids → approve solver → monitor resolution → view analytics.

---

### Phase 12: Integration Testing & Dry Run

**What to build:**
- End-to-end test harness simulating a full performance lifecycle:
  1. Seed venue + seat map + performance + bookings
  2. Trigger T-7 emails
  3. Simulate 47 bids with varying amounts and party sizes
  4. Trigger T-3 solver run
  5. Verify solver output (correct assignments, party integrity, inventory preserved)
  6. Run resolution (Stripe captures, email outcomes)
  7. Verify final state (all bids resolved, correct charges, correct emails)
- Load test: 1,300 patrons, 100 bids, solve in <120s
- Chaos test: card declines mid-resolution, solver timeout, email delivery failure

**Why last:** You can't integration-test what doesn't exist. This validates the full chain.

**Validate by:** Green end-to-end suite. Zero seat conflicts. Zero double-charges. Solver solves within time limit. All emails render correctly.

---

### Build Effort Estimates

| Phase | Estimated Effort | Cumulative |
|-------|-----------------|-----------|
| 1. Database schema | 2–3 days | 3 days |
| 2. Seat map & adjacency | 3–4 days | 1 week |
| 3. Core solver | 4–5 days | 2 weeks |
| 4. Inventory shaping | 2–3 days | 2.5 weeks |
| 5. Party integrity | 3–4 days | 3 weeks |
| 6. Second-price auction | 1–2 days | 3.5 weeks |
| 7. API layer | 5–7 days | 5 weeks |
| 8. Stripe pipeline | 4–5 days | 6 weeks |
| 9. Email system | 3–4 days | 7 weeks |
| 10. Patron portal | 5–7 days | 8.5 weeks |
| 11. Manager dashboard | 5–7 days | 10 weeks |
| 12. Integration testing | 3–5 days | 11 weeks |

> [!NOTE]
> These estimates assume AI-assisted development (you're prompting an AI coding agent for each phase). The AI dramatically accelerates boilerplate (API endpoints, DB migrations, email templates) but the solver phases (3–5) require careful human review of constraint logic. Budget extra time there.

### What to Give the AI at Each Phase

For best results with an AI coding agent, provide at each phase:

| Phase | Key Reference Documents |
|-------|------------------------|
| 1 | Master PRD §13 (Data Model), Dataflow v0.2 (entity definitions) |
| 2 | Solver Extended Spec §1.1 (seat adjacency graph), §2.1 (block pre-computation) |
| 3 | Solver Extended Spec §0, §2.2–2.3 (AllDifferent formulation, pseudocode) |
| 4 | Solver Extended Spec §4.1–4.3 (inventory shaping constraints) |
| 5 | Solver Extended Spec §2.1–2.3 (party integrity, block variables) |
| 6 | Master PRD §5.1 Phase 5, §8.1 (second-price rules) |
| 7 | Financial Solver API v0.1 §4–5 (full endpoint specifications) |
| 8 | Master PRD §12.3 (T-3 job sequence), Financial Solver API §3 (Stripe flow) |
| 9 | UX Flows v0.1 §A1, A8, A9 (email templates and copy) |
| 10 | UX Flows v0.1 §A2–A7 (patron screens, interaction flows) |
| 11 | UX Flows v0.1 §B1–B6 (manager screens) |
| 12 | GTM Playbook §4.3 (pilot KPIs — use as acceptance criteria) |

---

> [!CAUTION]
> **Before coding, resolve the cross-document inconsistencies identified in Part 2.4.** The revenue split (80/20 vs 75/25), auction type (first-price vs second-price at MVP), and patent subject (CUCR vs AllDifferent) must be decided — otherwise you'll build against conflicting specs.
