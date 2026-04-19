# Notebook Cleanup: Known Cluster Patterns

Per-topic consolidation guides based on observed NotebookLM notebook patterns.

---

## Claude Code Hooks (~10-15 sources typical) → Keep 3

**KEEP (canonical):**
1. Official docs: `code.claude.com/docs/en/hooks-guide`
2. Best conceptual: Steve Kinney "Hook Control Flow"
3. Best practical: paddo.dev "Hooks: Guardrails That Actually Work"

**DELETE (rehashes of above):**
- DEV Community hooks posts (rehash official docs)
- Reddit "all 23 hooks explained" (spam)
- PromptLayer hooks docs (thin rehash)
- DataCamp hooks tutorial (thin rehash)
- Kyle Redelinghuys hooks post (thin rehash)
- Dotzlaw consulting hooks (thin rehash)

---

## Ralph Wiggum / Autoresearch Loop (~15-30 sources typical) → Keep 5-6

**KEEP (canonical):**
1. `claudefa.st/blog/guide/mechanics/ralph-wiggum-technique` — best structured explainer
2. GitHub: `coleam00/ralph-loop-quickstart` — practical quickstart (NOT using Anthropic plugin variant)
3. GitHub: `harrymunro/ralph-wiggum` — specific implementation
4. `uditgoenka/autoresearch` — Claude Code-specific autoresearch
5. Kingy AI or DataCamp autoresearch explainer — conceptual backing

**DELETE (duplicate explanations):**
- All Reddit posts re-explaining the same loop concept
- "How Ralph Wiggum Changed How I Build Software" (Josh Owens) — duplicates
- ISHIR blog post — duplicates
- Awesome-ralph/README duplicates (keep the GitHub readme, not the awesome list)
- "Ralph Wiggum Breakdown" by Ibrahim Pima — duplicates
- 8+ blog posts that verbatim re-explain the same concept
- "The Ralph Wiggum Loop" multiple Reddit cross-posts

---

## Claude Code Configuration Guides (~5-8 sources) → Keep 2

**KEEP:**
1. Blake Crosley "Claude Code CLI: The Complete Guide" — best structured reference
2. Introl Blog "Claude Code CLI: The Definitive Technical Reference" — good depth

**DELETE:**
- Reddit "Complete Guide to Claude Code V2" (duplicate of above)
- "Complete Claude Code CLI Guide - Live & Auto-Updated" (GitHub, churn content)
- HackMD workflow guide (thin)
- Multiple DataCamp "best practices" posts (thin rehashes)

---

## MCP (Model Context Protocol) (~5-7 sources) → Keep 3

**KEEP:**
1. Official MCP architecture docs (`modelcontextprotocol.io/docs/learn/designitecture`)
2. Anthropic code execution with MCP
3. One vendor explainer (Neo4j or Obot)

**DELETE:**
- Duplicate MCP versioning doc
- Duplicate MCP explainer blogs

---

## LLM Reasoning / RCA Research (~2-3 sources) → Keep 1

**KEEP:** The more recent paper

**DELETE:** University of Waterloo published two nearly identical papers on LLM reasoning failures in cloud RCA. NotebookLM confirmed they share methodology and citations — keep only one.

---

## SEC/Financial Evidence Documents (~3 sources) → Keep 1

These are draft versions of the same document. Keep the most recent complete version.

---

## Generated Text Sources

**KEEP:** If NotebookLM query returns substantive synthesis (tables, original analysis, specific technical claims)

**DELETE:** If NotebookLM query returns only URL/link bibliographies with no body text

**Verification query template:**
```
Does "[SOURCE TITLE]" contain original synthesis and analysis, or is it primarily a bibliography of links? Summarize the main ideas in 2 sentences.
```
