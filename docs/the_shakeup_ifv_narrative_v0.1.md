# The Shakeup — Innovator Founder Visa Endorsement Narrative
### Version 0.1 | 2026-05-26
### Prepared for: Endorsing Body Application (UKES / Innovator International / Envestors)

---

> **Important:** This document is structured precisely around the three Home Office
> endorsement criteria: **Innovative**, **Viable**, and **Scalable**. Every section
> maps to one of these three tests. Endorsing bodies use these exact headings to
> assess applications — your business plan should mirror this structure.

---

## Executive Summary (One Page)

**Business name:** The Shakeup

**Sector:** Technology (B2B2C SaaS) applied to the performing arts / live entertainment

**One-line description:**
The Shakeup is a seat upgrade marketplace for live theatre — a combinatorial
optimisation platform that matches advance-booking theatre patrons with better seats
through a sealed-bid auction, generating incremental revenue for venues while
improving audience experience.

**The problem:**
West End theatres — the world's second largest theatrical market — operate with
chronic late-stage seat inventory waste. Premium central seats go unsold as day-seats
at steep discounts, while advance-booking patrons who paid full price sit in restricted-
view or peripheral seats they would gladly upgrade from if given the opportunity.
No technology platform exists to capture this value.

**The solution:**
The Shakeup runs a T-minus-7-day upgrade offer to eligible patrons, a T-minus-3-day
sealed-bid solver that maximises revenue across the full seat graph using constraint
programming (Google OR-Tools CP-SAT), and an automated payment and ticket reissuance
pipeline. Venue partners receive 80% of upgrade revenue with zero upfront cost.

**The founder:**
Joe Katz is a professional Data Engineer with deep expertise in Python, SQL,
optimisation algorithms, and backend system architecture — precisely the technical
profile required to build and operate this platform. He has conducted formal market
research with theatre professionals validating the demand, identified the pilot
production and venue (My Neighbour Totoro, Gillian Lynne Theatre / LW Theatres), and
developed a comprehensive product specification, solver formulation, and go-to-market
strategy prior to this application.

**Funding:**
Self-funded. The founder holds in excess of £1,000,000 in liquid assets. No external
investment is required to reach the pilot launch milestone (MVP estimated cost: £40–60k)
or the team-scale milestone (estimated £180k for first 18 months).

**Pilot target:** October 2026
**UK break-even:** 5 venues (~12 months post-pilot)
**UK profitable scale:** 42 venues (~24–36 months post-pilot)

---

## CRITERION 1: INNOVATIVE

*"Your business idea must be new and original. It must be genuinely different from
anything currently on the market."*

### 1.1 What Exists Today

Seat upgrade bidding is not a new concept in adjacent sectors:

- **Hotels:** Marriott Bonvoy and Hilton's bidding systems (powered by Nor1/Plusgrade)
  allow guests to bid for room upgrades. Widely deployed globally.
- **Airlines:** Airlines use upgrade auction systems for Business/First class seats.
  Common across major carriers.
- **Sports:** Some sports venues use dynamic pricing tools for seat changes.

**The critical distinction: these systems do not apply to reserved-seat theatre.**
Every implementation in hotels, airlines, and sports treats the upgrade unit as a
homogeneous category (room type, seat class) — not as a specific physical seat in a
precise geometric layout with adjacency constraints, restricted-view characterisations,
party integrity requirements, and downstream chain effects.

**No platform exists anywhere in the world that applies combinatorial optimisation
to reserved-seat theatre seat upgrades.**

A systematic search of:
- UK Companies House (theatre technology)
- Spektrix, Tessitura, Line-Up, ATG Ticketing partner directories
- US patent database (USPTO) for theatre seat upgrade algorithms
- Academic literature (operational research applied to performing arts)
- West End trade press (The Stage, WhatsOnStage) for competing products

...returns zero direct competitors. The concept exists in founder journals and
academic discussions but has never been commercialised as a product.

### 1.2 What Makes The Shakeup Genuinely Novel

**Innovation 1: The Theatre-Specific Constraint Problem**

Theatre seat management is fundamentally different from hotel or airline upgrades
because of four properties that do not exist in those domains:

1. **Party integrity:** A booking of N seats must be upgraded atomically — all N
   seats must move to a contiguous block. A family of 4 cannot be scattered to
   four different rows. This requires pre-computing valid seat blocks from the
   seat map graph before the solver runs.

