# req-refiner

将自然语言开发需求整理为 Claude Code 高质量输入的三层工作流。

## 为什么需要这个

Claude Code 的质量上限取决于需求描述的清晰度。用户用自然语言表达的需求通常：
- 缺少成功标准（如何验证完成）
- 遗漏约束（不能动什么）
- 边界模糊（哪些不做）

`req-refiner` 通过一套五步对话协议，在需求进入 Claude Code 前完成澄清，并为 Opus 4.7 和 Sonnet 4.6 分别生产优化的提示词。

---

## 三层架构

### 基础版 — 零依赖，任意 LLM 可用

1. 打开任意 LLM 对话窗口（claude.ai、ChatGPT、本地 Gemma 等）
2. 复制 `prompts/req-refiner-basic.md` 全文，粘贴到对话框
3. 在末尾粘贴你的需求
4. 完成五步对话后，获得 Opus 4.7 版和 Sonnet 4.6 版提示词

示例对话见 `examples/example-session.md`。

---

### 进阶版 — Claude Code Skill，读取项目上下文

部署：
```bash
mkdir -p ~/.claude/skills/req-refine
cp skill/SKILL.md ~/.claude/skills/req-refine/SKILL.md
```

使用：在任何项目的 Claude Code 会话中输入
```
/req-refine [你的需求]
```

Skill 会自动读取 CLAUDE.md / git log / HANDOFF.md，基于项目上下文提问，然后在 plan mode 中生成结构化需求文件。

---

### 高级版 — 本地 LLM 中间层（开发中）

基于 Gemma 4（Ollama）+ ChromaDB 向量记忆的本地应用，支持文本/语音/图像输入，并可将精炼后的需求直接写入 Claude Code。

开发状态：Phase A（记忆层）进行中。见 `core/` 目录。

---

## 文件结构

```
req-refiner/
├── README.md
├── prompts/
│   └── req-refiner-basic.md    ← 基础版 meta-prompt（直接复制使用）
├── examples/
│   └── example-session.md      ← 完整示例对话
├── skill/
│   └── SKILL.md                ← 进阶版 Claude Code skill
├── core/                       ← 高级版后端（开发中）
│   ├── collector.py            ← Claude Code transcript 收集器
│   ├── indexer.py              ← 项目文件向量化
│   ├── refiner.py              ← Gemma 4 精炼器
│   └── injector.py             ← 输出注入 Claude Code（TODO）
├── ui/
│   └── index.html              ← 高级版前端（开发中）
└── app.py                      ← FastAPI 入口（开发中）
```

---

## 快速开始（基础版）

不需要安装任何东西。打开 `prompts/req-refiner-basic.md`，复制全文，粘贴到任意 LLM 对话窗口，在末尾加上你的需求。
