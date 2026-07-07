---
name: video-vision
description: Let Claude actually WATCH a video — extract scene-aware deduplicated keyframes via the `crv` CLI (claude-real-video), then read the frames with vision-analysis or native vision. Use when a video's visual content (UI, diagrams, motion, on-screen text) matters beyond the transcript.
version: "1.0.0"
status: stable
enforcement: strict
category: ingestion
triggers:
  - 'video frames'
  - 'watch a video'
  - 'video keyframes'
  - 'claude-real-video'
  - 'crv video'
  - 'video vision'
aliases:
  - '/video-vision'
  - '/crv'

suggest:
  - vision-analysis
  - yt-nlm

workflow_steps:
  - Verify deps with `python scripts/crv_run.py --check` (resolves crv + ffmpeg)
  - Run `python scripts/crv_run.py <source> -o <out> [--max-frames N] [--scene 0.3] [--adaptive] [--no-transcribe]` (puts ffmpeg on PATH, then calls `crv`)
  - Read the emitted `<out>/MANIFEST.txt` (frame index + timestamps) and `<out>/transcript.txt` if present
  - Feed selected `<out>/frames/*.jpg` to vision-analysis (MiniMax understand_image) or Claude native vision, one question per frame batch
  - Synthesize what the video SHOWS (visual) with what it SAYS (transcript)

allowed_first_tools:
  - Bash
required_first_command_patterns:
  - '^python\s+.*crv_run'
required_first_command_hint: Run `python scripts/crv_run.py <source>` first — it resolves ffmpeg onto PATH (Windows PATH divergence breaks bare `crv`) and extracts frames before any visual analysis. Claude cannot see video pixels without extracted frames.

parameters:
  - name: source
    description: Video URL (YouTube/Instagram/TikTok) or local file path
    type: string
    required: true
  - name: max-frames
    description: Cap on extracted frames (default 150; lower for cheap vision passes)
    type: integer
    default: 150
  - name: scene
    description: Scene-change sensitivity 0-1, lower = more frames (default 0.30)
    type: float
    default: 0.30
  - name: no-transcribe
    description: Skip Whisper transcription (use when .vtt/.srt already exists or only frames matter)
    type: boolean
    default: false

---

# /video-vision — Let Claude watch a video

`crv` (PyPI `claude-real-video`) extracts scene-change keyframes + dedups near-identical frames + emits a timestamped transcript, so a vision-capable LLM can reason over a video instead of only its transcript. All processing is local; only the frames you choose to read enter context.

## Why this exists

Our `yt-*` skills extract **transcripts only**. `vision-analysis` reads a **single still image**. Nothing extracts video frames. When a video's value is visual (a UI walkthrough, a diagram being drawn, on-screen code, motion), the transcript alone loses it. `crv` bridges that gap.

## Dependencies

- `crv` CLI — `pip install claude-real-video` (MIT). The `[whisper]` extra is OPTIONAL; skip it when a `.vtt`/`.srt` already exists (crv detects and uses it).
- `ffmpeg` — required. crv shells out to bare `ffmpeg` via `shutil.which`, so it must be resolvable on PATH. **Do NOT call `crv` directly** — on Windows, ffmpeg is usually NOT on PATH (WinGet's Gyan.FFmpeg lands in a versioned package dir with no Links shim; crv's `imageio-ffmpeg` dep bundles a versioned-name binary crv can't see). `scripts/crv_run.py` resolves ffmpeg through PATH → WinGet → imageio-ffmpeg alias, then runs `crv`.
- `yt-dlp` — already present in this environment (crv uses it for URL sources).

Verify everything with the self-check:
```bash
python P:/packages/.claude-marketplace/plugins/cc-skills-media/skills/video-vision/scripts/crv_run.py --check
```

## Workflow

1. **Extract.** Point `crv` at a URL or local file. For a cheap first pass, cap frames:
   ```bash
   python scripts/crv_run.py "<url-or-path>" -o .claude/.artifacts/<terminal_id>/video-vision/<slug> --max-frames 30 --no-transcribe
   ```
   Use `--adaptive` for slow morphs/pans, `--grid` for a contact sheet, `--keep-audio` to retain audio.

2. **Read the manifest.** `<out>/MANIFEST.txt` lists each frame file with its timestamp — pick the frames relevant to the question rather than reading all (vision tokens are expensive).

3. **See the frames.** Read the chosen `.jpg`s:
   - Compose with `vision-analysis` (MiniMax `understand_image`) for per-image description, or
   - Use Claude's native image vision directly for "what does this frame show?"

4. **Synthesize.** Combine the visual read (frames) with the verbal read (transcript). Cite frame timestamps for visual claims.

## Composition

- After extraction, hand off per-frame description to **`/vision-analysis`** rather than reimplementing image understanding.
- For transcript-only needs (no vision), prefer **`/yt-nlm`** — cheaper, no frame extraction.
- Existing `.vtt`/`.srt` next to a local file is auto-detected by `crv`; pass `--no-transcribe` to avoid re-transcribing.

## Artifacts

Write extraction output to `.claude/.artifacts/{terminal_id}/video-vision/<slug>/` — never into the skill directory or package root (per `cc-skills-media/CLAUDE.md`).
