---
name: nlm
description: "Expert guide for the NotebookLM CLI (`nlm`) and MCP server - interfaces for Google NotebookLM. Use this skill when users want to interact with NotebookLM programmatically, including: creating/managing notebooks, adding sources (URLs, YouTube, text, Google Drive), generating content (podcasts, reports, quizzes, flashcards, mind maps, slides, infographics, videos, data tables), conducting research, chatting with sources, or automating NotebookLM workflows. Triggers on mentions of \"nlm\", \"notebooklm\", \"notebook lm\", \"podcast generation\", \"audio overview\", or any NotebookLM-related automation task."
version: "0.9.0"
status: stable
verified_cli_version: "0.5.9"
category: productivity
enforcement: advisory
triggers:
  - '/nlm'
workflow_steps:
  - execute_nlm_workflow
---

# NotebookLM CLI Expert

## Default Interface: CLI

**ALWAYS use the `nlm` CLI via Bash. Do NOT check for or use MCP tools.** The CLI is more reliable, has full feature parity, better error messages, and no server process to manage. MCP tools are documented in `references/mcp_tools.md` for reference only.

```bash
bash("nlm notebook list")
```

## Quick Start

```bash
nlm --help              # List all commands
nlm <command> --help    # Help for specific command
nlm --ai                # Full AI-optimized documentation (RECOMMENDED)
nlm --version           # Check installed version
```

### Command Styles

The CLI supports **TWO command styles**:

**Noun-first (shown in this guide)**:
```bash
nlm notebook list
nlm source add <nb-id> --url "https://..."
nlm studio status <nb-id>
```

**Verb-first (alternative)**:
```bash
nlm list notebooks
nlm add url <nb-id> <url>
nlm status artifacts <nb-id>
```

Both call the same functions. Use whichever feels natural.

## Critical Rules

1. **Authenticate on auth error — NEVER ask the user to run `nlm login`**: When any nlm command returns "Authentication Error" or "Cookies have expired", immediately run `nlm login` yourself (opens browser). Do NOT ask the user to do it.
2. **Sessions expire in ~20 minutes**: If commands fail after login, re-run `nlm login`
3. **ALWAYS ASK USER BEFORE DELETE**: Deletions are irreversible. Show what will be deleted and warn about permanent data loss.
4. **`--confirm` is REQUIRED**: All generation and delete commands need `--confirm` or `-y`
5. **Research requires `--notebook-id`**: The flag is mandatory, not positional
6. **Capture IDs from output**: Create/start commands return IDs needed for subsequent operations
7. **Use aliases**: `nlm alias set <name> <uuid>` simplifies long UUIDs
8. **Check aliases before creating**: Run `nlm alias list` to avoid conflicts
9. **Prefer `nlm notebook query` for scripted use**: `nlm chat start` launches an interactive REPL — use for exploratory sessions, not scripted workflows. For one-shot Q&A, `nlm notebook query` is preferred.
10. **Choose output format wisely**: Default = compact; `--quiet` for IDs; `--json` for parsing
11. **Use `--help` when unsure**: `nlm <command> --help` shows all options

## Notebook Organization Taxonomy

### Repos vs Topic Collections

Notebooks contain either git-ingested repos OR topic collections (URLs, PDFs, docs). Different rules apply:

| Type | How to add | Examples |
|------|-----------|----------|
| **Git repos** | Use `/gitingest` | MCP servers, frameworks, libraries |
| **Topic collections** | `nlm source add` individually | Curated URLs, papers, docs |

### Repo-Based Notebook Taxonomy

Git repos use a two-category split by what the repo IS:

**ext-Agentic-Platforms** — repos that ARE agent frameworks/platforms
- AI/research agent platforms (e.g., gpt-researcher, agentGPT)
- Agent orchestration frameworks (e.g., langgraph, crewai)
- MCP server implementations

**ext-Tools-and-Libraries** — repos that are tools/utilities used BY agents
- CLI tools (e.g., repomix, chrome-devtools-mcp)
- Libraries (e.g., Scrapling, genai-toolbox, yb-llms)
- Developer tools that feed into agent workflows

