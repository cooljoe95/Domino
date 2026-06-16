# The Shakeup — Dataflow Specification
### Version 0.1 | 2026-05-25

---

## 1. System Context (C4 Level 1)

```mermaid
graph TD
    subgraph External["External Systems"]
        TKT["🎭 Theatre Ticketing System<br/>(Spektrix / Tessitura / CSV)"]
        STRIPE["💳 Stripe<br/>(PaymentIntents + Connect)"]
        EMAIL["📧 Email Provider<br/>(SendGrid / Postmark)"]
        WEATHER["🌦 Weather API<br/>(Open-Meteo)"]
        CALENDAR["📅 Events Calendar API<br/>(local event feed)"]
    end

    subgraph Shakeup["The Shakeup Platform"]
        PORTAL["Patron Bid Portal<br/>(Web App)"]
        MGRDASH["Manager Dashboard<br/>(Web App)"]
        API["Core API<br/>(REST + Webhooks)"]
        SOLVER["Upgrade Solver<br/>(OR-Tools CP-SAT)"]
        DBIE["Demand Intelligence<br/>(DBIE / VDF)"]
        DB[("Primary Database<br/>(Postgres)")]
        QUEUE["Job Queue<br/>(scheduled batch jobs)"]
    end

    PATRON["👤 Patron"] --> PORTAL
    MANAGER["🏢 Theatre Manager"] --> MGRDASH
    PORTAL --> API
    MGRDASH --> API
    API --> DB
    API --> STRIPE
    API --> EMAIL
    QUEUE --> SOLVER
    SOLVER --> DB
    DBIE --> DB
    API --> TKT
    DBIE --> WEATHER
    DBIE --> CALENDAR
```

---

## 2. Data Entity Catalogue

These are the core tables/documents that data flows through. Every flow below reads or writes these.

| Entity | Key Fields | Notes |
|--------|-----------|-------|
| `venue` | venue_id, name, ticketing_system_type, config_json | One row per theatre building |
| `production` | production_id, venue_id, show_title, genre, start_date | One show run (e.g., "Hamilton — May 2026") |
| `performance` | performance_id, production_id, curtain_datetime, solver_run_at, status | One individual show date/time |
| `seat` | seat_id, venue_id, section_id, row, number, x_coord, y_coord, accessibility_flag, desirability_score | Static; set at venue onboarding |
| `section` | section_id, venue_id, name, face_value_£, desirability_rank, is_upgradeable_from, is_upgradeable_to | Defines upgrade direction |
| `seat_state` | seat_state_id, performance_id, seat_id, status, assigned_patron_id, hold_type | Dynamic per-performance seat map |
| `booking` | booking_id, performance_id, patron_id, original_seat_ids[], ticketing_ref, booking_source | Sourced from theatre ticketing system |
| `patron` | patron_id, email, phone, magic_link_token, token_expires_at | Minimal PII — no account needed at MVP |
| `bid` | bid_id, booking_id, patron_id, performance_id, target_section_id, max_bid_£, willingness_flags, status, payment_intent_id, created_at | Core transactional record |
| `bid_outcome` | outcome_id, bid_id, assigned_seat_id, charge_amount_£, freebie_bundle_id, solver_run_id | Written by solver post-resolution |
| `solver_run` | solver_run_id, performance_id, triggered_at, completed_at, objective_value, runtime_ms, status | Audit record per solver execution |
| `sales_history` | record_id, venue_id, production_id, seat_id, sale_datetime, sale_price_£ | Uploaded by manager; feeds VDF + DBIE |
| `demand_fingerprint` | fingerprint_id, venue_id, production_id, zone_id, time_bucket, p_late_sale, avg_late_price_£, velocity | Output of VDF pipeline |
| `freebie_bundle` | bundle_id, venue_id, description, monetary_value_£, fulfilment_type | e.g., "Bar credit £10 + programme" |
| `payment_event` | event_id, bid_id, stripe_event_type, amount_£, status, occurred_at | Append-only Stripe webhook log |

---

## 3. State Machines

### 3a. Bid Lifecycle

```mermaid
stateDiagram-v2
    [*] --> DRAFT : Patron starts bid form
    DRAFT --> PENDING : Card pre-auth succeeds (Stripe PI created)
    DRAFT --> ABANDONED : Patron exits without completing
    PENDING --> MATCHED : Solver assigns a seat
    PENDING --> UNMATCHED : Solver finds no feasible seat
    MATCHED --> CONFIRMED : Payment capture succeeds
    MATCHED --> CAPTURE_FAILED : Payment capture fails (retry exhausted)
    CONFIRMED --> [*] : New ticket issued
    UNMATCHED --> [*] : Pre-auth released
    CAPTURE_FAILED --> [*] : Pre-auth released, original seat retained
    ABANDONED --> [*]
```

