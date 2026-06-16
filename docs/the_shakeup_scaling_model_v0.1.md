# The Shakeup — Financial Scaling Model
### Version 0.1 | 2026-05-26
### Scenarios: No-guidance pilot (£10/seat) → Calibrated (£18/seat) | 80/20 split

---

## Key Corrected Assumptions

### The Hotel Analogy is Wrong — Per-Person Pricing Changes Everything

A Marriott room upgrade bid of £38 applies regardless of whether 1 or 4 guests sleep in the room.
In theatre, **every seat is a separate bid**. A family of 4 bidding £10/person generates £40 — 
comparable to the hotel room upgrade, but at a much lower per-person price.

```
Hotel upgrade:       £38 flat  (1 person or 4 people — same price)
Theatre upgrade:     £10/seat × party size
  Solo patron:       £10
  Couple:            £20
  Family of 3:       £30
  Family of 4:       £40    ← equivalent revenue to hotel at lower per-person bid
  Group of 5:        £50
```

**Weighted average party size for theatre (UK):**
| Party size | Est. share | Contribution |
|-----------|-----------|-------------|
| Solo | 12% | 0.12 |
| 2 (couple/friends) | 48% | 0.96 |
| 3 | 12% | 0.36 |
| 4 (family) | 22% | 0.88 |
| 5+ | 6% | 0.33 |
| **Weighted avg** | | **2.65 seats/booking** |

For Totoro specifically, the family demographic skews this upward — likely **2.8–3.0 seats/booking**.
Model uses **2.6 seats** (conservative blended).

---

## Model Parameters

| Parameter | Scenario A (pilot, no guidance) | Scenario B (calibrated, post-3 shows) |
|-----------|--------------------------------|--------------------------------------|
| Average bid per seat | £10 | £18 |
| Bid floor | £8 | £12 |
| Revenue split (venue/TS) | 80/20 | 80/20 |
| TS revenue per seat | £2.00 | £3.60 |
| Participation rate (of eligible patrons) | 8% | 15% |
| Pre-auth success rate | 92% | 92% |
| Solver match rate | 60% | 65% |

**Average upgrade transaction value (2.6 seats):**
- Scenario A: £10 × 2.6 = **£26/booking** → TS gets **£5.20**
- Scenario B: £18 × 2.6 = **£46.80/booking** → TS gets **£9.36**

---

## Venue Capacity Tiers

| Tier | Examples | Capacity | Shows/wk | Sections | Origin seats (40%) | Occupied (78%) | Chain mult |
|------|---------|----------|---------|---------|-------------------|----------------|------------|
| 1 — Studio | Donmar, Bush, Soho | 250 | 8 | 2–3 | 100 | 78 | 1.2× |
| 2 — Mid-size | Lyric Hammersmith, Menier | 500 | 8 | 3–4 | 200 | 156 | 1.3× |
| 3 — Standard West End | Noël Coward, Wyndham's | 800 | 8 | 4–5 | 320 | 250 | 1.4× |
| 4 — Large West End | Gillian Lynne, Drury Lane | 1,300 | 8 | 5–6 | 520 | 406 | 1.6× |
| 5 — Major | London Palladium, Coliseum | 2,300 | 6 | 6–8 | 920 | 717 | 1.8× |

**Formula:**
```
Base seat upgrades  = Occupied eligible × participation% × 92% pre-auth × 60% match
Chain seat upgrades = Base × chain_multiplier
Booking upgrades    = Chain seat upgrades ÷ 2.6 (party size)
Gross revenue/show  = Booking upgrades × avg bid per seat × 2.6
TS revenue/show     = Gross × 20%
```

---

## Revenue Per Show — All Tiers, Both Scenarios

### Scenario A: No Guidance, £10/seat, 8% participation

