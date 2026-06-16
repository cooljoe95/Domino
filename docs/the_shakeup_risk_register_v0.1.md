# The Shakeup — Risk Register
### Version 0.1 | 2026-05-26
### Pilot Reference: My Neighbour Totoro @ Gillian Lynne Theatre

---

## Risk Scoring Framework

| Score | Likelihood | Impact |
|-------|-----------|--------|
| 5 | Near certain (>80%) | Existential — kills the business or pilot |
| 4 | Likely (60–80%) | Critical — major revenue or reputational damage |
| 3 | Possible (30–60%) | Significant — material delay or cost |
| 2 | Unlikely (10–30%) | Moderate — manageable with effort |
| 1 | Rare (<10%) | Minor — noise-level impact |

**Risk Score = Likelihood × Impact. Priority threshold: ≥ 12 = Critical, 8–11 = High, 4–7 = Medium, ≤ 3 = Low**

---

## Risk Heat Map

```
Impact →    1-Minor    2-Moderate   3-Significant  4-Critical   5-Existential
           ─────────────────────────────────────────────────────────────────
5-Certain  │           │            │              │            │ R01        │
           ├───────────┼────────────┼──────────────┼────────────┼────────────┤
4-Likely   │           │            │ R15, R22     │ R04, R07   │ R02, R28   │
           ├───────────┼────────────┼──────────────┼────────────┼────────────┤
3-Possible │           │ R09, R18   │ R06, R11,    │ R03, R14   │ R23        │
           │           │            │ R17, R20,    │            │            │
           │           │            │ R24, R25     │            │            │
           ├───────────┼────────────┼──────────────┼────────────┼────────────┤
2-Unlikely │ R16, R27  │ R08, R10,  │ R05, R12,    │ R13, R19,  │ R21, R26   │
           │           │ R26        │ R21          │            │            │
           ├───────────┼────────────┼──────────────┼────────────┼────────────┤
1-Rare     │           │ R27        │              │            │            │
           └───────────┴────────────┴──────────────┴────────────┴────────────┘

🔴 Critical (≥12): R01, R02, R04, R07, R14, R23, R28
🟠 High (8–11):    R03, R06, R11, R13, R17, R19, R20, R21, R24, R25, R26
🟡 Medium (4–7):   R05, R08, R09, R10, R12, R15, R16, R18, R22, R27
🟢 Low (≤3):       Remainder
```

---

## Category 1: Venue Adoption Risks

### R01 — Box Office Staff Friction at MVP
**Description:** At MVP, every confirmed upgrade requires a box office team member to manually void the old ticket and process the swap in Line-Up. If the box office team finds this burdensome, makes mistakes, or deprioritises it, patron experience is damaged and The Shakeup's reputation with LW Theatres is at risk from day one.

| Attribute | Value |
|-----------|-------|
| Likelihood | 5 — Near certain (any new manual process causes friction) |
| Impact | 4 — Critical (bad patron experience poisons the pilot) |
| **Risk Score** | **20 — CRITICAL** |
| Owner | Head of Partnerships (The Shakeup) |

**Mitigation:**
- Appoint a named "Upgrade Champion" within the Gillian Lynne box office team — someone whose role visibly benefits from the pilot succeeding (e.g., share a small per-upgrade bonus with their team budget).
- Produce an ultra-simple box office runbook: one-page, step-by-step, with screenshots of the Line-Up swap workflow. Delivered in person, not emailed.
- The resolution email to box office must arrive pre-sorted by performance date, in processing order, with every field they need pre-filled. Zero ambiguity.
- Target: maximum 3 minutes of box office time per upgrade. Validate this timing in the first run and optimise.
- Cap the pilot at 2 performances per week initially to limit manual load while process is being refined.
- Frame V1 Line-Up API integration as "this goes away completely in 3 months" to maintain goodwill.

**Residual Risk:** Medium (3×4=12 → reduced to ~6 with mitigation)

**Early Warning Signal:** Box office team escalates to venue manager after first resolution run. Monitor for "we got it wrong" emails.

---

### R02 — Venue Non-Adoption at Scale
**Description:** The pilot succeeds with Totoro but other venues decline to partner — either because they don't trust the model, fear cannibalising their own dynamic pricing, or simply don't prioritise it.

| Attribute | Value |
|-----------|-------|
| Likelihood | 4 — Likely without clear proof of economics |
| Impact | 5 — Existential (no scale = no business) |
| **Risk Score** | **20 — CRITICAL** |
| Owner | Founder / CEO |