### 3b. Seat State (per Performance)

```mermaid
stateDiagram-v2
    [*] --> AVAILABLE : Performance created
    AVAILABLE --> SOLD : Booking confirmed by ticketing system
    AVAILABLE --> HELD : Manager sets inventory hold
    SOLD --> BID_VACATING : Patron bids to leave this seat (bid = PENDING)
    BID_VACATING --> SOLD : Bid becomes UNMATCHED or CAPTURE_FAILED
    BID_VACATING --> VACATED : Bid becomes CONFIRMED — seat released
    VACATED --> AVAILABLE : Released back to venue inventory
    HELD --> AVAILABLE : Hold removed by manager
    SOLD --> [*] : Performance completes
    AVAILABLE --> [*] : Performance completes (unsold)
    VACATED --> SOLD : (edge case) Late purchaser buys the vacated seat
```

### 3c. Payment State (Stripe PaymentIntent)

```mermaid
stateDiagram-v2
    [*] --> REQUIRES_PAYMENT_METHOD : PI created
    REQUIRES_PAYMENT_METHOD --> REQUIRES_CONFIRMATION : Card details submitted
    REQUIRES_CONFIRMATION --> REQUIRES_CAPTURE : Pre-auth succeeded ✅
    REQUIRES_CONFIRMATION --> FAILED : Card declined ❌
    REQUIRES_CAPTURE --> SUCCEEDED : Capture at T-3 ✅
    REQUIRES_CAPTURE --> CANCELED : Bid unmatched — pre-auth released
    SUCCEEDED --> [*]
    CANCELED --> [*]
    FAILED --> [*]
```

---

## 4. Phase-by-Phase Dataflow

### Phase 0: Venue Onboarding (One-time per Venue)

```mermaid
sequenceDiagram
    actor Manager
    participant Dashboard
    participant API
    participant DB
    participant VDF as VDF Pipeline

    Manager->>Dashboard: Upload seat map (JSON / CSV)
    Dashboard->>API: POST /venues/{id}/seatmap
    API->>DB: INSERT seat[], section[] records
    API-->>Dashboard: Seat map preview rendered

    Manager->>Dashboard: Configure upgrade ruleset
    Note over Manager,Dashboard: Which sections upgrade from/to,<br/>freebie bundles, blackout seats,<br/>inventory hold defaults
    Dashboard->>API: POST /venues/{id}/ruleset
    API->>DB: UPDATE venue.config_json

    Manager->>Dashboard: Upload historical sales CSV
    Dashboard->>API: POST /productions/{id}/sales-history (multipart)
    API->>DB: BULK INSERT sales_history[]
    API->>VDF: Trigger VDF pipeline job
    VDF->>DB: READ sales_history WHERE production_id = X
    VDF->>VDF: Compute zone × time_bucket demand matrix
    VDF->>DB: UPSERT demand_fingerprint[] records
    VDF-->>API: Pipeline complete
    API-->>Dashboard: "Demand fingerprint ready — recommended hold counts updated"
```

**Data written in this phase:**
- `venue`, `seat[]`, `section[]` (static; never changes unless venue is refurbished)
- `venue.config_json` (upgrade ruleset)
- `sales_history[]` (raw input)
- `demand_fingerprint[]` (derived output — drives all future inventory recommendations)

---

### Phase 1: Performance Setup (T–14 to T–7)

```mermaid
sequenceDiagram
    participant TKT as Theatre Ticketing System
    participant API
    participant DB
    participant QUEUE
    participant EMAIL

    TKT->>API: Webhook / nightly sync: performance_id, curtain_datetime, seat_bookings[]
    Note over TKT,API: Each booking: booking_ref, seat_id[], patron_email,<br/>sale_price, sale_datetime
    API->>DB: UPSERT performance record (status = SETUP)
    API->>DB: UPSERT booking[] records
    API->>DB: INSERT seat_state[] for all seats in this performance
    Note over API,DB: SOLD seats from bookings, AVAILABLE for rest
    API->>DB: READ demand_fingerprint for this production
    API->>DB: UPDATE seat_state SET hold_type = INVENTORY_HOLD<br/>for top-N seats per zone (N from fingerprint)

    QUEUE->>QUEUE: Schedule T-7 job: send_upgrade_offer_emails(performance_id)
    QUEUE->>QUEUE: Schedule T-3 job: run_solver(performance_id)

    QUEUE-->>EMAIL: At T-7: generate magic links for all SOLD patrons
    EMAIL-->>Patron: "You have an upgrade offer for [Show]" (branded per venue)
    API->>DB: UPDATE performance.status = BIDDING_OPEN
```

