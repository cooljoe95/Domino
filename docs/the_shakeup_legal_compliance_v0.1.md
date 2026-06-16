# The Shakeup — Security, Compliance & Legal Analysis
### Version 0.1 | 2026-05-26
### Reference Jurisdiction: England & Wales (primary); Scotland; Northern Ireland

> **Disclaimer:** This document is a product-led legal analysis intended to inform design decisions. It is not a substitute for qualified legal advice. Before launch, retain a solicitor specialising in consumer protection and fintech to review these conclusions and the final T&Cs / DPA templates.

---

## Executive Summary of Findings

| Framework | Verdict | Design Impact |
|-----------|---------|---------------|
| Consumer Rights Act 2015 | ✅ Compatible — bids are not purchases | Disclosure language in bid flow must be precise |
| Consumer Contracts Regs 2013 | ✅ Event ticket exemption applies | No 14-day cancellation right — but cancellation before T–3 must be offered voluntarily |
| DMCC Act 2024 (CMA) | ⚠️ Active risk — drip pricing rules | Total bid cost must be the headline figure from first screen |
| UK GDPR / ICO | ⚠️ Dual controller complexity | Requires bespoke DPA with each venue; DPIA needed |
| PCI DSS | ✅ SAQ A scope — Stripe.js handles all card data | No card data ever on The Shakeup servers |
| Payment Services Regs 2017 | ✅ MIT exemption applies — SCA at setup only | SetupIntent must force 3DS at bid placement |
| FCA Regulation | ✅ Not a payment institution — Stripe is the regulated entity | Stripe Connect must be used for revenue split (not manual invoicing) |

---

## 1. Consumer Rights Act 2015 & Consumer Contracts Regulations 2013

### 1.1 Is a bid a contract?

The most important legal question for the product is: **at what point does a binding contract form between The Shakeup and the patron?**

**Legal analysis:**

A bid in The Shakeup's system is an **offer from the patron**, not an acceptance of a contract. No contract forms until:
1. The solver selects the bid (creates a match), AND
2. The patron's card is successfully captured

