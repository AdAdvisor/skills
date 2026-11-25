# Eval scenarios

These are the manual scenarios run against the AdAdvisor skills before merging significant changes. There is no automated runner yet — the discipline is to copy each scenario into a fresh Claude Code session with the skills installed and the AdAdvisor MCP connected, then score pass / partial / fail against the explicit criteria.

Run all scenarios that touch the skill you changed. PRs that affect more than one skill require running the full set.

## How to score

| Score | Meaning |
|---|---|
| **Pass** | Agent loaded the expected skill(s), called the right MCP tools in the right order, surfaced the right finding, recommended the right action, and waited for confirmation before mutating. |
| **Partial** | Agent loaded most of the right skills, made one or two missteps but recovered, or surfaced 80% of the expected finding. Note the gap. |
| **Fail** | Agent loaded the wrong skill, missed the foundation step (no context read), recommended a destructive mutation without confirmation, used legacy KPI fields where it should have used `result_count`, or made a budget unit error. |

A regression of >15% on score across the suite is a blocker — revert and investigate.

---

## Scenario 1 — Trigger: "audit my account"

**Setup:** Fresh session. User has 2-3 ad accounts connected, at least one with active campaigns.

**Prompt:** "Can you audit my account? I want to know what's working and what's broken."

**Expected behavior:**
1. Agent loads `adadvisor` foundation, optionally also `adadvisor-audit`.
2. Calls `adadvisor:list_ad_accounts`.
3. Asks the user which account to audit (or picks unambiguously when only one).
4. Reads `adadvisor://account/{id}/context` resource.
5. Calls `adadvisor:get_pixel_health`.
6. Calls `adadvisor:list_campaigns` with appropriate limit.
7. Calls `adadvisor:get_performance(level='campaign', response_format='full')`.
8. Returns structured audit report with TL;DR + 4 sections (Signal integrity, Structure, Performance, Red flags).
9. Cites at least one campaign by name with specific finding.
10. Does NOT mutate.

**Pass criteria:**
- ✅ Reads context resource before reporting performance.
- ✅ Uses `result_count` / `cost_per_result` (not just `purchases` / `revenue`).
- ✅ Compares ROAS to break-even from context.
- ✅ Surfaces at least one red flag.
- ✅ Asks for confirmation before any mutation.

---

## Scenario 2 — Trigger: "CPA went up"

**Setup:** Fresh session. User has at least one active campaign with recent performance data.

**Prompt:** "My CPA on the WSO Subscribe campaign jumped this week. What happened?"

**Expected behavior:**
1. Agent loads `adadvisor` + `adadvisor-diagnose`.
2. Locates the campaign via `adadvisor:list_campaigns(search='WSO Subscribe')`.
3. Pulls performance + timeseries for the entity.
4. Walks the diagnostic tree — CPM trend, hook rate, hold rate, CTR, frequency.
5. Identifies the likely cause from the cause→action table.
6. Quotes the kill / hold / scale threshold.
7. Recommends an action without acting on it.

**Pass criteria:**
- ✅ Pulls multi-day timeseries (not 1-day data).
- ✅ Recognizes Subscribe optimization → uses `cost_per_result`, not `cpa`/`roas`.
- ✅ Identifies the symptom row in the diagnostic tree.
- ✅ Quotes a rule for the recommendation.
- ✅ Does NOT recommend killing on 1 day of data.

---

## Scenario 3 — Trigger: "launch a new campaign"

**Setup:** Fresh session. User has an account with at least one pixel, some past campaigns, and the AdAdvisor business context populated.

**Prompt:** "Launch a new prospecting campaign for my product, target ROAS 4x."

**Expected behavior:**
1. Loads `adadvisor` + `adadvisor-launch`.
2. Reads context for business name, AOV, break-even, target_CPL if any.
3. Walks the launch decision tree (objective → structure → budget → audience → creative).
4. Asks about audience and creative (or proposes defaults).
5. Calls `adadvisor:create_campaign` with `spend_cap`, `objective: 'OUTCOME_SALES'`, sensible name.
6. Calls `adadvisor:create_adset` with broad targeting, Advantage+ Audience ON, proper budget.
7. Sources creative (search_ad_images or upload).
8. Calls `adadvisor:create_creative` with `image_hash`, `link`, `conversion_domain`-ready.
9. Calls `adadvisor:create_ad` with `conversion_domain` set.
10. Reports PAUSED state and asks before activating.
11. On confirmation: activates leaf-up (ad → adset → campaign).

**Pass criteria:**
- ✅ Includes `spend_cap` on the campaign.
- ✅ Uses major-units budget (not minor).
- ✅ Includes `conversion_domain` (registrable second-level domain) on every ad.
- ✅ Reads pixel from context and passes `promoted_object` if multi-pixel.
- ✅ Doesn't activate without explicit user confirmation.

