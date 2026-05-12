# Working on the AdAdvisor Skills Repo (CLAUDE.md)

You are working inside the public AdAdvisor skills repository. This file is repo-level guidance for Claude when authoring, editing, or maintaining skills here. End users do NOT read this — they read `README.md` and the individual `SKILL.md` files.

## What this repo is

A public, MIT/Apache-2.0-licensed collection of Anthropic Agent Skills that pair with the **AdAdvisor MCP server**. The MCP server lives in a separate repo (`api-adadvisor`) and exposes ~33 Meta-ads tools to MCP-aware hosts (Claude Code, Claude.ai, ChatGPT, Cursor). This skills repo teaches the LLM *how* to use those tools effectively — workflow, sequencing, decision rules, anti-patterns. The MCP server is the plumbing; these skills are the brain.

## Cardinal rules

1. **MCP tool names use `adadvisor:` prefix.** In any `SKILL.md` prose, reference an MCP tool as `adadvisor:list_campaigns`, `adadvisor:get_performance`, etc. The colon form is what Anthropic's docs recommend for portability across hosts. Inside Claude Code the same tool surfaces as `mcp__adadvisor__list_campaigns` — do not put the underscore form in skill bodies.

2. **Skills teach *workflow*, not parameter schemas.** Tool parameter shapes live in the MCP server's `inputSchema`. The skill body should describe *when to call which tool*, *what to read before mutating*, and *how to interpret results* — not redocument every parameter. If a parameter detail is critical (e.g. `conversion_domain` on `create_ad` for pixel-tracked campaigns), call it out as a workflow gate rather than a schema dump.

3. **300-line / 5,000-token rule for SKILL.md.** Body content under 500 lines, target 200-300. The discriminator: a section earns its place in `SKILL.md` only if the agent uses it to choose *what to do next* — orientation, routing, decision tables, invariants. Look-up content (param tables, error catalogs, worked examples, threshold lists) is consulted later, after the path is picked, and belongs in `references/` where it loads on demand instead of taxing every turn.

4. **Every `description:` must include three blocks** — `Use when:`, `Chain with:`, `NOT for:`. CI enforces. Phrases inside `Use when:` are quoted natural-language utterances ("audit my account", "CPA went up"). `NOT for:` routes the agent to the correct sibling skill.

5. **No `../` parent references.** Every skill folder is independently installable. Reference files live at `<skill>/references/<name>.md` — one level deep from `SKILL.md`. Do not chain `SKILL.md → A.md → B.md`; Claude does partial reads and misses content past the first reference.

6. **Description = WHEN, not WHAT.** Quote from obra/superpowers: *"Testing revealed that when a description summarizes the skill's workflow, Claude may follow the description instead of reading the full skill content."* Keep `description` focused on triggering conditions; let the body deliver the workflow.

7. **Anti-patterns are first-class.** Every skill ends with a `## Anti-patterns` section listing concrete failure modes seen in real agent runs ("Don't kill an ad after 24 hours of $50 spend — that's noise, not signal"). LLMs are biased to do something obvious-but-wrong; explicit anti-patterns yank them away.

8. **Numbers come with their source.** When a skill says "kill at 3× target CPA with zero conversions" or "refresh creative every 7–10 days at $1k+/day", that's grounded in `research/senior-media-buyer-playbook.pdf` (Foxwell / CTC / Motion synthesis). When in doubt, cite.

9. **Status invariant: all created entities start PAUSED.** This is enforced by the MCP server (`AdSpec.status: Literal["PAUSED"]`, all `create_*` and `duplicate_*` default `PAUSED`). Skills must remind the agent to explicitly `change_entity_status(action='resume')` after creation — never assume cascade activation.

10. **Currency in major units.** All budget params in tool inputs are in account currency (e.g. `50.0` for $50/day). The MCP server converts to minor units before calling Meta. Skills should never say "5000" for "$50 daily budget".

## Naming conventions