This is structurally identical to how online hotel upgrade bidding (Marriott Bonvoy, Hilton's bidding system) operates in law — the patron makes a conditional offer, the hotel decides whether to accept, and the charge executes only on acceptance. Courts and the FCA have consistently treated this as a two-stage offer/acceptance rather than a purchase.

**The key legal protection:** The patron's original ticket (the underlying contract with the theatre) is **never affected** by placing a bid. At worst, a patron loses a card pre-authorisation hold (which costs them nothing); at best, they get a better seat. This is not a bet, not a financial product, and not a purchase — it's a conditional offer for an ancillary service.

**Conclusion:** The bid mechanism is legally sound under the CRA 2015. The CRA's implied terms about "services provided with reasonable care and skill" apply to The Shakeup's service (running the upgrade marketplace), not to the individual bid outcomes.

### 1.2 Event Ticket Exemption — No Cooling-Off Period

Under the Consumer Contracts (Information, Cancellation and Additional Charges) Regulations 2013, **leisure activity contracts for specific dates are exempt** from the standard 14-day cancellation right. This is the same exemption that allows theatres to sell non-refundable tickets online.

**Application to The Shakeup:**
- The upgrade service is tied to a specific performance date and curtain time.
- Once the solver runs and the charge is captured, there is no statutory right to cancel the upgrade.
- The patron cannot demand a refund of their upgrade fee simply because they changed their mind after the solver ran.

**However — voluntary cancellation before T–3 is critical:**

Even though you have no statutory obligation to allow cancellations after bid placement, **you must allow bid cancellation up until the T–3 pre-auth run**. Reasons:
1. The patron has committed nothing (card stored but not charged) — refusing to cancel a zero-cost bid would be commercially absurd and reputationally damaging.
2. The CMA's consumer protection focus makes unreasonable restriction of cancellation a target for investigation.
3. It builds trust and reduces chargebacks.

**Design implication:** The patron portal must display a clearly accessible "Cancel my bid" button with no friction, available up until the moment the T–3 pre-auth job runs. After that point, cancellation is no longer possible (the solver has already executed), and this must be disclosed.

### 1.3 Required Disclosure Language at Bid Placement

This is the most important UX design output from this section. The following information must be presented to the patron **before they confirm their bid** — not buried in T&Cs:

```
REQUIRED PRE-BID DISCLOSURE (must be visible on the bid confirmation screen):

"By placing this bid, you are making a conditional offer to upgrade your seat. 
Your card will not be charged now. 

At [T-3 datetime], we will:
  1. Temporarily hold up to £[max_bid_amount] on your card to verify funds.
  2. Run our upgrade matching process.
  3. If your bid is selected, your card will be charged exactly £[max_bid_amount]. 
     No further confirmation from you is required.
  4. If your bid is not selected, the hold will be released and you pay nothing.

You may cancel this bid at any time before [T-3 datetime] with no charge.
Your original seat [Section, Row, Seat] is always guaranteed — regardless of outcome.

This upgrade service is separate from your original ticket purchase."
```

This disclosure must:
- Be presented in the main UI flow, not a modal or expandable section
- Require an explicit checkbox acknowledgement ("I understand my card will be charged if my bid is selected")
- Be stored server-side with a timestamp (proof of informed consent for any chargeback dispute)

---

## 2. DMCC Act 2024 & CMA Enforcement — Pricing Transparency

### 2.1 The Drip Pricing Risk

The **Digital Markets, Competition and Consumers (DMCC) Act 2024** is the most active regulatory area for ticketing businesses in the UK right now. The CMA has enforcement powers to fine up to **10% of global turnover** for drip pricing violations. Following the Oasis dynamic pricing controversy, ticketing is under specific CMA scrutiny.

**What drip pricing means for The Shakeup:**

Drip pricing is the practice of advertising a low headline price and revealing mandatory extra charges during checkout. The Shakeup's model is inherently clean because:
- The patron bids what they choose (no hidden fees added on top)
- There is no "booking fee" on top of the bid amount
- The charge is exactly the bid amount — no surprises

**However, one specific risk:** If The Shakeup ever introduces a "service fee" on top of the bid (e.g., "bid £40 + £3 platform fee"), this fee must be shown as part of the total from the first moment the patron sees the bid input, not revealed at the payment step.

**Recommendation:** Keep the model clean — the bid amount IS the total amount paid. The Shakeup's revenue is taken as a percentage of the charge from the theatre's side (the 25/75 split is invisible to the patron). This is both the right consumer experience AND eliminates the drip pricing risk entirely.

### 2.2 Dynamic Pricing Disclosure

The bid recommendation engine produces a suggested bid range. The CMA requires that **dynamic pricing must be clearly communicated**. 

**Design implication:** The recommendation UI must state explicitly:
- *"This is a suggested range based on current demand and availability. You may bid any amount above £[floor_price]."*
- Do NOT frame recommendations as "prices" — frame them as "bid guidance." This avoids any inference that The Shakeup is setting a dynamic price for the seat.
- Crucially: never imply that bidding above the recommended range guarantees success, or that bidding below it guarantees failure. The match probability displayed must be based on real data and carry appropriate uncertainty language.

### 2.3 Resale Price Cap — Not Applicable, But Understand Why

The new resale price cap (tickets cannot be resold above face value) does **not** apply to The Shakeup, because:
- Patrons are not reselling tickets — they are bidding for an upgrade to a different seat
- The original ticket remains valid and is voided only after a successful capture
- The upgrade bid is for an ancillary service, not a ticket purchase

This distinction must be clearly reflected in the T&Cs. The Shakeup is **not a secondary ticketing platform**. It is a venue-partnered upgrade service. This framing should be explicit in all marketing materials and the venue partnership agreement.

---

## 3. UK GDPR & ICO — Data Protection

### 3.1 Dual Controller Analysis

This is the most legally complex area. The Shakeup processes personal data (patron email, booking reference, seat) that originally belongs to the **venue's customer relationship**. The data protection roles must be precisely defined:

| Context | Data Controller | Data Processor | Notes |
|---------|----------------|----------------|-------|
| Venue's own patron data (bookings, purchase history) | **Venue** | **The Shakeup** (processing on venue's behalf) | Venue instructs The Shakeup to email their patrons |
| Bid data created on The Shakeup platform | **The Shakeup** | — | The Shakeup determines purpose and means of bid processing |
| Aggregate analytics & demand fingerprint | **The Shakeup** (joint or sole) | — | Derived data; venue has interest in it |
| Stripe payment data | **Stripe** (independent controller) | — | Stripe's own DPA applies |

**The critical complexity:** When The Shakeup uses venue patron data (emails, booking refs) to build its **demand fingerprint and DBIE training model**, it transitions from acting as a pure processor to acting as a **joint controller** or even independent controller. The ICO will look at the reality of the relationship, not just the contract label.

