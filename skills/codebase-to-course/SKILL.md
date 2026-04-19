---
name: codebase-to-course
description: Turn any codebase into a beautiful, interactive single-page HTML course that teaches how the code works to non-technical people.
version: 1.0.0
status: stable
enforcement: advisory
category: education
---
# Codebase-to-Course

Transform any codebase into a stunning, interactive single-page HTML course. The output is a single self-contained HTML file (no dependencies except Google Fonts) that teaches how the code works through scroll-based modules, animated visualizations, embedded quizzes, and plain-English translations of code.

## First-Run Welcome

When the skill is first triggered and the user hasn't specified a codebase yet, introduce yourself and explain what you do:

> **I can turn any codebase into an interactive course that teaches how it works — no coding knowledge required.**
>
> Just point me at a project:
> - **A local folder** — e.g., "turn ./my-project into a course"
> - **A GitHub link** — e.g., "make a course from https://github.com/user/repo"
> - **The current project** — if you're already in a codebase, just say "turn this into a course"
>
> I'll read through the code, figure out how everything fits together, and generate a beautiful single-page HTML course with animated diagrams, plain-English code explanations, and interactive quizzes. The whole thing runs in your browser — no setup needed.

If the user provides a GitHub link, clone the repo first (`git clone <url> /tmp/<repo-name>`) before starting the analysis. If they say "this codebase" or similar, use the current working directory.

## Who This Is For

The target learner is a **"vibe coder"** — someone who builds software by instructing AI coding tools in natural language, without a traditional CS education. They may have built this project themselves (without looking at the code), or they may have found an interesting open-source project on GitHub and want to understand how it's built. Either way, they don't yet understand what's happening under the hood.

**Assume zero technical background.** Every CS concept — from variables to APIs to databases — needs to be explained in plain language as if the learner has never encountered it. No jargon without definition. No "as you probably know." The tone should be like a smart friend explaining things, not a professor lecturing.

**Their goals are practical, not academic:**
- Have enough technical knowledge to effectively **steer AI coding tools** — make better architectural and tech stack decisions
- **Detect when AI is wrong** — spot hallucinations, catch bad patterns, know when something smells off
- **Intervene when AI gets stuck** — break out of bug loops, debug issues, unblock themselves
- Build more advanced software with **production-level quality and reliability**
- Be **technically fluent** enough to discuss decisions with engineers confidently
- **Acquire the vocabulary of software** — learn the precise technical terms so they can describe requirements clearly and unambiguously to AI coding agents (e.g., knowing to say "namespace package" instead of "shared folder thing")

**They are NOT trying to become software engineers.** They want coding as a superpower that amplifies what they're already good at. They don't need to write code from scratch — they need to *read* it, *understand* it, and *direct* it.

## Why This Approach Works

This skill inverts traditional CS education. The old model is: memorize concepts for years → eventually build something → finally see the point (most people quit before step 3). This model is: **build something first → experience it working → now understand how it works.**

The learner already has context that traditional students don't — they've *used* the app, they know what it does, they may have even described its features in natural language. The course meets them where they are: "You know that button you click? Here's what happens under the hood when you click it."

Every module answers **"why should I care?"** before "how does it work?" The answer to "why should I care?" is always practical: *because this knowledge helps you steer AI better, debug faster, or make smarter architectural decisions.*

The single-file constraint is intentional: one HTML file means zero setup, instant sharing, works offline, and forces tight design decisions.

---

## The Process (4 Phases)

### Phase 1: Codebase Analysis

Before writing course HTML, deeply understand the codebase. Read all the key files, trace the data flows, identify the "cast of characters" (main components/modules), and map how they communicate. Thoroughness here pays off — the more you understand, the better the course.

**What to extract:**
- The main "actors" (components, services, modules) and their responsibilities
- The primary user journey (what happens when someone uses the app end-to-end)
- Key APIs, data flows, and communication patterns
- Clever engineering patterns (caching, lazy loading, error handling, etc.)
- Real bugs or gotchas (if visible in git history or comments)
- The tech stack and why each piece was chosen

