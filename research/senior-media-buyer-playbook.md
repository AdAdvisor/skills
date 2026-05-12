---
title: The Senior Meta Media Buyer Playbook
subtitle: A practitioner reference for diagnosing, scaling, and operating Meta ad accounts in 2026.
eyebrow: Reference Playbook
document_kind: Reference Playbook
meta:
  - label: Edition
    value: 2026
  - label: Date
    value: May 12, 2026
  - label: Document Type
    value: Reference Playbook
  - label: Audience
    value: Senior Media Buyers
footer_note: Confidential · Ad Advisor AI · For practitioner use
---

## Foreword

A synthesis of practitioner playbooks (Common Thread Collective, Foxwell Digital, Motion, Pilothouse, Tier 11, Charley Tichenor / Disrupter School, Andrew Faris, Nick Shackelford, Dara Denney, Barry Hott, Sarah Levinger, Triple Whale, Northbeam, Jon Loomer), Meta's official documentation, and post-Andromeda 2026 best practices.

This is a working reference, not a tutorial. It assumes you already know what a CBO is, how to read frequency, and why iOS 14.5 changed everything. It is meant to be opened on a Monday morning when something looks off, and to give you a defensible next move within five minutes.

<div class="callout">
  <strong>How to use this document:</strong> Section 1 is your daily and weekly cadence. Section 2 is the audit you run on any new account. Sections 3 through 11 are the deep references. Section 12 is the anti-pattern checklist. Sections 13 and 14 are mindset and tactical playbooks.
</div>

## 1. Daily and Weekly Routine

The first 90 seconds when Ads Manager opens. A senior buyer does not look at "yesterday." They look at pacing vs target, and anomalies vs the trailing 7-day baseline.

### Daily check (15 minutes, in order)

- Account health flag: any disabled ads, learning-limited ad sets, billing or payment errors, policy issues.
- Spend pacing vs daily and monthly target.
- Top-line MER and blended ROAS compared to in-platform Meta-reported ROAS.
- Yesterday's results vs trailing 7-day average at the campaign level only. Never make decisions on 1 day of ad-level data.
- Frequency check on top spenders. Prospecting 1.5 to 2.5 is healthy; retargeting 4 to 6; greater than or equal to 3 on prospecting is a fatigue early-warning.
- New creative delivery: are new ads getting impressions, or is Meta starving them.

### Weekly cadence (Monday 90-minute review)

- Creative-level performance roll-up in Motion, Foreplay, or Atria.
- Budget reallocation: shift 10 to 20 percent from underperformers to validated winners. Foxwell rule: never move more than 20 percent at a time.
- Refresh and launch slot: 2 to 4 new concepts per week post-Andromeda.
- Audience overlap audit on the 2 to 3 largest ad sets. Flag anything at 30 percent or above.
- Any campaign in learning for more than 7 days is examined for budget too low, audience too small, or optimization event too rare.

### Monthly cadence