**Key decisions made in this phase:**
- Which seats enter the upgrade pool (AVAILABLE - HELD = eligible destination seats)
- Which patrons receive emails (all SOLD seats in an upgradeable-from section)
- The solver job scheduled with a hard `execute_at` timestamp

---

### Phase 2: Bid Collection Window (T–7 to T–3)

```mermaid
sequenceDiagram
    actor Patron
    participant Portal
    participant API
    participant DB
    participant Stripe
    participant EMAIL

    Patron->>Portal: Clicks magic link (token in URL)
    Portal->>API: GET /auth/magic-link?token=XYZ
    API->>DB: SELECT patron WHERE magic_link_token = XYZ AND expires_at > now()
    API-->>Portal: Session established (patron_id, booking context)

    Portal->>API: GET /performances/{id}/seatmap?patron_id=X
    API->>DB: READ seat_state[], section[], current bid heatmap
    API-->>Portal: Seat map JSON (patron's current seat highlighted,<br/>available zones coloured, recommended bids per zone)

    Patron->>Portal: Selects target zone, enters max bid amount
    Portal->>API: GET /bids/recommendation?from_section=A&to_section=B&performance_id=X
    API->>DB: READ demand_fingerprint, current occupancy rate
    API-->>Portal: { recommended_min: £X, recommended_max: £Y, match_probability: Z% }

    Patron->>Portal: Confirms bid + enters card details
    Portal->>Stripe: Create PaymentIntent (amount=max_bid, capture_method=manual)
    Stripe-->>Portal: { payment_intent_id, client_secret, status: requires_capture }
    Portal->>API: POST /bids { target_section_id, max_bid_£, willingness_flags, payment_intent_id }
    API->>DB: INSERT bid (status=PENDING)
    API->>DB: UPDATE seat_state SET status=BID_VACATING for patron's current seat(s)
    API-->>EMAIL: Send bid receipt to patron
    EMAIL-->>Patron: "Bid confirmed — we'll notify you by [T-3 datetime]"
    API-->>Portal: { bid_id, status: PENDING }
```

**Data written in this phase:**
- `bid[]` records (one per zone target per patron — patron may bid on multiple zones)
- `seat_state` updated to `BID_VACATING` for origin seats
- `payment_event` (append-only log of Stripe webhook confirmations)

**Constraints enforced at bid creation time (pre-solver):**
- Patron may not have more than one active bid per performance (they can only move once)
- `max_bid_£ ≥ section.floor_price`
- Target section must be upgradeable-from patron's current section (ruleset check)
- Patron's current seat must be in status `SOLD` or `BID_VACATING` (not HELD or AVAILABLE)
- Pre-auth must succeed before bid record is written

---

### Phase 3: Solver Execution (T–3, Batch Job)

This is the architectural core of the platform.

```mermaid
sequenceDiagram
    participant QUEUE
    participant SOLVER
    participant DB
    participant DBIE

    QUEUE->>SOLVER: Execute solver_job(performance_id=X)
    SOLVER->>DB: READ all bids WHERE performance_id=X AND status=PENDING
    SOLVER->>DB: READ seat_state[] WHERE performance_id=X
    SOLVER->>DB: READ section[], upgrade_ruleset for this venue
    SOLVER->>DB: READ demand_fingerprint (for chain opportunity scoring)
    SOLVER->>DBIE: GET context features (weather, local events, day-of-week)

    Note over SOLVER: Build CP-SAT model:
    Note over SOLVER: Decision variables: x[bid_i, seat_j] ∈ {0,1}
    Note over SOLVER: Constraints: capacity, direction,<br/>party integrity, occupancy neutrality,<br/>inventory hold, chain integrity
    Note over SOLVER: Objective: maximise Σ bid_amount × x[i,j]<br/>+ Σ chain_opportunity_value × y[chain_k]
    Note over SOLVER: Solve with time limit (e.g., 60s wall clock)

    SOLVER->>DB: INSERT solver_run (status=RUNNING, triggered_at=now())
    SOLVER->>SOLVER: Run OR-Tools CP-SAT solver
    SOLVER->>DB: UPDATE solver_run (status=COMPLETE, objective_value, runtime_ms)
    SOLVER->>DB: INSERT bid_outcome[] for all MATCHED bids
    SOLVER->>DB: UPDATE bid.status = MATCHED for matched bids
    SOLVER->>DB: UPDATE bid.status = UNMATCHED for unmatched bids
    SOLVER->>QUEUE: Enqueue resolution_job(solver_run_id=Y)
```

