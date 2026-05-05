# Example Session — AskSancho Basic

> **Language / 语言**: [English](example-session.md) · [中文](example-session.zh.md)

This example shows the five-step protocol applied to a real, vague requirement.

---

## User's Original Input

> The flashcards are out of order. I want them sorted by KP number.

---

## S1 — Restate

You want to re-sort the entries in `flashcard_data.json` so they follow canonical KP order — Domain → Topic → Subtopic → sequence number — and have that order reflected in the UI after `inject_html.py` runs. **Is that right?**

*User confirms: Yes, exactly.*

---

## S2 — Three Core Questions

**1. Acceptance criteria** — what will you observe when this is done?

> Open the flashcard screen and KP-I-A-1-001 is first. Order within a domain goes topic alphabetically → subtopic numerically → KP sequence number. Domain order is I → II → III → IV → X.

**2. Must not touch** — what is absolutely off-limits?

> Card content fields (question / answer / kp / related_kps) must not change. Only the order. After `inject_html.py` runs, the HTML order must match the JSON.

**3. Known constraints**

> Sorting must happen before `inject_html.py` runs. The frontend does not sort — it reads order directly from the injected HTML.

---

## S3 — Intent Expansion

This is a data change task. Two things worth confirming:

- **One-shot or repeatable?** Your CLAUDE.md has a rule "Sort flashcard_data.json after every append" — should this be packaged as a reusable script rather than a one-time fix?
- **Domain X placement?** Should KP-X-\* entries sort last (X=10) or alphabetically among the domains?

*User: Package it as a script. X goes last.*

---

## S4 — Scope Confirmation

```
[Summary]
Goal: Sort flashcard_data.json by canonical KP order; package as a reusable script.

Acceptance criteria:
  1. After running the script, entries are ordered KP-I < KP-II < KP-III < KP-IV < KP-X
  2. Within a domain: topic alphabetically → subtopic numerically → sequence number ascending
  3. After inject_html.py runs, flashcard order in the HTML matches the JSON

Must not touch: question / answer / kp / related_kps field values — order only

Constraints:
  - Script runs before inject_html.py
  - Frontend does not sort; depends entirely on JSON order
  - Domain X always last

Out of scope:
  - No changes to frontend rendering logic
  - No changes to inject_html.py itself (only call it after sorting)
  - No handling of malformed kp fields (assumed compliant)
```

**Does this look right? Anything to adjust?**

*User confirms: Accurate, proceed.*

---

## S5 — Dual-Model Output

---

**=== FOR OPUS 4.7 ===**

Implement canonical KP-order sorting for `data/flashcard_data.json`.

**Background**: The project uses a data-drop + inject architecture — JSON is the single source of truth, `inject_html.py` writes to HTML in JSON order, and the frontend renders that order directly. New cards are always appended, so KP order degrades over time and no longer reflects the knowledge structure users expect.

**Requirement**: Package the sort as a standalone, idempotent script `data/sort_flashcards.py` that can be run after every append.

**Sort key** (KP format: `KP-{Domain}-{Topic}-{Subtopic}-{NNN}`):
- Domain priority: I=1, II=2, III=3, IV=4, X=10 (X always last)
- Within domain: topic alphabetically → subtopic numerically → NNN ascending
- Card content fields (question/answer/kp/related_kps) must not be modified

**Constraints**:
- Update `flashcard_data.json` in-place; no new output file
- Warn on malformed kp fields but do not abort
- Script output should be ready to pipe directly into inject_html.py

**Quality gate**: Before considering this done — (1) verify idempotency (run twice, result identical), (2) spot-check first 5 and last 5 cards for correct domain order, (3) check whether the CLAUDE.md "Sort flashcard_data.json" Mandatory rule needs updating.

---

**=== FOR SONNET 4.6 ===**

Implement `data/sort_flashcards.py` and integrate it into the development workflow.

**Ordered task list:**

1. Create `data/sort_flashcards.py`:
   - Read `data/flashcard_data.json`
   - Sort by: domain (I=1, II=2, III=3, IV=4, X=10) → topic alphabetically → subtopic numerically → KP sequence number
   - Write back in-place with `ensure_ascii=False`, `indent=2`
   - Print a warning for any malformed kp field; do not abort

2. Verify sort correctness:
   ```bash
   python data/sort_flashcards.py
   python -c "import json; d=json.load(open('data/flashcard_data.json')); print([c['kp'] for c in d[:5]])"
   ```
   Expected: first 5 entries all start with `KP-I-`, in ascending alpha/numeric order.

3. Add one comment line to the top of `data/inject_html.py`:
   `# Run sort_flashcards.py first if flashcards were appended.`
   Do not modify any logic.

4. Final verification:
   ```bash
   python data/sort_flashcards.py && python data/inject_html.py --tier full
   ```
   Confirm inject completes without errors.

**Constraint**: Do not modify the value of any question/answer/kp/related_kps field — order only.
