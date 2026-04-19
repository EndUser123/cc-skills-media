# cc-skills-media

Media skills for Claude Code — NotebookLM integration, YouTube processing, and course generation.

## Skills (10)

| Skill | Purpose |
|-------|---------|
| codebase-to-course | Codebase-to-Course |
| nlm | NotebookLM CLI Expert |
| nlm-cleanup | NotebookLM Notebook Cleanup |
| nlm-skill | NotebookLM CLI & MCP Expert |
| nlm-to-wiki | NLM to Wiki Sync |
| notebooklm | NotebookLM Automation |
| notebooklm-expert | NotebookLM Expert |
| yt-is | /yt-is — YouTube Channel Management |
| yt-nlm | /yt-nlm — NotebookLM Transcript Extraction |
| yt-selenium | /yt-selenium — YouTube Transcript Extraction via Selenium |

## Artifacts Convention

All runtime artifacts write to:



 from  env var (falls back to ).

Skills MUST NOT write state to their own directory or to the package root.

## Installation

Skills surfaced via junctions in :



Command frontends live in .
