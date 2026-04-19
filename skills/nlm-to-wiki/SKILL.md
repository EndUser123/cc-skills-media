---
name: nlm-to-wiki
description: Sync NotebookLM notebook content to wiki pages with provenance tracking
version: 1.0.0
category: sync
enforcement: advisory
triggers:
  - /nlm-to-wiki
  - /nlm2wiki
aliases:
  - /nlm-to-wiki
  - /nlm2wiki
depends_on_skills:
  - nlm
  - wiki
workflow_steps:
  - prepare: Parse arguments, resolve vault path, authenticate if needed
  - list: Show available notebooks if no notebook-id given
  - sources: Snapshot source IDs before query, compare against manifest to gate re-query
  - query: Query selected notebook(s) for structured concept content
  - parse: Parse query response into individual concept pages
  - write: Write wiki pages with provenance frontmatter
  - manifest: Write sync manifest tracking source IDs and concept slugs
  - link: Invoke wiki skill to trigger auto-linking on written pages
execution:
  directive: |
    Sync NotebookLM notebook content to wiki pages. Modes:
    - sync <notebook-id>: Sync single notebook
    - sync all: Sync all notebooks
    - sync --dry-run: Preview what would be synced
    - sync <notebook-id> (re-sync): If sources unchanged since last sync, skip query entirely
    - Re-sync <notebook-id>: Explicit re-sync; skips unchanged sources, overwrites changed concepts
  default_args: ""
  examples:
    - "/nlm-to-wiki sync abc123-def456"
    - "/nlm-to-wiki sync all"
    - "/nlm-to-wiki sync --dry-run"
---

# NLM to Wiki Sync

## Purpose

Syncs structured content from NotebookLM notebooks into the wiki vault. For each notebook, extracts major concepts with definitions, operational details, relationships, and specific values, then creates individual wiki pages with provenance-tracking frontmatter.

## Project Context

### Integration Points
- **NLM CLI**: Uses `nlm` via Bash for notebook queries
- **Wiki vault**: Writes to `OBSIDIAN_VAULT_PATH` from settings.json
- **Wiki auto-linking**: Triggers wiki's auto-linking phase to create [[wikilinks]]

### Configuration
Vault path from settings.json:
```bash
OBSIDIAN_VAULT_PATH=~/.obsidian/vaults/personal-wiki  # from settings.json
```

### Sync Manifest
Each synced notebook has a manifest at `<vault_path>/.nlm-sync-manifest.json`:
```json
{
  "notebook_id": "<uuid>",
  "notebook_title": "<title>",
  "last_synced_at": "YYYY-MM-DD",
  "source_ids": ["<uuid>", "..."],
  "concept_slugs": ["<slug>", "..."]
}
```
The manifest is written after each sync and is used to detect new sources on subsequent syncs.

## Operation Modes

| Mode | Description |
|------|-------------|
| `sync <notebook-id>` | Sync a single notebook by ID |
| `sync all` | Sync all available notebooks |
| `sync --dry-run` | Preview what would be synced: prints concept names, slugs, and target file paths for each page that would be created. No writes performed. |
| Re-sync <notebook-id> | Re-syncs an already-synced notebook: skips concepts with matching content hash, overwrites changed concepts, warns on slug collision from prior sync |

## Your Workflow

### Step 1: Prepare
Parse arguments and determine mode:
- If no notebook ID and no `all`: show usage error
- If `--dry-run`: set dry_run=true
- Resolve vault path from settings.json

### Step 2: Authenticate (if needed)
```bash
nlm login --check
```
If authentication error occurs, run `nlm login` immediately (auto-handler).
After running `nlm login`, verify with `nlm login --check`. If still unauthenticated after login attempt, fail with descriptive error including stderr output.

### Step 3: List (if no notebook-id given)
```bash
nlm notebook list --json
```
Show available notebooks with IDs and titles for user selection.

### Step 3.5: Source Snapshot (re-sync gate)
Before querying, snapshot current source IDs for comparison:
```bash
nlm source list <notebook-id> --json
```
Compare returned `source_ids[]` against the sync manifest (`.nlm-sync-manifest.json` in the vault root). If the IDs match the last-synced state and the notebook has been synced before, skip the query entirely and report "No new sources since last sync."

If no manifest exists for this notebook, proceed to Step 4. The manifest is created during Step 6.

### Step 4: Query Selected Notebook(s)
For each notebook to sync, query for structured content:
```bash
nlm notebook query <notebook-id> "For each major concept in this notebook, extract:
1. Concept name
2. What it is (definition)
3. Specific operational details (thresholds, parameters, mechanisms)
4. How it relates to other concepts in the notebook
5. Specific values and parameters that can be verified

Extract 5-20 major concepts per notebook. A major concept is a distinct topic, technique, tool, or architectural pattern that appears in the source material. Ignore minor mentions, tangentially related topics, and generic background information.

Format as structured markdown with ## for each concept."
```

