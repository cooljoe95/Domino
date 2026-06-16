# The Shakeup — UX Flow Specification
### Version 0.1 | 2026-05-26
### Pilot Reference: My Neighbour Totoro @ Gillian Lynne Theatre

---

## Design Principles

Before the screen-by-screen breakdown, five principles that govern every design decision:

1. **Mobile-first, always.** The T-7 email opens on a Totoro fan's iPhone on the Tube. Every patron-facing screen is designed at 390px width first, scaled up second.
2. **Three taps to bid.** From magic link landing to a bid in the basket: tap a zone → enter amount → confirm. Legal disclosure and card entry on first use only.
3. **Zero confusion at the moment of charge.** The patron must never be surprised. Every email and screen states exactly when and how much they'll be charged.
4. **The theatre's brand, not ours.** The patron's experience feels like a premium service from the Totoro production. The Shakeup's name appears in the footer, not the headline.
5. **The manager's dashboard is a decision support tool, not a data dump.** Surface the one thing they need to act on, prominently. Everything else is available but secondary.

---

# PART A: PATRON UX FLOW

## A1. Entry Point: The T–7 Upgrade Offer Email

**Trigger:** Automated job at `curtain_datetime - 7 days`. Sent from `upgrades@totoro-show.com` (white-labelled — PECR compliance).

**From:** My Neighbour Totoro | `upgrades@totoro-show.com`

---

### Subject Line A/B Tests (run all three in rotation, optimise from week 2):

| Variant | Subject Line | Hypothesis |
|---------|-------------|------------|
| A | `An upgrade for your Totoro seats, [First Name]` | Personalisation + specificity |
| B | `You're invited: bid for a better view of Totoro` | Action-oriented, curiosity |
| C | `Your Totoro seats on 15 Oct — there's an offer inside` | Date-specific urgency |

---

**Email body structure (plain-language, not marketing copy):**

```
[Totoro production logo — wordmark only, no Ghibli characters]

Hi [First Name],

You're coming to see My Neighbour Totoro on Thursday 15 October at 7:30pm.
Your seats: Stalls Side, Row C, Seats 14–15.

We're offering a small number of seat upgrades for this performance.
If you'd like to move to a more central position, you can place a bid —
you name your maximum price, and we'll let you know 3 days before
whether your bid was successful.

[  SEE YOUR UPGRADE OPTIONS  ]   ← single, prominent CTA

• No charge until your bid is confirmed
• Your original seats are always guaranteed
• Cancel your bid anytime before Tuesday 12 October

This offer is available until Tuesday 12 October at 10:00am.

Questions? Reply to this email or visit [help link].

─────────────────────────────────────────────────
Powered by The Shakeup | theshakeup.com
Sent on behalf of My Neighbour Totoro at the Gillian Lynne Theatre
Unsubscribe from upgrade offers [link]
```

**UX notes:**
- Single CTA — no secondary links competing for attention
- Plain English, not marketing voice
- Explicit unsubscribe from *upgrade offers* (not from all venue communications — these are separate lists)
- Mobile preview text: `Your seats are Stalls Side, Row C — here's how to upgrade them.`

---

## A2. Screen: Magic Link Landing

**URL:** `theshakeup.com/u?t={token}` (short, clean, not scary-looking)
**Trigger:** Patron taps the CTA button in the email

```
┌─────────────────────────────────────────┐
│  [Totoro wordmark]      powered by [S]  │
│                                         │
│  Welcome                                │
│  ─────────────────────────────────────  │
│                                         │
│  Your performance                       │
│  My Neighbour Totoro                    │
│  Thursday 15 October · 7:30pm          │
│  Gillian Lynne Theatre                  │
│                                         │
│  Your current seats                     │
│  Stalls Side · Row C · Seats 14–15     │
│                                         │
│  Upgrade offers close in               │
│  [  4 days  14 hours  22 mins  ]       │ ← countdown
│                                         │
│  ┌─────────────────────────────────┐   │
│  │    See upgrade options   →      │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Not you? [Get a new link]             │
└─────────────────────────────────────────┘
```

