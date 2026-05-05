# AskSancho

> *"Before you charge at windmills, make sure you know what you're charging at."*

Clarify your development requirement **before** it reaches Claude Code.

---

## The problem

Claude Code's output quality is bounded by how well you describe what you want. Most natural-language requirements are missing acceptance criteria, have fuzzy scope, or don't account for existing project constraints. The result is rework.

AskSancho runs a five-step clarification dialog and produces a structured spec — with separate versions for Opus 4.7 and Sonnet 4.6.

---

## Use it now (no install)

Copy [`prompts/asksancho-basic.md`](prompts/asksancho-basic.md) in full, paste it into any LLM chat window, add your requirement at the end.

---

## Claude Code skill (project-aware)

```bash
mkdir -p ~/.claude/skills/asksancho
cp skill/SKILL.md ~/.claude/skills/asksancho/SKILL.md
```

Then in any Claude Code session:

```
/asksancho I want to [your requirement]
```

The skill reads your `CLAUDE.md`, `HANDOFF.md`, and recent git log before asking questions, so clarifications are grounded in your actual project context.

---

## Tiers

| | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| **What** | Standalone prompt | Claude Code skill | Local LLM app |
| **Install** | None | Copy one file | Ollama + ChromaDB |
| **Context** | None | CLAUDE.md / git log | Full vector memory |
| **Input** | Text | Text | Text / voice / image |
| **Status** | Ready | Ready | In development |

---

## License

MIT
