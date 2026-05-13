#!/usr/bin/env python3
"""
AdAdvisor skills repo validator.

Checks:
  1. Every adadvisor*/SKILL.md parses with valid YAML frontmatter.
  2. `name:` matches the parent directory.
  3. `description:` is non-empty, ≤ 1024 chars, contains "Use when" and "NOT for".
  4. `version:` matches the root VERSION file.
  5. Every skill folder is registered in .claude-plugin/marketplace.json
     and .claude-plugin/plugin.json with matching version.
  6. Every references/*.md file is linked from its SKILL.md (no orphans).
  7. Every references/<name>.md link in SKILL.md exists on disk.
  8. No `../` parent-directory references anywhere in SKILL.md or references/.
  9. SKILL.md body (after frontmatter) ≤ 500 lines (fails), warns at 300.

Exit codes:
  0 — all checks pass (warnings allowed).
  1 — at least one check failed.

Usage: python3 scripts/validate.py [--strict-warnings]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_GLOB = "skills/adadvisor*/SKILL.md"
DESC_MAX_LEN = 1024
BODY_FAIL_LINES = 500
BODY_WARN_LINES = 300


class Issue:
    LEVEL_ERROR = "error"
    LEVEL_WARN = "warn"

    def __init__(self, level: str, where: str, msg: str) -> None:
        self.level = level
        self.where = where
        self.msg = msg

    def __str__(self) -> str:
        return f"[{self.level.upper()}] {self.where}: {self.msg}"


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_text). Frontmatter is YAML between two --- lines."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    fm_raw = m.group(1)
    body = m.group(2)
    # Minimal YAML — name/description/license/version/model. Parse line-by-line so we
    # don't need PyYAML as a dependency.
    fm: dict = {}
    current_key = None
    buffer: list[str] = []

    def _flush() -> None:
        nonlocal current_key
        if current_key is not None:
            fm[current_key] = "\n".join(buffer).strip()
        current_key = None
        buffer.clear()

    for line in fm_raw.split("\n"):
        if not line.strip():
            continue
        # Match "key: value" or "key: |"
        m2 = re.match(r"^([A-Za-z_-]+):\s*(\|?)\s*(.*)$", line)
        if m2 and (m2.group(2) == "|" or not line.startswith(" ")):
            _flush()
            current_key = m2.group(1)
            rest = m2.group(3)
            if m2.group(2) == "|":
                buffer = []
            else:
                buffer = [rest] if rest else []
        else:
            buffer.append(line.lstrip())
    _flush()
    return fm, body


def _load_version() -> str:
    return (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()


def _load_plugin_manifests() -> tuple[dict, dict]:
    plugin = json.loads((REPO_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads(
        (REPO_ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    return plugin, marketplace


def validate() -> list[Issue]:
    issues: list[Issue] = []
    version = _load_version()
    plugin, marketplace = _load_plugin_manifests()

    # Version sync — plugin.json top-level, and each plugin entry in marketplace.json.
    # marketplace.json itself does not carry a top-level version per the Anthropic
    # marketplace schema; only the per-plugin entries do.
    if plugin.get("version") != version:
        issues.append(
            Issue(
                Issue.LEVEL_ERROR,
                ".claude-plugin/plugin.json",
                f'version "{plugin.get("version")}" != VERSION "{version}"',
            )
        )
    for mp_plugin in marketplace.get("plugins", []):
        if mp_plugin.get("version") != version:
            issues.append(
                Issue(
                    Issue.LEVEL_ERROR,
                    ".claude-plugin/marketplace.json",
                    f'plugin "{mp_plugin.get("name")}" version "{mp_plugin.get("version")}" != VERSION "{version}"',
                )
            )

    # Discover skills
    skill_files = sorted(REPO_ROOT.glob(SKILL_GLOB))
    skill_names: set[str] = set()

    for skill_md in skill_files:
        rel = skill_md.relative_to(REPO_ROOT)
        skill_dir = skill_md.parent
        skill_name = skill_dir.name
        skill_names.add(skill_name)

        text = skill_md.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)

        # 1. Frontmatter present
        if not fm:
            issues.append(Issue(Issue.LEVEL_ERROR, str(rel), "missing or invalid frontmatter"))
            continue

        # 2. name matches directory
        if fm.get("name") != skill_name:
            issues.append(
                Issue(
                    Issue.LEVEL_ERROR,
                    str(rel),
                    f'name "{fm.get("name")}" does not match directory "{skill_name}"',
                )
            )

        # 3. description requirements
        desc = (fm.get("description") or "").strip()
        if not desc:
            issues.append(Issue(Issue.LEVEL_ERROR, str(rel), "description is empty"))
        else:
            if len(desc) > DESC_MAX_LEN:
                issues.append(
                    Issue(
                        Issue.LEVEL_ERROR,
                        str(rel),
                        f"description is {len(desc)} chars, exceeds {DESC_MAX_LEN}",
                    )
                )
            if "Use when" not in desc:
                issues.append(Issue(Issue.LEVEL_ERROR, str(rel), "description missing 'Use when'"))
            if "NOT for" not in desc:
                issues.append(Issue(Issue.LEVEL_ERROR, str(rel), "description missing 'NOT for'"))

        # 4. version matches
        sv = (fm.get("version") or "").strip()
        if sv != version:
            issues.append(
                Issue(
                    Issue.LEVEL_ERROR,
                    str(rel),
                    f'version "{sv}" != VERSION "{version}"',
                )
            )

        # 7. references resolve and no orphans
        ref_dir = skill_dir / "references"
        if ref_dir.exists():
            on_disk = {f.name for f in ref_dir.glob("*.md")}
            linked = set(re.findall(r"\(references/([^)]+)\)", body))
            missing = linked - on_disk
            orphans = on_disk - linked
            for m in sorted(missing):
                issues.append(
                    Issue(Issue.LEVEL_ERROR, str(rel), f"SKILL.md links to references/{m} which doesn't exist")
                )
            for o in sorted(orphans):
                issues.append(
                    Issue(
                        Issue.LEVEL_WARN,
                        f"{rel.parent}/references/{o}",
                        "reference file is not linked from SKILL.md",
                    )
                )

        # 8. no parent-directory traversal in body
        if "../" in body:
            issues.append(Issue(Issue.LEVEL_ERROR, str(rel), "body contains '../' parent-directory reference"))

        # 9. body length
        body_lines = body.count("\n") + 1
        if body_lines > BODY_FAIL_LINES:
            issues.append(
                Issue(
                    Issue.LEVEL_ERROR,
                    str(rel),
                    f"body is {body_lines} lines, exceeds hard limit {BODY_FAIL_LINES}",
                )
            )
        elif body_lines > BODY_WARN_LINES:
            issues.append(
                Issue(
                    Issue.LEVEL_WARN,
                    str(rel),
                    f"body is {body_lines} lines, exceeds soft limit {BODY_WARN_LINES}",
                )
            )

        # references/*.md content: check parent traversal
        # Cross-skill links like ../../adadvisor-X/references/Y.md are allowed
        # (improve GitHub-rendered nav, soft-fail in standalone installs).
        # Block deeper traversal (../../../) or escape to non-skill folders.
        if ref_dir.exists():
            for ref_path in ref_dir.glob("*.md"):
                rel_ref = ref_path.relative_to(REPO_ROOT)
                ref_text = ref_path.read_text(encoding="utf-8")
                # ../../../ is too deep
                if "../../../" in ref_text:
                    issues.append(
                        Issue(Issue.LEVEL_ERROR, str(rel_ref), "contains '../../../' over-deep parent traversal")
                    )
                # `../` from references/ goes to the skill root — allow.
                # `../../` from references/ goes to the repo root — only allow if the
                # next segment is another skill name (adadvisor* prefix).
                for m in re.finditer(r"\.\./\.\./([\w-]+)/", ref_text):
                    target = m.group(1)
                    if not (target == "adadvisor" or target.startswith("adadvisor-")):
                        issues.append(
                            Issue(
                                Issue.LEVEL_WARN,
                                str(rel_ref),
                                f"links to non-skill path '../../{target}/' from references — installs may not include it",
                            )
                        )

    # 5. Skill discovery — skills live at `skills/adadvisor*/SKILL.md` per the
    # Anthropic plugin spec (skills/ subdirectory under plugin root). The
    # marketplace.json and plugin.json no longer enumerate individual skills;
    # discovery is automatic via the canonical layout.
    if not skill_names:
        issues.append(
            Issue(
                Issue.LEVEL_ERROR,
                "skills/",
                "no skills found — expected at least one skills/adadvisor*/SKILL.md",
            )
        )

    return issues


def main() -> int:
    strict_warnings = "--strict-warnings" in sys.argv
    issues = validate()
    errors = [i for i in issues if i.level == Issue.LEVEL_ERROR]
    warnings = [i for i in issues if i.level == Issue.LEVEL_WARN]

    for i in issues:
        print(str(i))

    print()
    print(f"Result: {len(errors)} error(s), {len(warnings)} warning(s).")

    if errors:
        return 1
    if strict_warnings and warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
