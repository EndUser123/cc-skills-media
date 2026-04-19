# Gotchas — Common Failure Points

These are real problems encountered when building courses. Check every one before considering a course complete.

## Tooltip Clipping

Translation blocks use `overflow: hidden` for code wrapping. If tooltips use `position: absolute` inside the term element, they get clipped by the container. **Fix:** Tooltips must use `position: fixed` and be appended to `document.body`. Calculate position from `getBoundingClientRect()`. This is already specified in the reference files but is the #1 bug that appears in every build.

## Not Enough Tooltips

The most common failure is under-tooltipping. Non-technical learners don't know terms like REPL, JSON, flag, entry point, PATH, pip, namespace, function, class, module, PR, E2E, or even software names like Blender/GIMP. **Rule of thumb:** if a term wouldn't appear in everyday conversation with a non-technical friend, tooltip it. Err heavily on the side of too many. BUT: don't tooltip terms the user already knows well from their domain (e.g., AI/ML concepts for someone in AI).

## Walls of Text

The course looks like a textbook instead of an infographic. This happens when you write more than 2-3 sentences in a row without a visual break. Every screen must be at least 50% visual. Convert any list of 3+ items into cards, any sequence into step cards or flow diagrams, any code explanation into a code↔English translation block.

## Recycled Metaphors

Using "restaurant" or "kitchen" for everything. Every module needs its own metaphor that feels inevitable for that specific concept. If you catch yourself reaching for the same metaphor twice, stop and find one that fits the concept organically.

## Code Modifications

Trimming, simplifying, or "cleaning up" code snippets from the codebase. The learner should be able to open the real file and see the exact same code. Instead of editing code to be shorter, *choose* naturally short snippets (5-10 lines) from the codebase that illustrate the point.

## Quiz Questions That Test Memory

Asking "What does API stand for?" or "Which file handles X?" — those test recall, not understanding. Every quiz question should present a new scenario the learner hasn't seen and ask them to *apply* what they learned.

## Scroll-Snap Mandatory

Using `scroll-snap-type: y mandatory` traps users inside long modules. Always use `proximity`.

## Module Quality Degradation

Trying to write all modules in one pass causes later modules to be thin and rushed. Build one module at a time and verify each before moving on.

## Missing Interactive Elements

A module with only text and code blocks, no interactivity. Every module needs at least one of: quiz, data flow animation, group chat, architecture diagram, drag-and-drop. These aren't decorations — they're how non-technical learners actually process information.

---

# Bug Prevention Checklist

Run through every item before calling a course complete. These are real bugs found in production course HTML — each one was caught by adversarial review after the fact.

## CSS / Theme Correctness

- [ ] **CSS variable names match design tokens exactly.** The design system defines `--text-sm`, `--text-xs`, `--text-base`, etc. Typos like `var(--text-text-sm)` or `var(--color-text-smooth)` silently fall back to inherit and render at the wrong size. Search the generated HTML for `var(--` and cross-reference each name against `references/design-system.md`.
- [ ] **`prefers-color-scheme` change listener is wired.** `initTheme()` must listen for OS theme changes mid-session: `window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => applyTheme(e.matches ? 'dark' : 'light'))`. Without this, users who toggle dark/light mode while the course is open get a broken icon state.
- [ ] **`prefers-reduced-motion` is honored.** Add this block to CSS to disable all motion:
  ```css
  @media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
  }
  ```
- [ ] **Decorative SVGs have `aria-hidden="true"`.** Any SVG icon that is purely decorative (theme toggle sun/moon, etc.) must have `aria-hidden="true"` on the `<svg>` element so screen readers skip it.
- [ ] **Architecture diagram components deactivate siblings when clicked.** When a user clicks an `.arch-component` element in a diagram, the previously-active component must lose its `'active'` class before the new one gains it. Pattern:
  ```javascript
  // CORRECT — removes active from all siblings first
  document.querySelectorAll('#arch-desc-1 .arch-component').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  // WRONG — uses toggle which leaves siblings active
  el.classList.toggle('active');
  ```
- [ ] **Syntax highlighting colors are dark-mode-only.** The Catppuccin hex values (`.code-keyword`, `.code-string`, etc.) are intentionally hardcoded for dark backgrounds. Add a comment in the CSS: `/* Catppuccin Mocha palette — dark-mode-only, intentional */`. Light mode does not override these because dark-on-light code highlighting is harder to read.

## Accessibility

