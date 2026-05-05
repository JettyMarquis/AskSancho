# 示例会话 — AskSancho 基础版

> **Language / 语言**: [English](example-session.md) · [中文](example-session.zh.md)

本示例展示五步协议（five-step protocol）应用于一个真实的模糊需求。

---

## 用户原始输入

> 我想让闪卡按 KP 顺序排列，现在是乱的

---

## S1 — 原文复述（Restate）

你是想要将 `flashcard_data.json` 中的闪卡条目，按照 KP 编号的规范顺序（Domain → Topic → Subtopic → 序号）重新排列，使得在 UI 中展示时按这个顺序显示。**是这样吗？**

*用户确认：对，就是这个意思。*

---

## S2 — 三问套组（Three Core Questions）

**1. 成功标准（acceptance criteria）**：完成后会看到什么？

> 打开闪卡界面，KP-I-A-1-001 排在最前，按 I → II → III → IV → X 的 domain 顺序，同 domain 内按 topic 字母升序、subtopic 数字升序、KP 序号升序排列。

**2. 不能改动（must not touch）**：有哪些东西绝对不能动？

> 每张卡片的内容字段（question / answer / kp / related_kps）不能改，只能改顺序。`inject_html.py` 跑完之后 HTML 里的顺序要跟着变。

**3. 已知约束（known constraints）**：

> 要在 `inject_html.py` 运行前完成排序。前端（frontend）不做排序，只读 inject 后的 HTML 中的顺序。

---

## S3 — 意图补充（Intent Expansion）

根据这是数据变更任务，我想补充确认两点：

- **一次性还是可重复运行（repeatable）？** 你的 CLAUDE.md 有一条规则："Sort flashcard_data.json after every append"——是否希望将排序封装成可重复运行的脚本（script），而不是一次性操作？
- **KP-X-\* 的处理**：Domain X 排在最后（X=10），还是按字母顺序插入？

*用户回答：封装成脚本，每次 append 后跑。X domain 排最后。*

---

## S4 — 边界确认（Scope Confirmation）

```
【需求摘要】
目标：对 flashcard_data.json 按规范 KP 顺序排序，封装为可重复运行的脚本

成功标准（acceptance criteria）：
  1. 运行脚本后，条目顺序为 KP-I < KP-II < KP-III < KP-IV < KP-X
  2. 同 domain 内：topic 字母升序 → subtopic 数字升序 → KP 序号升序
  3. inject_html.py 运行后，HTML 中闪卡顺序与 JSON 一致

绝对不改（must not touch）：每张卡片的 question / answer / kp / related_kps 字段值，只改排列顺序

已知约束（constraints）：
  - 排序在 inject_html.py 前运行
  - 前端不做排序，依赖 JSON 顺序
  - X domain 排最后

范围之外（out of scope）：
  - 不修改前端渲染（rendering）逻辑
  - 不修改 inject_html.py 本身（仅在外部排序后调用）
  - 不处理 kp 字段格式异常（假设所有 kp 格式合规）
```

**以上内容是否准确？有需要修改的地方吗？**

*用户确认：准确，可以继续。*

---

## S5 — 双模型输出（Dual-Model Output）

---

**=== FOR OPUS 4.7 ===**

对 `data/flashcard_data.json` 实现按规范 KP 顺序排序的功能。

**背景（background）**：项目使用 data-drop + inject 架构——JSON 是内容的唯一来源，`inject_html.py` 按 JSON 顺序写入 HTML，前端直接渲染 HTML 中的顺序。当前新增卡片总是 append 到末尾，导致 KP 顺序混乱，用户看到的卡片顺序不反映知识体系结构。

**需求**：将排序封装为独立的、幂等（idempotent）的脚本 `data/sort_flashcards.py`，可在每次 append 后运行。

**排序规则**（KP 格式：`KP-{Domain}-{Topic}-{Subtopic}-{NNN}`）：
- Domain 优先级：I=1, II=2, III=3, IV=4, X=10（X domain 排最后）
- 同 domain 内：topic 字母升序 → subtopic 数字升序 → NNN 序号升序
- 卡片内容字段（question / answer / kp / related_kps）不可修改，只改排列顺序

**约束（constraints）**：
- 原地更新 `flashcard_data.json`，不生成新文件
- 对格式异常的 kp 字段打印 warning 但不中断
- 脚本运行后可直接调用 `inject_html.py`

**质量门控（quality gate）**：完成前请验证：(1) 脚本可幂等运行（运行两次结果相同），(2) 取前 5 和后 5 张卡片确认 domain 顺序正确，(3) 检查 CLAUDE.md 的 "Sort flashcard_data.json" 条目是否需要更新。

---

**=== FOR SONNET 4.6 ===**

在 `data/sort_flashcards.py` 中实现闪卡排序脚本，并集成到开发工作流。

**任务列表（ordered task list）**（按顺序执行）：

1. 创建 `data/sort_flashcards.py`：
   - 读取 `data/flashcard_data.json`
   - 按以下 key 排序：domain（I=1, II=2, III=3, IV=4, X=10）→ topic 字母 → subtopic 数字 → KP 序号
   - 原地写回，保持 JSON 格式（`ensure_ascii=False`, `indent=2`）
   - 对格式异常的 kp 字段打印 warning，不中断

2. 测试排序正确性：
   ```bash
   python data/sort_flashcards.py
   python -c "import json; d=json.load(open('data/flashcard_data.json')); print([c['kp'] for c in d[:5]])"
   ```
   预期输出：前 5 条 kp 均以 `KP-I-` 开头，按字母/数字升序。

3. 在 `data/inject_html.py` 文件头加一行注释：
   `# Run sort_flashcards.py before this script if flashcards were appended.`
   不修改任何逻辑。

4. 验证命令（verification command）：
   ```bash
   python data/sort_flashcards.py && python data/inject_html.py --tier full
   ```
   确认 inject 无报错。

**约束（constraint）**：不修改任何卡片的 question / answer / kp / related_kps 字段值，只改排列顺序。