| Tier | Occupied eligible | Base seat upgrades | Chain upgrades | Booking upgrades | Gross/show | **TS/show** |
|------|------------------|-------------------|----------------|-----------------|----------:|----------:|
| 1 — Studio (250) | 78 | 3.6 | 4.3 | 1.7 | £43 | **£9** |
| 2 — Mid (500) | 156 | 7.1 | 9.2 | 3.5 | £92 | **£18** |
| 3 — Std WE (800) | 250 | 11.4 | 16.0 | 6.1 | £159 | **£32** |
| 4 — Large WE (1,300) | 406 | 18.5 | 29.6 | 11.4 | £296 | **£59** |
| 5 — Major (2,300) | 717 | 32.7 | 58.8 | 22.6 | £588 | **£118** |

### Scenario B: With Guidance, £18/seat, 15% participation, 65% match

| Tier | Occupied eligible | Base seat upgrades | Chain upgrades | Booking upgrades | Gross/show | **TS/show** |
|------|------------------|-------------------|----------------|-----------------|----------:|----------:|
| 1 — Studio (250) | 78 | 7.0 | 8.4 | 3.2 | £150 | **£30** |
| 2 — Mid (500) | 156 | 14.0 | 18.2 | 7.0 | £327 | **£65** |
| 3 — Std WE (800) | 250 | 22.4 | 31.4 | 12.1 | £566 | **£113** |
| 4 — Large WE (1,300) | 406 | 36.4 | 58.2 | 22.4 | £1,049 | **£210** |
| 5 — Major (2,300) | 717 | 64.2 | 115.6 | 44.5 | £2,082 | **£416** |

---

## Revenue Per Week, Per Year (Single Venue)

### Scenario A — No guidance

| Tier | TS/show | Shows/wk | **TS/week** | **TS/year** |
|------|--------|---------|------------|------------|
| 1 — Studio | £9 | 8 | **£69** | **£3,600** |
| 2 — Mid | £18 | 8 | **£147** | **£7,600** |
| 3 — Std WE | £32 | 8 | **£253** | **£13,200** |
| 4 — Large WE | £59 | 8 | **£472** | **£24,500** |
| 5 — Major | £118 | 6 | **£706** | **£36,700** |

### Scenario B — Calibrated guidance

| Tier | TS/show | Shows/wk | **TS/week** | **TS/year** |
|------|--------|---------|------------|------------|
| 1 — Studio | £30 | 8 | **£242** | **£12,600** |
| 2 — Mid | £65 | 8 | **£524** | **£27,200** |
| 3 — Std WE | £113 | 8 | **£902** | **£46,900** |
| 4 — Large WE | £210 | 8 | **£1,678** | **£87,300** |
| 5 — Major | £416 | 6 | **£2,499** | **£130,000** |

> **Chain/cycle effect illustrated at Tier 4 (Scenario B):**
> Without chains: 36 seat upgrades → 13.9 bookings → TS £130/show
> With chains (1.6×): 58 seat upgrades → 22.4 bookings → TS £210/show
> **Chain effect adds £80/show per large venue — £640/week of pure algorithmic revenue**

---

## Profitability Thresholds

### The Shakeup Operating Cost Stages

| Stage | Team | Annual cost | Weekly cost |
|-------|------|------------|------------|
| **Stage 1** — Founder-only | 1 person | ~£70k | **£1,350** |
| **Stage 2** — Early team | 3 people (founder + 2 engineers) | ~£250k | **£4,800** |
| **Stage 3** — Growth team | 7 people | ~£600k | **£11,500** |
| **Stage 4** — Scaled | 15 people | ~£1.4M | **£26,900** |

---

## How Many Venues to Break Even — Portfolio Model

**Portfolio assumption (realistic West End + UK mix):**
- Large WE (Tier 4): 50% of portfolio
- Standard WE (Tier 3): 30% of portfolio
- Mid-size (Tier 2): 20% of portfolio

**Weighted TS/week per venue:**
- Scenario A: (0.5×£472) + (0.3×£253) + (0.2×£147) = £236 + £76 + £29 = **£341/venue/week**
- Scenario B: (0.5×£1,678) + (0.3×£902) + (0.2×£524) = £839 + £271 + £105 = **£1,215/venue/week**

### Venues Required to Cover Each Business Stage

