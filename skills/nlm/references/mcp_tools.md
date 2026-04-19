# NotebookLM MCP Tools Reference

This document contains detailed MCP tool signatures and usage for users who prefer MCP over CLI.

> **Note:** The CLI is the default interface. See SKILL.md for the CLI-first policy. MCP tools are documented here for reference.

## Authentication

```python
# Run CLI authentication (works for both CLI and MCP)
nlm login

# Then reload tokens in MCP
mcp__notebooklm-mcp__refresh_auth()

# Or manually save cookies via MCP (fallback)
mcp__notebooklm-mcp__save_auth_tokens(cookies="<cookie_header>")
```

**Switching MCP Accounts:** The MCP server always uses the active default profile. To switch Google accounts, use the CLI: `nlm login switch <name>`. Your next MCP tool call will instantly use the new account.

**Note:** Both MCP and CLI share the same authentication backend, so authenticating with one works for both.

## Notebook Management

Tools: `notebook_list`, `notebook_create`, `notebook_get`, `notebook_describe`, `notebook_query`, `notebook_rename`, `notebook_delete`.

All accept `notebook_id` parameter. Delete requires `confirm=True`.

## Source Management

Use `source_add` with these `source_type` values:
- `url` - Web page or YouTube URL (`url` param)
- `text` - Pasted content (`text` + `title` params)
- `file` - Local file upload (`file_path` param)
- `drive` - Google Drive doc (`document_id` + `doc_type` params)

Other tools: `source_list_drive`, `source_describe`, `source_get_content`, `source_rename`, `source_sync_drive` (requires `confirm=True`), `source_delete` (requires `confirm=True`).

## Research (Source Discovery)

Use `research_start` with:
- `source`: `web` or `drive`
- `mode`: `fast` (~30s) or `deep` (~5min, web only)

Workflow: `research_start` -> poll `research_status` -> `research_import`

## Content Generation (Studio)

Use `studio_create` with `artifact_type` and type-specific options. All require `confirm=True`.

| artifact_type | Key Options |
|--------------|-------------|
| `audio` | `audio_format`: deep_dive/brief/critique/debate, `audio_length`: short/default/long |
| `video` | `video_format`: explainer/brief, `visual_style`: auto_select/classic/whiteboard/kawaii/anime/watercolor/retro_print/heritage/paper_craft |
| `report` | `report_format`: Briefing Doc/Study Guide/Blog Post/Create Your Own, `custom_prompt` |
| `quiz` | `question_count`, `difficulty`: easy/medium/hard |
| `flashcards` | `difficulty`: easy/medium/hard |
| `mind_map` | `title` |
| `slide_deck` | `slide_format`: detailed_deck/presenter_slides, `slide_length`: short/default |
| `infographic` | `orientation`: landscape/portrait/square, `detail_level`: concise/standard/detailed, `infographic_style`: auto_select/sketch_note/professional/bento_grid/editorial/instructional/bricks/clay/anime/kawaii/scientific |
| `data_table` | `description` (REQUIRED) |

**Common options**: `source_ids`, `language` (BCP-47 code), `focus_prompt`

**Revise Slides:** Use `studio_revise` to revise individual slides in an existing slide deck.
- Requires `artifact_id` (from `studio_status`) and `slide_instructions`
- Creates a NEW artifact -- the original is not modified
- Slide numbers are 1-based (slide 1 = first slide)
- Poll `studio_status` after calling to check when the new deck is ready

## Studio (Artifact Management)

Use `studio_status` to check progress (or rename with `action="rename"`). Use `download_artifact` with `artifact_type` and `output_path`. Use `export_artifact` with `export_type`: docs/sheets. Delete with `studio_delete` (requires `confirm=True`).

**Status values**: `completed`, `in_progress`, `failed`

**Prompt Extraction**: The `studio_status` tool returns a `custom_instructions` field for each artifact containing the original focus prompt or custom instructions used to generate that artifact.

## Renaming Resources

**Source:** `source_rename(notebook_id, source_id, new_title)`

**Studio Artifact:** Use `studio_status` with `action="rename"`, `artifact_id`, and `new_title`.

## Server Info

```python
mcp__notebooklm-mcp__server_info()
# Returns: version, latest_version, update_available, update_command
```

## Chat Configuration and Notes

Use `chat_configure` with `goal`: default/learning_guide/custom. Use `note` with `action`: create/list/update/delete. Delete requires `confirm=True`.

## Notebook Sharing

Use `notebook_share_status` to check, `notebook_share_public` to enable/disable public link, `notebook_share_invite` with `email` and `role`: viewer/editor.

## Batch Operations

Use `batch` with `action` parameter. Select notebooks by `notebook_names`, `tags`, or `all=True`.

```python
batch(action="query", query="What are the key findings?", notebook_names="AI Research, Dev Tools")
batch(action="add_source", source_url="https://example.com", tags="ai,research")
batch(action="create", titles="Project A, Project B, Project C")
batch(action="delete", notebook_names="Old Project", confirm=True)
batch(action="studio", artifact_type="audio", tags="research", confirm=True)
```

## Cross-Notebook Query

```python
cross_notebook_query(query="Compare approaches", notebook_names="Notebook A, Notebook B")
cross_notebook_query(query="Summarize", tags="ai,research")
cross_notebook_query(query="Everything", all=True)
```

## Pipelines

```python
pipeline(action="list")  # List available pipelines
pipeline(action="run", notebook_id="...", pipeline_name="ingest-and-podcast", input_url="https://...")
```

**Built-in pipelines:** `ingest-and-podcast`, `research-and-report`, `multi-format`

## Tags & Smart Select

```python
tag(action="add", notebook_id="...", tags="ai,research,llm")
tag(action="remove", notebook_id="...", tags="ai")
tag(action="list")                           # List all tagged notebooks
tag(action="select", query="ai research")    # Find notebooks by tag match
```