2. **Upgrade chains (CUCR — Cascading Upgrade Chain Resolver):** When patron A
   upgrades from Section X to Section Y, their vacated seats in Section X become
   newly available. If patron B has bid to move from Section Z to Section X, patron B
   can now be satisfied — but only if the CUCR recognises and exploits this chain.
   A naïve independent-assignment solver misses this entirely. The CUCR is a
   pre-processing step that decomposes the full seat graph into exploitable chains
   before the CP-SAT solver runs, increasing total upgrade volume by an estimated
   40–80% per show.

3. **Inventory shaping (the Tetris constraint):** After all upgrades are assigned,
   the residual available seats have commercial value to the venue's day-of sales.
   A pair of adjacent available seats sells to a couple; an isolated single does not.
   The Shakeup's solver includes residual configuration constraints — it optimises
   upgrade assignments to simultaneously maximise upgrade revenue AND preserve
   commercially useful residual seat configurations. No yield management system in
   any sector implements this.

4. **Multi-section demand fingerprinting (VDF):** The Venue Demand Fingerprint models
   historical sell-through rates at section-row granularity, time-of-week, weeks-to-
   performance, and show phase (early run vs. mid-run vs. late-run). This determines
   the optimal inventory hold per section per performance — the set of seats to exclude
   from the upgrade pool because they will likely sell at full price. No theatre
   technology currently provides section-level sell-through prediction.

**Innovation 2: The Deferred Pre-Auth Saga**

Standard e-commerce captures payment at purchase. The Shakeup captures payment only
after the upgrade is confirmed — but must verify funds 3 days before the show to
inform the solver. This creates a unique payment flow: SetupIntent at bid placement
(SCA-compliant, MIT-flagged), pre-auth at T-3, capture only on solver confirmation.
This eliminates the Stripe 7-day capture expiry problem that would otherwise make
T-7 pre-auth commercially infeasible. The "deferred pre-auth saga" pattern is novel
in the theatre ticketing domain.

**Innovation 3: Bid-Aware Inventory Management**

The Shakeup is the first platform to unify the seat upgrade marketplace, the yield
management function, and the inventory optimisation function into a single solver run.
The CP-SAT objective function simultaneously maximises:
- Total upgrade revenue from confirmed bids
- Chain-exploited upgrade volume (CUCR contribution)
- Residual inventory commercial value (Tetris constraint soft objective)

Existing theatre technology (Spektrix, Line-Up, Tessitura) handles ticketing
transactions but has no yield management intelligence. Existing yield management
tools (if used in theatre at all) are revenue analysts' spreadsheets.

### 1.3 Proprietary Components

The following components constitute The Shakeup's proprietary algorithmic core:

| Component | Acronym | Function | IP Status |
|-----------|---------|----------|-----------|
| Cascading Upgrade Chain Resolver | CUCR | Decomposes seat graph into chains; feeds CP-SAT | Patent application to be filed |
| Seat Chain Opportunity Scorer | SCOS | Scores chain configurations by revenue potential | Part of CUCR filing |
| Demand-Based Inventory Engine | DBIE | ML model predicting section sell-through by show/time | Trade secret |
| Venue Demand Fingerprint | VDF | Per-venue, per-section historical demand model | Trade secret |

**Patent strategy:** A provisional UK patent application covering the CUCR + SCOS
combination applied to reserved-seat venue upgrade management is planned for filing
before the pilot announcement. UK provisional patent cost: approximately £170 + agent fees.

---

## CRITERION 2: VIABLE

*"Your business plan must be realistic and achievable. You must demonstrate sound
market research, a clear operational strategy, and that you have the skills to execute."*

### 2.1 Market Research Validation

Prior to this application, the founder conducted formal market research including:

- Survey-based demand analysis with UK theatre patrons (conducted May 2024)
- Desk research into West End occupancy patterns, day-seat pricing, and inventory
  management practices
- Mapping of the West End ticketing technology landscape (Spektrix, Line-Up, ATG, Tessitura)
- Financial modelling of unit economics for the Gillian Lynne Theatre / My Neighbour
  Totoro production as the primary pilot case
- Identification of named venue contacts and outreach strategy (Martin Crosier, MD,
  LW Tickets; Matt Simkin, Head of Commercial, LW Theatres)

**Key validated findings:**
1. West End occupancy averages 78% annually but varies from 55% (mid-week, limited
   run) to 99% (Saturday evening, long-running hit). The upgrade opportunity exists
   on all shows below approximately 92% occupancy.
2. Theatre patrons who book in advance pay a premium of £30–50 over restricted-view
   seats for the same performance — this spread is the upgrade bid ceiling.
