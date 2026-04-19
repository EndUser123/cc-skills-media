---
name: notebooklm-expert
description: Expert guide to building high-quality NotebookLM notebooks with the 4-step framework: Source Selection, Configuration, ACG Workflow, and Studio Outputs
version: 1.0.0
status: stable
author: NotebookLM Expert
category: productivity
tags: [notebooklm, research, documentation, ai-workflow, knowledge-management]
triggers:
  - "notebooklm setup"
  - "build a notebook"
  - "notebook lm sources"
  - "acg workflow"
  - "notebooklm configuration"
parameters:
  transcript_processing:
    enabled: true
    source_quality: high
  workflow_steps:
    - source_selection
    - configuration
    - acg_workflow
    - studio_outputs
---

# NotebookLM Expert

Master the 4-step framework for building high-quality NotebookLM notebooks that deliver actionable insights instead of generic summaries.

## The Core Principle

**Quality is decided before you type a single prompt.** NotebookLM uses ONLY sources you provide -- every answer comes exclusively from your documents. The quality of inputs directly controls the quality of outputs.

---

## Step 1: Strategic Source Selection

### The Common Mistake
Dumping a handful of PDFs into a "junk folder" and starting to chat produces vague summaries from unchecked information.

### The Right Approach
Every source should be already read/reviewed, credible, and purposefully chosen for the notebook's goal.

### Source Mix Strategy
Aim for **diverse source types**, not multiple of the same type:
- **Market research** -> Big picture context
- **Competitor pages** -> Positioning insights
- **Internal data** -> Audience-specific information
- **Firsthand accounts** -> Direct stakeholder input

> 8 diverse sources > 8 documents of the same type

### Built-in Research Tools

| Tool | Scope | Use For |
|------|-------|---------|
| Fast Research | Quick scan, handful of links | Initial exploration |
| Deep Research | Hundreds of pages, detailed report | Thorough source gathering |

For Deep Research, always specify source types in your prompt (see `references/prompt-templates.md`).

### Quality Gate: Contradiction Check

Before moving to step 2, ask NotebookLM to flag any conflicting data across sources. Catching contradictions before analysis prevents embarrassing stakeholder moments.

---

## Step 2: Notebook Configuration (30 Seconds That Changes Everything)

Click **"Configure Notebook"** to access two critical settings:

### Setting 1: Conversational Goal

| Option | Best For |
|--------|----------|
| Default | General-purpose (generic) |
| Learning Guide | Educational content |
| **Custom** | **Define exact role (recommended)** |

For custom role templates and before/after examples, see `references/prompt-templates.md`.

### Setting 2: Response Length

- **Shorter**: Daily briefings, highlights only
- **Longer**: Research, analysis, detailed breakdowns (recommended for most work)

---

## Step 3: ACG Workflow (Analyze -> Challenge -> Gap)

First drafts have blind spots. The ACG workflow catches them.

| Step | Purpose | Key Question |
|------|---------|--------------|
| **A**nalyze | Pull insights from sources | What are the key insights about [topic]? |
| **C**hallenge | Critique the output | What are the weakest assumptions? Which claims lack evidence? |
| **G**ap | Find what's missing | What topics/data would make this analysis complete? |

For detailed prompt templates and example outputs, see `references/prompt-templates.md`.

### The Compound Effect Loop

1. Run ACG workflow
2. Save best answers as notes
3. **Critical step**: Click note -> "Convert to Source"
4. Next round of questions automatically better (more context)

---

## Step 4: Studio Outputs (From Conversation to Deliverables)

Access Studio via the right panel (toggle "Studio" if not visible).

| Output Type | Best For | Time |
|-------------|----------|------|
| **Audio Overview** | Commute prep, hearing your data debated | ~5 min |
| **Reports** | Briefing docs, playbooks, executive summaries | ~90 sec |
| **Data Tables** | Structured comparisons, export to Sheets | ~1 min |

For detailed usage instructions for each output type, see `references/studio-outputs.md`.

---

## Quick Reference Checklist

### Starting a New Notebook

**Step 1: Sources**
- [ ] Select only verified, credible sources
- [ ] Mix source types (market research, competitors, internal data, firsthand accounts)
- [ ] Use Deep Research with specific inclusions/exclusions
- [ ] Run contradiction check before proceeding

**Step 2: Configuration**
- [ ] Set Conversational Goal to "Custom"
- [ ] Write specific role with priorities
- [ ] Set Response Length to "Longer" for analysis work

**Step 3: ACG Workflow**
- [ ] **A**nalyze: Pull insights from sources
- [ ] **C**hallenge: Identify weak assumptions and unsupported claims
- [ ] **G**ap: Find missing topics/data points
- [ ] Save best answers -> Convert to Source
- [ ] Repeat as notebook strengthens

**Step 4: Studio Outputs**
- [ ] Audio Overview: Use pencil icon -> Select format + Add focus instruction
- [ ] Reports: Choose preset or create custom for deliverables
- [ ] Data Tables: Export structured comparisons to Sheets

### Before Stakeholder Meetings

- [ ] Listen to Audio Overview (commute preparation)
- [ ] Generate Briefing Doc with execution checklist
- [ ] Create comparison tables for key metrics
- [ ] Run Challenge prompt to pre-empt stakeholder questions
- [ ] Verify all claims with citations

---

## Common Pitfalls

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Dumping unverified sources | Vague, unreliable outputs | Select only read/reviewed sources |
| Skipping configuration | Generic, reusable answers | Always set custom role + response length |
| One-and-done querying | First drafts with blind spots | Run full ACG workflow repeatedly |
| Ignoring contradictions | Embarrassing stakeholder moments | Run contradiction check before analysis |
| Not converting notes to source | Linear improvement only | Compound knowledge by converting insights |
| Default audio overview | Unfocused content | Always use pencil icon + focus instruction |
| Blended source queries | Untargeted answers | Use checkboxes to isolate sources |

---

## Key Takeaways

1. **Source quality > Source quantity**: 8 diverse, verified sources > 50 unchecked documents
2. **Configuration is mandatory**: 30 seconds that changes generic -> specific
3. **ACG is iterative**: Run repeatedly, convert notes to sources, compound knowledge
4. **Studio for deliverables**: Don't manually build what Studio generates in 90 seconds
5. **Citations are your safety net**: Verify any claim in 2 seconds before presenting

---

## References

| File | Contents |
|------|----------|
| `references/prompt-templates.md` | Deep Research prompts, custom role templates, ACG prompts, before/after examples |
| `references/studio-outputs.md` | Audio Overview, Reports, and Data Tables detailed usage |
| `references/advanced-features.md` | Citations, source filtering, save-to-source, sharing, Gemini integration |
| `references/end-to-end-workflow.md` | Full Day 1-4 product launch workflow example |
