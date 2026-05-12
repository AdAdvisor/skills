# Contributing to AdAdvisor Skills

This repo is a small, opinionated public collection. The bar is high and the surface area is intentionally narrow — most PRs we accept refine an existing skill (better trigger phrases, tighter decision rules, sharper anti-patterns) rather than ship new ones. Please read this entire file before opening a PR; the validator is mechanical, but the review is taste-driven.

## Before you open a PR

Run through this checklist:

- [ ] Read [CLAUDE.md](./CLAUDE.md) — repo-level conventions.
- [ ] Read the relevant existing skill(s) so your change fits the voice and structure.
- [ ] If you're adding a new skill, justify it: which trigger phrasing is currently routing to the wrong skill, and what specifically does your new skill encode that's missing? Skills are a finite budget (every description costs description-listing context).
- [ ] If you're changing thresholds, named frameworks, or kill rules, **cite the source** in your PR description. "I think 5× is more conservative" is not enough — quote a practitioner, link a study, or describe the lived experience.
- [ ] Run `python3 scripts/validate.py` locally. CI runs the same.

## What "good" looks like

A high-quality skill, from observation of the reference repos and our own evals:

1. **Use-when phrases match real user utterances.** Quote 4–8 natural-language phrases under `Use when:`. Phrases come from real conversations, not hypotheticals.
2. **Body is workflow-shaped.** Numbered or named steps, not prose. The agent should be able to lift a checklist and use it verbatim in its response.
3. **Decision rules are mathematical when possible.** "Kill at 3× target CPA with zero conversions" beats "kill if it's not working." Brand-agnostic, parametric.
4. **Anti-patterns are concrete.** "Don't kill an ad after 24 hours of $50 spend — that's noise" beats "don't kill prematurely."
5. **Pointers to references are tight.** `See [pixel-deep-dive.md](references/pixel-deep-dive.md) for the EMQ/CAPI/AEM checklist` — one line, one file.
6. **Examples use real-account shape.** Account IDs and campaign names that look like the real Meta IDs we already see (`120248745953090399` etc.), not `<your_id>` placeholders.

## What "bad" looks like

- A skill that summarizes its own workflow in the description. The description should describe *when* to use the skill, not *how*. (Observed failure: "Claude reads the description summary and follows that instead of the body.")
- A skill body that re-documents tool parameter schemas. The MCP server's `inputSchema` is the source of truth — refer to it, don't redocument.
- A skill that says "you can use X, or Y, or Z" without picking a default. Pick. Add escape hatches for the exceptions.
- A skill that exceeds 500 lines / 5,000 tokens. Move detail to `references/`.
- A skill that calls Meta's API directly (`curl https://graph.facebook.com/...`). Everything goes through MCP tools.

## Adding a new skill

1. Create `adadvisor-<noun>/SKILL.md` with the frontmatter template from [CLAUDE.md](./CLAUDE.md).
2. Body sections in order: title → `## When to use` → `## Workflow` → `## Decision rules` → `## Anti-patterns` → `## References`.
3. Add 2–4 reference files in `references/` with targeted detail.
4. Register the skill in `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`.
5. Add one eval scenario in `evals/scenarios.md` that exercises both the trigger phrasing AND a representative body workflow.
6. Run `python3 scripts/validate.py`.

## Editing an existing skill

- **Use-when phrases:** stable unless you have a documented trigger-miss. Changing routing affects auto-discovery for everyone.
- **Anti-patterns:** can only get stricter / longer. Removing one requires a "why" in the PR description.
- **Thresholds:** require a source. PR description must answer "why this number, why now."
- **Workflow ordering:** if you're reordering steps, run the relevant eval scenario before and after.

## Conventional commits

Use [conventional commits](https://www.conventionalcommits.org/). The validator looks at the merged-commit message for release-please automation.

Common prefixes:

- `feat(adadvisor-audit): ...` — new content or new skill
- `fix(adadvisor-diagnose): ...` — fix bad threshold, fix broken reference
- `docs(README): ...` — README / INSTALL changes
- `chore(scripts): ...` — validator tweaks, plumbing
- `refactor(adadvisor-launch): ...` — restructure without behavior change

## CI invariants (what blocks merge)

`.github/workflows/validate-skills.yml` enforces all of:

1. Every `SKILL.md` parses; `name` matches directory; `description` ≤ 1024 chars; contains `Use when:` and `NOT for:`.
2. `VERSION` matches every skill's `version:` field, plus `marketplace.json` and `plugin.json`.
3. Every `adadvisor*/` folder is registered in `marketplace.json`.
4. Every `references/*.md` link in `SKILL.md` resolves on disk, and conversely every file under `references/` is reachable from a `SKILL.md` link. Files that drift out of the link graph either get linked back in or deleted.
5. No `../` parent-directory traversal anywhere.
6. SKILL.md body length: warn at 300 lines, fail at 500.

## Eval discipline

The evals in [evals/scenarios.md](./evals/scenarios.md) are run **manually** before merging significant changes. The format: 11 scenarios in a fresh session, scored pass / partial / fail with explicit criteria. There's no automated runner (yet) — the discipline alone catches regressions.

Before a PR that touches a SKILL.md body or description: run the relevant scenario(s) and paste the transcript into the PR. Note any failures or partials and explain whether they're fixed by your change.

## License

Submitting a PR means you're releasing the change under [Apache 2.0](./LICENSE) on the same terms as the rest of the repo. If you can't agree to that (e.g. employer policy), flag it in the PR description.