**Solver I/O Contract:**

**Input document (JSON passed to solver process):**
```
{
  "performance_id": "uuid",
  "seats": [
    { "seat_id": "uuid", "section_id": "uuid", "status": "AVAILABLE|HELD|SOLD|BID_VACATING" }
  ],
  "bids": [
    {
      "bid_id": "uuid",
      "patron_id": "uuid",
      "party_seat_ids": ["uuid", "uuid"],
      "target_section_id": "uuid",
      "max_bid_£": 45.00,
      "willingness_flags": {
        "accept_split_party": false,
        "accept_lateral_move": true,
        "accept_freebie_bundle": true
      }
    }
  ],
  "upgrade_graph": {
    "edges": [{ "from_section": "upper_circle", "to_section": "dress_circle" }]
  },
  "seat_chains": [
    { "chain_id": "uuid", "seat_ids": ["uuid","uuid"], "p_sell": 0.72, "avg_price_£": 85.00 }
  ],
  "chain_weight": 0.6,
  "solver_time_limit_seconds": 60
}
```

**Output document:**
```
{
  "solver_run_id": "uuid",
  "status": "OPTIMAL|FEASIBLE|TIMEOUT",
  "objective_value_£": 1240.00,
  "runtime_ms": 4200,
  "assignments": [
    {
      "bid_id": "uuid",
      "assigned_seat_id": "uuid",
      "charge_amount_£": 35.00,
      "freebie_bundle_id": null,
      "chain_ids_unlocked": ["uuid"]
    }
  ],
  "unmatched_bid_ids": ["uuid", "uuid"]
}
```

---

### Phase 4: Resolution & Ticket Reissuance (T–3, immediately post-solver)

```mermaid
sequenceDiagram
    participant QUEUE
    participant API
    participant DB
    participant Stripe
    participant TKT as Theatre Ticketing System
    participant EMAIL

    QUEUE->>API: Execute resolution_job(solver_run_id=Y)
    API->>DB: READ bid_outcome[] WHERE solver_run_id=Y

    loop For each MATCHED bid
        API->>Stripe: CapturePaymentIntent(payment_intent_id, amount=charge_amount_£)
        alt Capture succeeds
            Stripe-->>API: { status: succeeded }
            API->>DB: INSERT payment_event (type=CAPTURED)
            API->>DB: UPDATE bid.status = CONFIRMED
            API->>DB: UPDATE seat_state: new_seat → SOLD(patron), old_seat → VACATED
            API->>TKT: POST /tickets/reissue { old_booking_ref, new_seat_id, patron_email }
            TKT-->>API: { new_ticket_ref, qr_code_url }
            API->>DB: UPDATE booking.current_seat_ids = [new_seat_id]
            API-->>EMAIL: Send confirmation (new seat, QR code, freebie details if applicable)
            EMAIL-->>Patron: "Your upgrade is confirmed — enjoy [Section B, Row D, Seat 14]!"
        else Capture fails (retry once after 30s)
            API->>DB: UPDATE bid.status = CAPTURE_FAILED
            API->>DB: REVERT seat_state: old_seat → SOLD(patron), new_seat → AVAILABLE
            API->>Stripe: CancelPaymentIntent(payment_intent_id)
            API-->>EMAIL: Send failure notice
            EMAIL-->>Patron: "Payment issue — your original seat is retained"
        end
    end

    loop For each UNMATCHED bid
        API->>Stripe: CancelPaymentIntent(payment_intent_id)
        API->>DB: INSERT payment_event (type=CANCELED)
        API->>DB: UPDATE bid.status = UNMATCHED
        API->>DB: REVERT seat_state: origin_seat → SOLD (remove BID_VACATING flag)
        API-->>EMAIL: Send "no upgrade" notice
        EMAIL-->>Patron: "No upgrade available — your original seat is confirmed"
    end

    API->>DB: UPDATE performance.status = RESOLUTION_COMPLETE
    API-->>Manager Dashboard: Trigger real-time push notification: "Resolution complete — X upgrades confirmed, £Y revenue"
```

