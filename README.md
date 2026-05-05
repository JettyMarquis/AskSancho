# AskSancho

<p align="center">
  <img src="docs/asksancho.jpeg" alt="AskSancho" width="600">
</p>

<p align="center">
  <a href="README.md"><b>English</b></a> · <a href="README.zh.md">中文</a>
</p>

> *"Before you charge at windmills, make sure you know what you're charging at."*

Clarify your development requirement **before** it reaches Claude Code.

---

## The problem

Claude Code's output quality is bounded by how well you describe what you want. Most natural-language requirements have one or more of these issues:

- **No acceptance criteria** — neither you nor the model knows what "done" means
- **Fuzzy scope** — Claude quietly expands into adjacent features
- **Missing constraints** — your CLAUDE.md rules, deadlines, and compatibility requirements go unmentioned
- **Wrong model usage** — Opus 4.7 and Sonnet 4.6 need very different prompt styles

AskSancho runs a five-step clarification protocol and produces a structured spec optimized separately for Opus 4.7 and Sonnet 4.6.

---

## Use it now (no install)

Copy [`prompts/asksancho-basic.md`](prompts/asksancho-basic.md) in full, paste it into any LLM chat window, add your requirement at the end.

---

## Claude Code skill (project-aware)

```bash
mkdir -p ~/.claude/skills/asksancho ~/.claude/skills/asksancho-clarify
cp skill/SKILL.md ~/.claude/skills/asksancho/SKILL.md
cp skill/CLARIFY_SKILL.md ~/.claude/skills/asksancho-clarify/SKILL.md
```

Two skills, two sessions — main context stays clean:

**Session A** (your current session):
```
/asksancho I want to [your requirement]
```
Reads `CLAUDE.md`, `HANDOFF.md`, and recent git log → writes a task file → opens a new Terminal window automatically (macOS).

**Session B** (the new window):
```
/asksancho-clarify
```
Reads the task file → runs the full 5-step clarification dialog → writes the finished spec to `~/.claude/scratch/last-requirement-spec.md`.

**Back in Session A**:
```
@~/.claude/scratch/last-requirement-spec.md
```
Reference the spec and proceed. The clarification dialog never touched your main context.

---

## Three tiers

| | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| **What** | Standalone prompt | Claude Code skill | Local LLM app |
| **Install** | None | Copy two files | Ollama + ChromaDB |
| **Context** | None | CLAUDE.md / git log | Full vector memory |
| **Input** | Text | Text | Text / voice / image |
| **Status** | Ready | Ready | In development |

---

## License

MIT
