# cc-skills-media

Media skills for Claude Code — NotebookLM integration, YouTube processing, and course generation.

## Skills (7)

| Skill | Purpose | Home |
|-------|---------|------|
| /nlm | Unified NotebookLM Engine (CLI, MCP, API, Strategy) | `nlm/` |
| /yt-is | /yt-is — YouTube Channel Management | `yt-is/` |
| /yt-nlm | /yt-nlm — NotebookLM Transcript Extraction | `yt-nlm/` |
| /yt-selenium | /yt-selenium — YouTube Transcript Extraction (Selenium) | `yt-selenium/` |
| codebase-to-course | Codebase-to-Course Generation | `codebase-to-course/` |
| nlm-to-wiki | NLM to Wiki Sync | `nlm-to-wiki/` |
| nlm-cleanup | NotebookLM Source Cleanup (moved to /nlm clean) | `nlm/` |

## Artifacts Convention

All runtime artifacts write to:

```
.claude/.artifacts/{terminal_id}/{skill_name}/
```

Skills MUST NOT write state to their own directory or to the package root.

## Installation

Skills surfaced via junctions in `P://.claude/skills/`.