- Skill folders: `adadvisor-<noun>` (`adadvisor-audit`, `adadvisor-scale`). The root foundation skill is just `adadvisor`.
- Skill `name:` in frontmatter MUST match the folder name exactly. CI enforces.
- Marketplace invocation: `/adadvisor:<verb>` (e.g. `/adadvisor:audit`). The verb is shorter than the folder suffix and not always literal — `/adadvisor:launch` covers `adadvisor-launch`, `/adadvisor:start` covers `adadvisor` itself.
- Reference files: kebab-case, descriptive purpose (`pixel-deep-dive.md`, `kill-rules.md`, `bfcm-timeline.md`). Avoid generic names like `troubleshooting.md` unless that's truly all it is.

## Frontmatter template

```yaml
---
name: adadvisor-<noun>
description: |
  <One paragraph: what this skill does and which AdAdvisor MCP surfaces it wraps.>
  Use when: "<trigger phrase>", "<trigger phrase>", "<trigger phrase>".
  Chain with: adadvisor (always loaded first) for account discovery and business context;
  adadvisor-<other> when <condition>.
  NOT for: <case A> (use adadvisor-<X>), <case B> (use adadvisor-<Y>).
license: Apache-2.0
version: 0.1.0
---
```

Optional Claude-Code-specific fields: `model: opus | sonnet`, `argument-hint`, `allowed-tools`. Keep these to a minimum for portability.

## Adding a new skill

1. Create `adadvisor-<noun>/SKILL.md` with the full frontmatter template above.
2. Body sections in order: title → `## When to use` → `## Workflow` → `## Decision rules` → `## Anti-patterns` → `## References`.
3. Move detail to `references/`. Target SKILL.md under 300 lines.
4. Add the skill to `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`.
5. Add at least one eval scenario in `evals/scenarios.md` that exercises the trigger phrasing AND the body content.
6. Run `python3 scripts/validate.py` locally — CI runs the same.

## Editing an existing skill

- Keep the `Use when` phrases stable unless you have a documented trigger-miss in the eval log. Changing trigger phrasing can change auto-routing for users in subtle ways.
- Anti-patterns can only get stricter / longer, never looser. Removing an anti-pattern requires a PR description that explains *why* it's no longer needed.
- Updating numeric thresholds (kill rates, refresh cadence, audience size minima) requires citing the source in the PR description.

## CI invariants

`.github/workflows/validate-skills.yml` enforces:

1. Frontmatter parses; `name` matches directory; `description` contains `Use when` and `NOT for`; `description` ≤ 1024 chars (Anthropic limit).
2. Version sync — root `VERSION` matches every `SKILL.md` `version:` matches `marketplace.json`/`plugin.json` versions.
3. Marketplace coverage — every `adadvisor*/` folder is listed in `marketplace.json`.
4. References resolve — every `[link](references/foo.md)` in `SKILL.md` exists, and every file in `references/` is linked from `SKILL.md`.
5. No parent-directory traversal — `grep` for `../` returns nothing.
6. SKILL.md body length — warn at >300 lines, fail at >500 lines.

## Don't

- **Don't include MCP tool argument schemas in SKILL.md.** The MCP server's `inputSchema` is the source of truth. If a parameter is non-obvious, mention it as a workflow gate ("when `objective='OUTCOME_LEADS'`, you must set `promoted_object`"). Don't redocument the entire Pydantic model.
- **Don't recommend tools from other platforms.** This skill is Meta-only. The MCP server explicitly does NOT support Google Ads / TikTok / etc. Skills should say so.
- **Don't write skills that bypass the MCP.** No direct Meta Marketing API calls, no `curl https://graph.facebook.com/...` examples. Everything goes through MCP tools.
- **Don't add backwards-compat shims for retired Meta enums.** Example: `CREDIT` special ad category was retired Jan 14 2025 → use `FINANCIAL_PRODUCTS_SERVICES`. If old prose mentions retired values, fix it.
- **Don't duplicate the SERVER_INSTRUCTIONS string from the MCP server.** Those instructions are always in context for any AdAdvisor session. Skills add depth and workflow on top, they don't repeat.

## When in doubt

The two reference PDFs in `research/` are authoritative:
- **`senior-media-buyer-playbook.pdf`** — the underlying media-buying expertise (Foxwell / CTC / Tichenor / Faris synthesis).
- **`skills-design-rationale.pdf`** — why the skills are split the way they are, what each is meant to encode.

Skills should be derivable from these documents. If you find yourself making up a number or recommending a workflow that isn't in either, that's a signal to either (a) update the research first or (b) leave the skill silent on that question.