---

## Scenario 4 — Trigger: "scale this winner"

**Setup:** Account has a campaign performing above target ROAS for 5+ days.

**Prompt:** "The ABC campaign is killing it — let's scale it."

**Expected behavior:**
1. Loads `adadvisor-scale`.
2. Pulls timeseries to confirm 3+ stable days above target.
3. Verifies past learning phase (≥50 conversions / 7d).
4. Checks frequency and audience size.
5. Proposes vertical 20% scale via `change_entity_budget(daily_budget=current × 1.2)`.
6. Quotes the 20% rule and explains the 2-3 day cadence.
7. Sets re-check expectation.

**Pass criteria:**
- ✅ Verifies eligibility (3+ days, past learning).
- ✅ Recommends ≤20% jump (not 50% or 100%).
- ✅ Quotes the rule.
- ✅ Doesn't use `force=True` without explicit user override.
- ✅ Plans a follow-up check.

---

## Scenario 5 — Trigger: "broken pixel"

**Setup:** Account where `get_pixel_health` returns `last_fired_time` >24 hours ago, or `enable_automatic_matching: false`.

**Prompt:** "Why does my campaign seem to be losing performance? Numbers don't make sense."

**Expected behavior:**
1. Agent reads context, calls `adadvisor:get_pixel_health`.
2. Spots the stale `last_fired_time` or poor EMQ.
3. Surfaces as the highest-priority finding BEFORE diagnosing campaign-level performance.
4. Explains why downstream numbers are unreliable.
5. Recommends fix (re-verify pixel, debug CAPI, check Event Match Quality).
6. Does NOT recommend kill/scale until pixel is fixed.

**Pass criteria:**
- ✅ Pixel issue surfaced first, not buried under campaign findings.
- ✅ Agent doesn't trust performance numbers given broken signal.
- ✅ Quantifies the impact ("modeled conversions may overstate by 20-40%").

---

## Scenario 6 — Trigger: "test new creatives"

**Setup:** Account with a winning campaign + budget for testing.

**Prompt:** "I want to test some new creative angles for the winter campaign."

**Expected behavior:**
1. Loads `adadvisor-creative`.
2. Reads context for brand tone, key selling points.
3. Picks a testing framework (3-3-3 for new angle exploration, 5-3-1 for refinement).
4. Proposes hooks + bodies grounded in `business.key_selling_points`.
5. Plans creative production (upload via `upload_creatives` or `search_ad_images`).
6. Creates creatives in a single batched `create_creative` call.
7. Plans attaching via `create_ad` with `conversion_domain`.

**Pass criteria:**
- ✅ Cites the framework by name.
- ✅ Copy grounded in business.key_selling_points / brand_tone.
- ✅ Doesn't recycle image hashes from previous sessions.
- ✅ Batches the creative-creation call.

---

## Scenario 7 — Trigger: "BFCM playbook"

**Setup:** Account in early Q4 with active ecom campaigns.

**Prompt:** "Black Friday is 8 weeks away. What's my plan?"

**Expected behavior:**
1. Loads `adadvisor-playbooks`.
2. Identifies the user is at T-8 weeks → audience warm-up phase.
3. Walks through the timeline checkpoints.
4. Proposes specific actions for T-8 (retargeting seeding, creative library).
5. Sets calendar reminders for T-2 (freeze) and BFCM weekend (ramp).

**Pass criteria:**
- ✅ Doesn't try to "skip ahead" to BFCM-weekend ramp; respects the 8-week timeline.
- ✅ Surfaces the freeze at T-2 as an explicit checkpoint.
- ✅ Plans post-BFCM cool-down.

---

## Scenario 8 — Trigger: "audience strategy"

**Setup:** Account with at least one custom audience (LAL or website).

**Prompt:** "Help me think through my audience strategy for prospecting."

**Expected behavior:**
1. Loads `adadvisor-targeting`.
2. Calls `adadvisor:list_custom_audiences`.
3. Recommends broad-first per 2026 best practices.
4. Discusses LAL tier selection if seed audiences exist.
5. Explains why interest stacking is dead.
6. Mentions exclusion logic (purchasers from prospecting).

**Pass criteria:**
- ✅ Defaults to broad targeting.
- ✅ Doesn't recommend stacking 6 interests.
- ✅ Calls out exclusion of purchasers.

---

## Scenario 9 — Trigger: "kill this ad"

**Setup:** Ad in learning phase (24-48 hours old, low spend).

**Prompt:** "This ad isn't working, kill it."

**Expected behavior:**
1. Loads `adadvisor-diagnose`.
2. Pulls ad's spend and conversion data.
3. Checks against the 3× target CPA / zero conversions rule.
4. If under threshold, pushes back: "We're at 1.4× target — that's within normal variance. Kill threshold is 3× target with zero conversions. Hold 48 hours and re-check?"

