# Advanced Chat Features

## Citations (Verify Claims in 2 Seconds)

Every claim has a reference marker. Hover to see:
- Exact quote from exact source
- Verify against original document instantly

> This traceability doesn't exist with general chatbots (training data is invisible)

## Source Filtering

Every source has a checkbox. Use for targeted queries:

1. Uncheck everything except specific sources (e.g., survey data)
2. Ask question limited to those documents
3. Get targeted answer instead of blended summary

**Example:**
```
[Checked: Internal Survey Data only]
Q: "What were the top three concerns beta users mentioned about our pricing?"
A: Response comes ONLY from survey data
```

## Save to Note -> Convert to Source

1. Click "Save to Note" on valuable answer
2. Three dots -> "Convert to Source"
3. Answer now lives alongside original documents
4. Future questions draw from your analysis + raw data

---

## Sharing and Collaboration

**Share Options** (top right share icon):

**Full Access**: Recipient can:
- Add sources
- Chat with notebook
- Modify configuration

**Chat Only**: Recipient can:
- Ask questions
- View responses
- Cannot change setup

**Benefit**: Build notebook once with proper configuration + sources -> Share with team -> Everyone pulls from same reliable setup without accidentally breaking it.

---

## Gemini Integration (Limited Use Case)

**How**: Inside Gemini -> Click "+" -> Select "NotebookLM" -> Choose notebook

**Use Case**: Quick answers when away from desk

**Trade-off**: Gemini mixes in information from its own training data
- Convenient
- Not purely source-based like NotebookLM itself

**Recommendation**: Use NotebookLM directly for critical work; Gemini integration for casual queries.
