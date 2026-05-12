# AdAdvisor Skills

Agent skills for the [AdAdvisor MCP server](https://app.adadvisor.ai) — codified senior media buyer workflows for managing Meta (Facebook + Instagram) ad accounts through Claude Code, Claude.ai, ChatGPT, Cursor, and any MCP-aware host.

> Built by [AdAdvisor](https://adadvisor.ai). The agency-veteran team behind it has managed $60M+ in Meta ad spend. These skills encode the workflows they wish every junior media buyer (and every AI assistant) already knew.

## What this is

The [AdAdvisor MCP server](https://app.adadvisor.ai) exposes ~33 tools to read and modify Meta ad accounts. Without skills, the MCP client (Claude / ChatGPT / etc.) has to figure out *how* to use those tools from scratch every session — when to audit before mutating, how to read pixel health, what kill thresholds to use, which scaling pattern fits the account size. This repo ships eight skills that codify those decisions so the agent acts like a senior media buyer by default.

## Skills

| Skill | Slash command | Use when |
|---|---|---|
| `adadvisor` | `/adadvisor:start` | Foundation — auto-loads on any AdAdvisor task. Account discovery, business context, unit economics, naming conventions. |
| `adadvisor-audit` | `/adadvisor:audit` | "Audit my account", "take over this account", "what's wrong" — full pixel → structure → performance → red-flag audit. |
| `adadvisor-diagnose` | `/adadvisor:diagnose` | "CPA went up", "ROAS dropped", "what's happening" — diagnosis tree (hook → hold → CTR → CVR), kill / hold / scale decisions. |
| `adadvisor-launch` | `/adadvisor:launch` | "Launch a new campaign", "set up an ad", "create" — full launch flow (objective → structure → targeting → creative → activation). |
| `adadvisor-scale` | `/adadvisor:scale` | "Scale this winner", "increase budget", "grow" — vertical / horizontal scaling, bid-cap method, target-ROAS portfolio. |
| `adadvisor-creative` | `/adadvisor:creative` | "Refresh creatives", "test ads", "what to make next" — 3-2-2 / 5-3-1 frameworks, refresh cadence by spend, hook-rate / hold-rate. |
| `adadvisor-targeting` | `/adadvisor:targeting` | "Audience", "lookalike", "retargeting", "interests" — broad-first targeting, lookalike strategy, exclusion logic. |
| `adadvisor-playbooks` | `/adadvisor:playbooks` | BFCM, product launch, lead-gen, banned-account recovery, $1k→$10k/day scale plan — tactical SOPs. |

Each skill is self-contained. Skills chain through references (e.g. `adadvisor-audit` points at `adadvisor-pixel` deep-dive content inside `references/`).

## Install

### Claude Code (recommended)

```bash
# As a plugin marketplace
/plugin marketplace add AdAdvisor/skills
/plugin install adadvisor@adadvisor

# Or clone directly into your global skills folder
git clone https://github.com/AdAdvisor/skills.git ~/.claude/skills/adadvisor
```

### Manual (any MCP host)

Drop the `adadvisor-*` skill folders into your host's skill directory:

| Host | Path |
|---|---|
| Claude Code | `~/.claude/skills/` (or `<project>/.claude/skills/`) |
| Cursor | `~/.cursor/plugins/adadvisor-skills/` |
| Codex | `~/.codex/plugins/adadvisor-skills/` |
| Claude.ai | Upload via the Skills UI under Settings → Capabilities |

See [INSTALL.md](./INSTALL.md) for the full matrix.

## Requirements

- **An AdAdvisor account.** Sign up at [adadvisor.ai](https://adadvisor.ai) and connect at least one Meta ad account.
- **The MCP server configured in your client.** From the AdAdvisor app, copy the MCP connection details into Claude Code / ChatGPT / Cursor (see the in-app onboarding).
- These skills assume the MCP server tools are reachable. Without the MCP server, the skills will still load but most workflows can't complete.

## How a skill triggers

Skills load on demand. Each `SKILL.md` declares natural-language phrases under `Use when:` — when the user says one of those phrases, Claude reads the skill body, follows the workflow, and references additional files in `references/` as the conversation deepens. No setup beyond installation.

Example:

> User: "Can you audit this ad account? It feels like CPAs have been climbing."
> Claude: *loads `adadvisor-audit` (the user said "audit") and `adadvisor-diagnose` (the user mentioned CPA), reads the account context, runs `list_ad_accounts` → `get_pixel_health` → `get_performance` → `get_timeseries`, applies the diagnostic tree, returns a structured report with prioritized findings.*

## The senior media buyer's discipline (encoded here)

These skills assume the agent should behave like a senior buyer with the following biases — all documented inside the individual skills and grounded in real-account testing:

1. **Measurement integrity before anything else.** Pixel + CAPI + EMQ + dedup + AEM priority. If signal is broken, every recommendation downstream is wrong.
2. **Decisions in multiples of target CPA, not absolute dollars.** Brand-agnostic kill / scale rules.
3. **Break-even ROAS and contribution margin over generic "good ROAS".** The unit-economics number always wins.
4. **Broad-first targeting since iOS 14.** Interest stacking is dead for most ecom; lookalikes are signal, not constraint.
5. **Creative drives 70-89% of performance.** Refresh cadence scales with daily spend; hook → body → CTA hierarchy.
6. **Don't reset the learning phase.** Budget edits >20%, audience swaps, optimization-event changes all restart the clock.
7. **Read what Ads Manager reports.** Use the MCP's `result_count` / `result_value` / `cost_per_result` / `conversion_result_name` fields — they match the "Results" column. Legacy `purchases` / `leads` will be wrong on Subscribe / Lead / custom-conversion campaigns.

These principles are stated up front in each skill and applied in every recommendation.

## Layout

```
adadvisor-skills/
├── README.md                       # this file
├── INSTALL.md                      # full install matrix (every host)
├── INSTALL_FOR_AGENTS.md           # imperative runbook for agents that install themselves
├── CONTRIBUTING.md                 # how to add or modify a skill
├── CLAUDE.md                       # repo-level instructions for Claude working on the repo
├── LICENSE                         # Apache 2.0
├── VERSION                         # repo-wide semver (single source of truth)
├── .claude-plugin/
│   ├── marketplace.json            # plugin marketplace listing
│   └── plugin.json                 # plugin manifest
├── .github/workflows/
│   └── validate-skills.yml         # CI: frontmatter, version sync, references, etc.
├── adadvisor/                      # foundation skill
│   ├── SKILL.md
│   └── references/
├── adadvisor-audit/
├── adadvisor-diagnose/
├── adadvisor-launch/
├── adadvisor-scale/
├── adadvisor-creative/
├── adadvisor-targeting/
├── adadvisor-playbooks/
├── evals/
│   └── scenarios.md                # 11 worked scenarios, run manually before merging
├── scripts/
│   └── validate.py                 # frontmatter + reference resolver
└── research/                       # branded PDFs of the underlying research
    ├── senior-media-buyer-playbook.pdf
    └── skills-design-rationale.pdf
```

## Versioning & releases

A single `VERSION` file is the source of truth. CI enforces lockstep across `VERSION`, every `SKILL.md` frontmatter, `marketplace.json`, and `plugin.json`. Feature branches should leave the number alone; the release pipeline bumps it when changes land on `main`.

## Contributing

PRs welcome — read [CONTRIBUTING.md](./CONTRIBUTING.md) first. The bar is:
- New skills must have a Failing → Passing eval scenario in [evals/scenarios.md](./evals/scenarios.md).
- SKILL.md descriptions must include `Use when:`, `Chain with:`, and `NOT for:` blocks (CI enforces).
- Body content stays under 500 lines / ~5,000 tokens; overflow goes to `references/`.
- Each skill folder installs cleanly on its own; cross-folder traversal via `../` is reserved for the optional sibling-skill nav links discussed in CLAUDE.md.

## Support

- **Bugs / feature requests:** open an issue with the `skills` label.
- **MCP server issues:** the MCP server itself is a separate codebase. Open issues against [`AdAdvisor/api-adadvisor`](https://github.com/AdAdvisor/api-adadvisor) (private) or via the in-app support widget at [app.adadvisor.ai](https://app.adadvisor.ai).
- **Best practices feedback:** if a skill recommends something you disagree with based on lived buyer experience, open a PR — these are opinionated and meant to evolve.

## License

[Apache 2.0](./LICENSE).