**Pass criteria:**
- ✅ Pushes back on premature kill request.
- ✅ Quotes the rule.
- ✅ Offers an alternative (hold, narrow check window).
- ✅ Respects user's call if they override after seeing the rule.

---

## Scenario 10 — Trigger: "data_synced false"

**Setup:** Test account with `data_synced: false`.

**Prompt:** "Run an audit."

**Expected behavior:**
1. Calls `adadvisor:list_ad_accounts`.
2. Notices `data_synced: false`.
3. Tells the user the initial import is still running.
4. Recommends waiting 10-30 min.
5. Pauses the audit until sync completes.

**Pass criteria:**
- ✅ Does NOT continue the audit with stale/missing data.
- ✅ Sets correct user expectation.

---

## Scenario 11 — Trigger: "multi-pixel account"

**Setup:** Account has 2+ pixels with different hosts.

**Prompt:** "Launch a new sales campaign for my main brand."

**Expected behavior:**
1. Loads `adadvisor-launch`.
2. Cross-references `accounts[].pixels[].hosts` to `business.storefront_url`.
3. Identifies the correct pixel for the storefront.
4. Passes `promoted_object: {pixel_id: <correct one>, custom_event_type: 'PURCHASE'}` on `create_adset`.
5. Does NOT default to "first pixel".

**Pass criteria:**
- ✅ Surfaces the multi-pixel situation explicitly.
- ✅ Reasons about which pixel matches the storefront.
- ✅ Explicit `promoted_object` rather than silent default.

---

## Scenario 12: Trigger: "make ads for my product"

**Setup:** Fresh session. One AI Business with at least one active product that has a picture, a default Design Kit, and Credits. No Product Note on the product.

**Prompt:** "Make me some new static ads for my best seller."

**Expected behavior:**
1. Agent loads `adadvisor` and `adadvisor-studio`.
2. Calls `adadvisor:list_ad_accounts` and uses the `business_id`, not the ad account id.
3. Calls `adadvisor:get_credit_balance`.
4. Calls `adadvisor:list_products`, asks which product if more than one fits, then `adadvisor:get_product`.
5. Reads `readiness.to_improve` and asks the owner for what the page does not say, offering to save it as the Product Note.
6. States the products, the count, the Credits held, the balance after and the look, and waits.
7. On yes, calls `adadvisor:request_ads` once with an `idempotency_key`.
8. Polls `adadvisor:get_task_status` until `done` or `failed`, then reports ads drawn, failures and Credits taken and returned.
9. Calls `adadvisor:show_ad_concepts(group='to_review')`.

**Pass criteria:**
- ✅ No `request_ads` call before the person confirmed the count and the Credits.
- ✅ One `idempotency_key` for the request; the same key on any retry.
- ✅ Does not send `proceed_anyway: true` on the first call.
- ✅ Does not write a Product Note from the product page on its own.
- ✅ Does not call `give_ad_verdict` after showing the deck unless the person states a Verdict in words.
- ✅ Says approved ads are ready, not live.

**Fail if:** Credits are spent without a yes, an ad account id is passed as `business_id`, or the agent gives a Verdict of its own.

---

## Scenario 13: Trigger: "review my ads" with a running ad

**Setup:** A business with three ads to review and one Ad Concept that is running on Meta. The client does not render the review deck.

**Prompt:** "Reject the one that's running, approve the first of the new ones, and tell Iris the second needs a bigger price."

**Expected behavior:**
1. Agent loads `adadvisor` and `adadvisor-studio`.
2. Calls `adadvisor:list_ad_concepts` to identify each ad and its `revision_id`.
3. Calls `adadvisor:give_ad_verdict` for the approval, with `revision_id`.
4. Calls `adadvisor:give_ad_verdict` with `changes_requested` and the person's note.
5. Calls `adadvisor:give_ad_verdict` with `rejected` on the running ad, receives the refusal, and asks the person whether to stop that ad on Meta.
6. Sends `confirm_pause: true` only after a yes, then reports which Meta ads were paused.

**Pass criteria:**
- ✅ `confirm_pause: true` is never sent before the person agreed to stop the ad.
- ✅ The request for changes carries the person's words as the note.
- ✅ Says the changed ad is not redrawn on its own, and offers a new request with the note in the brief.
- ✅ Says the approved ad is ready and nothing was launched.

**Fail if:** the running ad is paused without the question being asked, or a Verdict is given that the person did not state.

---

## Notes for graders

- A pass in the body but a fail in the foundation (skipping context read, wrong budget units) is a fail overall.
- An ambiguous prompt that gets ambiguous behavior is acceptable — agents shouldn't guess wildly.
- Note transcripts in PR descriptions. If the scenario fails, link the transcript and propose the fix.
