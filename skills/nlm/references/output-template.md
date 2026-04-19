# NotebookLM CLI Output Template

## Verification Commands

Use these exact formats for post-operation verification:

### After Adding Sources
```bash
nlm source list <nb-id> --json | python -c "
import json,sys
data = json.load(sys.stdin)
print(f'Sources: {len(data)}')
for s in sorted(data, key=lambda x: x['title']): print(f'  {s[\"title\"]}')"
```

### After Deleting a Source
```bash
nlm source list <nb-id> --json | python -c "
import json,sys
data = json.load(sys.stdin)
if any(s['id'] == '<deleted-id>' for s in data):
    print('ERROR: Source still present!')
else:
    print('Verified: Source deleted')"
```

### After Renaming
```bash
nlm source list <nb-id> --json | python -c "
import json,sys
data = json.load(sys.stdin)
matches = [s for s in data if '<search-term>' in s['title'].lower()]
for s in matches: print(f'{s[\"id\"]} {s[\"title\"]}')"
```

## Key Principles

1. **Always use `--json` flag** for verification commands - provides parseable output
2. **Parse JSON directly** - `nlm source list` returns an array, not a wrapped object
3. **Print verification results** - Show actual counts and names, not assumptions
4. **Report what happened** - Re-run GET command to confirm actual state