**ext-Video-Pipelines** — video processing repos (YouTube APIs, transcription, OCR, etc.)

### Topic Collections

Curated notebooks of URLs, PDFs, papers — additive, not repo-based. Keep as-is:
- ext-sickn33-antigravity-awesome-skills
- ext-Gemini CLI and Claude Code
- ext-The Renaissance of the Terminal
- etc.

Do NOT force topic collections into the repo taxonomy.

### Naming Convention

All external reference notebooks use `ext-` prefix. Format: `ext-Short-Name` (kebab-case, max 3 words).

## Post-Operation Verification

**ALWAYS verify after mutating operations.** Check the actual state matches the intended outcome before reporting success.

See [references/output-template.md](references/output-template.md) for exact verification command formats.

**Key rules:**
- Use `--json` flag for all verification commands
- Parse JSON directly (array, not wrapped object)
- Report actual state, not assumptions

**Rule: Report what actually happened, not what should have happened.** Re-run the GET command to confirm.

## Workflow Decision Tree

```
User wants to...
|
+-> First time        -> nlm login -> nlm notebook create "Title"
+-> Add git repos     -> /gitingest (uses gitingest_runner.py pipeline)
+-> Add topic content -> nlm source add <nb-id> --url/--text/--drive
+-> Generate content  -> nlm audio/report/quiz/flashcards/mindmap/slides/infographic/video create <id> --confirm
+-> Ask questions     -> nlm notebook query <nb-id> "question"
+-> Check generation  -> nlm studio status <nb-id>
+-> Manage            -> nlm notebook/source list, delete with --confirm
+-> Re-ingest repo    -> Delete old sources first, then /gitingest
```

## Command Categories (CLI Quick Reference)

### Authentication
```bash
nlm login                           # Primary method (opens browser)
nlm login --check                   # Validate session
nlm login --profile <name>          # Named profile (multi-account)
nlm login switch <profile>          # Switch default profile
```

Multi-profile support: each profile gets isolated browser session. Session lifetime: ~20 minutes. See `references/command_reference.md` for full auth options.

### Notebook Management
```bash
nlm notebook list [--json|--quiet]  # List notebooks
nlm notebook create "Title"         # Create, returns ID
nlm notebook get <id>               # Get details
nlm notebook describe <id>          # AI summary + topics
nlm notebook query <id> "question"  # One-shot Q&A (NOT chat start)
nlm notebook rename <id> "Title"    # Rename
nlm notebook delete <id> --confirm  # PERMANENT deletion
```

### Source Management
```bash
nlm source add <nb-id> --url "https://..."        # Web page/YouTube
nlm source add <nb-id> --text "content" --title X  # Pasted text
nlm source add <nb-id> --drive <doc-id> [--type doc|slides|sheets|pdf]
nlm source list <nb-id> [--drive] [--quiet]        # List sources
nlm source stale <nb-id>                           # Check Drive freshness
nlm source sync <nb-id> --confirm                  # Sync stale Drive sources
nlm source delete <id> --confirm                   # Delete source
```

### Research (Source Discovery)
```bash
nlm research start "query" --notebook-id <id> [--mode fast|deep] [--source web|drive]
nlm research status <nb-id> [--max-wait 300]       # Poll until done
nlm research import <nb-id> <task-id> [--indices 0,2,5]  # Import sources
```
Modes: `fast` (~30s, ~10 sources) | `deep` (~5min, ~40+ sources, web only)

### Content Generation (Studio)
All commands require `--confirm`. Common flags: `--source-ids`, `--language`, `--focus`

| Type | Command | Key Options |
|------|---------|-------------|
| Audio | `nlm audio create <id>` | `--format` deep_dive/brief/critique/debate, `--length` short/default/long |
| Report | `nlm report create <id>` | `--format` "Briefing Doc"/"Study Guide"/"Blog Post"/"Create Your Own" |
| Quiz | `nlm quiz create <id>` | `--count` N, `--difficulty` 1-5 |
| Flashcards | `nlm flashcards create <id>` | `--difficulty` easy/medium/hard |
| Mind Map | `nlm mindmap create <id>` | `--title` |
| Slides | `nlm slides create <id>` | `--format` detailed/presenter, `--length` short/default |
| Infographic | `nlm infographic create <id>` | `--orientation`, `--detail`, `--style` |
| Video | `nlm video create <id>` | `--format` explainer/brief, `--style` |
| Data Table | `nlm data-table create <id> "desc"` | Description is required positional arg |

