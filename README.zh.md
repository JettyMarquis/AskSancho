# AskSancho

<p align="center">
  <img src="docs/asksancho.jpeg" alt="AskSancho" width="600">
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md"><b>中文</b></a>
</p>

> *"在冲向风车之前，先搞清楚你在冲向什么。"*

在需求进入 Claude Code 之前，先把它说清楚。

---

## 问题所在

Claude Code 的输出质量，取决于你的需求描述有多清晰。大多数自然语言需求都有以下问题：

- **没有验收标准（acceptance criteria）** — 你和模型都不知道"完成"是什么意思
- **边界模糊（fuzzy scope）** — Claude 会悄悄扩展到相邻功能
- **遗漏约束（missing constraints）** — CLAUDE.md 规则、时间限制、兼容性要求都没提到
- **错误的模型使用方式** — Opus 4.7 和 Sonnet 4.6 需要截然不同的 prompt 风格

AskSancho 通过五步澄清协议（five-step clarification protocol）解决这些问题，并为 Opus 4.7 和 Sonnet 4.6 分别生成优化后的 prompt。

---

## 立即使用（无需安装）

复制 [`prompts/asksancho-basic.zh.md`](prompts/asksancho-basic.zh.md) 的全部内容，粘贴到任意 LLM 对话窗口（claude.ai、ChatGPT、本地 Gemma 等），在末尾加上你的需求。

---

## Claude Code Skill（感知项目上下文）

```bash
mkdir -p ~/.claude/skills/asksancho
cp skill/SKILL.md ~/.claude/skills/asksancho/SKILL.md
```

在任意 Claude Code 会话中输入：

```
/asksancho 我想要 [你的需求]
```

Skill 会预读你的 `CLAUDE.md`、`HANDOFF.md` 和近期 git log，压缩成上下文块，然后交给一个独立的 **Sonnet 4.6 subagent**。整个澄清对话在 subagent 里完成——主进程上下文只收到最终的结构化 spec，不被中间问答污染。

---

## 三层架构

| | 基础版（Tier 1） | 进阶版（Tier 2） | 高级版（Tier 3） |
|---|---|---|---|
| **形式** | 独立 prompt | Claude Code skill | 本地 LLM 应用 |
| **安装** | 无需安装 | 复制一个文件 | Ollama + ChromaDB |
| **上下文** | 无 | CLAUDE.md / git log | 全量向量记忆 |
| **输入** | 文本 | 文本 | 文本 / 语音 / 图像 |
| **状态** | 可用 | 可用 | 开发中 |

---

## License

MIT
