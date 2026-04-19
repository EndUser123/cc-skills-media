---
name: nlm-cleanup
description: Analyze and clean up NotebookLM notebooks by identifying duplicate, off-topic, and redundant sources. Use when a notebook has "too many sources" or known content sprawl. Triggers on requests to clean up, dedupe, trim, or reduce NotebookLM notebook sources.
version: "1.0.0"
status: stable
category: productivity
triggers:
  - /nlm-cleanup
  - /notebook-cleanup
  - /notebooklm cleanup
  - /notebooklm clean
suggest:
  - /nlm
  - /notebooklm
---

# NotebookLM Notebook Cleanup

Analyze a NotebookLM notebook for duplicate, off-topic, and redundant sources, then remove them.

## Workflow

```
User reports "too many sources" or wants cleanup
  |
  v
1. DISCOVER   -> nlm source list <nb-id> --json
2. ANALYZE    -> Pattern match + NotebookLM query for content quality
3. REPORT     -> Categorize: [DELETE] [CONSOLIDATE] [MOVE] [KEEP]
4. EXECUTE    -> User confirms, then batch delete with --confirm
```

## Phase 1: Discover

```bash
# Get all sources as JSON
nlm source list <notebook-id> --json

# Check total count
python3 -c "import json,sys; data=json.load(sys.stdin); print(f'Total: {len(data)}')"
```

## Phase 2: Analyze

### Step 2a: Cluster by type

```bash
# Cluster by source type, title patterns, and URL domains
python3 -c "
import json, sys
from collections import defaultdict

data = json.load(sys.stdin)

# Group by type
by_type = defaultdict(list)
for s in data:
    by_type[s['type']].append(s['title'][:60])

for t, titles in sorted(by_type.items(), key=lambda x: -len(x[1])):
    print(f'\n=== {t} ({len(titles)}) ===')
    for t in titles[:5]:
        print(f'  {t}')
    if len(titles) > 5:
        print(f'  ... and {len(titles)-5} more')
"
```

### Step 2b: Find duplicates by URL domain

```bash
# Find sources from same domain (high redundancy risk)
python3 -c "
import json, sys
from urllib.parse import urlparse
from collections import defaultdict

data = json.load(sys.stdin)
by_domain = defaultdict(list)
for s in data:
    url = s.get('url') or ''
    if url:
        domain = urlparse(url).netloc
        by_domain[domain].append((s['id'], s['title'][:60]))

for domain, items in sorted(by_domain.items(), key=lambda x: -len(x[1])):
    if len(items) > 2:
        print(f'\n=== {domain} ({len(items)}) ===')
        for id, title in items:
            print(f'  {id} | {title}')
"
```

### Step 2c: Find off-topic by title keywords

```bash
# Flag obviously off-topic sources (customize keywords per notebook theme)
python3 -c "
import json, sys

data = json.load(sys.stdin)

#通用 off-topic 关键词 (customize per notebook)
off_topic_keywords = [
    'seo audit', 'scope creep', 'cultural heritage', 'ai 2027', 'scribd',
    'spotlytt', 'proof-of-state', 'settlement constitution',
]

off_topic = []
for s in data:
    t = s['title'].lower()
    for kw in off_topic_keywords:
        if kw in t:
            off_topic.append((s['id'], s['title'][:80], kw))
            break

print(f'Off-topic sources: {len(off_topic)}')
for id, title, kw in off_topic:
    print(f'  {id} | {kw} | {title}')
"
```

### Step 2d: Identify clusters for consolidation

```bash
# Cluster Ralph Wiggum / autoresearch / autonomous loop sources
python3 -c "
import json, sys

data = json.load(sys.stdin)

Ralph_KEYWORDS = ['ralph wiggum', 'ralph-loop', 'autoresearch', 'autonomous loop', 'karpathy']
mcp_KEYWORDS = ['model context protocol', 'mcp server', 'mcp ']
hooks_KEYWORDS = ['claude code hooks', 'stop hook', 'pretooluse', 'posttooluse']
claude_guide_KEYWORDS = ['claude code cli', 'claude code best practice', 'claude code configuration']

clusters = {'ralph_autoresearch': [], 'mcp': [], 'hooks': [], 'claude_guides': []}

for s in data:
    t = s['title'].lower()
    if any(k in t for k in Ralph_KEYWORDS):
        clusters['ralph_autoresearch'].append((s['id'], s['title'][:70]))
    elif any(k in t for k in mcp_KEYWORDS):
        clusters['mcp'].append((s['id'], s['title'][:70]))
    elif any(k in t for k in hooks_KEYWORDS):
        clusters['hooks'].append((s['id'], s['title'][:70]))
    elif any(k in t for k in claude_guide_KEYWORDS):
        clusters['claude_guides'].append((s['id'], s['title'][:70]))

for name, items in clusters.items():
    if len(items) > 3:
        print(f'\n=== {name} cluster: {len(items)} sources (keep 2-3) ===')
        for id, title in items:
            print(f'  {id} | {title}')
"
```

### Step 2e: Verify generated_text content quality

```bash
# For generated_text sources, verify they have real body content (not just bibliographies)
# Query NotebookLM about each generated_text source
nlm notebook query <notebook-id> "Does the source titled 'TITLE' have substantive content? Summarize its key ideas in 2 sentences." 2>&1
```

If NotebookLM returns only URL/link lists with no synthesis → mark for DELETE.
If NotebookLM returns substantive analysis → KEEP.

## Phase 3: Report

Present findings in this format:

```
## Cleanup Plan for "<notebook-title>"

**Total sources: X → Y** (Z to delete)

### [DELETE] Off-topic (Z sources)
| Source | Reason |
|--------|--------|
| ID | TITLE (off-topic: SEO/cultural heritage/etc.) |

### [CONSOLIDATE] Cluster: NAME (N→K)
Keep: ID1 (TITLE), ID2 (TITLE)
Delete: ID3, ID4, ID5...

### [KEEP] Canonical sources per cluster
...
```

## Phase 4: Execute

```bash
# User confirms, then:
nlm source delete <id1> <id2> <id3> --confirm
```

## Deletion Decision Rules

| Condition | Action |
|-----------|--------|
| Off-topic keyword match (SEO, cultural heritage, unrelated domain) | DELETE |
| Duplicate URL domain + similar title | CONSOLIDATE (keep 2) |
| Reddit cross-post of same article | DELETE copy |
| Blog post that rehashes official docs | DELETE blog, KEEP official |
| generated_text with only URL lists | DELETE |
| generated_text with substantive synthesis | KEEP |
| Research paper + its direct follow-up by same authors | KEEP newer only |
| Canonical explainer (claudefa.st, official docs) | KEEP 1 |
| N resources on same sub-topic (N>3) | CONSOLIDATE to 2-3 |

## Known Off-Topic Clusters (General)

These topics are rarely relevant to agentic engineering notebooks:
- SEO audit reports
- Cultural heritage / museum digitization
- AI-2027 speculative timelines
- Scope creep / project management contracts
- Proof-of-state / financial settlement docs

## Reference Patterns

See `references/cluster-patterns.md` for per-domain consolidation patterns.
