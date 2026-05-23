---
name: nlm
description: "Unified entry point for Google NotebookLM — handles CLI, MCP, API, and maintenance operations. Use for creating notebooks, adding sources (URLs, YouTube, Drive), generating content (podcasts, reports), and notebook hygiene."
version: "2.0.0"
status: stable
category: productivity
enforcement: advisory
triggers:
  - /nlm
  - /notebooklm
  - /notebooklm cleanup
  - /notebooklm clean
  - /notebooklm expert
suggest:
  - /explore
  - /yt-is

workflow_steps:
  - step_detect_interface: Detect available interfaces (CLI vs MCP vs API)
  - step_authenticate: Ensure session is active via 'nlm login' or API check
  - step_execute: Route to appropriate subcommand or reference
---

# /nlm — Unified NotebookLM Engine

Single command for all NotebookLM operations, maintenance, and expert strategy.

## ⚡ INTERFACE ROUTING

**Identify which toolset to use based on availability:**

1. **CLI (Primary)**: Use `nlm` commands via Bash. Reliable, full feature set.
2. **MCP (Alternative)**: Use `mcp_notebooklm_*` tools. Ask user preference if CLI is also available.
3. **API (Library)**: Use `notebooklm-py` for pure Python AST/automation tasks.

---

## Subcommands & Modes

| Command | Purpose | Implementation |
|---------|---------|----------------|
| `/nlm` | General CLI/MCP guidance | `nlm-skill` logic |
| `/nlm clean` | Source cleanup & deduping | `nlm-cleanup` logic |
| `/nlm api` | Python API documentation | `notebooklm` skill |
| `/nlm expert`| ACG Workflow & Strategy | `notebooklm-expert` skill |

---

## 1. Core Operations (`/nlm`)

**Critical Rule: NEVER ask the user to run `nlm login`.** If you see "Authentication Error", run `nlm login` yourself (opens browser).

### Quick Reference
```bash
nlm notebook list         # List notebooks
nlm source add <id> --url # Add web/YouTube source
nlm audio create <id>     # Generate Deep Dive podcast
nlm studio status <id>    # Check generation progress
```

---

## 2. Notebook Maintenance (`/nlm clean`)

Analyze and prune source sprawl.

**Workflow:**
1. `nlm source list <id> --json`
2. Cluster by type/domain (detect duplicates)
3. Flag off-topic keywords (SEO, scope creep, cultural heritage)
4. `nlm source delete <ids> --confirm`

---

## 3. Python API Documentation (`/nlm api`)

Reference for the `notebooklm-py` library.

**Installation:** `pip install notebooklm-py`
**Usage:** `import notebooklm; client = notebooklm.Client()`

---

## 4. Expert Strategy (`/nlm expert`)

**The ACG Workflow (Analyze -> Challenge -> Gap)**

1. **Strategic Selection**: 8 diverse sources > 50 junk documents.
2. **Configuration**: Set custom role + "Longer" response length.
3. **Iterative Loop**: Run ACG prompts → Save best answers as notes → **Convert Note to Source**.
4. **Studio**: Generate Audio/Reports only after the notebook is "strengthened."

---

## References

| File | Contents |
|------|----------|
| `references/cli_reference.md` | Full CLI command table and flags |
| `references/api_reference.md` | Python library classes and methods |
| `references/cleanup_logic.md` | Python snippets for source analysis |
| `references/strategy_guide.md` | ACG Workflow and source mix strategy |