- [ ] **Skip-to-content link exists and is first DOM element inside `<body>`.** Keyboard users need a way to bypass the fixed nav. Pattern:
  ```html
  <a class="skip-link" href="#content">Skip to content</a>
  ```
  With CSS:
  ```css
  .skip-link { position: absolute; top: -100%; left: 0; z-index: 9999; /* ... */ transition: top 0.2s; }
  .skip-link:focus { top: 0; }
  ```
- [ ] **Quiz containers have `role="radiogroup"`.** Each `.quiz-options` container wrapping `<button>` elements acting as radio options must have `role="radiogroup"`. Individual option buttons should have `role="radio"`.

## Quiz Correctness

- [ ] **Quiz explanation objects cover ALL wrong answer keys.** The `getExplanation` function uses `exp['wrong_' + q.dataset.correct]`. If a quiz's correct answer is "c" but the explanation object only has `wrong_a` and `wrong_b`, wrong answers pick `wrong_c` which doesn't exist → silent empty string feedback. Every explanation object must have a `wrong_{letter}` key for every wrong answer letter used in the quiz.

## JavaScript Patterns

- [ ] **No unused function parameters or dead code arrays.** If a function accepts a parameter it never uses, remove it. If an array is defined but never referenced, delete it. Dead code signals incomplete implementation and confuses future maintainers.
- [ ] **`window.*` assignments are avoided for course-specific functions.** Functions like `showArchDesc`, `selectOption`, `checkQuiz`, `flowNext` should not be assigned to `window` unless needed for `onclick` HTML attributes. Use `addEventListener` with `data-*` attributes inside the IIFE instead. If `window` assignment is needed (e.g., for external HTML `onclick` wiring), document why explicitly.

## Dark Mode Completeness

- [ ] **No `inline style=` attributes for color/border on interactive elements.** Inline styles bypass CSS theming entirely — they will not respond to `[data-theme="dark"]` changes without `!important` overrides. Use CSS classes instead. If an inline `style=` with color/border is unavoidable, add a corresponding `[data-theme="dark"]` override with `!important` immediately below it.
- [ ] **`!important` overrides are minimal in dark mode.** Every `!important` in dark mode CSS is a smell — it means something upstream is using an inline style or non-CSS-variable approach. Before adding a new `!important` override, first fix the root cause (convert inline style to CSS class or CSS variable).

---

# Animation Tools — What Exists and What to Use

The self-contained constraint (only Google Fonts CDN allowed) limits external JS libraries. Here's the honest landscape:

## Popular Animation Tools (NOT suitable for self-contained HTML)

| Tool | Why It Doesn't Fit | Cost |
|------|---------------------|------|
| **Remotion** | Outputs MP4/HEVC video files, not inline HTML | Free tier + paid |
| **Rive** | Free editor, but export requires editor login | Free tier + paid |
| **Lottie** | Player is free (lottie-player web component), but creation requires After Effects | Free player, paid creation |
| **GSAP** | Now 100% free (May 2025, including all plugins), but adds ~60KB CDN dependency | Free |
| **Anime.js** | MIT licensed, ~10KB, could work as CDN include | MIT |
| **Vivus.js** | MIT licensed, ~3KB, SVG line-drawing only | MIT |

## What Works for Self-Contained HTML

**CSS + Intersection Observer (built into every course by default)**
- Scroll-triggered fade/slide reveals
- Hover state transitions
- No extra dependency

**JavaScript-powered (adds ~1-2KB inline)**
- Step-sequenced animations (animate a trace through a diagram)
- Particle/path effects using inline SVG + JS
- Tab toggles, accordion reveals, quiz feedback

**Third-party CDN libraries (optional, trade-off decision)**
- Anime.js: Versatile, ~10KB, MIT. Use if course needs complex sequenced animations beyond what CSS/JS can do cleanly.
- Vivus.js: SVG line-drawing only, ~3KB. Good for "draw this diagram" effect.

**Note on GSAP:** GSAP became 100% free in May 2025 including all plugins (ScrollTrigger, SplitText, MorphSVG). Previously had a commercial license paywall. It can be included via CDN but adds 60KB+ to the page weight. For a course that's primarily scroll-based with simple reveals, the built-in CSS approach is lighter and sufficient.

## Recommendation

Default to: CSS animations + Intersection Observer (already in the design system).

Add Anime.js or Vivus.js via CDN only if:
- The course has complex multi-step animated sequences that are hard to coordinate in raw JS
- The SVG count is high enough that hand-rolled animation code becomes spaghetti

Do NOT use Remotion, Rive, or Lottie — they produce video files, not HTML content.
