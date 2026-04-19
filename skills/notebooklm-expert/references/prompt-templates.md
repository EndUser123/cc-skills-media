# NotebookLM Prompt Templates & Examples

## Deep Research Prompt Template

```
Research [topic] for [context].
Focus on: [source types to include]
Exclude: [source types to avoid]
```

**Example:**
```
Research product launch strategies for B2B SaaS companies.
Focus on: industry reports, case studies, consulting firm data
Exclude: blog posts, opinion pieces, listicles
```

## Contradiction Check Prompt

```
Are there any contradictions or conflicting data points across my sources?
```

**Example output:**
- Report A: "Enterprise pricing: $20,000-$250,000 annually"
- Report B: "Average enterprise contract: $75,000-$250,000 annually"

## Custom Role Templates

### Product Marketing
```
Act as a product marketing strategist preparing a B2B SaaS launch.
Prioritize: competitive positioning, messaging clarity, pricing sensitivity, go-to-market sequencing
```

### User Research
```
Act as a user researcher analyzing customer feedback.
Focus on: pain points, feature requests, usability patterns, sentiment trends
```

### Getting Role Suggestions from NotebookLM

Not sure how to phrase your custom role? Ask before configuring:
```
Based on the sources in this notebook, suggest three custom roles I should configure for the most useful responses
```

NotebookLM will analyze your documents and recommend roles matching the content.

## ACG Workflow Prompts

### Analyze
```
What are the key insights about [topic] based on my sources?
```

### Challenge
```
What are the weakest assumptions in this analysis?
Which claims have the least supporting evidence?
```

### Gap
```
What's missing from my sources?
What topics or data points would I need to make this analysis complete?
```

## Before vs After Configuration

**Before Config**:
```
Q: "What are the strongest positioning angles for our launch?"
A: Five generic angles applicable to any SaaS product in any market
```

**After Config** (with custom role):
```
Q: "What are the strongest positioning angles for our launch?"
A: Specific angles pulling from actual competitor weaknesses in your sources,
   connected to beta user feedback, tailored to your market context
```

## Audio Overview Focus Instructions

```
Focus on whether our pricing model is competitive enough based on market data.
Challenge any assumptions in the beta user feedback.
```

## Data Table Prompt Template

```
Create a comparison table of all [items] with columns for:
- [Column 1]
- [Column 2]
- [Column 3]
- Biggest weakness mentioned in my sources
```

**Example:**
```
Create a comparison table of all three competitors with columns for:
- Pricing tiers
- Free trial length
- Onboarding support
- Biggest weakness mentioned in my sources
```