3. No venue currently operates a patron-facing upgrade bidding system. The category
   is entirely unaddressed.
4. Spektrix, the leading independent venue ticketing system (650+ UK venues), offers
   an open API partner programme — the technical integration path is documented and free.

### 2.2 Founder Credentials

The founder brings the precise technical and commercial profile required:

**Technical (Data Engineering):**
- Proficient in Python (primary implementation language), SQL (PostgreSQL),
  and pipeline architecture (Apache Airflow / Celery / Redis)
- Experience with optimisation and heuristic methods directly applicable to the
  CP-SAT solver implementation
- Backend system architecture: API design, database schema, job scheduling,
  observability
- This profile is unusual in theatre technology — The Shakeup's competitive
  moat depends on algorithmic complexity that most theatre technology companies
  cannot replicate

**Commercial:**
- Conducted independent market research demonstrating product-market fit
- Developed a full go-to-market playbook including a three-meeting sales process,
  LOI term structure, and identified named contacts at the primary pilot partner

**Relevant gap & mitigation:**
The founder does not have direct theatre industry experience. Mitigation:
- Named LOI targets in senior commercial roles at LW Theatres — this validates
  the business model independently of the founder's theatre background
- The product is B2B2C; the venue relationship is the commercial foundation,
  and the founder's data engineering credibility is more relevant than theatre
  domain expertise in the sales conversation

### 2.3 Operational Plan

**Phase 0 — Pre-pilot (months 1–4):**
- Incorporate The Shakeup Ltd (done / immediate)
- Register as ICO data controller (£40/year — mandatory for GDPR compliance)
- Stripe Connect account setup and KYC verification
- IP solicitor consultation: CUCR + SCOS provisional patent application
- Outreach to LW Theatres / Martin Crosier (target: meeting within 4 weeks)
- MVP development: CSV seat map ingest, bid portal, solver, manual reissuance
- DPA and LOI drafted and reviewed by solicitors

**Phase 1 — Pilot (months 5–7, targeting October 2026):**
- Single venue (Gillian Lynne / My Neighbour Totoro)
- ~100 performances across 3 months
- Manual box office reissuance (MVP)
- Data collection: bid volumes, bid amounts, chain effects, participation rates
- Target: 15–25 upgrades per show, £200–500 gross upgrade revenue per show

**Phase 2 — Early scale (months 8–18):**
- Second venue LOI signed during Phase 1 (parallel, not sequential)
- Line-Up API integration for automated reissuance (LW Theatres)
- Spektrix API integration for independent venues
- Target: 5 venues, break-even on operating costs
- First hire: product engineer (Python/backend)

**Phase 3 — UK scale (months 18–36):**
- 10–20 venues across West End and UK regional
- DBIE ML model trained on pilot + Phase 2 data (sufficient volume)
- Stripe Connect group deal with LW Theatres estate
- Target: £1.5M annual revenue, team of 5–7

### 2.4 Financial Projections

