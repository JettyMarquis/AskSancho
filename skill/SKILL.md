---
name: asksancho
description: Clarifies natural-language development requirements through structured dialogue. Reads lightweight project context (CLAUDE.md, git log, HANDOFF.md), runs an interactive clarification dialog, then produces a structured spec with dual-model prompts (Opus 4.7 + Sonnet 4.6).
version: "1.0.0"
---

# AskSancho — Claude Code Skill

> **Trigger**: `/asksancho [your requirement in natural language]`
> **Output**: structured spec ready for plan mode or copy-paste

---

## Step 1: Read lightweight context

Read the following in order (skip silently if missing):

```bash
# 1. Project rules
cat CLAUDE.md 2>/dev/null | head -80

# 2. Recent work direction
git log --oneline -10 2>/dev/null

# 3. Current todos
grep -A 20 "待办\|TODO\|Next\|下一步" HANDOFF.md 2>/dev/null | head -30
```

**Constraint**: no glob, no source file reads — only these three sources.

---

## Step 2: Context-aware clarification

Use `AskUserQuestion` for up to **2 rounds** of clarification (max 4 questions per round).

**Question principles**:
- If the requirement touches a Mandatory rule in CLAUDE.md, flag it explicitly
- If it overlaps with a recent git commit, note the connection
- Always ask: **acceptance criteria** and **what must not change** (most commonly omitted)

**Standard question set** (when no strong context signal):
1. What specific change will you or the system observe when this is done? How do you verify?
2. What files or behaviors are absolutely off-limits?
3. Any known technical constraints? (dependencies, compatibility, performance)
4. One-shot change or a repeatable mechanism?

---

## Step 3: Boundary confirmation

Before entering plan mode, output a requirement summary and ask for confirmation:

```
[Summary]
Goal: [one sentence]
Acceptance criteria: [1-3 verifiable conditions]
Must not touch: [list]
Constraints: [list]
Out of scope: [explicit exclusions]
```

Ask: **"Does this look right? I'll generate the execution plan once confirmed."**

---

## Step 4: Enter plan mode, generate structured spec

Call `EnterPlanMode` and write:

```markdown
# Context

[Why this requirement — 1-2 sentences on problem or motivation]

---

## Requirement boundaries

| | Content |
|---|---|
| Goal | [one sentence] |
| Acceptance criteria | [list, verifiable] |
| Must not touch | [list] |
| Constraints | [list] |
| Out of scope | [list] |

## Code references

[Files / functions from Step 1 context — only list confirmed relevant ones]

---

## FOR OPUS 4.7

[Longer prompt: includes "why" background, known constraints, quality gate, open to alternative approaches]

---

## FOR SONNET 4.6

[Concise prompt: no ambiguity, ordered task list, explicit verification command, no discretionary decisions]

---

## Verification

[End-to-end verification: what command to run / what output = success]
```

---

## Step 5: ExitPlanMode

Once approved, the plan file is the complete context for the next task. Paste the `FOR OPUS 4.7` or `FOR SONNET 4.6` section directly into a new session.

---

## Deploy

```bash
mkdir -p ~/.claude/skills/asksancho
cp skill/SKILL.md ~/.claude/skills/asksancho/SKILL.md
```

Then `/asksancho` is available in any Claude Code session.