**Resolution strategy:**
- Define in the DPA exactly what The Shakeup can and cannot do with venue patron data
- The Shakeup processes booking data to: (a) send upgrade offer emails, (b) validate bids, (c) trigger resolution — all on the venue's instruction. **Processor.**
- The Shakeup uses **aggregated, anonymised** outcome data to train the DBIE and VDF. Individual patron data is never used in training directly — only aggregated zone-level outcomes. **This keeps The Shakeup as processor for personal data; the aggregate data is no longer personal data under UK GDPR.**
- This must be technically enforced (training pipeline receives anonymised feature vectors, not raw patron records) and legally documented in the DPA.

### 3.2 Data Processing Agreement (DPA) — Required Clauses

A DPA must be signed with **every venue** before any patron data is accessed. Key mandatory clauses under UK GDPR Article 28(3):

```
Mandatory DPA Clauses for The Shakeup ↔ Venue:

1. SUBJECT MATTER & DURATION
   "The Shakeup processes personal data solely to deliver the upgrade 
   marketplace service for the specified performances of [Production Name] 
   at [Venue] for the duration of the pilot agreement."

2. NATURE & PURPOSE OF PROCESSING
   Permitted purposes ONLY:
   a. Sending upgrade offer emails to eligible patrons
   b. Validating booking references against bid requests
   c. Executing ticket reissuance notifications post-resolution
   d. Generating anonymised performance analytics for the venue

3. CATEGORIES OF DATA SUBJECTS & PERSONAL DATA
   Data subjects: Theatre patrons who have purchased tickets for eligible performances
   Personal data: Email address, booking reference, seat identifiers, performance date
   Special categories: None (no health, biometric, or financial data stored beyond Stripe tokens)

4. SUB-PROCESSORS
   The Shakeup's authorised sub-processors (venue must approve):
   - Stripe, Inc. (payment processing — Stripe's own DPA governs card data)
   - SendGrid / Postmark (transactional email delivery)
   - [Cloud provider: AWS/GCP] (hosting and data storage)
   
5. RETENTION & DELETION
   Personal data deleted or anonymised within 30 days of performance date,
   except payment_event records retained for 7 years (financial regulation).
   Venue may request earlier deletion subject to regulatory minimum retention.

6. DATA BREACH NOTIFICATION
   The Shakeup will notify the venue within 48 hours of becoming aware of 
   any breach affecting venue patron data. Venue remains responsible for 
   ICO notification within 72 hours as the data controller.

7. TRAINING DATA RESTRICTION
   The Shakeup shall not use individual patron personal data for model training.
   Demand fingerprint and DBIE models are trained exclusively on aggregated, 
   anonymised zone-level outcomes where no individual is identifiable.

8. AUDIT RIGHTS
   The venue may request an annual compliance report from The Shakeup covering 
   data handling practices. On-site audits available with 30 days notice.
```

### 3.3 Lawful Basis for Processing

| Processing Activity | Lawful Basis | Notes |
|--------------------|-------------|-------|
| Sending upgrade offer email to patrons | **Legitimate Interest** (venue's interest in revenue; patron's interest in upgrade opportunity) | Venue must conduct LIA; soft opt-in under PECR if using existing customer relationship |
| Storing patron email + booking ref | **Legitimate Interest** (necessary to deliver the service the patron opted into via the bid) | |
| Card storage via Stripe SetupIntent | **Contractual necessity** (pre-bid card storage is explicitly consented to at bid placement) | |
| Processing bid outcomes | **Contractual necessity** (necessary to fulfil the conditional upgrade offer the patron made) | |
| DBIE model training | **Legitimate Interest** (aggregate analytics — no personal data involved) | Must be genuinely anonymised; confirm with ICO guidance on anonymisation |

### 3.4 PECR — Email Marketing Rules

The **Privacy and Electronic Communications Regulations (PECR)** govern marketing emails separately from UK GDPR. The upgrade offer email sent at T–7 is **not marketing** in the strict sense — it is a service communication about an existing booking. However:

