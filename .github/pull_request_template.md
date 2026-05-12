## Summary

<!-- 1-3 bullets describing what this PR changes. -->

## Type of change

- [ ] New skill
- [ ] Modification to existing skill (body / description / references)
- [ ] Bug fix (skill misroutes, recommends wrong action, breaks on MCP response)
- [ ] Docs / scaffolding (README, INSTALL, CONTRIBUTING)
- [ ] CI / validator
- [ ] Versioning / release

## Checklist

- [ ] I read [CLAUDE.md](../CLAUDE.md) and matched the repo conventions.
- [ ] Frontmatter contains `Use when` / `Chain with` / `NOT for` blocks.
- [ ] Description ≤ 1024 chars.
- [ ] Body ≤ 500 lines (warn at 300).
- [ ] All `references/*.md` linked from SKILL.md exist; no orphans.
- [ ] No `../../../` deep parent traversal.
- [ ] `python3 scripts/validate.py` passes locally.
- [ ] If I changed thresholds / named frameworks, I cited the source.
- [ ] Relevant eval scenarios in [evals/scenarios.md](../evals/scenarios.md) were run; transcripts attached below.

## Eval transcripts

<!-- Paste pass / partial / fail for each scenario you ran. -->

## Sources

<!-- If thresholds changed: cite the practitioner / study / experiment. -->
