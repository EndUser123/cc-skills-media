# cc-skills-media

Media skills for Claude Code — NotebookLM integration, YouTube processing, course generation, and MiniMax AI content generation.

## Skills (13)

| Skill | Purpose | Home |
|-------|---------|------|
| /nlm | Unified NotebookLM Engine (CLI, MCP, API, Strategy) | `nlm/` |
| /yt-is | YouTube Channel Management | `yt-is/` |
| /yt-nlm | NotebookLM Transcript Extraction | `yt-nlm/` |
| /yt-selenium | YouTube Transcript Extraction (Selenium) | `yt-selenium/` |
| codebase-to-course | Codebase-to-Course Generation | `codebase-to-course/` |
| nlm-to-wiki | NLM to Wiki Sync | `nlm-to-wiki/` |
| nlm-cleanup | NotebookLM Source Cleanup (moved to /nlm clean) | `nlm/` |
| frontend-dev | MiniMax Frontend Development | `frontend-dev/` |
| vision-analysis | MiniMax Vision/Image Analysis | `vision-analysis/` |
| fullstack-dev | MiniMax Fullstack Development | `fullstack-dev/` |
| minimax-music-gen | MiniMax Music Generation | `minimax-music-gen/` |
| minimax-music-playlist | MiniMax Music Playlist | `minimax-music-playlist/` |
| minimax-multimodal-toolkit | MiniMax CLI (mmx) — text, image, video, speech, music, search | `minimax-multimodal-toolkit/` |

## Artifacts Convention

All runtime artifacts write to:

```
.claude/.artifacts/{terminal_id}/{skill_name}/
```

Skills MUST NOT write state to their own directory or to the package root.

## Installation

Skills surfaced via junctions in `P://.claude/skills/`.