- Strategy review against unit economics: blended ROAS and MER vs target, CAC vs LTV, payback period.
- Cohort analysis and new customer rate (Curtis Howland's "Net New Reach").
- Attribution audit: Meta vs Triple Whale or Northbeam vs GA4 vs Shopify.

## 2. The Full Account Audit

The order matters. Measurement first, structure second, performance third, creative last.

### Step 1: Signal integrity (the half-day that saves the quarter)

- Pixel installed? CAPI live? Deduplication keys set?
- Event Match Quality (EMQ) per event. 6.0 to 7.9 is "Good," 8.0 to 10 is "Great." Below 6 means Meta is under-attributing meaningfully.
- AEM (Aggregated Event Measurement) priority ordering. Purchase always in position 1.
- Domain verified, business verification done.
- UTM tagging consistent.

### Step 2: Account hygiene

- Naming convention: `Campaign-Type | Objective | Audience | Date`.
- Number of active campaigns. Most audits find 5 to 10 times more campaigns than they should.
- Audience overlap on major prospecting ad sets.
- Exclusion logic: existing customers excluded from prospecting? 30-day purchasers excluded from retargeting?

### Step 3: Structure

- CBO / Advantage+ Campaign Budget vs ABO mix.
- Ad sets greater than 50 conversions per week (out of learning)?
- Placements set to Advantage+ or automatic.

### Step 4: Performance baseline at multiple windows

- 7-day for diagnosis, 14-day for decisions, 28 or 30-day for strategy, 90-day for trend.
- 7d-click and 1d-view default, with 1d-click for comparison.

### Step 5: Red flags

- Winning ad sets capped at low budgets.
- High frequency (greater than 3) on small audiences (less than 1M).
- All spend going to one ad while 7 others starve.
- Negative feedback rates on any ad. 0.1 percent or higher is yellow, 0.2 percent or higher is red.

## 3. Campaign Structure Best Practices (2025 to 2026)

Default to consolidation. Meta's own guidance: "When you run too many ad sets at the same time, each one gets fewer opportunities to learn."

**Recommended scaffold (DTC ecom):** 1 to 2 prospecting campaigns, plus 1 retargeting, plus 1 testing. Maximum of 1 to 3 ad sets per prospecting campaign.

**Advantage+ Sales Campaigns (ASC)** are the default for ecom. Tinuiti reports ASC delivers 4.52x ROAS vs 3.70x for manual, a 22 percent lift.

**Manual still wins** when you need control over creative-level kill decisions, when working with a small but high-LTV audience, or for lead gen.

**Ads per ad set:** post-Andromeda, run 3 to 6 distinctly different creative concepts per ad set.

**Budget threshold to exit learning:** 50 optimization events per 7 days per ad set.

<div class="callout">
  <strong>Formula:</strong> <code>min_budget = (target_CPA × 50) / 7</code>. At a 30 dollar target CPA, that is 214 dollars per day per ad set just to exit learning reliably.
</div>

**CBO vs ABO in 2026.** Lebesgue's 2024 study found ABO hit 94 percent of target ROAS vs CBO at 81 percent on prospecting. CBO wins on retargeting and at scale. Foxwell's working rule: ABO for testing, CBO for scaling.

## 4. Performance Diagnosis

The senior buyer's diagnostic stack reads top to bottom:

**Hook Rate** → **Watch Rate (Hold Rate)** → **CTR** → **CVR** → **AOV**.

### Benchmark table

| Metric | Healthy | Strong | Weak |
|---|---|---|---|
| Hook Rate (3-sec / impressions) | 25 to 35% | 30 to 45% | <20% |
| Hold Rate (15-sec / 3-sec) | 40 to 50% | 60%+ | <30% |
| CTR (outbound link) | 1.0 to 1.8% | 2.0%+ | <0.8% |
| CTR (all) | 2%+ | 3%+ | <1% |
| CPM (prospecting) | $10 to $25 | <$15 | >$30 |
| Frequency (prospecting) | 1.5 to 2.5 | <2 | 3+ |

### Diagnostic tree

| Symptom | Likely cause | Action |
|---|---|---|
| CPM up, CTR up, CVR down | Wrong audience, or LP friction | Fix LP, not ads |
| CPM up, CTR down, CVR flat | Creative fatigue, or audience saturation | Refresh creative or expand audience |
| CPM flat, CTR down, CVR flat | Creative fatigue | Kill or refresh |
| CPM up, CTR flat, CVR flat | Competition or seasonality | Hold, or raise bid |
| CPM flat, CTR flat, CVR down | Offer, price, or LP change | Fix offer or LP |
| Quality ranking "Below Avg" | Negative feedback | Replace creative |

## 5. Break-even ROAS and Unit Economics

The math that decides whether scaling helps you or kills you.

- `break_even_ROAS = 1 / contribution_margin`. At 30 percent margin, that is 3.33x. At 50 percent margin, 2.0x.
- `target_ROAS = break_even × (1 + desired_margin)`.
- `LTV:CAC` of 3:1 is healthy, 5:1 or higher is elite, less than 2:1 is unsustainable.
- CAC payback by category: Food and Bev 1 to 3 months; Apparel 3 to 6; Electronics and Subscription 6 to 12 or more.
- MER = Total Revenue / Total Marketing Spend. Most mature DTC accounts run 3.0x to 5.0x MER.

<div class="callout">
  <strong>The iceberg insight:</strong> ROAS tells you how efficiently you are buying revenue. Contribution margin tells you how much of that revenue you actually keep. A buyer scaling at 4x ROAS on 20 percent contribution margin is silently going broke.
</div>

## 6. Creative Strategy

Creative drives 70 to 89 percent of Meta ad performance (AppsFlyer 2025, Nielsen). Everything else is plumbing.

### Frameworks

- **3-2-2 (Tichenor):** 3 creatives, 2 primary texts, 2 headlines, for 12 dynamic variants.
- **3-3-3 (Pilothouse):** 3 concepts, 3 formats, 3 hooks, for 27 combinations.
- **5-3-1 (Ben and Vic via Motion):** 5 hook variations, 3 body variations, 1 CTA.
- **Hook → Body → CTA hierarchy:** test hooks first, then iterate body on the winning hook, then CTA.

### Refresh cadence by spend tier

| Daily spend | Refresh cadence |
|---|---|
| $100 to $200 / day | Every 2 to 3 weeks |
| $1,000+ / day | Every 7 to 10 days |
| $10,000+ / day | Weekly, 4 to 6 new concepts |

### Format and production (2026)

- UGC dominates prospecting. Polished video is for retargeting and brand.
- Video length sweet spot: 5 to 15 seconds.
- Aspect ratios: 4:5 portrait and 9:16 vertical are mandatory. 1:1 is the safety net. Horizontal is dead.

## 7. Scaling Principles

**Vertical scaling, the 20 percent rule.** Raise budget by no more than 20 percent every 2 to 3 days. Bigger jumps reset learning.

**Horizontal scaling.** Duplicate winners with same creative and a new audience, or same audience and a new creative angle.

**Bid-cap escalation (Tichenor).** Cap = target_CPA × 1.20. Start Lowest Cost, then duplicate with bid cap. If stable, duplicate again with a higher cap, building a portfolio.

**Target ROAS portfolio (Faris).** "70 percent of the money I spend is on Target ROAS campaigns." Duplicate a confirmed winner into a Target ROAS variant as a stability floor.

## 8. Killing Campaigns, Ad Sets, and Ads

Hard rules to remove emotion from the decision.

- 3x target CPA, zero conversions: kill (especially in learning phase).
- 2x target CPA, 1 conversion: hold 48 hours.
- 1.5x target CPA, steady conversions: optimize, do not kill.
- ROAS below 0.5x break-even for 3 or more days: kill.
- Frequency above 5 on a small audience with declining CTR: fatigue kill.

### Budget per test ad, by account size (GrowwithBA 2026)

| Monthly spend | Test ad daily budget |
|---|---|
| Under $10K / mo | $25 to $75 / day |
| $10K to $50K / mo | $50 to $150 / day |
| $50K to $200K / mo | $100 to $300 / day |
| $200K+ / mo | $300 to $1,000 / day |

## 9. Audience Strategy (Post iOS 14, Post Andromeda)

Broad has decisively won. The 2026 audience hierarchy:

- **Broad** (just age, gender, geo, with Advantage+ Audience ON): the default for prospecting.
- **Advantage+ Custom Audience:** seed Meta with a customer list or pixel events as signal.
- **Lookalikes:** now signals inside Advantage+ Audience. Value-based LALs outperform basic.
- **Interest stacking:** dead. Meta consolidated this in June 2025.
- **Retargeting:** 30, 60, 90-day site visitors, 180-day video viewers, email subscribers, abandoned cart.

### Audience sizing

- Prospecting: 1M or more, ideally 5M to 50M.
- Retargeting: 1,000 or more.
- Excluding existing customers (30 to 90 day window) is mandatory.

## 10. Bidding and Budget Allocation

### Bidding strategies

- **Lowest Cost / Highest Volume:** the default. Roughly 80 percent of spend.
- **Cost Cap:** target_CPA × 1.15 to 1.20. Stabilizes CPA.
- **Bid Cap:** Tichenor's signature. target_CPA × 1.20. A hard ceiling.
- **ROAS Goal / Maximize ROAS:** Faris's 70 percent bias.

### Budget allocation by maturity

| Stage | Testing | Prospecting | Retargeting |
|---|---|---|---|
| New brand, first 90 days | 40% | 40% | 20% |
| Established DTC | 10% | 70 to 80% | 10 to 20% |

### Dayparting in 2026

- Most ecom: no.
- Lead gen with business-hour patterns: yes.
- BFCM: yes, with hour-by-hour pacing.

## 11. Pixel and Measurement

### The 2026 baseline

- Pixel and CAPI dual-fire with deduplication.
- EMQ 7 to 7.9 is good, 8 to 10 is great.
- Required hashed identifiers: email, phone, FN, LN, IP, UA, `_fbp` cookie, `_fbc` click ID, external ID, click ID.

### Cross-check

Meta-reported revenue divided by Shopify revenue should be between 0.4 and 0.8. Above 1.0 means a deduplication bug. Below 0.3 means the pixel is broken.

## 12. Common Mistakes and Anti-Patterns

The checklist worth printing.

- Budget changes greater than 20 percent reset learning.
- Too many starved ad sets.
- Ignoring frequency until CPM is up 40 percent and CTR is down 30 percent.
- No creative testing system.
- Confusing correlation with causation at the ad level.
- Killing too early on 24-hour data.
- Restrictive placements.
- Optimizing for the wrong event (Add-to-Cart instead of Purchase).
- ASC and manual prospecting on the same audience without exclusions.

## 13. The Senior Buyer's Mindset

**Hypothesis-driven testing.** Sarah Levinger's frame: "Understanding Customer Reality, then filtering through Brand Reality."

### Read platform signals as language

- "Learning Limited": the budget, audience, and optimization-event combo cannot produce 50 events per week.
- "Creative Limited": audience saturation.
- "Below Average" quality ranking: users hide or scroll past more than competitors.

### When to trust Meta's AI

- **Advantage+ Audience:** trust it.
- **Advantage+ Shopping Campaigns:** trust it for scale.
- **Dynamic Creative:** trust for combination testing.
- **Advantage+ Creative (auto-text and crops):** test before trusting.

### Macro mix by spend

| Daily spend | Performance | Upper funnel / brand |
|---|---|---|
| $1K / day | 100% | 0% |
| $10K / day | 80 to 90% | 10 to 20% |
| $50K+ / day | 60 to 70% | 30 to 40% |

## 14. Tactical Playbooks

### BFCM

- T minus 8 to T minus 6 weeks: audience warm-up, build the creative library.
- T minus 2 weeks: freeze structural changes.
- T minus 1 week: final QA, budgets up 30 to 50 percent.
- BFCM weekend: ramp 200 to 400 percent, hour-by-hour pacing, expect CPM up 50 to 80 percent.
- Cyber Week: last-chance creative, urgency messaging.
- Post-BFCM (Dec 1 to 15): cool down minus 30 to 40 percent, welcome series.

### New product launch

- T minus 2 weeks: TOF video views to seed retargeting.
- Week 1: ASC and manual side by side, with exclusions. Run 5 to 8 distinct concept angles.
- Week 1 to 2: tight kill rules (3x target CPA, zero conversions).
- Week 2 plus: standard scaling.

### Banned account recovery

- One careful appeal with full documentation through Account Quality.
- Warm up a backup ad account in parallel.
- New-account discipline: 50 percent of normal budget for the first 7 days.

### Scaling $1K to $10K per day

- **Stage 1 ($1K to $2.5K):** vertical 20 percent, lock in 3 to 5 creatives.
- **Stage 2 ($2.5K to $5K):** horizontal scale, ASC and manual together, weekly creative production.
- **Stage 3 ($5K to $10K):** bid-cap diversification, plus Target ROAS, plus a brand and awareness layer.

## Closing

Treat this playbook as a working reference, not a script. The fundamentals (signal integrity, unit economics, creative testing, disciplined kill rules) outlast every platform update. The tactics change every quarter; the operating system does not.

<div class="callout">
  <strong>If you remember nothing else:</strong> measurement first, structure second, performance third, creative last. Read frequency before CTR, contribution margin before ROAS, and kill rules before scaling rules.
</div>
