---
name: req-refine
description: Requirement clarification skill for Claude Code. Reads lightweight project context (CLAUDE.md, git log, HANDOFF.md), runs an interactive clarification dialog, then produces a structured plan file with dual-model prompts (Opus 4.7 + Sonnet 4.6).
version: "1.0.0"
---

# Requirement Refiner — Claude Code Skill

> **触发**: `/req-refine [自然语言需求]`
> **产出**: 结构化需求 plan 文件，直接可作为下一个任务执行

---

## Step 1: 读取轻量上下文

按顺序读取以下内容（任一不存在则跳过，不报错）：

```bash
# 1. 项目规则
cat CLAUDE.md 2>/dev/null | head -80

# 2. 最近工作方向
git log --oneline -10 2>/dev/null

# 3. 当前待办
grep -A 20 "待办\|TODO\|Next\|下一步" HANDOFF.md 2>/dev/null | head -30
```

**约束**：不 glob 代码文件，不读取源码，只读这三个来源。

---

## Step 2: 上下文感知的澄清环

基于读取的上下文，用 `AskUserQuestion` 进行最多 **2 轮**澄清（每轮最多 4 个问题）。

**问题生成原则**：
- 如果需求涉及 CLAUDE.md 中的 Mandatory 规则，主动点出（例："这个改动会触及 tier/lock 系统，确认 L-14–L-18 的约束都满足吗？"）
- 如果需求与最近 git commit 相关，指出关联（例："上一个 commit 刚修改了 inject_html.py，这次需求是否与其相关？"）
- 始终问：**成功标准** 和 **绝对不改的东西**（这两项最常被遗漏）

**标准澄清问题套组**（在无明显上下文关联时使用）：
1. 完成后会看到什么具体变化？如何验证？
2. 有哪些文件或行为绝对不能改动？
3. 有已知的技术约束吗？（依赖、兼容性、性能）
4. 这是一次性改动还是需要可重复运行的机制？

---

## Step 3: 边界确认

在进入 plan mode 前，输出需求摘要并确认：

```
【需求摘要】
目标：[一句话]
成功标准：[1–3条可验证的条件]
绝对不改：[列出]
约束：[列出]
OUT OF SCOPE：[明确排除项]
```

问用户："**以上准确吗？确认后我将生成执行计划。**"

---

## Step 4: 进入 Plan Mode，生成结构化需求文件

调用 `EnterPlanMode`，在 plan 文件中写入以下内容：

```markdown
# Context

[为什么做这个需求 — 1–2 句话，说明问题或动机]

---

## 需求边界

| | 内容 |
|---|---|
| 目标 | [一句话] |
| 成功标准 | [列出，可验证] |
| 绝对不改 | [列出] |
| 约束 | [列出] |
| OUT OF SCOPE | [列出排除项] |

---

## FOR OPUS 4.7

[较长提示词：含"为什么"背景、已知约束、质量门控、允许推理替代方案]

---

## FOR SONNET 4.6

[精简提示词：消除歧义、有序任务列表、明确验证命令、不让模型自行决策]

---

## 验证

[端到端验证步骤：运行什么命令 / 看到什么输出 = 成功]
```

---

## Step 5: ExitPlanMode

用户批准后，计划文件即为下一个任务的完整上下文。可直接粘贴 `FOR OPUS 4.7` 或 `FOR SONNET 4.6` 部分到新会话使用。

---

## 部署方式

将本文件复制到全局 skill 目录：

```bash
mkdir -p ~/.claude/skills/req-refine
cp skill/SKILL.md ~/.claude/skills/req-refine/SKILL.md
```

之后在任何项目的 Claude Code 会话中，输入 `/req-refine` 即可触发。