- The email must be sent **by the venue** (or clearly on the venue's behalf) — not by The Shakeup independently
- The venue must have an existing direct marketing consent or soft opt-in relationship with the patron
- The email must relate directly to the patron's booking (it does — their specific performance)
- The Shakeup's name may appear in the email but the "From" sender must be the venue or a clearly branded venue subdomain (e.g., `upgrades@totoro-show.com powered by The Shakeup`)

**Design implication:** The email sending infrastructure must allow per-venue sender domains. White-labelled sending is not just a product nicety — it's a PECR compliance requirement.

### 3.5 DPIA Requirement

A **Data Protection Impact Assessment (DPIA)** is mandatory under UK GDPR Article 35 when processing is likely to result in a high risk to individuals. Triggers that apply to The Shakeup:

- ✅ **Automated decision-making** that significantly affects individuals: the solver deciding who gets upgraded — though "significantly affects" is debatable given the patron's original seat is retained
- ✅ **Large-scale processing** of sensitive data: once The Shakeup operates across multiple venues, it processes patron data at scale
- ✅ **Systematic profiling**: the DBIE model profiles patrons based on historical bidding behaviour (once post-MVP)

**Recommendation:** Conduct a DPIA before MVP launch (even for the pilot). The DPIA is a structured process, not a barrier — it demonstrates diligence to venue partners and to the ICO. A DPIA for the pilot (one venue, no DBIE model) will be relatively brief. Update it as the product scales.

**Key DPIA mitigation measure to document:** Patrons are never disadvantaged by the automated process — they always retain their original seat. The solver's automated decision only offers a benefit (upgrade), never removes one. This materially reduces the "significant effect" finding.

---

## 4. PCI DSS — Payment Card Industry Data Security Standard

### 4.1 Scope Determination

**Good news: The Shakeup qualifies for SAQ A** — the simplest PCI DSS self-assessment questionnaire (~22 questions, no penetration test required at this tier).

**Why SAQ A:**
- All cardholder data entry is handled entirely by **Stripe.js / Stripe Elements** in the patron's browser — raw card numbers never touch The Shakeup's servers or network
- The Shakeup stores only: `stripe_customer_id` (e.g., `cus_XXXX`) and `stripe_payment_method_id` (e.g., `pm_XXXX`) — these are tokens, not card data
- Stripe is the only entity that sees or stores actual card numbers

**What SAQ A requires from The Shakeup:**
- HTTPS on all pages that include the Stripe payment form (mandatory anyway)
- No card data in server logs, query strings, or error messages
- Annual self-assessment questionnaire completion
- A valid ASV vulnerability scan of internet-facing systems (quarterly)

**What The Shakeup never does (and must enforce technically):**
- Never log full request bodies that could contain card data
- Never accept card numbers via its own API endpoints
- Never cache or store Stripe webhook payloads that contain full card details

### 4.2 Off-Session Payment Security

The T–3 pre-auth and capture involve charging a card when the patron is not present. This is specifically handled by Stripe as a **Merchant-Initiated Transaction (MIT)**, which is explicitly out of scope for Strong Customer Authentication (SCA) under PSD2/PSR2017 — provided the initial SetupIntent was completed with SCA.

**Critical implementation requirement:**

When storing the patron's card at bid placement, the SetupIntent **must** be created with:
```python
stripe.SetupIntents.create({
    'customer': customer_id,
    'payment_method_types': ['card'],
    'usage': 'off_session',    # ← MANDATORY: tells Stripe this card will be charged off-session later
})
```

And confirmed with Stripe Elements that enforces 3DS2 authentication. If the patron's bank requires 3DS, it will prompt at this point (not at T–3). This is the only point where SCA is needed.

At T–3, the PaymentIntent is created as:
```python
stripe.PaymentIntents.create({
    'customer': customer_id,
    'payment_method': payment_method_id,
    'amount': max_bid_pence,
    'currency': 'gbp',
    'capture_method': 'manual',
    'confirm': True,
    'off_session': True,       # ← MANDATORY: flags as MIT, out of SCA scope
    'mandate_data': {
        'customer_acceptance': {
            'type': 'online',
            'online': { 'ip_address': patron_ip, 'user_agent': patron_user_agent }
        }
    }
})
```

The `mandate_data` field records the patron's consent (captured at bid placement) as evidence for the issuing bank.

**Failure mode:** If a card issuer refuses the off-session charge anyway (some do, particularly older European banks), the pre-auth returns a `requires_action` error. At MVP, this is treated as a `PRE_AUTH_FAILED` — the bid is excluded from the solver. This is an acceptable edge case at pilot scale.

---

## 5. Payment Services Regulations 2017 — FCA Scope

### 5.1 Is The Shakeup a Payment Institution?

**No — and this is important to maintain.**

The Shakeup does not:
- Hold customer funds in a segregated account
- Transfer money between parties directly
- Operate a payment account

The Shakeup **instructs Stripe** to process payments. Stripe is the FCA-regulated entity (authorised as an Electronic Money Institution). The Shakeup is acting as a **merchant** who has set up payment processing with an FCA-regulated PSP — which is identical to how any e-commerce business operates.

**The one risk:** If The Shakeup moves to a model where it **collects the full bid amount from the patron, holds it briefly, and then remits 75% to the venue** — that is money remittance and IS regulated. 

**This is why Stripe Connect is non-negotiable for the revenue split model.** With Stripe Connect:
- The patron pays into Stripe's regulated infrastructure
- Stripe automatically routes 75% to the venue's connected account and 25% to The Shakeup's platform account
- No funds ever sit in The Shakeup's bank account in transit
- The Shakeup is not a payment institution; Stripe is

**At MVP (before Stripe Connect is implemented):**
The current MVP model is: The Shakeup charges the full bid amount to the patron → The Shakeup invoices the venue monthly for 75% of total upgrade revenue → Venue pays The Shakeup's invoice → The Shakeup remits the 75%.

This **does** involve The Shakeup briefly holding funds (the 75% owed to the venue sits in The Shakeup's bank account between charge and monthly remittance). For a pilot with one venue and small volumes, the FCA is unlikely to take interest. However, this must be resolved before scaling to multiple venues, which is why Stripe Connect is a V1 requirement, not a Phase 2 nicety.

**Interim MVP mitigation:** Structure the commercial terms with LW Theatres as "The Shakeup remits 75% of upgrade revenue within 15 business days of each performance date." Keep this window short and document it clearly. Consider a separate client account for holding venue remittances.

---

## 6. Automated Decision-Making (UK GDPR Article 22)

The CP-SAT solver makes automated decisions about who gets upgraded. Under UK GDPR Article 22, purely automated decisions that produce **"legal or similarly significant effects"** on individuals require:
- The right to obtain human intervention
- The right to express their point of view
- The right to contest the decision

**Does the solver's decision qualify as "significantly affecting" a patron?**

Likely **no**, because:
- The patron's original ticket is unaffected — no negative consequence flows from a non-match
- The upgrade is a voluntary, additional service
- The patron set their own bid parameters (they are not surprised by the outcome)

**However, best practice:** 

1. Include in the T&Cs a statement that upgrade allocation is determined by an automated optimisation process, and that patrons may contact The Shakeup to understand why their bid was not selected.
2. The solver must be auditable — the `solver_run` table stores all inputs and outputs so that any individual bid outcome can be explained post-hoc. ("Your bid of £35 for Stalls Centre was not matched because all 23 available seats in Stalls Centre were assigned to higher bids.")
3. Do not use automated decisions to permanently profile or exclude patrons — each performance is independent. A patron whose bid didn't succeed this time gets a fresh opportunity next show.

---

## 7. Summary: Product Design Changes Required

These are the concrete changes to the product spec that flow from this legal analysis:

| # | Change | Priority | Affects |
|---|--------|----------|---------|
| 1 | Pre-bid disclosure screen with explicit checkbox consent before card storage | 🔴 Critical — before MVP | Patron UX Flow |
| 2 | SetupIntent must use `usage: 'off_session'` and force 3DS at bid placement | 🔴 Critical — before MVP | API / Stripe integration |
| 3 | "Cancel bid" button freely accessible until T–3, with no friction | 🔴 Critical — before MVP | Patron UX Flow |
| 4 | Bid total = bid amount (no added platform fee visible to patron) | 🔴 Critical — before MVP | Financial model |
| 5 | Upgrade offer email sent from venue's domain (white-labelled From:) | 🔴 Critical — before MVP | Email infrastructure |
| 6 | DPA template drafted and signed with LW Theatres before data access | 🔴 Critical — before MVP | Legal / business |
| 7 | DPIA conducted and documented before pilot launch | 🟡 High — before pilot | Internal process |
| 8 | Training pipeline must use anonymised aggregate data only | 🟡 High — before DBIE launch | DBIE / VDF pipelines |
| 9 | Stripe Connect implemented before scaling beyond pilot | 🟡 High — V1 | Financial infrastructure |
| 10 | Solver audit trail: every bid outcome explainable from stored inputs | 🟢 Standard — already in data model | solver_run table |
| 11 | T&Cs must explicitly state: "This is not a secondary ticket platform" | 🟢 Standard — before launch | Legal / marketing |
| 12 | Bid recommendation UI language: "guidance" not "price" | 🟢 Standard — before launch | Patron UX Flow |

---

## 8. Legal Counsel Checklist (Pre-Launch)

These items should be reviewed by a qualified solicitor before the pilot launches:

- [ ] T&Cs and Privacy Policy reviewed by consumer law specialist
- [ ] DPA template reviewed by data protection solicitor
- [ ] DPIA conducted (can be internal, but document it formally)
- [ ] Confirmation from payment law specialist that MVP remittance structure (pre-Stripe Connect) does not trigger PSR2017 money remittance licensing
- [ ] IP solicitor review of CUCR + SCOS combination for provisional patent applicability
- [ ] Venue partnership agreement reviewed (separate from DPA — this is the commercial term sheet)
- [ ] Consider ICO registration as a data controller (£40–£60/year — straightforward, but mandatory if you process personal data for commercial purposes)