**Mitigation:**
- Generate a compelling pilot case study from Totoro with real numbers: upgrades confirmed, £ generated, patron satisfaction scores (simple post-upgrade email survey), occupancy impact. Make this publishable.
- Price the pilot as entirely risk-free for LW Theatres: zero upfront, zero guaranteed minimums, pure revenue share. Remove every financial objection.
- Target the pilot announcement in The Stage or a trade publication once the first successful resolution runs — trade press drives inbound.
- The second venue should ideally be a different LW Theatres show (not Totoro) to demonstrate group-level scalability and lock in the relationship before approaching outside groups.
- Identify one Spektrix client in the West End as the parallel target (separate ticketing system, separate group — proves the model isn't show-specific or system-specific).

**Residual Risk:** High — this is the defining business risk and cannot be fully mitigated pre-launch. The pilot IS the mitigation.

**Early Warning Signal:** First venue meeting ends without a "yes, let's trial it" or "tell me more." Means the pitch or the economics model needs revision.

---

### R03 — Venue Internalises the Model (Build vs. Buy)
**Description:** After seeing the pilot succeed, LW Theatres or ATG decides to build an equivalent system in-house rather than pay The Shakeup a revenue share indefinitely.

| Attribute | Value |
|-----------|-------|
| Likelihood | 3 — Possible (large groups have technical teams) |
| Impact | 4 — Critical (loss of anchor venue partnerships) |
| **Risk Score** | **12 — CRITICAL** |
| Owner | Founder / CEO |

**Mitigation:**
- The moat is not the concept — it's the **data**. The DBIE model trained across 50+ shows at multiple venues is orders of magnitude more accurate than anything a single venue's internal team could build. Communicate this explicitly in the partnership pitch.
- Multi-year commercial agreements with exclusivity clauses (e.g., "LW Theatres agrees not to operate a competing upgrade auction service during the term of this agreement") — standard in SaaS enterprise deals.
- Proprietary patent applications (CUCR + SCOS) filed before any public announcement to create a legal barrier.
- Rapid venue expansion: the more venues on the platform, the less attractive the "build in-house" option becomes (they'd need to rebuild the cross-venue demand model from scratch).
- Offer venues equity or warrants in a Series A as strategic investors — aligns their incentive with The Shakeup's success.

**Residual Risk:** Medium

**Early Warning Signal:** Venue partner's technical team starts asking unusually detailed questions about the solver architecture. Venue delays contract renewal without explanation.

---

### R04 — Low Patron Participation Rate
**Description:** Fewer patrons than projected click the upgrade offer email and place bids, making the solver's output trivial (3–5 upgrades per show rather than 20+).

| Attribute | Value |
|-----------|-------|
| Likelihood | 4 — Likely in early shows (brand unfamiliarity) |
| Impact | 4 — Critical (undermines the revenue case for venues) |
| **Risk Score** | **16 — CRITICAL** |
| Owner | Product / Growth |

**Mitigation:**
- Email subject line is everything. A/B test from day one. "You're invited to upgrade your Totoro seats" vs. "Fans of My Neighbour Totoro: your upgrade offer is inside" vs. "How would you like to sit closer to Totoro?" Test open rates relentlessly.
- The email must load in under 2 seconds and render perfectly on mobile. Most theatre patrons will open this on an iPhone. Invest in email design.
- Framing: the email must not feel like a sales pitch. It must feel like an exclusive invitation from the theatre to their most loyal patrons. White-labelling (sent from the venue's domain) is critical to open rates.
- Reduce friction to zero: magic link authentication (no password, no registration), mobile-optimised seat map, under 3 taps to place a bid.
- Target an initial email open rate of 40%+ (the venue has an existing trusted relationship with their patrons). 
- If participation rate is <10% after first 5 performances, trigger an A/B test on the email copy and the bid flow UX. Do not wait.

**Residual Risk:** Medium — participation will grow with brand recognition but initial numbers will be low.

**Early Warning Signal:** Open rate <25% or bid placement rate <8% of openers on the first send.

---

### R05 — Venue Sets Floor Prices Too High
**Description:** The venue manager sets unrealistically high floor prices (e.g., £80 minimum for a Stalls Centre upgrade) that result in near-zero bids, making the whole system appear broken.

| Attribute | Value |
|-----------|-------|
| Likelihood | 2 — Unlikely with proper onboarding |
| Impact | 3 — Significant (wasted pilot capacity) |
| **Risk Score** | **6 — Medium** |
| Owner | Customer Success |

**Mitigation:**
- Dashboard shows a real-time "estimated bid volume at this floor price" simulation during ruleset configuration — visual feedback that floor prices have consequences.
- Default floor prices pre-populated from The Shakeup's recommended ranges (based on section desirability delta and face value differential). Manager must actively override, not actively set.
- Customer success calls with manager before first T–7 trigger to review ruleset settings.

**Residual Risk:** Low

---

## Category 2: Technical & Solver Risks

### R06 — T–3 Batch Job Silent Failure
**Description:** The scheduled pre-auth + solver + resolution job fails silently (throws an exception that is swallowed, or the scheduler crashes) with no notification to The Shakeup platform team. The performance happens with no upgrades processed.

| Attribute | Value |
|-----------|-------|
| Likelihood | 3 — Possible without robust alerting |
| Impact | 3 — Significant (missed revenue; patron emails never sent; box office never notified) |
| **Risk Score** | **9 — High** |
| Owner | Engineering |

**Mitigation:**
- Every job execution writes a `solver_run` record with status. A separate watchdog job polls every 10 minutes for `performance_id` records where `curtain_datetime - now() < 80h` and `status ≠ RESOLUTION_COMPLETE`. If found, PagerDuty alert fires immediately.
- Dead man's switch pattern: at T–4h, if the solver job hasn't completed for a performance that is T–3 window-eligible, an alert escalates to the on-call engineer.
- All job failures send to a Slack alerting channel in addition to email.
- The T–3 window is wide enough (runs at exactly 72h before curtain) that a 2-hour window exists for manual re-triggering before the job is meaningfully late.
- Never run the pre-auth and solver in a single atomic job — split into three separate queued jobs (pre-auth → solver → resolution) so a failure in any one stage is independently observable and retriable.

**Residual Risk:** Low with proper observability implementation.

**Early Warning Signal:** Watchdog alert fires. Solver_run table shows no entry for a performance within 2h of its scheduled trigger time.

---

### R07 — Solver Produces Invalid Assignments (Double-Booking)
**Description:** A bug in the constraint formulation or solver implementation results in the same physical seat being assigned to two different patrons, or a patron moved to a seat that was already SOLD.

| Attribute | Value |
|-----------|-------|
| Likelihood | 4 — Likely in early versions without comprehensive testing |
| Impact | 4 — Critical (patron shows up to find someone in their new seat; catastrophic experience) |
| **Risk Score** | **16 — CRITICAL** |
| Owner | Engineering |

**Mitigation:**
- Post-solve validation layer (mandatory, runs before resolution job starts): verify every assigned `seat_id` appears exactly once in the assignment list; verify every `seat_id` is AVAILABLE in `seat_state` at the time of assignment. If validation fails, abort resolution and alert platform team — no charges captured, no tickets reissued.
- Unit tests covering: capacity constraint (1 seat = 1 patron), eligibility constraint, patron single-satisfaction constraint, with both small hand-constructed inputs and fuzz-generated inputs.
- Integration test: run solver against a synthetic full Gillian Lynne house (1,295 seats, 200 bids) and manually verify output.
- Staged rollout: first 3 pilot performances, solver output is reviewed by a platform engineer before the resolution job is unblocked. Manual approval gate. Remove after validation.

**Residual Risk:** Low with post-solve validation. The validation layer is the last line of defence and is simpler to write correctly than the solver constraints themselves.

**Early Warning Signal:** Post-solve validation fails. Any chargeback dispute citing wrong seat.

---

### R08 — Stripe Pre-Auth Failure Rate Higher Than Modelled
**Description:** The assumed 8% pre-auth failure rate is materially exceeded (e.g., 20–25%), driven by off-session MIT declines from specific card issuers, particularly older European bank cards.

| Attribute | Value |
|-----------|-------|
| Likelihood | 2 — Unlikely but possible |
| Impact | 2 — Moderate (reduces solver input quality; some annoyed patrons) |
| **Risk Score** | **4 — Medium** |
| Owner | Engineering |

**Mitigation:**
- At bid placement, SetupIntent is confirmed with `usage: 'off_session'` and full 3DS2 — this is the SCA establishment that should reduce off-session declines significantly.
- Monitor pre-auth failure rates by card type and issuer country. If European cards show disproportionate failure rates, investigate whether `mandate_data` is correctly passed.
- Contingency: if pre-auth failure rate exceeds 15% in pilot, add an optional step where patrons with failed pre-auths can re-enter card details via a secondary email sent at T–3 (a 2-hour window before the solver runs).

**Residual Risk:** Low

---

### R09 — Concurrent Solver Runs for Same Venue
**Description:** The Gillian Lynne runs a Thursday matinée and a Thursday evening performance. Both T–3 jobs trigger simultaneously, competing for the same AVAILABLE seats in the database.

| Attribute | Value |
|-----------|-------|
| Likelihood | 3 — Certain to happen (most venues run matinée + evening on same day) |
| Impact | 2 — Moderate (if not handled, seat_state corruption is possible) |
| **Risk Score** | **6 — Medium** |
| Owner | Engineering |

**Mitigation:**
- `seat_state` is partitioned by `performance_id` — seats for the 2pm matinée and the 7:30pm evening are completely separate rows. Each performance has its own independent pool of AVAILABLE seats.
- Solver jobs are performance-scoped: they only read and write `seat_state` for their specific `performance_id`. No cross-performance contention.
- Job queue uses performance-level locking: only one solver job per `performance_id` can be in RUNNING state simultaneously.
- No design change needed beyond confirming the data model is correctly partitioned.

**Residual Risk:** Low

---

### R10 — Ticket Reissuance Fails After Payment Captured
**Description:** The payment capture succeeds but the subsequent ticket reissuance step fails — either because the Line-Up API is unavailable (V1) or because the box office email is not received/actioned (MVP). The patron has been charged but has no new ticket.

| Attribute | Value |
|-----------|-------|
| Likelihood | 2 — Unlikely for MVP (email is reliable); possible for V1 API |
| Impact | 2 — Moderate (requires manual resolution; patron inconvenience) |
| **Risk Score** | **4 — Medium** |
| Owner | Engineering + Customer Success |

**Mitigation:**
- Distributed saga pattern: if reissuance fails after capture, auto-refund the captured amount via Stripe immediately. Do not wait for manual intervention.
- Platform operator alert fires instantly on reissuance failure, with all context needed to manually resolve.
- At MVP: send box office email with 48h lead time before performance. If not actioned within 24h, send follow-up automatically.
- Retain original ticket in valid state until reissuance is confirmed — patrons always have a valid ticket to the show.

**Residual Risk:** Low

---

## Category 3: Consumer & Patron Risks

### R11 — Patron Dissatisfied With New Seat
**Description:** A patron wins an upgrade to Stalls Centre, Row A — and discovers it's too close to the stage for Totoro's aerial puppetry, or has a partially obstructed view they didn't anticipate. They feel worse off than their original seat.

| Attribute | Value |
|-----------|-------|
| Likelihood | 3 — Possible |
| Impact | 3 — Significant (chargeback risk; negative social media; venue relationship strain) |
| **Risk Score** | **9 — High** |
| Owner | Product |

**Mitigation:**
- Seat map must show **honest** section descriptions, including known limitations. If Row A Stalls Centre is "very close to the stage — best for immersive experience, not optimal for aerial scenes," say so. The Shakeup's reputation depends on under-promising and over-delivering.
- "Restricted view" labels from the venue's own seat map data are inherited and displayed prominently.
- Pre-bid disclaimer on each section card: "This is the best available view in this section — based on [venue description]."
- The bid confirmation screen shows the section name, its description, and a sightline indicator before checkout.
- Consider a 24-hour post-upgrade survey: "Rate your new seat (1–5 stars)." Data feeds back into section desirability scores over time. If a specific seat consistently scores poorly, it can be removed from the upgrade pool.

**Residual Risk:** Medium — some dissatisfaction is unavoidable in any upgrade system. The key is ensuring the patron made an informed choice.

---

### R12 — Chargeback Spike
**Description:** Multiple patrons file chargebacks claiming they didn't authorise the upgrade charge. If The Shakeup's chargeback rate exceeds Stripe's 0.5% threshold, Stripe may place the account under review or terminate it.

| Attribute | Value |
|-----------|-------|
| Likelihood | 2 — Unlikely with correct disclosure |
| Impact | 3 — Significant (Stripe review; reputational; legal exposure) |
| **Risk Score** | **6 — Medium** |
| Owner | Operations / Legal |

**Mitigation:**
- The pre-bid disclosure screen with explicit checkbox consent, timestamped server-side, is the primary defence against any "I didn't authorise this" claim.
- Stripe Radar rules configured to flag unusual patterns (e.g., same patron filing multiple chargebacks).
- Outcome confirmation email includes: the original bid amount, the exact charge amount, the explicit statement "This charge was authorised by you on [bid_placed_at]."
- Maintain a 30-day post-charge window where patrons can contact The Shakeup's support to resolve issues without going directly to their bank — a good dispute resolution process reduces chargebacks materially.
- Target chargeback rate: <0.2%.

**Residual Risk:** Low with correct disclosure implementation.

---

### R13 — Patron Shows Up to Wrong Seat
**Description:** A patron arrives at the theatre holding their new upgrade ticket but their old seat reference has not been voided in the venue's system. Either the box office didn't process the swap (MVP) or the reissuance failed silently (V1). A confrontation occurs.

| Attribute | Value |
|-----------|-------|
| Likelihood | 2 — Unlikely but realistic at MVP |
| Impact | 4 — Critical (public scene, viral social post, venue relationship damaged) |
| **Risk Score** | **8 — High** |
| Owner | Operations |

**Mitigation:**
- At MVP: resolution emails sent to box office with **72-hour advance notice** (not 3 days — the actual time gap between T–3 and curtain). The Shakeup follows up 24h before curtain with a "confirmation check" email listing all upgrades for that performance. Box office replies "confirmed" or raises an issue.
- Escalation path: if a patron contacts The Shakeup on show day with a seating issue, there is a direct mobile number for the venue's duty manager. Never leave a patron stranded.
- Patron's upgrade confirmation email must state: "If you experience any issue on arrival, please show this email to box office staff" — with The Shakeup support number included.
- V1: API-based reissuance makes this risk near-zero by removing the manual step entirely.

**Residual Risk:** Medium at MVP (manual dependency). Low at V1.

**Early Warning Signal:** Any box office escalation about a seating conflict on show day.

---

### R14 — Perceived Unfairness of the Selection Process
**Description:** Patrons whose bids are not selected — particularly those who bid a large amount — may feel the process is rigged, random, or unfair. Social media complaints of "I bid £70 and didn't get upgraded while someone else got it for £30" could damage brand perception.

| Attribute | Value |
|-----------|-------|
| Likelihood | 4 — Likely (human nature; similar complaints arise in airline upgrade bidding) |
| Impact | 3 — Significant (reputational damage; viral risk in tight-knit theatre community) |
| **Risk Score** | **12 — CRITICAL** |
| Owner | Product / Communications |

**Mitigation:**
- Unmatched bid notification email must be specific and honest: "Your bid for Stalls Centre (£55) was not selected because all 18 available seats in that section were matched to other bids. Your original Stalls Side seats are confirmed and ready."
- **Never** imply the selection is random. It is explicitly revenue-maximising — higher bids are prioritised. State this clearly in the T&Cs and FAQs.
- Consider publishing a high-level transparency statement: "Upgrades are awarded to the highest bids that can be feasibly assigned. Availability depends on how many seats are open in your target section."
- If a patron bids £70 and doesn't get upgraded, it means all STALLS_CTR seats were allocated to other patrons — likely at higher bids. This is fair by design; the communication must be clear enough that the patron understands this.
- Explore: showing patrons their "bid rank" after resolution — "Your bid ranked 4th for Stalls Centre. Only 3 seats were available." This transparency defuses anger.

**Residual Risk:** Medium — some perception of unfairness is inevitable. Transparency and clear communication are the levers.

---

### R15 — Very Low Pre-Auth Bid Window (T–3 Surprise)
**Description:** A patron places a bid at T–6 days but forgets about it. The T–3 pre-auth hits their card unexpectedly, they panic and call their bank, triggering a fraud dispute.

| Attribute | Value |
|-----------|-------|
| Likelihood | 4 — Likely for some patrons |
| Impact | 2 — Moderate (support load; potential chargeback) |
| **Risk Score** | **8 — High** |
| Owner | Product / Communications |

**Mitigation:**
- Send a **T–4 day reminder email**: "Just a reminder — your upgrade bid for My Neighbour Totoro will be processed tomorrow. If you'd like to cancel, click here by [T-3 time]."
- This email serves dual purpose: reduces forgotten-bid surprises AND creates a final cancellation opportunity. Call it out as a feature in patron comms: "We'll always remind you the day before we process."
- The pre-bid disclosure screen must state the T–3 datetime explicitly (not "in a few days" — the actual date and time).

**Residual Risk:** Low

---

## Category 4: Regulatory & Legal Risks

### R16 — GDPR Enforcement Action
**Description:** The ICO investigates The Shakeup following a data breach or a patron complaint about how their data was used.

| Attribute | Value |
|-----------|-------|
| Likelihood | 2 — Unlikely at pilot scale |
| Impact | 4 — Critical (fines up to 4% of global turnover; reputational damage) |
| **Risk Score** | **8 — High** |
| Owner | Legal / Engineering |

**Mitigation:**
- DPA signed with LW Theatres before data access (mandatory per legal analysis).
- DPIA conducted and documented before launch.
- ICO registration completed (£40/year — no reason not to).
- Data minimisation: only email and seat reference stored. No name, no address, no payment data.
- Breach response plan documented: 48h venue notification, 72h ICO notification path.
- All patron data on encrypted storage. Access logs for all database queries touching patron records.

**Residual Risk:** Low

---

### R17 — CMA Investigation into Bid Recommendations
**Description:** The CMA investigates The Shakeup's bid recommendation engine on the grounds that it constitutes unfair dynamic pricing or manipulative recommendation design.

| Attribute | Value |
|-----------|-------|
| Likelihood | 3 — Possible, given CMA's current ticketing focus |
| Impact | 3 — Significant (investigation cost; required product changes; reputational hit) |
| **Risk Score** | **9 — High** |
| Owner | Legal / Product |

**Mitigation:**
- Recommendations framed as "guidance based on demand data" — not as prices. The patron is always free to bid any amount above the floor price.
- The recommendation algorithm is explainable and documented. If the CMA asks "why did you recommend £45?", there is a clear, data-driven answer.
- No dark patterns: the recommended range is presented as a range, not a default that the patron has to actively change. The bid input starts blank.
- The bid recommendation is based on aggregated historical data and current occupancy — it doesn't use individual patron data or behavioural profiling to manipulate bids upward.
- Legal review of the recommendation UI copy before launch.

**Residual Risk:** Low — the model is inherently clean because the patron sets their own price.

---

### R18 — FCA Scrutiny of Revenue Split Model
**Description:** Before Stripe Connect is implemented (MVP), The Shakeup briefly holds theatre revenue (the 75% share) between charge and monthly remittance. The FCA determines this constitutes regulated money remittance.

| Attribute | Value |
|-----------|-------|
| Likelihood | 2 — Unlikely at pilot volumes |
| Impact | 2 — Moderate (requires urgent Stripe Connect implementation) |
| **Risk Score** | **4 — Medium** |
| Owner | Legal / Finance |

**Mitigation:**
- Keep the MVP remittance window short (15 business days maximum from performance date).
- Open a dedicated client account for holding venue remittances — segregated from The Shakeup's operating funds.
- Consult a payment law specialist before processing more than 10 venues simultaneously to confirm the regulatory position.
- Stripe Connect implementation is a V1 requirement (not Phase 2).

**Residual Risk:** Low at pilot scale; needs reassessment at 10+ venues.

---

## Category 5: Competitive & Market Risks

### R19 — Primary Ticketing Platforms Add Upgrade Features
**Description:** Ticketmaster, See Tickets, or LW Theatres' own Line-Up platform introduces a native seat upgrade bidding feature, making The Shakeup redundant for venues already using those systems.

| Attribute | Value |
|-----------|-------|
| Likelihood | 2 — Unlikely in the short term (ticketing platforms move slowly) |
| Impact | 4 — Critical (direct substitution for the core product) |
| **Risk Score** | **8 — High** |
| Owner | CEO / Strategy |

**Mitigation:**
- Speed is the primary defence — build the data flywheel (DBIE, VDF) fast. A ticketing platform building an equivalent from scratch would need years of outcome data to match the recommendation quality.
- Proprietary patent applications on CUCR + SCOS filed before public launch.
- Long-term venue contracts with exclusivity clauses.
- The insight: ticketing platforms are primarily interested in primary sale revenue. Upgrade yield management is an ancillary service that doesn't threaten them — it actually grows their venues' overall revenue, making them more committed customers. Frame The Shakeup as a complement, not a competitor, to ticketing platforms. Explore formal partnership / referral relationships with Line-Up and Spektrix.

**Residual Risk:** Medium — this is a watch risk, not an immediate threat.

**Early Warning Signal:** Any announcement from major ticketing platforms about "dynamic upgrade" features. Set Google Alerts for "Ticketmaster upgrade bidding", "See Tickets upgrade", "Line-Up seat upgrade."

---

### R20 — Adjacent Market Entrant (Hotel/Airline Upgrade Tech)
**Description:** A well-funded company from the hotel upgrade bidding market (e.g., a Nor1 / Plusgrade equivalent) decides to expand into theatre.

| Attribute | Value |
|-----------|-------|
| Likelihood | 3 — Possible (the concept is not novel in hospitality) |
| Impact | 3 — Significant (better-funded competition, faster venue acquisition) |
| **Risk Score** | **9 — High** |
| Owner | CEO / Strategy |

**Mitigation:**
- Theatre is a more complex domain than hotel upgrades: reserved seating, party integrity, multi-section upgrade graphs, the chain opportunity scorer. An entrant from hospitality would underestimate this complexity.
- The key differentiator is the **solver** — specifically CUCR and SCOS. These don't exist in hotel bidding (hotels don't have reserved seating with adjacency constraints). A hotel tech entrant would need 12–18 months of domain-specific development to match.
- UK theatre relationships are relationship-driven and long-tenured. The Shakeup's advantage is being the known brand in this specific niche before anyone else is.
- Rapid expansion into multiple West End shows means any late entrant faces an "already signed" problem.

**Residual Risk:** Medium

---

### R21 — IP Not Protectable
**Description:** A solicitor advises that the CUCR + SCOS combination is not novel enough to patent, leaving The Shakeup with no formal IP protection.

| Attribute | Value |
|-----------|-------|
| Likelihood | 2 — Possible (software patents are difficult in the UK) |
| Impact | 3 — Significant (moat relies more heavily on data and relationships) |
| **Risk Score** | **6 — Medium** |
| Owner | Legal |

**Mitigation:**
- UK software patents require a "technical effect" — the CUCR's graph-based chain decomposition pre-processing step applied to physical reserved seating venues may qualify. Worth a £2–3k IP solicitor opinion before ruling out.
- Even without patent, trade secrets law (the DBIE training data, the specific constraint formulations, the VDF demand model parameters) provides protection — these are not publicly disclosed.
- The primary moat is the data flywheel: 2 years of upgrade outcome data across 100+ shows is not replicable by any entrant regardless of patent status.

**Residual Risk:** Medium — manageable.

---

## Category 6: Financial & Operational Risks

### R22 — Revenue Per Show Too Low to Sustain the Business
**Description:** Unit economics at pilot scale (1 venue, ~24 upgrades/show, ~£228 platform revenue/show) are insufficient to cover The Shakeup's operating costs, and venue scaling is slower than projected.

| Attribute | Value |
|-----------|-------|
| Likelihood | 4 — Certain in the pilot phase |
| Impact | 3 — Significant (requires external funding to bridge to profitability) |
| **Risk Score** | **12 — CRITICAL** |
| Owner | CEO / Finance |

**Mitigation:**
- This is a known and expected bootstrapping challenge — the business is not designed to be profitable at 1 venue. The pilot's purpose is proof of concept, not P&L.
- Financial plan: The Shakeup needs approximately 6–8 venues running simultaneously to reach breakeven at conservative participation rates. That requires 6–12 months of runway from either personal capital, angel investment, or an Innovator Founder Visa-linked grant.
- The pilot economics (£1,768/week from Totoro alone) are enough to demonstrate the model; the fundraising story is the scale economics (6 shows × £1,768 = ~£10,600/week → ~£550k/year).
- Explore: an Innovator Founder Visa endorsement from a recognised body in the arts/tech sector as a funding/credibility catalyst. The prior market research conversation (afc8dfce) may already be progressing this angle.

**Residual Risk:** High — this is a runway problem, not a model problem.

---

### R23 — Totoro Closes Before The Shakeup Launches
**Description:** My Neighbour Totoro ends its run (currently booking to January 2027) before The Shakeup completes MVP development and pilot launch.

| Attribute | Value |
|-----------|-------|
| Likelihood | 3 — Possible if MVP timeline slips |
| Impact | 5 — Existential for the pilot (anchor show gone; must find new first partner) |
| **Risk Score** | **15 — CRITICAL** |
| Owner | CEO / Engineering |

**Mitigation:**
- Set a hard internal milestone: **MVP must be live and processing real bids by October 2026** — giving 3+ months of buffer before the January 2027 close.
- The MVP scope is deliberately narrow (CSV ingest + manual reissuance) specifically to enable this timeline.
- Parallel track: identify a second candidate production to partner with at the same time as the Totoro outreach, so that if Totoro timing doesn't work, there is an immediate backup.
- If Totoro extends its run (very possible — it's a hit), the risk disappears. Monitor LW Theatres booking calendar.

**Residual Risk:** Medium — timeline-dependent.

**Early Warning Signal:** Development timeline slips past September 2026 without a signed LOI from LW Theatres.

---

### R24 — Show Occupancy Too High (No Upgrade Inventory)
**Description:** For peak Saturday evening Totoro performances, the show is essentially sold out — Stalls Centre is 98% SOLD, leaving almost nothing to upgrade into. The solver returns zero matches.

| Attribute | Value |
|-----------|-------|
| Likelihood | 3 — Likely for Saturday evenings and school holiday matinées |
| Impact | 3 — Significant (The Shakeup appears ineffective on the shows patrons care most about) |
| **Risk Score** | **9 — High** |
| Owner | Product |

**Mitigation:**
- The Venue Demand Fingerprint (VDF) is specifically designed to address this: it predicts which shows will have high last-72h sell-through in premium sections. For a Saturday evening of Totoro where Stalls Centre historically sells out, the VDF recommends holding 0 seats in the upgrade pool from those sections — the T–7 email should simply not go out for that performance.
- Targeting strategy: focus the upgrade programme on **Tuesday–Thursday evening performances and mid-week matinées** where premium inventory is available. This is where the marginal revenue opportunity lives.
- Set patron expectation in the T–7 email: "Based on current demand, we have [N] Stalls Centre seats available for upgrade." If N=0, don't send the email.
- Dashboard metric: "Upgrade eligibility rate" per performance — visible to venue manager. Helps them understand the capacity dynamics.

**Residual Risk:** Low — VDF-driven targeting makes this a feature, not a bug.

---

### R25 — Show Occupancy Too Low
**Description:** If Totoro's mid-week occupancy falls significantly (show running long, press reviews turn negative, IP popularity wanes), the upgrade economics work differently — there's plenty of premium inventory, but patrons are self-selecting the good seats at original purchase and there's less demand to upgrade from the lower sections.

| Attribute | Value |
|-----------|-------|
| Likelihood | 3 — Possible at 18+ months into a run |
| Impact | 3 — Significant (bid volumes fall; solver matches fewer) |
| **Risk Score** | **9 — High** |
| Owner | Product / Business Development |

**Mitigation:**
- This is actually less severe than R24 — a lower-occupancy show has MORE available upgrade inventory, meaning the solver can satisfy more bids, even if bids are fewer in number.
- The bid recommendation engine should automatically adjust its suggested ranges downward as occupancy falls (signalling to patrons that bids are more likely to succeed at lower amounts — increasing conversion).
- A struggling show is also a show where the theatre is most motivated to maximise per-patron revenue — The Shakeup becomes more valuable, not less, to the venue partner.
- Diversification: the more shows on the platform, the less exposure to any single production's occupancy fluctuation.

**Residual Risk:** Low

---

### R26 — Stripe Terminates the Platform Account
**Description:** Stripe reviews The Shakeup's account as high-risk (off-session charges, high chargeback concentration around T–3 events) and terminates or severely restricts the account.

| Attribute | Value |
|-----------|-------|
| Likelihood | 1 — Rare (Stripe actively courts platforms like this) |
| Impact | 5 — Existential (payment processing is the backbone of the product) |
| **Risk Score** | **5 — Medium** |
| Owner | Engineering / Finance |

**Mitigation:**
- Maintain chargeback rate well below 0.5% through correct disclosure and pre-bid consent documentation.
- Proactively communicate with Stripe's partnership team (not just their standard support). Explain the business model, the MIT pattern, the pre-auth-then-capture flow. Get it reviewed before launch.
- Secondary payment processor on standby: Adyen or Braintree could serve as a fallback. The adapter-pattern approach to payment integration should abstract the processor enough to make a migration possible within 2–4 weeks.
- Never let The Shakeup's Stripe account go dormant between pilot shows — keep activity consistent.

**Residual Risk:** Low

---

### R27 — Magic Link Security Vulnerability
**Description:** An attacker brute-forces or predicts magic link tokens and accesses other patrons' bid portals, potentially placing or cancelling bids on their behalf.

| Attribute | Value |
|-----------|-------|
| Likelihood | 1 — Rare with proper token generation |
| Impact | 2 — Moderate (patron data exposure; fraudulent bid manipulation) |
| **Risk Score** | **2 — Low** |
| Owner | Engineering |

**Mitigation:**
- Magic link tokens must be cryptographically random: `secrets.token_urlsafe(32)` in Python generates 256 bits of entropy. Brute-forcing is computationally infeasible.
- Tokens are one-time use (invalidated immediately on first authenticated request).
- Tokens expire at T–3 (even if unused).
- Rate limiting on the `/auth/magic-link/verify` endpoint: 5 failed attempts per IP per hour triggers a block.
- Tokens are hashed before storage in the database — the raw token only exists in the email link.

**Residual Risk:** Low

---

### R28 — Single-Show Dependency Risk
**Description:** If The Shakeup launches with only Totoro and then the production team declines to renew/expand, or Totoro closes, the company has no revenue and no active partnerships to demonstrate.

| Attribute | Value |
|-----------|-------|
| Likelihood | 4 — Likely in the early phase |
| Impact | 4 — Critical (no evidence of repeatability; fundraising becomes very difficult) |
| **Risk Score** | **16 — CRITICAL** |
| Owner | CEO |

**Mitigation:**
- The second venue LOI should be a goal for the same month as the Totoro pilot launch — not sequentially after proving it works.
- Target: by the end of the first pilot performance month, have signed LOIs from at least 2 venues (1 LW Theatres show + 1 independent/Spektrix venue).
- Use the Totoro LOI signing as a press moment: a brief announcement in The Stage or WhatsOnStage generates inbound interest from other venues and signals momentum.
- Build an investor story that explicitly frames the risk: "We have one pilot show; here is exactly when we expect the second and third." Investors fund the path, not just the starting point.

**Residual Risk:** High — this is the most fundamental execution risk in the early phase.

---

## Top 10 Prioritised Action List

Sorted by Risk Score and time-sensitivity:

| Priority | Risk | Score | Action Required | By When |
|----------|------|-------|----------------|---------|
| 1 | R07 — Solver double-booking | 16 | Post-solve validation layer + manual approval gate for first 3 shows | Before any production run |
| 2 | R04 — Low patron participation | 16 | A/B email testing framework + mobile-first bid portal UX | Before T–7 first send |
| 3 | R28 — Single show dependency | 16 | Second venue LOI target date set; pipeline established | Month 1 of pilot |
| 4 | R01 — Box office friction | 20 | Box office runbook, upgrade champion, capped initial volume | Before MVP launch |
| 5 | R02 — Venue non-adoption | 20 | Pilot case study template ready; trade press strategy planned | Month 2 of pilot |
| 6 | R23 — Totoro closes first | 15 | Hard October 2026 MVP launch milestone; backup show identified | Immediately |
| 7 | R14 — Perceived unfairness | 12 | Unmatched bid email copy written with bid-rank transparency | Before T–3 first run |
| 8 | R22 — Revenue insufficient | 12 | Funding runway plan aligned with 6-venue breakeven target | Before launch |
| 9 | R06 — T–3 silent failure | 9 | Watchdog job + PagerDuty alerts + split job architecture | Before any production run |
| 10 | R13 — Patron at wrong seat | 8 | 72h advance box office email + 24h confirmation check | Before MVP launch |