| Business stage | Weekly cost | Scenario A (no guidance) | Scenario B (calibrated) |
|----------------|------------|------------------------:|------------------------:|
| Stage 1 — Founder | £1,350/wk | **4 venues** | **2 venues** |
| Stage 2 — Early team | £4,800/wk | **15 venues** | **4 venues** |
| Stage 3 — Growth | £11,500/wk | **34 venues** | **10 venues** |
| Stage 4 — Scaled | £26,900/wk | **79 venues** | **23 venues** |
| **"Very profitable"** | £50,000+/wk | **~150 venues** | **~42 venues** |

> **Key insight:** The transition from Scenario A → B (adding guidance after 3 shows) is
> a **3.6× revenue multiplier** that reduces the venue count needed for profitability by ~73%.
> The data from the Totoro pilot is literally worth millions in reduced scale requirement.

---

## Revenue at Scale — What Does a Big Portfolio Look Like?

### UK West End only (~50 productions running simultaneously)

| Scenario | Venues | TS/week | TS/year |
|---------|--------|--------|--------|
| A — No guidance | 50 | £17,050 | £886,600 |
| B — Calibrated | 50 | £60,750 | **£3.16M** |

### UK-wide (Spektrix network: 650 venues, ~300 active at any time)

| Portfolio | TS/week | TS/year |
|---------|--------|--------|
| 100 venues, Scenario B | £92,000 | **£4.8M** |
| 200 venues, Scenario B | £184,000 | **£9.6M** |
| 300 venues, Scenario B | £276,000 | **£14.4M** |

### Broadway overlay (40 major productions, avg 1,700 seats, higher bid tolerance ~£25/seat)

| Portfolio | TS/week | TS/year |
|---------|--------|--------|
| 40 Broadway productions | £87,880 | **£4.6M** |

**Combined UK + Broadway:** 300 UK venues + 40 Broadway = **~£19M/year**

---

## The Chain Effect in Detail

At a Tier 4 venue (1,300 seats), Scenario B:

```
WITHOUT chains (no CUCR):
  18 available Stalls Centre seats
  → 18 direct upgrades
  → 6.9 bookings → TS: £65/show

WITH chains (CUCR, 1.6× mult):
  18 Stalls Centre vacancies
  → 18 direct: Stalls Side → Stalls Centre
  → 11 chain moves: Stalls Rear → Stalls Side (now vacant)
  → 7 further:  Circle → Stalls Rear (now vacant)
  → Total: 36 seat upgrades from 18 original vacancies
  → 13.8 bookings → TS: £129/show

Chain premium: £64/show | £512/week per venue
At 42 venues: £21,500/week purely from chain resolution
```

---

## Milestone Map

```
Venues   TS/week (Scen B)    Annual revenue    Stage milestone
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1       £1,215              £63k              Pilot — data collection
  2       £2,430              £126k             ✓ Founder break-even
  4       £4,860              £253k             Stage 2 approaching
  5       £6,075              £316k             ✓ Stage 2 break-even
 10       £12,150             £632k             Stage 3 approaching
 23       £27,945             £1.45M            ✓ Stage 4 break-even
 42       £51,030             £2.65M            ✓ "Very profitable"
 50 (WE)  £60,750             £3.16M            Full West End
100 (UK)  £121,500            £6.32M            Dominant UK player
200 (UK)  £243,000            £12.6M            + Broadway → £17M+
```

---

## Summary Answer: How Many Venues?

| Target | With guidance (Scenario B) | Notes |
|--------|--------------------------|-------|
| Founder-viable | **2 venues** | Achievable within 6 months of pilot |
| Small team profitable | **5–10 venues** | Year 1 target |
| **"Very profitable"** | **42 venues** | Year 2–3, full West End penetration |
| £10M+ revenue | **~80 venues** | UK + selective international |
| £20M+ revenue | **UK + Broadway** | Year 4–5, defines the business |

The number that matters most: **42 venues in Scenario B = £2.65M/year**.
That is achievable within 2–3 years of the Totoro pilot, requires no external capital if
founder-funded through the first 5 venues, and represents a genuinely valuable, profitable business
before any international expansion is contemplated.
