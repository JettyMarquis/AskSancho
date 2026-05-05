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

## 什么时候用，什么时候不用

**需要用 AskSancho** 的信号：
- 预计执行时间超过 10 分钟
- 需求里有"重构"、"重新设计"、"新功能"、"接入"这类词
- 涉及多个文件或系统
- 你现在写不出一句话的验收标准

**可以跳过** AskSancho 的情况：
- 错误信息明确、修复方式清晰的 bug
- 单行或单文件修改，且有精确指令
- 运行命令或脚本

**判断规则**：如果你现在能用一句话写出验收标准，直接执行。写不出来，用 AskSancho。

| 需求 | 是否使用？ | 原因 |
|---|---|---|
| "修复 README 第 42 行的拼写错误" | 不需要 | 已明确指定，< 1 分钟 |
| "把按钮颜色改成 #3B82F6" | 不需要 | 已给出具体值 |
| "添加用户认证" | **需要** | OAuth 还是密码登录？涉及哪些页面？有没有现成 JWT？ |
| "提升性能" | **需要** | 完全没有验收标准 |
| "重构数据管道" | **需要** | 范围、约束、不能动哪里——全不清楚 |
| "加一行 console.log 调试" | 不需要 | 单行，一次性 |

---

## 立即使用（无需安装）

复制 [`prompts/asksancho-basic.zh.md`](prompts/asksancho-basic.zh.md) 的全部内容，粘贴到任意 LLM 对话窗口（claude.ai、ChatGPT、本地 Gemma 等），在末尾加上你的需求。

---

## Claude Code Skill（感知项目上下文）

```bash
mkdir -p ~/.claude/skills/asksancho ~/.claude/skills/asksancho-clarify
cp skill/SKILL.md ~/.claude/skills/asksancho/SKILL.md
cp skill/CLARIFY_SKILL.md ~/.claude/skills/asksancho-clarify/SKILL.md
```

两个 skill，两个会话——主进程上下文保持干净：

**会话 A**（你当前的会话）：
```
/asksancho 我想要 [你的需求]
```
预读 `CLAUDE.md`、`HANDOFF.md` 和近期 git log → 写入任务文件 → 自动打开新 Terminal 窗口（macOS）。

**会话 B**（新打开的窗口）：
```
/asksancho-clarify
```
读取任务文件 → 运行五步澄清对话 → 将完成的 spec 写入 `~/.claude/scratch/last-requirement-spec.md`。

**回到会话 A**：
```
@~/.claude/scratch/last-requirement-spec.md
```
引用 spec 继续执行。澄清对话全程未进入主进程上下文。

---

## 三层架构

| | 基础版（Tier 1） | 进阶版（Tier 2） | 高级版（Tier 3） |
|---|---|---|---|
| **形式** | 独立 prompt | Claude Code skill | 本地 LLM 应用 |
| **安装** | 无需安装 | 复制两个文件 | Ollama + ChromaDB |
| **上下文** | 无 | CLAUDE.md / git log | 全量向量记忆 |
| **输入** | 文本 | 文本 | 文本 / 语音 / 图像 |
| **状态** | 可用 | 可用 | 开发中 |

---

## License

MIT