**Start-up costs (self-funded, Year 1):**
| Item | Cost |
|------|-----|
| Incorporation, legal, DPA, IP | £8,000 |
| MVP development (founder's own time + tooling) | £12,000 |
| Stripe Connect setup, infrastructure | £4,000 |
| Marketing, pilot collateral | £3,000 |
| Operating reserve (12 months) | £60,000 |
| **Total Year 1 outlay** | **£87,000** |

All self-funded from founder's liquid assets (>£1,000,000). No external investment required.

**Revenue projections (with guidance, 80/20 split, £10/seat average):**
| Stage | Venues | TS Revenue/year |
|-------|--------|----------------|
| Pilot (3 months) | 1 | £14,400 (annualised) |
| Year 1 end | 5 | £252,000 |
| Year 2 end | 20 | £1,010,000 |
| Year 3 end | 42 | **£2,650,000** |
| Year 5 | 100 UK + 20 Broadway | **£7,200,000** |

**Path to profitability:** 5 venues covers a 2-person operating cost base.
10 venues covers a 5-person team. No external funding required for this trajectory.

---

## CRITERION 3: SCALABLE

*"You must demonstrate the potential for significant growth and job creation,
with a clear strategy for expanding into national and international markets."*

### 3.1 UK Market Size

**Total addressable market — UK theatre:**
- ~1,400 professional theatre venues in the UK (UK Theatre / SOLT data)
- ~250 active at any given time with 5+ shows/week
- ~50 major West End productions running simultaneously
- Total seats in West End: ~50,000 per night × 8 performances/week
  = 400,000 seat-nights/week

**Serviceable addressable market:**
- West End (50 productions, avg 1,100 seats): 50 venues
- UK regional major venues (100 venues, avg 600 seats): 100 venues
- Subtotal: 150 venues

**At 150 UK venues (Scenario B — calibrated guidance):**
Revenue: ~£9M/year for The Shakeup

The Shakeup does not need to capture the entire UK market to be highly profitable.
42 venues = £2.65M/year = a genuinely profitable, sustainable business with a 10+ person team.

### 3.2 International Expansion

**Broadway (Stage 3, Year 3–4):**
- 40+ Broadway productions running simultaneously
- Average house: ~1,700 seats
- Higher price tolerance: average bid modelled at £25/seat (vs. £10–18 UK)
- Regulatory differences: no PSD2 SCA requirement (US payment rules); different
  ticketing systems (TodayTix, Telecharge, OvationTix)
- Entry strategy: establish UK pilot data and UK brand credibility first; approach
  one Broadway producer with UK pilot case study in Year 3

**Additional markets:**
- Germany (Berlin, Hamburg — strong musical theatre scene; Ticketmaster-dominated)
- Australia (Sydney Opera House, Melbourne Theatre Company)
- North America touring circuit (45 touring productions annually)

**Long-term TAM (global live theatre, upper bound):**
~5,000 professional venues globally running 10+ shows/week.
At average £250/week The Shakeup revenue per venue: **£65M/year** total addressable.

### 3.3 UK Job Creation Plan

| Timeline | Headcount | Roles |
|---------|-----------|-------|
| Year 1 (Pilot) | 1 (founder) | Founder/CEO/CTO |
| Year 1 end | 2 | + Backend Engineer |
| Year 2 | 4 | + Customer Success + Product Manager |
| Year 2 end | 6 | + 2nd Engineer + Sales |
| Year 3 | 10 | + Data Scientist (DBIE) + 3 engineers + Marketing |
| Year 5 | 20+ | Full product, engineering, commercial teams |

All roles based in London (UK). The engineering roles require senior Python/data
engineering skills — contributing to the UK tech talent pipeline. The data science
role (Year 3) develops original ML methodology in the operational research domain.

### 3.4 Scalability Architecture

The platform is architected for horizontal scale from day one:
- Stateless API layer (FastAPI/Python) — horizontally scalable
- Per-performance job queue (Celery/Redis) — each performance's solver run is
  an independent, parallelisable job
- PostgreSQL with performance-level partitioning — queries on a 50-venue system
  are identical in structure to a 1-venue system; index design scales linearly
- The CP-SAT solver is single-performance-scoped — 1,000 simultaneous performances
  across 50 venues run as 1,000 independent jobs. No shared solver state.

**Bottleneck analysis:** The only potential scaling constraint is the T-3 batch window,
when many performances (across all venues) trigger simultaneously. At 50 venues ×
average 2 shows/day = 100 solver runs/day. Each run takes 30–90 seconds on 8 cores.
A modest Kubernetes cluster with 20 workers handles this comfortably.

---

## Endorsing Body Strategy

### Which Body to Apply To

As of May 2026, three bodies can issue new IFV endorsements:

| Body | Best fit | Fee | Notes |
|------|---------|-----|-------|
| **UKES (UK Endorsing Services)** | Technology + creative sector | ~£1,000 | Broadest remit; most applications processed |
| **Innovator International** | Tech-forward, international ambition | ~£1,000 | Good for founder with global expansion plan |
| **Envestors Limited** | Investment-ready businesses | ~£1,000 | Better fit if raising; less relevant here |

**Recommendation: UKES as primary, Innovator International as backup.**

UKES processes the largest volume of IFV endorsements across sectors. The Shakeup
sits clearly in the technology/innovation category and does not require a sector-
specific body. Innovator International is a strong backup given the Broadway and
international expansion narrative.

**Do not apply to both simultaneously** — endorsing bodies can see multiple applications
and this signals uncertainty about the business concept.

### Endorsement Interview Preparation

The endorsement assessment typically involves a 45–60 minute interview (video call)
with an assessor from the endorsing body. The assessor is looking for:

1. **Can the founder explain the innovation clearly to a non-technical audience?**
   Prepare a 90-second plain-English explanation of what The Shakeup does, who it
   serves, and why it doesn't exist already.

2. **Is the business plan specific and evidenced?** Generic plans fail. The assessor
   wants to see named venues, real financial projections with named assumptions,
   a timeline that could be cross-checked.

3. **Does the founder understand the risks?** Assessors are suspicious of founders
   who haven't thought about what could go wrong. Referencing the risk register
   (venue adoption friction, solver complexity, market timing) demonstrates maturity.

4. **Is the UK specifically the right market first?** This is the visa's core
   question. Answer: West End is the world's second largest theatrical market.
   The ticketing infrastructure (Spektrix, Line-Up) is more open and standardised
   than Broadway. UK consumer protection law (DMCC Act) actually creates useful
   guardrails for the pricing model. The UK pilot creates the credibility needed
   for Broadway and international expansion.

**Anticipated hard questions and prepared answers:**

*Q: "Why can't Ticketmaster or See Tickets just build this?"*
A: They can, eventually. But The Shakeup has a 2–3 year data moat advantage. The
demand fingerprint and chain resolver trained on 50+ shows is not replicable by
a late entrant. We are also targeting independent venues and non-Ticketmaster
properties specifically — the underserved segment.

*Q: "What if the first venue doesn't work out?"*
A: We have named backup venues in the Spektrix network (650 UK venues with open API
access). The technology works at any venue using a standard ticketing system. The
first venue failure would mean we go to the second venue faster, not that we stop.

*Q: "How is this different from just selling day seats more aggressively?"*
A: Day seats go to whoever shows up at the box office window that morning. Our system
specifically rewards advance-booking loyal patrons — the people who committed to the
show months ago — by giving them a premium upgrade opportunity before anyone else.
The venue's day-of sales are explicitly protected by the inventory shaping constraints.
These are completely different mechanisms serving different audience segments.

*Q: "What's your background in theatre?"*
A: Direct theatre experience is not the relevant credential for building this product.
The relevant credential is data engineering and optimisation systems — which is the
technical foundation this product requires. I have conducted formal market research
with theatre professionals, identified named contacts at the target venue, and designed
the product around the specific operational constraints of West End theatre. The venue
relationship provides the theatre expertise; I provide the algorithmic capability.

---

## Business Plan Structure (for Formal Submission)

The formal business plan document submitted to the endorsing body should be
structured as follows (total: 20–30 pages, excluding appendices):

```
1. Executive Summary (2 pages)
   → One-liner, problem, solution, ask

2. INNOVATION (5–7 pages)
   → What exists today and why it doesn't work
   → The four novel technical contributions (CUCR, SCOS, Tetris, VDF)
   → Why this cannot be easily replicated
   → Patent strategy

3. VIABILITY (8–10 pages)
   → Market research findings
   → Founder credentials and relevant experience
   → Operational plan with milestones and dates
   → Financial projections (3-year detailed, 5-year summary)
   → Risk register (summary — 5 highest risks with mitigations)
   → Legal and regulatory compliance framework

4. SCALABILITY (5–7 pages)
   → UK market sizing (TAM/SAM/SOM)
   → International expansion strategy (Broadway + Europe)
   → Job creation plan
   → Technical architecture scalability

5. Appendices
   A. Founder CV
   B. Financial model (detailed spreadsheet)
   C. Market research summary
   D. Letters of support / interest (if any — an LOI from LW Theatres
      dramatically strengthens this section)
   E. Technical architecture diagram
   F. Solver pseudocode summary (demonstrates technical depth)
```

**The single most valuable addition to any IFV application: a Letter of Intent.**
If LW Theatres or any other named venue provides even a non-binding LOI expressing
interest in the pilot, the endorsing body treats this as independent validation of
viability. This is worth more than any financial projection. The GTM outreach to
Martin Crosier is therefore not just a business milestone — it is a critical input
to the visa application itself.

---

## Visa Timeline Integration

```
June 2026      Outreach to LW Theatres (Martin Crosier / Matt Simkin)
July 2026      Meeting 1 with LW Theatres
               → Endorsing body application submitted to UKES
July–Aug 2026  Endorsement assessment (typically 4–8 weeks from submission)
August 2026    Endorsement letter received
               LOI signed with LW Theatres
September 2026 IFV visa application submitted to Home Office
               (typically 3 weeks processing for out-of-country application;
                8 weeks if applying from within the UK on a different visa)
October 2026   Visa granted / entry to UK
               MVP development finalised
               DPA signed with LW Theatres
               First T-7 email sent to Totoro patrons
November 2026  First real upgrades processed ← visa milestone evidence
```

**Critical: the LW Theatres LOI and the endorsement application should run in parallel,
not sequentially.** Apply to the endorsing body as soon as the business plan is ready —
you do not need the LOI to apply. But if the LOI arrives before the endorsement
decision, submit it as supplementary evidence immediately.