**Atomicity guarantee:** Each bid's capture + seat_state update + ticket reissuance is wrapped in a distributed saga:
- If ticket reissuance fails after payment capture → refund the captured amount automatically and revert seat_state
- Payment event log (`payment_event`) is append-only; never update, only insert

---

### Phase 5: Post-Show Analytics Feed

Runs automatically 24h after curtain.

```mermaid
sequenceDiagram
    participant QUEUE
    participant API
    participant DB
    participant DBIE

    QUEUE->>API: Execute post_show_analytics_job(performance_id=X)
    API->>DB: READ all bid_outcome[], solver_run, seat_state for performance
    API->>DB: Compute and store analytics_report:
    Note over API,DB: - total_upgrades_confirmed (count)<br/>- total_upgrade_revenue_£<br/>- avg_bid_£ vs avg_charge_£ (bid efficiency)<br/>- match_rate (%) = confirmed / (confirmed + unmatched)<br/>- seats_released_to_inventory (count)<br/>- chain_opportunities_created (count)<br/>- freebie_bundles_redeemed (count)
    API->>DB: UPDATE production.cumulative_stats (rolling aggregates)
    API->>DBIE: Append outcome records to training dataset
    Note over DBIE: bid_id, zone_pair, max_bid_£, charge_amount_£,<br/>matched (bool), contextual features at time of bid
    API-->>Manager: Send post-show analytics email digest
```

---

## 5. Critical Data Flows — Edge Cases & Failure Modes

| Scenario | Detection | Resolution |
|----------|-----------|------------|
| Magic link expired (patron clicks email after 7 days) | `token_expires_at < now()` | Return 401; offer to resend link if T–3 not yet passed |
| Patron places bid, then their booking is cancelled by the theatre | Nightly ticketing sync finds booking voided | Auto-cancel bid + release pre-auth; notify patron |
| Stripe pre-auth expires before solver runs (>7 day window) | `payment_intent.status = expired` at solver time | Exclude bid from solver input; notify patron to re-bid if time permits |
| Solver times out without reaching OPTIMAL | `status = FEASIBLE` or `TIMEOUT` in solver output | Use best feasible solution found; log for review; alert Platform Operator |
| Ticket reissuance API call fails after payment captured | Exception in resolution saga | Immediately trigger refund via Stripe; revert seat_state; alert Platform Operator for manual intervention |
| Two patrons bid for the same seat (not a bug — solver handles this) | Solver constraint: seat capacity = 1 | Solver assigns at most one patron per seat; the other bid remains UNMATCHED |
| Party of 2, `accept_split_party = false`, no 2 adjacent seats available in target zone | Solver constraint: party integrity | Bid is UNMATCHED; both patrons retain original seats |
| Chain cascade unwind (Patron A confirmed, Patron B capture fails — both in same chain) | `chain_ids` in bid_outcome links them | Both bids reverted; both patrons retain original seats; A's payment refunded |

---

## 6. Integration Contracts (MVP vs. Full)

| Integration Point | MVP Approach | Full Integration (Phase 2) |
|------------------|--------------|-----------------------------|
| Seat map ingestion | Manager uploads JSON/CSV via dashboard | Direct API pull from Spektrix / Tessitura |
| Booking data sync | Nightly CSV export from ticketing system | Real-time webhook from ticketing system |
| Ticket reissuance | The Shakeup emails a PDF/QR ticket; manager manually voids old ticket | API call to ticketing system: `void_ticket` + `issue_ticket` in one transaction |
| Payment | Stripe PaymentIntents (direct charge to patron) | Stripe Connect (revenue split routed to venue sub-account automatically) |
| Freebie fulfilment | Email voucher code (manual redemption at bar) | POS integration (voucher validated by venue's bar system) |
| Weather data | Open-Meteo REST API (free tier) | Commercial weather API with venue-local station data |

---

## 7. Data Retention & Privacy Notes

- `patron` records contain email only (+ phone optionally). No name, no payment details (Stripe tokenises these).
- `magic_link_token` is a one-time token; expires 7 days after issuance or upon first use, whichever comes first.
- `sales_history` data uploaded by the venue is owned by the venue; The Shakeup uses it only in aggregate/model training form.
- `payment_event` log is retained for 7 years (financial regulation compliance).
- All other transactional data retained for 2 years post-performance, then anonymised (patron_id nulled, email hashed).
- GDPR right-to-erasure: patron_id and email can be nulled on request without breaking referential integrity of analytics aggregates.