### Step 5: Parse Response into Concept Pages
Parse the query response:
- Split by `## ` headings to isolate each concept
- Extract concept name as title
- Extract definition, details, relationships, values
- Generate wiki page slug: `nlm-<notebook-id-short>-<concept-name-slug>.md`
  - notebook-id-short: first 8 characters of UUID
  - concept-name-slug: lowercase, hyphenated, max 50 chars

**Parse validation:** After splitting, validate that at least one concept was extracted and each concept has a non-empty body. If zero concepts extracted, fail with descriptive error and surface the raw query response. Do not proceed to write phase.

**Slug collision detection:** Maintain a seen-slug set during parsing. If a colliding slug is detected, append a numeric suffix (e.g., `-2`). Log each collision as a warning.

### Step 6: Write Wiki Pages with Provenance Frontmatter

**Pre-write vault validation:** Before any writes, validate: (1) vault path exists, (2) is a directory, (3) is writable. Fail immediately with descriptive error if any check fails. Use `pathlib.Path` with `.expanduser().resolve()` for normalization.

**Atomic writes:** Write pages to a staging temp directory first, then atomically move to vault. If move fails, clean up staging and report error. Alternatively, track written pages in a manifest and support resume.

For each concept, write a wiki page at:
`<vault_path>/wiki/concepts/nlm-<notebook-id-short>-<concept-name-slug>.md`

**Frontmatter schema:**
```yaml
---
nlm_sync:
  version: "1.0"
  notebook_id: "<uuid>"
  notebook_title: "<title>"
  synced_at: "YYYY-MM-DD"
  source_ids: []
  query_prompt: "<the prompt used>"
provenance:
  - claim: "<specific claim text>"
    source_id: "<source uuid>"
    cited_text: "<exact text from source>"
sources:
- id: "<notebook-id>"
  title: "<notebook-title>"
tags:
- nlm-synced
created: YYYY-MM-DD
---

## Concept Name

<extracted content>

## Related

<auto-linked wikilinks will be added by wiki skill's auto-linking phase>
```

### Step 7: Link Phase
After writing all pages, invoke the wiki skill to trigger auto-linking:
```bash
/wiki ingest <vault_path>/wiki/concepts/nlm-<notebook-id-short>-*.md
```
This creates [[wikilinks]] between related concept pages. If the wiki skill is unavailable, print a warning listing the pages that need linking and instruct the user to run `/wiki ingest` manually.
Print summary: report pages created, any slug collisions detected, and linking status.

### Step 8: Write Sync Manifest
After all pages are written and linked, write the sync manifest to the vault root:
```bash
<vault_path>/.nlm-sync-manifest.json
```
```json
{
  "notebook_id": "<uuid>",
  "notebook_title": "<title>",
  "last_synced_at": "YYYY-MM-DD",
  "source_ids": ["<uuid>", "..."],
  "concept_slugs": ["<slug>", "..."]
}
```
Overwrite any existing manifest for this notebook. The manifest is the source-of-truth for the re-sync source comparison in Step 3.5.

## Validation Rules

- **Auth errors**: Auto-run `nlm login` without prompting
- **Notebook not found**: Run `nlm notebook list` to verify ID
- **Rate limiting**: 2 second delay between query operations AND between notebook queries in sync-all mode. On rate-limit error: retry with exponential backoff (1s, 2s, 4s), then fail with partial-sync report indicating which notebooks were not synced.
- **Frontmatter**: Use `yaml.safe_dump` for all YAML serialization
- **Path safety**: Validate vault path exists before writing

## Examples

### Sync a Single Notebook
```
/nlm-to-wiki sync abc123-def456-7890
```

### Sync All Notebooks
```
/nlm-to-wiki sync all
```

### Dry Run Preview
```
/nlm-to-wiki sync --dry-run
```

## Output Format

After sync completes, report:
```
NLM to Wiki Sync Complete
=========================
Notebook: <title> (<id>)
Concepts extracted: N
Pages created:
  - wiki/concepts/nlm-abc12345-concept-one.md
  - wiki/concepts/nlm-abc12345-concept-two.md
  ...
Total pages: N
```

## Security Notes

- YAML frontmatter uses `yaml.safe_dump` exclusively
- User-controlled content (titles, concept names) sanitized before path construction
- Path traversal prevention: slugs are alphanumeric/hyphen only

## Integration Points

| Component | Role |
|-----------|------|
| `nlm` CLI | Notebook queries |
| Wiki skill | Auto-linking [[wikilinks]] after ingest |
| settings.json | OBSIDIAN_VAULT_PATH configuration |
