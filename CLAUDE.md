# Working on the AdAdvisor Skills Repo (CLAUDE.md)

You are working inside the public AdAdvisor skills repository. This file is repo-level guidance for Claude when authoring, editing, or maintaining skills here. End users do NOT read this — they read `README.md` and the individual `SKILL.md` files.

## What this repo is

A public, MIT/Apache-2.0-licensed collection of Anthropic Agent Skills that pair with the **AdAdvisor MCP server**. The MCP server lives in a separate repo (`api-adadvisor`) and exposes about 60 tools (Meta ads, plus a business's products, Design Kits and the ads AdAdvisor makes for it) to MCP-aware hosts (Claude Code, Claude.ai, ChatGPT, Cursor). This skills repo teaches the LLM *how* to use those tools effectively — workflow, sequencing, decision rules, anti-patterns. The MCP server is the plumbing; these skills are the brain.

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

- Skill folders live under `skills/` (Anthropic-canonical plugin layout). Folder names: `skills/adadvisor-<noun>/` (`skills/adadvisor-audit/`, `skills/adadvisor-scale/`). The foundation skill is `skills/adadvisor/`.
- Skill `name:` in frontmatter MUST match the folder name exactly. CI enforces.
- Marketplace invocation: `/adadvisor:<skill-folder-name>` per Claude Code's namespacing rule (plugin name `adadvisor` + skill folder name). e.g. `skills/adadvisor-audit/` becomes `/adadvisor:adadvisor-audit`.
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

`.github/workflows/validate-skills.yml` runs `scripts/validate.py`, which enforces:

1. Frontmatter parses; `name` matches directory; `description` contains `Use when` and `NOT for`; `description` ≤ 1024 chars (Anthropic limit).
2. Version sync — root `VERSION` matches every `skills/adadvisor*/SKILL.md` `version:` field, the top-level `plugin.json` `version`, and each `plugins[].version` inside `marketplace.json`. `marketplace.json` itself has no top-level `version` per the Anthropic spec.
3. Skill discovery — at least one `skills/adadvisor*/SKILL.md` exists. Skill discovery is automatic via the canonical `skills/` layout, so `marketplace.json` does not enumerate skills.
4. References resolve — every `[link](references/foo.md)` in `SKILL.md` exists, and every file in `references/` is linked from `SKILL.md`.
5. No deep parent traversal — `../../../` is rejected. Cross-skill links via `../<other-skill>/references/X.md` are allowed (they degrade gracefully in standalone installs but improve GitHub navigation).
6. SKILL.md body length — warn at >300 lines, fail at >500 lines.

## Releases and ZIP distribution

End users install in one of two ways. Both routes consume artifacts the release pipeline produces; nothing is built ad-hoc.

| Audience | Install route | Artifact |
| --- | --- | --- |
| Claude Code | `/plugin marketplace add AdAdvisor/skills` + `/plugin install adadvisor@adadvisor` | Live `main` branch (or a tag if pinned) |
| Claude.ai web / Claude Desktop | Settings → Capabilities → Skills → Upload ZIP | GitHub release artifact |
| Cursor / Codex / other | `git clone` or download release tarball | GitHub release artifact |

### What ships in each release

`.github/workflows/release.yml` triggers on every `v*.*.*` tag push and produces nine ZIPs (one per skill) attached to the GitHub release:

| Artifact | Contents | Typical size |
| --- | --- | --- |
| `adadvisor.zip` | Just `skills/adadvisor/` (foundation, required) | ~22 KB |
| `adadvisor-audit.zip` | Just `skills/adadvisor-audit/` | ~28 KB |
| `adadvisor-diagnose.zip` | Just `skills/adadvisor-diagnose/` | ~22 KB |
| `adadvisor-launch.zip` | Just `skills/adadvisor-launch/` | ~31 KB |
| `adadvisor-scale.zip` | Just `skills/adadvisor-scale/` | ~26 KB |
| `adadvisor-creative.zip` | Just `skills/adadvisor-creative/` | ~34 KB |
| `adadvisor-targeting.zip` | Just `skills/adadvisor-targeting/` | ~28 KB |
| `adadvisor-playbooks.zip` | Just `skills/adadvisor-playbooks/` | ~32 KB |
| `adadvisor-studio.zip` | Just `skills/adadvisor-studio/` | ~8 KB |

Each ZIP wraps exactly one SKILL.md inside one top-level folder — the shape Claude.ai's and Claude Desktop's upload validator requires. We do NOT ship a multi-skill bundle: Claude.ai rejects ZIPs with more than one SKILL.md, and Claude Code installs the entire plugin via `/plugin install adadvisor@adadvisor` (no ZIP needed).

The Mintlify docs at `adadvisor.ai/docs/` link to these ZIPs via the `https://github.com/AdAdvisor/skills/releases/latest/download/<name>.zip` URL pattern, so docs never go stale — every cut release becomes "latest" automatically and the existing doc links pick up the new build.

### Cutting a new release

Don't hand-bump versions on feature branches. The release pipeline is the only thing that should produce new versions. The flow on `main`:

1. Decide the new version (`vMAJOR.MINOR.PATCH`).
2. Update `VERSION` at the repo root.
3. Update the `version:` field in every `skills/adadvisor*/SKILL.md` frontmatter.
4. Update the `version` field in `.claude-plugin/plugin.json`.
5. Update each `plugins[].version` in `.claude-plugin/marketplace.json`.
6. Run `python3 scripts/validate.py`. It will fail if any of the five locations drift.
7. Commit (`chore(release): v0.1.1`).
8. Tag and push: `git tag v0.1.1 && git push origin main --tags`.
9. The `release.yml` workflow takes over: validates, builds all nine ZIPs, creates a GitHub release with the auto-generated changelog, attaches the artifacts.

Once the workflow completes, the `releases/latest/download/<name>.zip` URLs immediately serve the new build. No docs change required.

### Manual release (bootstrap or hotfix)

If the workflow is broken or you need to ship before it lands, you can mirror it locally:

```bash
mkdir -p /tmp/release
cd skills
for d in adadvisor*/; do
  name="${d%/}"
  zip -qr "/tmp/release/${name}.zip" "$d"
done
cd ..

gh release create vX.Y.Z \
  --title "vX.Y.Z — <one-line summary>" \
  --generate-notes \
  /tmp/release/*.zip
```

This is exactly what the workflow does — keep them in sync if you change one.

### What NOT to do

- **Don't host ZIPs in the docs repo.** They go stale the moment we cut a new skills release. Docs always link to `releases/latest/download/`.
- **Don't hand-edit the `releases/latest` URL** in docs to a version-pinned one. Latest tracking is intentional.
- **Don't commit pre-built ZIPs to the skills repo.** They're build artifacts. The workflow rebuilds them on every tag, and the `.gitignore` already excludes them.
- **Don't bump only some of the five version locations.** The validator catches drift, but the CI run takes a minute. Use the checklist above.

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