**UX notes:**
- No login, no password, no account creation. The token IS the authentication.
- "Not you?" link triggers a new magic link to the booking's email address — handles forwarded emails gracefully
- Countdown creates mild urgency without being aggressive
- Patron sees their booking confirmed immediately — reduces anxiety ("is this real?")

**Error states:**
- Token expired: `"This link has expired. Your original seats are confirmed. [Contact box office]"`
- Token already used: Redirect to their current bid status page (if bids exist) or "offer closed" state
- Bidding closed (T–3 passed): `"Upgrade offers for this performance are now closed. [See your result →]"`

---

## A3. Screen: Interactive Seat Map (Core Screen)

![Patron bid portal seat map](patron_seat_map_screen_1779752793131.png)

This is the central product screen. Everything hinges on making this feel immediate, clear, and trustworthy on a phone screen.

```
┌─────────────────────────────────────────┐
│  My Neighbour Totoro                    │
│  Thu 15 Oct · 7:30pm                   │
│  Your seats: Stalls Side · Row C · 14–15│
│                                         │
│  ┌─────────────────────────────────┐   │
│  │                                 │   │
│  │       [SEAT MAP SVG]            │   │
│  │                                 │   │
│  │   Circle: [teal glow]           │   │
│  │                                 │   │
│  │   Stalls:                       │   │
│  │   [grey][GREEN GLOW][grey]      │   │
│  │   Left   Centre    Right        │   │
│  │                                 │   │
│  │   [AMBER] = your current seats  │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ── Tap a highlighted zone to bid ──    │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ 🟢 Stalls Centre                  │ │
│  │ Central view · full stage         │ │  ← bottom sheet,
│  │ 18 seats available                │ │    slides up on tap
│  │ Bid guidance: £25 – £55           │ │
│  │ At £40: ~70% match probability    │ │
│  │                                   │ │
│  │      [  Place bid  →  ]           │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [My bids (0)]        [Need help?]      │
└─────────────────────────────────────────┘
```

**Zone colour coding:**
| Colour | Meaning |
|--------|---------|
| 🟡 Amber / pulsing | Patron's current seats |
| 🟢 Green glow | Eligible upgrade destination — available |
| 🔵 Teal glow | Secondary eligible destination |
| ⬜ Dark grey | Not eligible (same or lower desirability, or SOLD OUT) |
| 🔴 Faint red outline | HELD — not available for upgrade this show |