See `references/command_reference.md` for complete option tables.

### Studio (Artifact Management)
```bash
nlm studio status <nb-id> [--full|--json]   # List/check artifacts
nlm download audio <nb-id> --output file.mp3 # Download artifact
nlm export docs <nb-id> <artifact-id> --title "Title"  # Export to Google Docs
nlm studio delete <nb-id> <artifact-id> --confirm      # Delete artifact
```

### Batch, Cross-Notebook, Pipelines, Tags
```bash
nlm batch query "question" --notebooks "id1,id2"  # or --tags "ai" or --all
nlm cross query "question" --notebooks "id1,id2"  # Aggregated with per-notebook citations
nlm pipeline run <nb> ingest-and-podcast --url "..."  # Multi-step workflow
nlm tag add <nb> --tags "ai,research"              # Tag for organization
```

Built-in pipelines: `ingest-and-podcast`, `research-and-report`, `multi-format`

### Other Commands
```bash
# Sharing
nlm share status <nb-id>                          # Check sharing
nlm share public <nb-id> [--off]                  # Public link on/off
nlm share invite <nb-id> email@x.com --role editor # Invite collaborator

# Notes
nlm note create <nb-id> --content "text" --title "Title"
nlm note list <nb-id>

# Aliases
nlm alias set <name> <uuid>    # Create
nlm alias list                 # List all

# Configuration
nlm config show                # Show settings
nlm config set <key> <value>   # Update setting
```

## Output Formats

| Flag | Description |
|------|-------------|
| (none) | Rich table (human-readable) |
| `--json` | JSON output (for parsing) |
| `--quiet` | IDs only (for piping) |
| `--title` | "ID: Title" format |
| `--full` | All columns/details |

## Error Recovery

| Error | Solution |
|-------|----------|
| "Authentication Error" / "Cookies have expired" | **Run `nlm login` immediately** (do NOT ask user) |
| "Notebook/Source not found" | `nlm notebook list` / `nlm source list <nb-id>` |
| "Rate limit exceeded" | Wait 30s, retry |
| "Research already in progress" | Use `--force` or import first |

**Built-in Auto-Recovery**: The CLI has automatic recovery for common errors:
- **Auth Recovery (3-layer)**: CSRF/session refresh → token reload from disk → headless auth (if browser profile has saved login)
- **Server Error Retry**: Automatic retry with exponential backoff (1s, 2s, 4s) for 429, 500, 502, 503, 504 errors

Most transient errors are handled automatically. Manual `nlm login` is only needed when all auto-recovery layers fail.

See `references/troubleshooting.md` for detailed error handling.

## Rate Limiting

| Operation | Delay |
|-----------|-------|
| Source/Research/Query | 2 seconds |
| Content generation | 5 seconds |

## Reference Files

| File | Contents |
|------|----------|
| [command_reference.md](references/command_reference.md) | Complete command signatures, all flags and options |
| [troubleshooting.md](references/troubleshooting.md) | Detailed error handling and recovery procedures |
| [workflows.md](references/workflows.md) | End-to-end task sequences (research pipeline, study materials, etc.) |
| [mcp_tools.md](references/mcp_tools.md) | MCP tool signatures (for reference; CLI is preferred) |

## Changelog

### 0.9.0
- Added `verified_cli_version: "0.5.9"` to frontmatter for version tracking
- Added Command Styles section — CLI supports both noun-first and verb-first command styles
- Reconciled `nlm chat start` guidance — clarified it launches interactive REPL, preferred for exploratory sessions, not scripted workflows
- Added Built-in Auto-Recovery documentation — 3-layer auth recovery and server error retry with exponential backoff
