# Installing AdAdvisor Skills

These skills work in any host that supports the [Anthropic Agent Skills](https://agentskills.io/specification) format. The exact path varies — pick your host below.

## Prerequisites

1. **An AdAdvisor account** with at least one Meta ad account connected. Sign up at [adadvisor.ai](https://adadvisor.ai).
2. **The AdAdvisor MCP server configured in your client.** The skills assume tools like `adadvisor:list_ad_accounts` and `adadvisor:get_performance` are reachable.
3. **`git`** (or download a release tarball).

Without the MCP server, the skills still load but most workflows can't complete — they'll instruct the agent to call MCP tools that aren't available.

## Claude Code

### Option A — Plugin marketplace (recommended)

```bash
/plugin marketplace add AdAdvisor/skills
/plugin install adadvisor@adadvisor
```

`adadvisor@adadvisor` reads as `<plugin-name>@<marketplace-name>`. Both happen to be `adadvisor` because this repo hosts a single-plugin marketplace whose marketplace name and plugin name are the same.

Verify:

```bash
/plugin list | grep adadvisor
```

You should see all nine skills listed.

### Option B — Global skills directory

```bash
git clone https://github.com/AdAdvisor/skills.git ~/.claude/plugins/adadvisor
```

Or for project-scoped install:

```bash
git clone https://github.com/AdAdvisor/skills.git .claude/plugins/adadvisor
```

Then enable in `.claude/settings.json`:

```json
{
  "plugins": {
    "adadvisor": { "enabled": true }
  }
}
```

### Option C — Hand-picked skills

If you want only some skills (e.g. only the audit workflow), copy individual `adadvisor-<name>/` folders into your skills directory:

```bash
git clone https://github.com/AdAdvisor/skills.git /tmp/adadvisor-skills
cp -r /tmp/adadvisor-skills/adadvisor-audit ~/.claude/skills/
cp -r /tmp/adadvisor-skills/adadvisor ~/.claude/skills/   # always include the foundation
```

The foundation skill (`adadvisor`) provides session-level conventions every other skill assumes — keep it.

## Cursor

Cursor reads skills from `~/.cursor/plugins/`.

```bash
git clone https://github.com/AdAdvisor/skills.git ~/.cursor/plugins/adadvisor-skills
```

Restart Cursor. Skills will auto-load when their trigger phrases appear.

## Codex (Cursor's variant)

```bash
git clone https://github.com/AdAdvisor/skills.git ~/.codex/plugins/adadvisor-skills
```

## Claude.ai (web / desktop)

Web Claude supports skills via Settings → Capabilities → Skills → Upload. Skills are uploaded as ZIP files containing the skill folder.

```bash
git clone https://github.com/AdAdvisor/skills.git
cd skills
# Zip each skill individually (Claude.ai accepts one skill per upload)
for d in adadvisor*/; do
  (cd "$d" && zip -r "../${d%/}.zip" SKILL.md references/ 2>/dev/null)
done
# Upload each *.zip via Settings → Capabilities → Skills
```

## ChatGPT (with MCP via Custom Connectors)

ChatGPT Plus / Team / Enterprise can connect to MCP servers via Custom Connectors. Skills aren't a first-class concept in ChatGPT yet, but you can drop the contents of `SKILL.md` into your custom instructions or workspace prompt. Pick the 2–3 skills most relevant to your day and inline them.

A more practical pattern: use the [AdAdvisor app](https://app.adadvisor.ai) directly — it ships these workflows as in-app prompts.

## Verifying the install

Open a new chat with your host. Try:

> "Audit my AdAdvisor account."

You should see the agent:

1. Acknowledge it's loading the `adadvisor-audit` skill.
2. Call `adadvisor:list_ad_accounts` to discover available accounts.
3. Ask which account to audit (if there are multiple).
4. Read `adadvisor://account/<id>/context` for business thresholds.
5. Call `adadvisor:get_pixel_health` and `adadvisor:get_performance` to gather the audit inputs.
6. Return a structured audit report with pixel/structure/performance/red-flag sections.

If none of that happens, the skill isn't loading — check that `~/.claude/skills/adadvisor-audit/SKILL.md` exists and that the MCP server is connected.

## Updating

```bash
cd ~/.claude/plugins/adadvisor
git pull
```

Or via Claude Code's plugin marketplace:

```
/plugin update adadvisor
```

Version is single-sourced from the repo-root `VERSION` file (and propagated to every skill's frontmatter and the plugin manifests). Check current installed version:

```bash
cat ~/.claude/plugins/adadvisor/VERSION
```

## Uninstalling

```bash
/plugin uninstall adadvisor
```

Or, for git-clone installs:

```bash
rm -rf ~/.claude/plugins/adadvisor
```

## Troubleshooting

**"The agent doesn't seem to load the skill."** Skills are matched by their `description` field — make sure your prompt uses one of the `Use when` phrases (see the table in [README.md](./README.md)). If you say "look at my account" instead of "audit my account", the agent may not auto-route to `adadvisor-audit`. You can also invoke explicitly: `/adadvisor:audit`.

**"`adadvisor:list_ad_accounts` doesn't exist."** The MCP server isn't connected. In Claude Code, run `/mcp` and verify `adadvisor` is listed and `connected`. The connection details are in the AdAdvisor app under Settings → MCP Server.

**"The skill recommended a tool that returned an error."** Possible causes:
1. Your Meta access token expired — reconnect via the AdAdvisor app (the MCP error usually mentions code 190).
2. `data_synced=false` on the account — the initial data import is still running. Wait 10–30 min.
3. You hit a Meta rate limit (code 4 / 17 / 32 / 613). Retry in 5 min.

**"The skill description in `description:` is too long for my host."** Some hosts truncate at 1024 chars; some at 1536. The Anthropic spec limit is 1024. If you see a truncation warning, it's a bug in the skill — please open an issue.

## See also

- [INSTALL_FOR_AGENTS.md](./INSTALL_FOR_AGENTS.md) — imperative runbook for an AI agent that's installing these skills on behalf of a user.
- [README.md](./README.md) — overview of what each skill does.
- [agentskills.io/specification](https://agentskills.io/specification) — the open Agent Skills spec.
