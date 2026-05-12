---
title: AdAdvisor Skills
subtitle: Design Rationale for the Eight-Skill Public Repository
eyebrow: Design Rationale
document_kind: Design Rationale
meta:
  - label: Repository
    value: AdAdvisor/skills
  - label: Version
    value: v0.1.0
  - label: Date
    value: May 12, 2026
  - label: Status
    value: Published
footer_note: Confidential · Ad Advisor AI · Design Rationale
---

The "why" behind the eight skills shipped in `AdAdvisor/skills`.

## 1. The problem we're solving

The AdAdvisor MCP server exposes ~33 tools to read and modify Meta ad accounts through any MCP-aware host (Claude Code, Claude.ai, ChatGPT, Cursor). Without skills, the MCP client has to figure out every workflow from scratch every session: when to audit before mutating, how to read pixel health, what kill thresholds to use, which scaling pattern fits the account size. Our production logs show recurring patterns where the LLM:

- Calls `get_performance` before reading the business context resource (ungrounded recommendations against generic "good ROAS").
- Treats Subscribe / Lead campaigns by `purchases` (which is 0; those campaigns optimize on different events).
- Forgets `conversion_domain` on `create_ad` (Meta subcode 2490408).
- Misses pixel-pick on multi-pixel accounts (silently breaks attribution).
- Recommends killing campaigns after 24 hours on small budgets (noise, not signal).
- Sets `is_dynamic_creative: true` and attaches 3 ads (Dynamic Creative ad sets accept ONE ad).
- Activates one entity and reports "campaign is live" (activation doesn't cascade).

Each of these is a recurring miss. The LLM has the tools and could figure it out, but defaults aren't right. Skills fix this by encoding the right defaults and the workflow.

## 2. The framing: "brain and plumbing"

Simon Willison via Subramanya N: "MCP provides the 'plumbing' for tool access, while agent skills provide the 'brain' or procedural memory for how to use those tools effectively." The AdAdvisor MCP is the plumbing (schemas, auth, tool boundaries). These skills are the brain (workflow, sequencing, decision rules, anti-patterns).

Anthropic's engineering blog confirms the pairing: "We'll explore how Skills can complement Model Context Protocol (MCP) servers by teaching agents more complex workflows that involve external tools and software."

## 3. Why eight skills (not three, not twenty)

Skills load on demand. Each skill's `description` field is loaded into the system prompt at session start, costing ~100 tokens per skill. Anthropic's docs recommend keeping the total skill listing under 1% of the model's context window, so the budget is meaningful.

We considered:

- **3-4 broad skills.** Too coarse. "AdAdvisor" alone can't cover audits AND launches AND scaling without exceeding the 500-line body limit.
- **15+ narrow skills.** Too granular. "kill-rules" and "scale-decisions" overlap so much that having both confuses routing.
- **8 skills.** Each represents a distinct workflow with its own trigger phrasing, its own decision rules, and its own MCP tool subset. Cross-skill chaining is explicit.

The eight:

| Skill | Trigger | What it codifies |
|---|---|---|
| `adadvisor` | Foundation (loads on any AdAdvisor session) | Account discovery, context reading, unit economics, KPI decoding, naming conventions |
| `adadvisor-audit` | "audit my account", "take over" | Pixel integrity, structure, performance, red flags |
| `adadvisor-diagnose` | "CPA went up", "should I kill" | Hook/hold/CTR/CVR/AOV tree, kill/hold/scale decision rules |
| `adadvisor-launch` | "create", "set up", "launch" | Objective, structure, targeting, creative, activation |
| `adadvisor-scale` | "scale", "increase budget", "winner" | Vertical/horizontal/bid-cap/target-ROAS scaling axes |
| `adadvisor-creative` | "test ads", "refresh", "fatigue" | 3-2-2/5-3-1 frameworks, refresh cadence, dynamic creative |
| `adadvisor-targeting` | "audience", "lookalike", "interest" | Broad-first, lookalike strategy, exclusion patterns |
| `adadvisor-playbooks` | "BFCM", "launch playbook", "recovery" | Multi-week sequences with checkpoints |

## 4. The principles in every skill

### A. Workflow before tools

Each SKILL.md leads with the workflow ("here's what to do, in order"), not a tool catalog. Tools are referenced by name (`adadvisor:list_campaigns`) but the focus is the sequence and the decision points between calls.

### B. Decisions in multiples of the user's target

Every kill/scale/hold rule is expressed as a multiple of target CPA or target ROAS, never an absolute dollar amount. This makes the skills brand-agnostic and parametric. A bootstrapped DTC at $30 CPA target gets the same rules as a SaaS at $300 CPL target. The rule is "3x target, not 3x $30."

### C. Anti-patterns are first-class

Every skill ends with a `## Anti-patterns` section listing concrete failure modes. From obra/superpowers research: LLMs are biased to do something obvious-but-wrong; explicit anti-patterns yank them away from the obvious default. Examples:

<div class="callout">
<strong>Wrong:</strong> "Activating the campaign and assuming everything inside is on." <br/>
<strong>Right:</strong> Activate from leaf up.<br/><br/>
<strong>Wrong:</strong> "Stacking 8 interests as detailed targeting on prospecting." <br/>
<strong>Right:</strong> Broad with Advantage+ Audience.<br/><br/>
<strong>Wrong:</strong> "Killing a creative after 24 hours of $50 spend." <br/>
<strong>Right:</strong> Use the 3x target CPA rule with the right account-size kill threshold.
</div>

### D. The 300/500-line rule for SKILL.md

Bodies target 250-300 lines; hard fail at 500. Detail moves to `references/` files (one level deep, never chained). This is Anthropic's progressive disclosure pattern: keep the always-loaded body tight, lazy-load the depth.

### E. `Use when` / `Chain with` / `NOT for` description contract

Every description ends with three blocks:

- `Use when:` quoted natural-language phrases the user might say (4-8 phrases).
- `Chain with:` other skills this composes with.
- `NOT for:` explicit anti-routing to the correct sibling skill.

CI enforces these. Descriptions missing `Use when` or `NOT for` fail the build.

### F. Description = WHEN, not WHAT

From obra: "Testing revealed that when a description summarizes the skill's workflow, Claude may follow the description instead of reading the full skill content." Descriptions stay focused on triggering conditions; bodies deliver workflow.

## 5. Why these specific frameworks

The skills cite specific named frameworks because grounding makes the recommendations sticky:

- **3-2-2 (Tichenor / Disrupter School)** for creative testing
- **5-3-1 (Ben & Vic / Motion)** for creative refinement
- **3-3-3 (Pilothouse)** for new-concept exploration
- **20% rule** for vertical scaling
- **Bid-cap method (Tichenor)** for scaling past spend ceilings
- **Target ROAS portfolio (Faris)** for stability at scale
- **3x target CPA / zero conversions kill rule (Coinis, GrowwithBA, Reddit consensus)** for unambiguous kills
- **Foxwell's MER over ROAS at scale** for company-level health
- **Levinger's "Customer Reality to Brand Reality"** for hypothesis-driven creative

When a skill says "kill at 3x target CPA," the user can disagree, but they shouldn't be surprised.

## 6. Inspiration from the reference repos

We studied two reference repositories before settling on the structure.

### higgsfield-ai/skills (image/video generation, 4 skills)

- One `VERSION` file as the single source of truth, propagated via CI.
- Plugin marketplace ships alongside Claude Code, Cursor, Codex from one source.
- 300-line rule with the "if removing this would NOT break decision-making, move it to references/" test.
- `INSTALL_FOR_AGENTS.md` in imperative voice for agents installing themselves.
- `## UX Rules` numbered block at the top of every SKILL.md.
- `evals/scenarios.md` as 10 to 15 worked scenarios run manually.

### nextlevelbuilder/ui-ux-pro-max-skill (UI/UX, 1 main skill)

- Curated CSV knowledge base + BM25 search engine.
- "Step 2 is REQUIRED" workflow rule that produces an opinionated bundle.
- Anti-patterns treated as first-class.
- Severity tagging + priority table.

We adopted: single-VERSION-file source of truth, the description contract, the 300-line rule, the `evals/scenarios.md` discipline, anti-patterns sections, named frameworks with citations.

We deferred: large CSV knowledge bases (the MCP server already returns structured data; no need to duplicate), Python search engines (skills should be readable; complexity belongs in the MCP).

## 7. The senior buyer's discipline (encoded across all skills)

Every skill assumes these biases:

1. **Measurement integrity before anything else.** Pixel + CAPI + EMQ + dedup + AEM priority. If signal is broken, every recommendation downstream is wrong.
2. **Decisions in multiples of target CPA, not absolute dollars.** Brand-agnostic kill / scale rules.
3. **Break-even ROAS and contribution margin over generic "good ROAS".** The unit-economics number always wins.
4. **Broad-first targeting since iOS 14.** Interest stacking is dead for most ecom; lookalikes are signal, not constraint.
5. **Creative drives 70-89% of performance.** Refresh cadence scales with daily spend; hook to body to CTA hierarchy.
6. **Don't reset the learning phase.** Budget edits >20%, audience swaps, optimization-event changes all restart the clock.
7. **Read what Ads Manager reports.** Use the MCP's `result_count` / `result_value` / `cost_per_result` / `conversion_result_name` fields. They match the "Results" column.

These principles aren't repeated in every skill (that would bloat bodies). They live in the foundation skill (`adadvisor`) and are referenced from the others.

## 8. What we deliberately don't ship

- **No Google Ads / TikTok / X support.** The AdAdvisor MCP is Meta-only; skills mirror that.
- **No image / video generation.** Skills can recommend creative concepts and route to image-gen tools, but generating creative is out of scope for this repo.
- **No direct Meta Marketing API calls.** Everything goes through the MCP. The MCP handles auth, retries, currency conversion, audit logging.
- **No customer-list audience uploads via MCP.** CSV upload is done in the AdAdvisor app (PII handling). Skills surface uploaded audiences via `list_custom_audiences` but don't manage upload.
- **No scheduled / cron actions.** Skills are user-driven workflow primitives, not scheduled jobs. Scheduled optimization is a feature of the AdAdvisor app itself.

## 9. Testing and rollout

`evals/scenarios.md` ships 11 worked scenarios run manually before merging significant changes:

1. "audit my account": full account audit workflow
2. "CPA went up": diagnosis with timeseries
3. "launch a new campaign": full launch with PAUSED-by-default
4. "scale this winner": 20% vertical with eligibility check
5. "broken pixel": surface measurement issues first
6. "test new creatives": framework selection
7. "BFCM playbook": multi-week sequence
8. "audience strategy": broad-first
9. "kill this ad": push back on premature kill
10. "data_synced false": wait for sync
11. "multi-pixel account": pixel-pick

Each scenario has explicit pass/partial/fail criteria. The discipline alone catches regressions; no automated runner needed (yet).

## 10. Versioning and contribution

Single `VERSION` file (currently `0.1.0`) propagated to every skill's frontmatter and the plugin manifests. CI enforces lockstep. Don't hand-bump versions in a feature branch; release automation handles it on merge.

PRs that change a SKILL.md body or description must:

- Cite sources for new numeric thresholds.
- Run the relevant eval scenarios and paste transcripts.
- Pass `python3 scripts/validate.py`.

## 11. What's next

V0.1.0 ships the eight skills with reference depth. Roadmap:

- More tactical playbooks (B2B SaaS launch, agency onboarding, post-iOS17 attribution).
- Automated eval runner via a test MCP server.
- Cursor + Codex plugin manifests (currently Claude Code only).
- Hooks for safety guardrails (block destructive mutations without context confirmation).
- Multi-language description variants for non-English MCP hosts.

<div class="callout">
<strong>End of document.</strong> For implementation details, see the individual <code>SKILL.md</code> files in <code>AdAdvisor/skills</code> and the worked scenarios in <code>evals/scenarios.md</code>.
</div>