**Figure out what the app does yourself** by reading the README, the main entry points, and the UI code. Don't ask the user to explain the product — they may not be familiar with it either. The course should open by explaining what the app does in plain language (a brief "here's what this thing does and why it's interesting") before diving into how it works. The first module should start with a concrete user action — "imagine you paste a YouTube URL and click Analyze — here's what happens under the hood."

### Phase 2: Curriculum Design

Structure the course as 5-8 modules. The arc always starts from what the learner already knows (the user-facing behavior) and moves toward what they don't (the code underneath). Think of it as zooming in: start wide with the experience, then progressively peel back layers.

| Module Position | Purpose | Why it matters for a vibe coder |
|---|---|---|
| 1 | "Here's what this app does — and what happens when you use it" | Start with the product (what it does, why it's interesting), then trace a core user action into the code. Grounds everything in something concrete. |
| 2 | Meet the actors | Know which components exist so you can tell AI "put this logic in X, not Y" |
| 3 | How the pieces talk | Understand data flow so you can debug "it's not showing up" problems |
| 4 | The outside world (APIs, databases) | Know what's external so you can evaluate costs, rate limits, and failure modes |
| 5 | The clever tricks | Learn patterns (caching, chunking, error handling) so you can request them from AI |
| 6 | When things break | Build debugging intuition so you can escape AI bug loops |
| 7 | The big picture | See the full architecture so you can make better decisions about what to build next |

Not every codebase needs all 7. A simple CLI tool might only need 4-5 modules. A microservices app might need 8. Adapt the arc to the codebase's complexity — use your judgment on which modules are worth including based on what would actually help the learner steer AI and debug better.

**The key principle:** Every module should connect back to a practical skill — steering AI, debugging, making decisions. If a module doesn't help the learner DO something better, cut it or reframe it until it does.

**Each module should contain:**
- 3-6 screens (sub-sections that flow within the module)
- At least one code-with-English translation
- At least one interactive element (quiz, visualization, or animation)
- One or two "aha!" callout boxes with universal CS insights
- A metaphor that grounds the technical concept in everyday life — but NEVER reuse the same metaphor across modules, and NEVER default to the "restaurant" metaphor (it's overused). Pick metaphors that organically fit the specific concept. The best metaphors feel *inevitable* for the concept, not forced.

**Do NOT present the curriculum for approval — just build it.** The user wants a course, not a planning document. Design the curriculum internally, then go straight to generating the HTML. If they want changes, they'll tell you after seeing the result.

### Phase 3: Build the Course

Generate a single HTML file with embedded CSS and JavaScript. Read `references/design-system.md` for the complete CSS design tokens, typography, and color system. Read `references/interactive-elements.md` for implementation patterns of every interactive element type.

**Build order (task by task):**

1. **Foundation first** — HTML shell with all module sections (empty), complete CSS design system, navigation bar with progress tracking, scroll-snap behavior, keyboard navigation, and scroll-triggered animations. After this step, you should have a working skeleton you can scroll through.

2. **One module at a time** — Fill in each module's content, code translations, and interactive elements. Don't try to write all 8 modules in one pass — the quality drops. Build Module 1, verify it works, then Module 2, etc.

3. **Polish pass** — After all modules are built, do a final pass for transitions, mobile responsiveness, and visual consistency.

4. **Bug Prevention verification** — Before declaring the course complete, work through every item in `references/gotchas-and-qa.md`. This is not optional — these are real bugs found in shipped course HTML that simple checklists would have caught.

**Critical implementation rules:**
- The file must be completely self-contained (only external dependency: Google Fonts CDN)
- Use CSS `scroll-snap-type: y proximity` (NOT `mandatory` — mandatory traps users in long modules)
- Use `min-height: 100dvh` with `100vh` fallback for sections
- Only animate `transform` and `opacity` for GPU performance
- Wrap all JS in an IIFE, use `passive: true` on scroll listeners, throttle with `requestAnimationFrame`
- Include touch support for drag-and-drop, keyboard navigation (arrow keys), and ARIA attributes

### Phase 4: Review and Open

After generating the course HTML file, open it in the browser for the user to review. Walk them through what was built and ask for feedback on content, design, and interactivity.

---

## Content Philosophy

These principles are what separate a great course from a generic tutorial. They should guide every content decision.

### Show, Don't Tell -- Aggressively Visual

People's eyes glaze over text blocks. The course should feel closer to an infographic than a textbook.

**Text limits:**
- Max **2-3 sentences** per text block. If you're writing a fourth sentence, stop and convert it into a visual instead.
- Every screen must be **at least 50% visual** (diagrams, code blocks, cards, animations, badges).

**Convert text to visuals:**
- A list of 3+ items -> **cards with icons**
- A sequence of steps -> **flow diagram with arrows** or **numbered step cards**
- "Component A talks to Component B" -> **animated data flow** or **group chat visualization**
- Explaining what code does -> **code-English translation block** (not a paragraph *about* the code)
- Comparing two approaches -> **side-by-side columns** with visual contrast

**Visual breathing room:**
- Use generous spacing between elements (`--space-8` to `--space-12`)
- Every module should have at least one "hero visual" -- a diagram, animation, or interactive element that dominates the screen and teaches the core concept at a glance

### Code-English Translations

Every code snippet gets a side-by-side plain English translation. Left panel: real code with syntax highlighting. Right panel: line-by-line plain English.

**Critical rules:**
- No horizontal scrollbars on code. Use `white-space: pre-wrap` so code wraps.
- Use original code exactly as-is. Never modify, simplify, or trim code snippets. Choose naturally short snippets (5-10 lines) that illustrate the concept well.

### Metaphors First, Then Reality

Introduce every new concept with a metaphor from everyday life. Then immediately ground it: "In our code, this looks like..."

**No recycled metaphors.** Do NOT default to "restaurant" for everything. Each concept deserves its own metaphor that feels natural to *that specific idea*. A database is a library with a card catalog. Auth is a bouncer checking IDs. An event loop is an air traffic controller. If you catch yourself using "restaurant" or "kitchen" more than once in a course, stop and rethink.

### Glossary Tooltips -- No Term Left Behind

Every technical term gets a dashed-underline tooltip on first use in each module. 1-2 sentence plain-English definition on hover (desktop) or tap (mobile).

**Be extremely aggressive with tooltips.** If there is even a 1% chance a non-technical person doesn't know a word, tooltip it. This includes: software names (Blender, GIMP), developer terms (REPL, JSON, flag, CLI, API), programming concepts (function, variable, class), infrastructure terms (PATH, pip, namespace), and all acronyms.

**The vocabulary IS the learning.** Each tooltip should teach the term in a way that helps the learner USE it -- e.g., "A **flag** is an option you add to a command to change its behavior. When talking to AI, you'd say 'add a flag for verbose output.'"

**Cursor:** Use `cursor: pointer` on terms (not `cursor: help`).

**Tooltip overflow fix:** Tooltips must use `position: fixed` and be appended to `document.body`. Calculate position from `getBoundingClientRect()`. This prevents clipping by containers with `overflow: hidden`.

### Quizzes That Test Application, Not Memory

**What to quiz (in order of value):**
1. **"What would you do?" scenarios** -- "You want to add a 'save to favorites' feature. Which files would you need to change?"
2. **Debugging scenarios** -- "A user reports X is broken. Where would you look first?"
3. **Architecture decisions** -- "Would you put this logic in the frontend or backend? Why?"
4. **Tracing exercises** -- "When a user does X, trace the path the data takes."

**What NOT to quiz:** Definitions, file name recall, syntax details, or anything answerable by scrolling up.

**Quiz tone:** Encouraging, non-judgmental. Wrong answers get explanations that teach something new. No scores.

**How many:** One per module, 3-5 questions, placed at the end after all content.

See `references/content-philosophy.md` for expanded guidelines including learn-by-tracing, memorable callouts, and detailed quiz tone rules.

---

## Design Identity

The visual design should feel like a **beautiful developer notebook** — warm, inviting, and distinctive. Read `references/design-system.md` for the full token system, but here are the non-negotiable principles:

- **Warm palette**: Off-white backgrounds (like aged paper), warm grays, NO cold whites or blues
- **Bold accent**: One confident accent color (vermillion, coral, teal — NOT purple gradients)
- **Distinctive typography**: Display font with personality for headings (Bricolage Grotesque, or similar bold geometric face — NEVER Inter, Roboto, Arial, or Space Grotesk). Clean sans-serif for body (DM Sans or similar). JetBrains Mono for code.
- **Generous whitespace**: Modules breathe. Max 3-4 short paragraphs per screen.
- **Alternating backgrounds**: Even/odd modules alternate between two warm background tones for visual rhythm
- **Dark code blocks**: IDE-style with Catppuccin-inspired syntax highlighting on deep indigo-charcoal (#1E1E2E)
- **Depth without harshness**: Subtle warm shadows, never black drop shadows

---

## Gotchas -- Common Failure Points

These are real problems encountered when building courses. Check every one before considering a course complete.

**Tooltip Clipping** -- The #1 recurring bug. Translation blocks use `overflow: hidden`. Tooltips MUST use `position: fixed` appended to `document.body`, positioned via `getBoundingClientRect()`. Never use `position: absolute` inside the term element.

**Not Enough Tooltips** -- The most common failure. If a term wouldn't appear in everyday conversation with a non-technical friend, tooltip it. Err heavily on the side of too many.

**Walls of Text** -- Every screen must be at least 50% visual. If you're writing more than 2-3 sentences without a visual break, stop and convert to a visual element.

**Recycled Metaphors** -- Every module needs its own metaphor. If you catch yourself using "restaurant" or "kitchen" twice, stop and find a better fit.

**Code Modifications** -- Never trim, simplify, or "clean up" code snippets. Choose naturally short ones (5-10 lines) instead.

**Quiz Questions That Test Memory** -- Every quiz question should present a new scenario and ask the learner to *apply* what they learned. No definition recall.

**Scroll-Snap Mandatory** -- Using `scroll-snap-type: y mandatory` traps users. Always use `proximity`.

**Module Quality Degradation** -- Build one module at a time, verify each before moving on. Writing all modules in one pass causes later modules to be thin and rushed.

**Missing Interactive Elements** -- Every module needs at least one of: quiz, data flow animation, group chat, architecture diagram, or drag-and-drop.

**See `references/gotchas-and-qa.md`** for the full bug prevention checklist (CSS correctness, accessibility, quiz correctness, JS patterns, dark mode completeness).

---

## Animation Tools

The self-contained constraint (only Google Fonts CDN allowed) limits external JS libraries.

**What works for self-contained HTML:**
- **CSS + Intersection Observer** (built in, no extra dependency) -- scroll-triggered fade/slide reveals, hover transitions
- **JavaScript-powered** (~1-2KB inline) -- step-sequenced animations, particle/path effects, tab toggles, quiz feedback
- **Anime.js** (~10KB CDN, MIT) -- complex sequenced animations beyond what CSS/JS can do cleanly
- **Vivus.js** (~3KB CDN, MIT) -- SVG line-drawing "draw this diagram" effect only

**What does NOT work:**

| Tool | Why Not |
|------|---------|
| **Remotion** | Outputs video files, not inline HTML |
| **Rive** | Export requires editor login |
| **Lottie** | Creation requires After Effects |
| **GSAP** | 100% free but adds 60KB+ CDN weight; overkill for scroll-based courses |

**Default to:** CSS animations + Intersection Observer. Add Anime.js or Vivus.js via CDN only for complex multi-step sequences or high SVG counts. Do NOT use Remotion, Rive, or Lottie.

See `references/gotchas-and-qa.md` for expanded trade-off analysis.

---

## Reference Files

The `references/` directory contains detailed implementation specs. Read them when you reach the relevant phase:

| File | When to Read | Contents |
|------|-------------|----------|
| `references/design-system.md` | Before writing CSS | Complete CSS custom properties, color palette, typography scale, spacing, shadows, animations |
| `references/interactive-elements.md` | Before building interactive elements | Implementation patterns for quizzes, translations, group chats, flow diagrams, architecture diagrams, pattern cards |
| `references/content-philosophy.md` | Before writing content | Visual rules, code translation guidelines, metaphor constraints, tooltip implementation, quiz design |
| `references/gotchas-and-qa.md` | Before declaring complete | Common failure points, bug prevention checklist (CSS, accessibility, quiz, JS, dark mode), animation tools comparison |
