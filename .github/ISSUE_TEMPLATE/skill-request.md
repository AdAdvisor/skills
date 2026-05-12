---
name: Skill request
about: Suggest a new skill or significant addition to an existing skill.
title: '[SKILL] '
labels: enhancement
assignees: ''
---

## Problem

What workflow are you trying to codify? What's currently broken about handling this without a skill?

## Trigger phrases

What would the user say? List 4-8 quoted natural-language phrases.

## Existing skill?

Could this be an addition to `adadvisor-<existing>` instead of a new skill? If yes, which.

## MCP tools involved

Which `adadvisor:<tool>` calls would the workflow chain? Sketch the sequence.

## Decision rules

If the skill encodes thresholds (kill / scale / hold rates, refresh cadence, etc.), what should they be? Cite sources.

## Anti-patterns

What's the obvious-but-wrong thing the agent does today without this skill?

## Acceptance test

What's the eval scenario that would prove the skill works? See [evals/scenarios.md](../../evals/scenarios.md) for format.
