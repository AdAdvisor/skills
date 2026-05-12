# Install AdAdvisor Skills (Agent Runbook)

This file is the imperative install script for AI agents acting on behalf of a user (Claude Code, Cursor's agent mode, Codex, etc.). If a human is reading it, they want [INSTALL.md](./INSTALL.md) instead. Execute the steps below in order; don't paraphrase, don't skip.

## 1. Detect the host

Run the file-existence check that matches your host's skill directory:

| Host signal | Skills directory |
|---|---|
| `~/.claude/` exists | Claude Code → `~/.claude/plugins/adadvisor/` |
| `~/.cursor/` exists | Cursor → `~/.cursor/plugins/adadvisor-skills/` |
| `.claude/settings.json` exists in cwd | Claude Code (project-scoped) → `<cwd>/.claude/plugins/adadvisor/` |
| `~/.codex/` exists | Codex → `~/.codex/plugins/adadvisor-skills/` |

If none match, ask the user which host they're using.

## 2. Clone the repo into the target path

```bash
git clone https://github.com/AdAdvisor/skills.git "$TARGET_PATH"
```

If the directory already exists, prefer `git pull` over reinstalling:

```bash
cd "$TARGET_PATH" && git pull --ff-only
```

If pull fails on local changes, ask the user before discarding anything.

## 3. Verify the AdAdvisor MCP server is configured

After cloning, ask the user whether their MCP client has the `adadvisor` server connected. The skills assume tools like `adadvisor:list_ad_accounts` exist. If not configured:

- Direct the user to [app.adadvisor.ai](https://app.adadvisor.ai) → Settings → MCP Server, and have them copy the connection details into their MCP client configuration.
- Do NOT attempt to configure MCP servers programmatically — that's a user-credential operation.

## 4. Confirm the install

Run a smoke test in the same session — list the installed skills:

```bash
ls "$TARGET_PATH"/adadvisor*/SKILL.md
```

You should see 8 files. If fewer, the clone failed — investigate.

## 5. Surface what to do next

Tell the user:

> "AdAdvisor skills installed at `$TARGET_PATH`. Restart your client (or run `/plugin reload adadvisor` in Claude Code) and try one of these to verify:
>
> - `/adadvisor:start` — initialize the session against one of your accounts.
> - `/adadvisor:audit` — full account audit (start here if you've inherited an account).
> - `/adadvisor:diagnose` — investigate a recent performance drop.
> - `/adadvisor:launch` — set up a new campaign end-to-end.
>
> Or just describe what you want naturally — the skills auto-load on phrases like 'audit my account', 'why did my ROAS drop', 'launch a new campaign', 'scale this winner'."

## Don't

- **Don't run `/plugin install`** as if you were the user — that's a host-specific slash command that the user must type. You can suggest they run it, but don't try to issue it from inside your tool calls.
- **Don't write to the user's `settings.json`** without asking. Plugins are enabled differently per host; let the user enable.
- **Don't `git pull` past local changes** — if `git status` shows modifications, stop and ask. The user may be developing custom skills on top.
- **Don't claim "done" without verifying** — always run the `ls SKILL.md` smoke test before reporting success.