**Bottom sheet panel (appears when zone is tapped):**
- Zone name and honest sightline description (from venue's own config)
- Available seat count (live)
- "Bid guidance" range — explicitly labelled as guidance, not a price
- Match probability at the midpoint of the guidance range
- "Place bid" CTA
- Swipe down to dismiss, tap another zone to switch

**Bid heatmap overlay (subtle):**
A faint intensity overlay on the seat map shows bid concentration from other patrons (anonymised). If Stalls Centre is already dense with bids, a slightly warmer overlay cues the patron that competition is high — without revealing individual bid amounts. This is honest demand signalling.

**UX compliance notes:**
- Bid guidance explicitly NOT labelled "price" — it is "guidance" (CMA requirement)
- Match probability shown at a specific bid amount, not as a guarantee
- Available seat count is live from `seat_state` — no inflated numbers

---

## A4. Screen: Bid Entry

Appears when patron taps "Place bid" from the zone detail panel.

```
┌─────────────────────────────────────────┐
│  ← Back          Stalls Centre          │
│                                         │
│  Your bid for Stalls Centre             │
│  ─────────────────────────────────────  │
│                                         │
│  Maximum you'd pay for this upgrade     │
│                                         │
│  £ [       ]    ← large input, focused  │
│                                         │
│  Guidance: £25–£55 · Floor: £20        │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ At this amount:                 │   │  ← updates live
│  │ Match probability: ~70%         │   │     as user types
│  └─────────────────────────────────┘   │
│                                         │
│  ── Your party ──────────────────────   │
│  2 seats (Row C, 14–15)                 │
│                                         │
│  ○ Keep us together (same section)      │
│  ○ Happy to sit in same section         │
│    even if not adjacent at this stage   │
│                                         │
│  ── Freebie offers ──────────────────   │
│  □ I'd also consider a lateral move     │
│    to a less central position if        │
│    offered a bar credit bundle          │
│    (venue's discretion)                 │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │      Add to my bids  +          │   │
│  └─────────────────────────────────┘   │
│                                         │
│  You can place bids for multiple zones. │
│  Only one bid will ever be filled.      │
└─────────────────────────────────────────┘
```

**UX details:**
- Bid input starts **blank** — not pre-filled with the recommended midpoint (CMA compliance: the recommendation must not become a default that nudges)
- Live match probability updates as the patron types their amount — this is the key engagement mechanic. Watching it jump from 45% at £30 to 72% at £45 is intuitive and informative
- Party integrity options shown only if booking has >1 seat
- Freebie option shown only if venue has configured freebie bundles
- "You can place bids for multiple zones. Only one bid will ever be filled." — displayed before add-to-basket, managing expectations proactively

**Validation:**
- Below floor price: inline error `"Minimum bid for this section is £20"`
- Non-numeric input: numeric keyboard on mobile (no opportunity for this error)
- Empty input: CTA remains disabled until a valid amount is entered

---

## A5. Screen: Bid Basket

```
┌─────────────────────────────────────────┐
│  ← Back              My Bids (2)        │
│                                         │
│  My Neighbour Totoro · Thu 15 Oct       │
│  ─────────────────────────────────────  │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 🟢 Stalls Centre                │   │
│  │ Max bid: £45 · ~70% match       │   │
│  │ 2 seats · keep together         │   │
│  │                          [Edit] │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 🔵 Circle Centre                │   │
│  │ Max bid: £28 · ~55% match       │   │
│  │ 2 seats · keep together         │   │
│  │                    [Edit] [✕]   │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [+ Add another zone]                   │
│                                         │
│  ─────────────────────────────────────  │
│  Only one bid will be filled.           │
│  Stalls Centre is your higher bid       │
│  and will be prioritised by the         │
│  matching process.                      │
│                                         │
│  Upgrade offers close                   │
│  Tue 12 Oct · 10:00am                  │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   Continue to payment setup →   │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**UX notes:**
- Each bid shows key details at a glance — section, amount, probability, party preference
- Edit restores the bid entry screen pre-filled with the current values
- ✕ removes the bid (with a brief undo toast: "Bid removed · [Undo]")
- "Stalls Centre is your higher bid and will be prioritised" — transparent about how the solver handles multi-bid patrons. Reduces the "why wasn't I upgraded?" complaint if they only win their second choice
- If patron has only 1 bid, the "only one bid will be filled" message is hidden (no need to explain to single-bid patrons)
- "Continue to payment setup" — deliberately NOT "pay now" — because no money changes hands here

---

## A6. Screen: Pre-Bid Disclosure + Card Entry *(first use only)*

This is the legally mandated disclosure screen. It must be impossible to skip and must generate a timestamped consent record.

```
┌─────────────────────────────────────────┐
│  ← Back        Set up payment          │
│                                         │
│  How this works                         │
│  ─────────────────────────────────────  │
│                                         │
│  ① Your card is NOT charged today.      │
│                                         │
│  ② On Tuesday 12 October at 10:00am:   │
│     • We hold up to £45 on your card   │
│       to verify funds.                  │
│     • Our matching process runs.        │
│                                         │
│  ③ If your bid is selected:            │
│     Your card is charged £45.          │
│     A new ticket is sent to you.       │
│     No further action needed.           │
│                                         │
│  ④ If your bid is not selected:        │
│     The hold is released. You pay      │
│     nothing. Your original seats       │
│     are confirmed.                      │
│                                         │
│  You can cancel any bid before          │
│  Tue 12 Oct · 10:00am at no cost.      │
│  Your original seats are always         │
│  guaranteed regardless of outcome.      │
│                                         │
│  ─────────────────────────────────────  │
│  □ I understand — charge my card up    │
│    to £45 if my bid is selected on     │  ← explicit checkbox
│    12 October without further          │     REQUIRED before
│    confirmation from me.               │     card entry unlocks
│  ─────────────────────────────────────  │
│                                         │
│  [Card entry — Stripe Elements]         │
│  [Card number        ] [MM/YY] [CVC]   │  ← locked until checkbox
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   Save card & confirm bids  →   │   │  ← disabled until both
│  └─────────────────────────────────┘   │     checkbox + valid card
│                                         │
│  🔒 Payments secured by Stripe.         │
│     Your card number is never stored    │
│     by The Shakeup.                     │
└─────────────────────────────────────────┘
```

**Critical UX/legal notes:**
- The checkbox wording is legally precise: it names the exact amount, the exact date, and the "without further confirmation" clause. This is the consent record.
- The checkbox must be **unchecked by default** (pre-ticking would negate consent under UK GDPR)
- Card entry fields are **disabled** (visually greyed out) until checkbox is ticked
- "Save card & confirm bids" button is disabled until both checkbox AND valid card details are present
- Server records: `{patron_id, consent_timestamp, ip_address, user_agent, bid_amounts[], performance_id}` — stored before the Stripe SetupIntent is confirmed
- **Returning patrons** (second show, same card stored): This screen is skipped and replaced by a simpler "Confirm bids" screen showing their stored card (last 4 digits) and an updated disclosure. Checkbox still required each time — consent is per-bid-session, not a one-time lifetime consent.

---

## A7. Screen: Bid Confirmation

```
┌─────────────────────────────────────────┐
│                                         │
│           ✓                             │
│       Bids confirmed                    │
│                                         │
│  My Neighbour Totoro · Thu 15 Oct       │
│  ─────────────────────────────────────  │
│                                         │
│  Your 2 bids:                           │
│  Stalls Centre · max £45               │
│  Circle Centre · max £28               │
│                                         │
│  What happens next                      │
│  ─────────────────────────────────────  │
│  Mon 11 Oct  We'll remind you tomorrow  │
│  Tue 12 Oct  We run the matching        │
│  10:00am     process and let you know   │
│              by 12:00pm the same day.   │
│                                         │
│  Your original seats are guaranteed     │
│  whatever happens.                      │
│                                         │
│  ─────────────────────────────────────  │
│  [📅 Add to calendar]                   │
│  [View / cancel my bids]               │
│                                         │
│  A confirmation has been sent to        │
│  sarah@example.com                      │
└─────────────────────────────────────────┘
```

**UX notes:**
- "Add to calendar" creates a calendar event for the T–3 resolution datetime — not the show itself. This mental anchoring reduces the "my card was charged without warning" complaint.
- "View / cancel my bids" deep-links to a bid management page accessible from the magic link (or from the confirmation email)
- Confirmation email sent immediately with same information

---

## A8. Email: T–4 Day Reminder

**Subject:** `Your Totoro upgrade bids — processed tomorrow`
**From:** `upgrades@totoro-show.com`

```
Hi [First Name],

Just a reminder — your upgrade bids for My Neighbour Totoro
(Thu 15 Oct, 7:30pm) will be processed tomorrow morning.

Your bids:
  Stalls Centre · max £45
  Circle Centre · max £28

What happens tomorrow (Tue 12 Oct at 10:00am):
  We'll temporarily hold up to £45 on your card.
  If your bid is selected, your card is charged and
  a new ticket is sent to you.
  If not, the hold is released and you pay nothing.

If you'd like to cancel either bid before tomorrow,
you have until 10:00am:

  [Cancel or change my bids]

Your original seats (Stalls Side, Row C, 14–15)
are confirmed regardless.

See you at the show,
My Neighbour Totoro at the Gillian Lynne Theatre
```

---

## A9. Emails: T–3 Resolution Outcomes (Three Variants)

### Variant A: CONFIRMED ✅

**Subject:** `🎭 Your upgrade is confirmed — new seats for Totoro`

```
[Totoro wordmark]

You're upgraded.

My Neighbour Totoro · Thu 15 Oct · 7:30pm

Your new seats
Stalls Centre · Row F · Seats 7–8

[  View your new ticket  ]

You were charged £45 to your card ending 4242.

What to bring: Your new ticket (attached / in the app).
Your original ticket is now void — please use the new one.

If there's any issue at the box office on the night,
show this email and call: [venue box office number]

─────────────────────────────────────────
Enjoy the show.
My Neighbour Totoro at the Gillian Lynne Theatre
Powered by The Shakeup

[Rate your experience] ← 1-tap star rating in email
```

**Notes:**
- Subject uses emoji — appropriate for a Totoro fan base; increases open rate
- New seat shown prominently (section, row, seat number — not just "Stalls Centre")
- Exact charge amount and card last 4 stated — eliminates confusion
- Old ticket void warning is prominent, not buried
- Box office phone number for show day emergencies
- One-tap star rating generates post-show satisfaction data without requiring a separate survey visit

---

### Variant B: UNMATCHED ❌

**Subject:** `Your Totoro upgrade — here's what happened`

```
[Totoro wordmark]

No upgrade this time.

My Neighbour Totoro · Thu 15 Oct · 7:30pm

Your bid for Stalls Centre (£45) placed 4th out of 
3 available seats this performance. Your bid for 
Circle Centre (£28) was not matched either.

Nothing was charged to your card. The hold has
been released.

Your original seats are confirmed and ready:
Stalls Side · Row C · Seats 14–15

Keep your original ticket — it's still valid.

─────────────────────────────────────────
Coming to another Totoro performance?
You'll get another upgrade opportunity 7 days before.

See you at the show,
My Neighbour Totoro at the Gillian Lynne Theatre
```

**Notes:**
- "Placed 4th out of 3 available seats" — the bid rank transparency from the risk register (R14). This specific, honest explanation transforms frustration into understanding.
- "Nothing was charged" stated explicitly and first — this is the patron's primary concern
- Original ticket validity confirmed — patron knows exactly what to do
- Future opportunity mentioned — closes the loop without overselling

---

### Variant C: PRE_AUTH_FAILED 💳

**Subject:** `We couldn't process your Totoro upgrade bid`

```
[Totoro wordmark]

We couldn't verify your payment.

My Neighbour Totoro · Thu 15 Oct · 7:30pm

When we attempted to verify funds for your upgrade
bid today, we weren't able to complete the check
on your card ending 4242.

Your bids have not been entered into the matching
process. Nothing was charged.

Your original seats are confirmed:
Stalls Side · Row C · Seats 14–15

Your original ticket is valid — no action needed.

─────────────────────────────────────────
If you'd like to know more about why this happened,
your bank can advise. Common reasons include
temporary card holds or spending limits.

See you at the show.
My Neighbour Totoro at the Gillian Lynne Theatre
```

**Notes:**
- Diplomatic about the reason ("we couldn't complete the check") — not accusatory
- "Nothing was charged" first and foremost
- Original seat confirmed prominently
- No attempt to upsell or ask them to re-enter card details (this is too close to showday for that to be useful)

---

---

# PART B: MANAGER DASHBOARD UX FLOW

## B1. Onboarding Wizard — New Venue Setup

A stepped wizard with a persistent progress indicator. Cannot be completed in one sitting — designed to save progress at each step.

```
Step 1 of 4: Venue details
Step 2 of 4: Seat map
Step 3 of 4: Upgrade rules
Step 4 of 4: Review & launch

[●●○○]  Step 2: Seat map
```

**Step 1 — Venue Details:**
```
Venue name:          [Gillian Lynne Theatre          ]
Address:             [Drury Lane, London, WC2B 5BP   ]
Ticketing system:    [Line-Up                    ▼   ]
                      Spektrix / Tessitura / TixTrack
                      Line-Up / Manual (CSV)

Contact name:        [Martin Crosier                 ]
Contact email:       [m.crosier@lwtheatres.co.uk     ]

[ Save and continue → ]
```

---

**Step 2 — Seat Map Upload:**

```
┌─────────────────────────────────────────────────────┐
│  Upload seat map                                    │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │                                               │ │
│  │   Drag your seat map file here               │ │
│  │   or [browse files]                          │ │
│  │                                               │ │
│  │   Accepted formats: JSON, CSV                │ │
│  │   [Download template]                        │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  Required columns (CSV):                           │
│  seat_id · section · row · number · x · y ·        │
│  accessibility_flag · desirability_score           │
│                                                     │
│  ── OR ──                                           │
│                                                     │
│  We have this venue on file:                        │
│  ○ Gillian Lynne Theatre — Standard Proscenium     │
│    (1,295 seats · last updated 2026-03-14)         │
│  → Use this layout                                  │
└─────────────────────────────────────────────────────┘
```

**After upload — map preview:**
- Interactive seat map rendered from uploaded data
- Seat count per section displayed
- Accessibility seats flagged in a distinct colour
- "Does this look correct?" confirmation before proceeding
- Error messages if CSV has missing columns or unrecognised section names

---

**Step 3 — Upgrade Ruleset:**

This is the most complex step. Split into three sub-sections with a tab bar.

**Tab A: Upgrade directions**
```
Which sections can patrons upgrade from → to?

Drag to connect sections, or use the toggles:

[SECTION GRAPH — visual directed arrows]

Stalls Side   ──►  Stalls Centre  ✓
Stalls Rear   ──►  Stalls Centre  ✓
Circle Side   ──►  Circle Centre  ✓
Circle Rear   ──►  Circle Centre  ✓
Circle Rear   ──►  Stalls Centre  ✓
Circle Side   ──►  Stalls Centre  ✓

Floor prices (minimum bid):
Stalls Side → Stalls Centre:  £ [20]
Stalls Rear → Stalls Centre:  £ [15]
Circle → Stalls Centre:       £ [30]
...
```

**Tab B: Inventory holds**
```
How many seats to reserve from upgrades per section?
(Based on your demand fingerprint — editable)

Section          Fingerprint rec.   Your setting
─────────────────────────────────────────────────
Stalls Centre    Hold 4             [  4  ]  ▲▼
Circle Centre    Hold 2             [  2  ]  ▲▼

"These seats are reserved for late single-ticket
sales and are excluded from the upgrade pool."

ℹ Upload historical sales data to improve these
  recommendations. [Upload sales history]
```

**Tab C: Freebie bundles (optional)**
```
Offer freebies to patrons willing to make a
lateral or split move?

[Toggle: Enable freebie bundles]

Bundle 1:  Bar credit £10 + programme
           Offer when: patron moves to Circle Side from Circle Centre
           Estimated cost to venue: £12
           [Edit] [Remove]

[+ Add another bundle]

ℹ Freebie fulfilment is handled by your team at
  the bar. The Shakeup sends patrons a voucher code
  to redeem on arrival.
```

---

**Step 4 — Review & Launch:**
```
┌──────────────────────────────────────────┐
│  Ready to launch                         │
│                                          │
│  ✓ Venue: Gillian Lynne Theatre          │
│  ✓ Layout: Standard Proscenium          │
│    1,295 seats · 6 sections             │
│  ✓ Upgrade rules: 6 direction pairs     │
│  ✓ Inventory holds: 6 seats total       │
│  ✓ Freebie bundles: 1 configured        │
│                                          │
│  First production to add:               │
│  [My Neighbour Totoro              ]    │
│  Start date: [15 Sep 2026]             │
│  End date:   [10 Jan 2027]             │
│  Layout:     Standard Proscenium  ▼    │
│                                          │
│  [  Launch venue →  ]                   │
└──────────────────────────────────────────┘
```

---

## B2. Per-Show Live Dashboard

![Manager dashboard](manager_dashboard_screen_1779752804440.png)

Accessible from `dashboard.theshakeup.com`. Auto-refreshes every 60 seconds during the bid window.

**Layout: three-column desktop / single-column mobile**

**Top bar:**
```
My Neighbour Totoro  ·  Thu 15 Oct · 7:30pm  ·  T-minus 71 hours
[◀ Prev show]                                          [Next show ▶]
```

**KPI row (3 cards):**
```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  47          │  │  £1,840      │  │  ~26         │
│  Bids placed │  │  Bid value   │  │  Proj. upg.  │
│  ▲ +12 today │  │              │  │  est. £684   │
└──────────────┘  └──────────────┘  └──────────────┘
```

**Bid heatmap (left/centre, 60% width):**
- Seat map SVG with bid intensity overlaid as a heat gradient
- Toggle: "Show bid count" / "Show bid value" 
- Hover/tap on a section reveals: `"Stalls Centre: 31 bids · £1,250 total value · 18 available seats"`
- Sections with 0 bids shown as muted

**Live feed (right, 40% width):**
```
Live bids                              [Filter ▼]
─────────────────────────────────────────────────
2 min ago   Circle Centre      £32
5 min ago   Stalls Centre      £55   ← highest today
8 min ago   Stalls Centre      £41
12 min ago  Circle Centre      £28
...
```
- Feed shows section and amount only — no patron details
- Highest bid of the day highlighted

**Occupancy panel (bottom left):**
```
Occupancy breakdown         1,295 total seats
────────────────────────────────────────────
Sold (confirmed bookings):          1,010  78%
Available for upgrades:               209  16%
Inventory hold:                         6  <1%
Bid-vacating (origin seats):           70   5%

[View full seat map]
```

**Solver countdown + actions (bottom right):**
```
┌──────────────────────────────────────────┐
│  Solver runs in                          │
│  71 : 04 : 22                            │
│  Tue 12 Oct · 10:00am                   │
│                                          │
│  [  Run solver early  ]                  │
│  (requires manual approval)              │
│                                          │
│  [  Pause upgrade offers  ]              │
│  (stops new bids; does not affect        │
│   existing bids)                         │
└──────────────────────────────────────────┘
```

---

## B3. Solver Review Screen (Optional — if venue opts into manual approval)

Appears after solver completes, before resolution runs. The manager has a 30-minute window to review.

```
┌──────────────────────────────────────────────────────┐
│  Solver complete · Review proposed upgrades          │
│  My Neighbour Totoro · Thu 15 Oct · 7:30pm          │
│                                                      │
│  26 upgrades proposed · £1,014 total revenue        │
│  ──────────────────────────────────────────────────  │
│                                                      │
│  Section-level summary:                              │
│  Stalls Centre:  18 seats filled / 18 available      │
│  Circle Centre:   8 seats filled / 14 available      │
│                                                      │
│  [Before / After seat map toggle]                    │
│  ← BEFORE (current)   AFTER (proposed) →            │
│                                                      │
│  Upgrade list (first 5 of 26):                      │
│  ─────────────────────────────────────────────────  │
│  Booking REF-xxx  Stalls Side C14  →  Stalls Ctr F7  £45 │
│  Booking REF-xxx  Circle Rear A3   →  Stalls Ctr H12 £55 │
│  ...                                                 │
│                                                      │
│  [Download full list as CSV]                         │
│                                                      │
│  ──────────────────────────────────────────────────  │
│                                                      │
│  ┌────────────────┐    ┌────────────────────────┐   │
│  │  ← Reject all  │    │  Approve and execute → │   │
│  └────────────────┘    └────────────────────────┘   │
│                                                      │
│  Review window closes in: 27:14                      │
│  If no action taken: auto-approved at 10:27am        │
└──────────────────────────────────────────────────────┘
```

**UX notes:**
- Before/After toggle makes the impact of the solver immediately visual — not just a list of numbers
- Auto-approve timer means the manager doesn't need to be watching; they only need to intervene if something looks wrong
- "Reject all" is available but should almost never be needed — include a friction confirmation: "Are you sure? This will release all pre-authorisations and notify 26 patrons that their bids were unsuccessful."
- "Download full list" creates the box office CSV in one click

---

## B4. Resolution Monitoring Screen

Live during the 30-minute resolution window after approval.

```
┌──────────────────────────────────────────┐
│  Resolution in progress                  │
│  My Neighbour Totoro · Thu 15 Oct        │
│                                          │
│  ████████████████████░░░░  82%           │
│  21 of 26 processed                      │
│                                          │
│  ✓ Confirmed:       19                   │
│  ✕ Unmatched:        2                   │
│  ⚠ Payment failed:   0                   │
│  ⟳ In progress:      5                   │
│                                          │
│  Revenue captured so far: £874           │
│                                          │
│  ─────────────────────────────────────   │
│  [  View individual outcomes  ]          │
│                                          │
│  ⚠ Alerts (0)                           │
│  No issues detected.                     │
└──────────────────────────────────────────┘
```

**Alert states that appear here:**
- 🔴 `Payment capture failed — [Booking ref]. Retrying in 30s. [Contact patron manually]`
- 🔴 `Ticket reissuance failed — [Booking ref]. Payment has been automatically refunded. [Action required]`
- 🟡 `2 unmatched bids — patrons notified automatically.`

---

## B5. Post-Show Analytics Report

Available 24h after curtain. Accessible from the Dashboard under "Past performances."

```
┌─────────────────────────────────────────────────────┐
│  Post-show report                                   │
│  My Neighbour Totoro · Thu 15 Oct · 7:30pm         │
│                                                     │
│  ─── Revenue ────────────────────────────────────── │
│  Upgrade revenue (gross):          £988             │
│  Your share (75%):                 £741             │
│  Upgrades confirmed:               26               │
│  Average charge per upgrade:       £38              │
│                                                     │
│  ─── Participation funnel ──────────────────────── │
│                                                     │
│  Eligible patrons emailed:     519  ████████████   │
│  Emails opened:                234  █████          │  45%
│  Bids placed:                   47  █              │   9%
│  Reached solver:                43  █              │   8%
│  Upgrades confirmed:            26  ▌              │   5%
│                                                     │
│  ─── Section performance ───────────────────────── │
│  Section        Bids   Filled   Avg bid   Revenue  │
│  Stalls Centre   31      18      £43       £774    │
│  Circle Centre   12       8      £27       £216    │
│                                                     │
│  ─── Patron satisfaction ───────────────────────── │
│  Post-upgrade ratings received:  14 / 26  (54%)    │
│  Average rating:                 ★★★★½  4.4 / 5    │
│                                                     │
│  ─── Vs. previous shows ────────────────────────── │
│  [Comparison chart — this show vs last 5]          │
│                                                     │
│  [Download PDF report]    [Export CSV]             │
└─────────────────────────────────────────────────────┘
```

**UX notes:**
- Participation funnel is the most important diagnostic tool. If "Bids placed" is low, the problem is email copy or bid portal friction. If "Reached solver" is low, the problem is pre-auth failure rate. If "Upgrades confirmed" is low, the problem is solver inventory constraints.
- Section performance table lets the manager identify which zones generate the most bid revenue — informs floor price and inventory hold decisions for future shows
- Post-upgrade satisfaction ratings (via the star rating link in the confirmation email) appear here. If a specific section consistently rates below 4.0, flag it for sightline description review
- "Vs. previous shows" comparison chart — after 3+ shows, this becomes the manager's primary proof that the system is working and growing

---

## B6. Manager Mobile Experience

The manager dashboard is desktop-first but the key show-day actions must work on mobile. On mobile, the dashboard collapses to:

```
[Header: Show name · T-minus timer]

[ 47 Bids ] [ £1,840 Value ] [ ~26 Proj. ]

[Tap for bid heatmap — full screen]

[Solver countdown — large]
[Approve solver / Run early]

[Resolution status — when running]
```

The post-show report is email-delivered as well as web-accessible, so the manager doesn't need to log in to see the headline numbers.
