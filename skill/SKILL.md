---
name: asksancho
description: Clarifies natural-language dev requirements via a two-session scratch bridge. Reads project context (CLAUDE.md, git log, HANDOFF.md), writes a task file to ~/.claude/scratch/, then opens a companion Claude Code session via osascript. The companion session (/asksancho-clarify) runs the full 5-step AskUserQuestion dialog and writes the finished spec back to scratch. Main context stays clean.
version: "2.1.0"
---

# AskSancho — Orchestrator Skill

> **Trigger**: `/asksancho [your requirement in natural language]`
> **触发方式**: `/asksancho [用自然语言描述你的需求]`

---

## Architecture

Two-session scratch bridge. This skill is the **orchestrator** — it reads context and writes the task file. The companion skill `/asksancho-clarify` runs the interactive dialog in a fresh session where `AskUserQuestion` is available.

```
/asksancho [requirement]
        │
Phase 1: read CLAUDE.md / git log / HANDOFF.md
Phase 2: write ~/.claude/scratch/asksancho-task.md
Phase 3: open new Terminal window via osascript
Phase 4: tell user → run /asksancho-clarify in new window
        │
        ▼ (user switches to new session)
/asksancho-clarify
        │
        reads task file → AskUserQuestion dialog → writes spec
        │
        ▼ (user returns to this session)
@~/.claude/scratch/last-requirement-spec.md
```

---

## Phase 1 — Collect and compress project context

Run these commands. If a file or command is missing, skip silently — do not error.

```bash
cat CLAUDE.md 2>/dev/null | head -80
git log --oneline -8 2>/dev/null
grep -A 40 "待办\|TODO\|Next\|下一步\|Priority" HANDOFF.md 2>/dev/null | head -40
```

Compress the output into a single `<project_context>` block:

```
<project_context>
## CLAUDE.md (rules and forbidden patterns)
[paste excerpt — truncate at 800 chars if longer]

## Recent git log
[paste git log output]

## HANDOFF.md (current todos / priorities)
[paste grep output — truncate at 400 chars if longer]
</project_context>
```

If all three sources are empty, write:
```
<project_context>
No project context found. Treat this as a greenfield project with no existing constraints.
</project_context>
```

---

## Phase 2 — Write task file

Capture the working directory, then write the task file.

```bash
mkdir -p ~/.claude/scratch
pwd
```

Write to `~/.claude/scratch/asksancho-task.md` with this exact structure — substitute `{{REQUIREMENT}}` with the user's verbatim input, `{{CWD}}` with the captured working directory, and `{{PROJECT_CONTEXT}}` with the block from Phase 1:

```
---
requirement: {{REQUIREMENT}}
working_directory: {{CWD}}
---

{{PROJECT_CONTEXT}}
```

---

## Phase 3 — Open companion session

Run this command to open a new Terminal window with Claude Code in the same directory:

```bash
CWD=$(pwd) && osascript -e "tell application \"Terminal\" to do script \"cd '$CWD' && claude\""
```

- If exit 0: tell the user "New Terminal window opened."
- If exit non-zero (Linux, iTerm2, permission): tell the user "Could not auto-open a Terminal (run it manually)." Do not error out — continue to Phase 4.

---

## Phase 4 — Hand off to user

Print this message verbatim:

```
Task file written: ~/.claude/scratch/asksancho-task.md

In the new Terminal window (or open one manually in this directory):
  1. Run: /asksancho-clarify
  2. Answer the clarification questions (4–5 rounds)
  3. Return here and enter: @~/.claude/scratch/last-requirement-spec.md
```

Stop here. Do not continue until the user returns with the spec reference.

---

## Deploy

```bash
mkdir -p ~/.claude/skills/asksancho
cp skill/SKILL.md ~/.claude/skills/asksancho/SKILL.md
```
