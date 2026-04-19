# cc-skills-media

Media skills for Claude Code — NotebookLM integration, YouTube processing, and course generation.

## Skills (8)

| Skill | Purpose |
|-------|---------|
| codebase-to-course | Convert codebase to interactive course |
| nlm | NotebookLM integration |
| nlm-cleanup | NotebookLM cleanup |
| nlm-skill | NotebookLM skill wrapper |
| nlm-to-wiki | NotebookLM to wiki conversion |
| notebooklm-expert | NotebookLM expert mode |
| yt-nlm | YouTube to NotebookLM pipeline |
| yt-selenium | YouTube Selenium automation |

## Artifacts Convention

All runtime artifacts write to:

```
P:/.claude/.artifacts/{terminal_id}/<skill-name>/
```

`terminal_id` from `CLAUDE_TERMINAL_ID` env var (falls back to `"default"`).

Skills MUST NOT write state to their own directory or to the package root. The `.gitignore` covers `.evidence/`, `.state/`, `.benchmarks/`, `__pycache__/`, `.claude/`.

## NotebookLM Auth

Several skills require NotebookLM authentication cookies. See individual skill docs for auth setup details.

## Installation

Skills surfaced via junctions in `.claude/skills/`:

```powershell
New-Item -ItemType Junction -Path "P:/.claude/skills/<name>" -Target "P:/packages/cc-skills-media/skills/<name>"
```

Command frontends live in `.claude/commands/<name>.md`.
