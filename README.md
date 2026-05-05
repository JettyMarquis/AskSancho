# AskSancho

> *"Before you charge at windmills, make sure you know what you're charging at."*

**AskSancho** is a three-tier workflow that clarifies natural-language development requirements before they reach Claude Code — so the AI builds the right thing the first time.

---

## Why

The quality ceiling of Claude Code is the clarity of your requirement. Natural-language requests typically suffer from:

- **No acceptance criteria** — neither you nor the model knows when "done" is done
- **Fuzzy scope** — Claude silently expands into adjacent territory
- **Missing constraints** — CLAUDE.md rules, timing, compatibility requirements go unmentioned
- **Wrong model framing** — Opus 4.7 and Sonnet 4.6 need fundamentally different prompt styles

AskSancho uses a five-step clarification protocol to fix all of this *before* the spec hits Claude Code, and produces separate optimized prompts for Opus 4.7 and Sonnet 4.6.

---

## Three Tiers

### Tier 1 — Basic (zero install, any LLM)

Copy `prompts/asksancho-basic.md` in full, paste into any LLM chat window (Claude.ai, ChatGPT, local Gemma, etc.), append your requirement at the bottom, and start the conversation.

The five-step protocol runs:
1. **Restate** — model echoes the requirement back for confirmation
2. **Disambiguate** — one ambiguity at a time, most impactful first
3. **Probe** — surfaces four commonly omitted categories (acceptance criteria, out-of-scope, edge cases, failure behavior)
4. **Consolidate** — final check before output
5. **Output** — structured spec with model-specific hints

See `examples/example-session.md` for a worked example.

---

### Tier 2 — Claude Code Skill (project-aware)

Deploy:
```bash
mkdir -p ~/.claude/skills/asksancho
cp skill/SKILL.md ~/.claude/skills/asksancho/SKILL.md
```

Trigger inside any Claude Code session:
```
/asksancho [your requirement in natural language]
```

The skill reads lightweight project context (CLAUDE.md, HANDOFF.md, git log) before asking clarifying questions, then produces a structured spec with a **Code references** section populated from actual project files. Three handoff options: plan mode, clipboard output, or file bridge (`~/.claude/scratch/last-requirement-spec.md`).

---

### Tier 3 — Local LLM middleware (in development)

A local FastAPI application backed by Gemma 4 (via Ollama) and ChromaDB vector memory. Accepts text, voice (whisper.cpp), and image input. Automatically injects the refined spec into Claude Code.

Development status: architecture document complete, implementation planned in five phases. See `core/` and `docs/advanced-tier-architecture.md`.

---

## Spec Template (all tiers)

```
## Goal
## In scope
## Out of scope
## Inputs / Outputs
## Constraints
## Acceptance criteria
## Open questions for Claude Code
## Code references          <- Tier 2 / Tier 3 only
```

---

## Repository Structure

```
AskSancho/
├── LICENSE
├── README.md
├── prompts/
│   └── asksancho-basic.md      <- Tier 1 meta-prompt (copy and use directly)
├── examples/
│   └── example-session.md      <- Full worked example session
├── skill/
│   └── SKILL.md                <- Tier 2 Claude Code skill
├── core/                       <- Tier 3 backend (in development)
│   ├── collector.py            <- Claude Code transcript collector (implemented)
│   ├── indexer.py              <- Project file vectorizer (TODO Phase A)
│   ├── refiner.py              <- Gemma 4 refiner (TODO Phase B)
│   └── injector.py             <- Claude Code injection bridge (TODO Phase E)
├── ui/
│   └── index.html              <- Tier 3 frontend (TODO Phase C)
├── app.py                      <- FastAPI entry point (TODO Phase C)
└── dist/
    └── req-refiner-spec-v1.0.0.docx   <- Design specification document
```

---

## Quick Start

**No install needed.** Open `prompts/asksancho-basic.md`, copy everything, paste into any LLM chat window, add your requirement at the end.

---

## License

MIT -- see [LICENSE](LICENSE).
