# AskSancho 效率分析报告

> 生成日期：2026-05-04  
> 作者：Claude Code（基于 /asksancho 生成的 spec + 对 AskSancho repo 的直接读取）

---

## Part A — README 差异分析

### A.1 创作时间线（基于 git log）

```
477b35f  feat: initial req-refiner — 基础版 prompt + skill 骨架
62ad9cb  chore: rebrand req-refiner → AskSancho，添加 MIT license
b0e91a5  docs: 精简 README（英文版 v1）
6a7d015  docs: 添加 banner 图片到 README
d5f6757  docs: 添加双语支持（English / Chinese）← README.zh.md 在此诞生
7d7680c  docs: 更新 README（英 + 中）以反映 v2.0 subagent 架构
```

README.md 先经过三轮独立迭代（b0e91a5 → 6a7d015），才在 d5f6757 诞生了 README.zh.md。两个文件从未有过"以一个为权威源、另一个是翻译"的关系——它们始终是独立写成的。

---

### A.2 逐节差异对照表

| 节 | README.md（英文） | README.zh.md（中文） | 差异类型 |
|---|---|---|---|
| 语言切换器 | `**English** · 中文` | `English · **中文**` | 粗体方向相反（正确，各自为主） |
| Motto 引言 | "Before you charge at windmills, make sure you know what you're charging at." | "在冲向风车之前，先搞清楚你在冲向什么。" | 语义等价，翻译流畅 |
| 问题描述格式 | **散文段落**，三句话，不分条 | **四条 bullet**，每条有标签+释义 | **结构差异**（见 A.3.1） |
| "无需安装"引用的文件 | `prompts/asksancho-basic.md` | `prompts/asksancho-basic.zh.md` | 正确，各自指向本语言版 |
| 二级标题 | `## Claude Code skill (project-aware)` | `## Claude Code Skill（感知项目上下文）` | 大小写 + 括注内容不同（见 A.3.2） |
| Skill 说明正文 | 无"不被中间问答污染"这句 | 有"不被中间问答污染" | **内容缺失**（见 A.3.3） |
| Tier 表格列标题 | `Tier 1 / Tier 2 / Tier 3` | `基础版（Tier 1）/ 进阶版（Tier 2）/ 高级版（Tier 3）` | 中文版加了友好名称（见 A.3.4） |
| Tier 表格行标题 | `What / Install / Context / Input / Status` | `形式 / 安装 / 上下文 / 输入 / 状态` | 纯中文，无英文对照 |

---

### A.3 四处具体差异详解

#### A.3.1 问题描述段落 vs Bullet 列表

**README.md（英文）——散文风格**

```
Claude Code's output quality is bounded by how well you describe what you want.
Most natural-language requirements are missing acceptance criteria, have fuzzy scope,
or don't account for existing project constraints. The result is rework.

AskSancho runs a five-step clarification dialog and produces a structured spec —
with separate versions for Opus 4.7 and Sonnet 4.6.
```

**README.zh.md（中文）——结构化 bullet**

```
- **没有验收标准（acceptance criteria）** — 你和模型都不知道"完成"是什么意思
- **边界模糊（fuzzy scope）** — Claude 会悄悄扩展到相邻功能
- **遗漏约束（missing constraints）** — CLAUDE.md 规则、时间限制、兼容性要求都没提到
- **错误的模型使用方式** — Opus 4.7 和 Sonnet 4.6 需要截然不同的 prompt 风格
```

**成因**：英文版在 b0e91a5 重写时已定型为精简散文。中文版在 d5f6757 独立撰写时，作者选择了更适合扫读的 bullet 格式，并增加了第四条"错误的模型使用方式"——这一条在英文版中完全不存在。这不是翻译遗漏，而是两次独立写作时的差异判断。

---

#### A.3.2 二级标题的大小写与括注

| 版本 | 标题 |
|---|---|
| 英文 | `## Claude Code skill (project-aware)` |
| 中文 | `## Claude Code Skill（感知项目上下文）` |

英文标题用小写"skill"、英文括号；中文标题用大写"Skill"、中文括号，并将"project-aware"意译为"感知项目上下文"。两者是同一节的标题，但英中版本各自写作，未经对照校正。

---

#### A.3.3 Skill 说明正文的独家内容

**README.md（英文）**

```
The skill pre-reads your `CLAUDE.md`, `HANDOFF.md`, and recent git log,
compresses them into a context block, then hands everything to a **Sonnet 4.6 subagent**.
The subagent runs the full clarification dialog — your main conversation context
only receives the finished spec.
```

**README.zh.md（中文）**

```
Skill 会预读你的 `CLAUDE.md`、`HANDOFF.md` 和近期 git log，压缩成上下文块，
然后交给一个独立的 **Sonnet 4.6 subagent**。整个澄清对话在 subagent 里完成
——主进程上下文只收到最终的结构化 spec，不被中间问答污染。
```

中文版末尾比英文版多了"**不被中间问答污染**"这七个字。这是一个对产品价值的核心说明——主进程保持干净——英文版漏掉了它。

---

#### A.3.4 Tier 表格列标题

| 版本 | 列标题 |
|---|---|
| 英文 | `Tier 1 / Tier 2 / Tier 3`（纯技术编号） |
| 中文 | `基础版（Tier 1）/ 进阶版（Tier 2）/ 高级版（Tier 3）`（编号 + 友好名） |

中文版列标题更具可读性，并且与正文中"基础版 / 进阶版 / 高级版"的称呼保持一致。英文版仅有技术编号，没有同等的助记名称（英文正文中也未统一命名）。

---

### A.4 根本原因：独立写作，而非单一权威源翻译

Prompt 双语文件的差异可以作为佐证。比较 `prompts/asksancho-basic.md` 和 `prompts/asksancho-basic.zh.md`：

| 位置 | asksancho-basic.md（英文） | asksancho-basic.zh.md（中文） |
|---|---|---|
| S2 问题标签 | 中文标签（`成功标准 / 不能改动 / 已知约束`），无英文括注 | 中英双语（`成功标准（acceptance criteria）`等） |
| S4 摘要格式 | `OUT OF SCOPE`（大写） | `out of scope`（小写） |
| S3 分类标签 | `For UI/frontend changes:` | `UI / 前端（frontend）变更：` |
| 整体语气 | 指令式英文（"Write a longer prompt. Include:"） | 指令式中文（"写较长的 prompt。包含："）含英文技术词括注 |

Prompt 文件和 README 文件呈现出相同的模式：**中文版不是英文版的逐句翻译，而是在理解同一设计意图后，用中文独立重写**。这就导致：
- 中文版在某些地方比英文版更详细（S2/S4 加了英文括注，方便中文用户理解术语）
- 英文版在某些地方比中文版更完整（问题说明段落覆盖的角度在 prompt 层面有差异）
- 两版同步更新时（7d7680c），各自用本语言重新诠释 v2.0 变化，而非机械同步

**结论**：差异的根本原因是"两份文件由同一会话的不同 pass 独立写成，不是从单一权威源翻译"——即便写作者（Claude Code）是同一个，每次独立写作仍会产生措辞、格式和内容细节上的偏移。

---

## Part B — AskSancho 效率研究 Memo

> **重要声明**：以下所有 token 估算均为**理论值**，非实测数据。模型来源为对话结构分析 + 已记录的实际事件（v9.4.0 卡拉OK事件）。无 Claude Code API telemetry 访问权限，不拟合统计模型到实际使用日志。

---

### B.1 Token 节省模型

#### 基准假设（无澄清，直接执行）

```
一次任务的 token 开销 = T_execute + T_rework
T_execute = 正确理解需求时所需的执行 token（基准）
T_rework  = 因需求模糊导致的返工 token（方向错误 × 修正次数）
```

#### AskSancho 开销

```
T_clarify = 5 步澄清协议的 token（S1~S5，每步平均 1 轮 AskUserQuestion）
          ≈ 5 轮 × 平均 800 tokens/轮 = ~4,000 tokens
T_spec    = 生成结构化 spec 的 token
          ≈ ~2,000 tokens
T_asksancho_total ≈ 6,000 tokens（固定开销）
```

#### 场景比较

---

**场景 1：小改动（例：修改一个 CSS 按钮的 hover 颜色）**

| | 无澄清 | 有 AskSancho |
|---|---|---|
| 假设 | 需求"把按钮变蓝"有歧义：background 还是 hover？ | 澄清确认目标是 hover state，hex 色值 #3B82F6 |
| 执行 token | ~3,000（改错方向） | ~2,500（直接命中） |
| 返工 token | ~2,000（1 次修正） | 0 |
| 澄清 token | 0 | ~6,000 |
| **合计** | **~5,000** | **~8,500** |
| 节省 | — | **-3,500（增加 70%）** |

> **假设**：小改动场景，AskSancho 开销高于收益。这是合理的——五步协议对极小任务有负收益。实际使用中，有经验的用户会对"30 秒能做完的事"跳过澄清，直接执行。

---

**场景 2：中型功能（例：添加一个用户认证流程）**

| | 无澄清 | 有 AskSancho |
|---|---|---|
| 假设 | "加认证"未指定 OAuth 还是密码登录；未说明是否已有 JWT 基础 | 澄清后确定：OAuth（Google），已有 JWT，不改现有密码登录 |
| 执行 token | ~5,000（初始错误方向，密码流程） | ~4,000（直接按 OAuth 执行） |
| 返工 token | ~12,000（推倒重来，1 次大返工） | 0 |
| 澄清 token | 0 | ~6,000 |
| **合计** | **~17,000** | **~10,000** |
| 节省 | — | **~7,000（节省约 41%）** |

> **假设**：返工规模 = 执行 token × 2.4（重建比初建复杂）；澄清完全消除返工。

---

**场景 3：大型架构决策（例：重新设计数据管道）**

| | 无澄清 | 有 AskSancho |
|---|---|---|
| 假设 | 需求"重新设计 pipeline"未确认输出格式、是否保留旧接口、并发要求 | 澄清后确定：NDJSON 输出、旧接口向后兼容 2 个版本、单线程 |
| 执行 token | ~6,000（初始框架） | ~5,000（直接命中） |
| 返工 token | ~35,000（多阶段错误方向 + 1 次全面重写） | 0 |
| 澄清 token | 0 | ~6,000 |
| **合计** | **~41,000** | **~11,000** |
| 节省 | — | **~30,000（节省约 73%）** |

> **假设**：大型架构任务的返工规模 ≈ 初始执行的 5~7 倍（含多阶段设计错误）；一次完整澄清可将执行 token 降低约 15%（spec 提供约束上下文，减少 Claude 的探索性推断）。

---

### B.2 v9.4.0 卡拉OK事件——量化案例

**事件背景**（记录于 `~/.claude/rules/clarification-before-action.md`）

用户提问："能否让被朗读的内容发生颜色变化、变粗体，来帮助用户把音频和内容对应起来？"

**用户实际想要**：朗读到哪一行/哪个模块，那个**幻灯片内容块**就高亮（颜色+粗体）。

**Claude 实际做了**：发现音频管道已有逐字时间戳 → 能力 ≠ 授权 → 自行新增了字幕栏字幕卡拉OK高亮（subtitle bar word karaoke）功能。

**量化成本估算**（理论值）

| 阶段 | 开销来源 | 估算 token |
|---|---|---|
| Phase 1~6 错误构建 | 朝错误方向执行 8 个阶段 | ~45,000 |
| Phase 7 全面回滚 | 撤销 Phase 6 的全部工作 | ~12,000 |
| Phase 8 正确重建 | 用正确理解重新执行 | ~15,000 |
| **总计（实际路径）** | | **~72,000** |
| **假设有 AskSancho** | 澄清 + 直接正确执行 | ~8,000~12,000 |
| **可节省** | | **~60,000（约 83%）** |

**关键问题**：Claude 在问"完整方案对不对"时，给出的选项是"Phase 7 一起发布 / Phase 8 推迟"——两个选项都包含了字幕卡拉OK功能，用户没有"完全不做这个功能"的选项。AskSancho 的 S4（边界确认）步骤专门要求列出"范围之外（Out of Scope）"，会强制暴露这个问题。

**如果 S2 询问了"成功标准"**：用户会说"幻灯片里的行或模块改变颜色"，而非"字幕栏"——Phase 1~7 的方向错误会在会话开始的第一分钟被识别。

---

### B.3 生产力收益分类（非 token 维度）

#### 收益 1：消除方向性返工（最高价值）

返工不只是 token 成本，还有：
- **时间成本**：build → test → revert 循环通常需要 20~60 分钟真实时间
- **心理成本**：用户需要重新解释需求，审查不符预期的代码，维持对话连贯性
- **上下文损耗**：每次返工都让对话上下文更长、更嘈杂，影响后续任务质量

AskSancho 通过 S4（边界确认）将"你要什么/你不要什么"外化为文档，可在多次对话中引用。

---

#### 收益 2：主进程上下文保持干净

没有 AskSancho 时，需求澄清发生在主进程里：
- 用户说"加认证"→ Claude 问"哪种认证？"→ 用户回答 → Claude 又问 → ... → 最终明确
- 这 4~6 轮问答全部留在主进程上下文，占用 token 窗口，并在压缩后可能导致关键信息丢失

有 AskSancho（companion session 方案）时，澄清对话在独立 Session B 进行，主进程只收到最终 spec 的引用（`@scratch/last-requirement-spec.md`）。主进程上下文保持简洁，留给实际执行使用。

---

#### 收益 3：Opus / Sonnet 模型分工优化

不同模型需要不同的 prompt 风格：

| 模型 | 最优 prompt 风格 |
|---|---|
| Opus 4.7 | 保留适当模糊性，包含"为什么"背景，鼓励推理替代方案 |
| Sonnet 4.6 | 消除所有歧义，给出有序任务列表，指定验证命令 |

AskSancho 通过 S5（双模型输出）为同一需求自动生成两版 prompt，用户无需了解两个模型的差异就能获得最优指令。没有这个步骤，用户通常会把同一段文字直接发给任意模型——对 Sonnet 来说太模糊，对 Opus 来说太指令化。

---

#### 收益 4：需求 Spec 的跨会话复用

AskSancho 生成的 `<spec>` 写入 `~/.claude/scratch/last-requirement-spec.md`，可以：
- 在任意未来会话中用 `@~/.claude/scratch/last-requirement-spec.md` 引用
- 作为 git commit 的需求上下文存档
- 在任务中途发生 compaction 时作为恢复点（Claude 可以重读 spec 重建上下文）
- 提供给 code reviewer 作为"验收标准"的参照

自然语言需求"加个蓝按钮"在会话中是一次性的；结构化 spec 是持久的工件（artifact）。

---

#### 收益 5：强制暴露遗漏约束

大多数模糊需求的问题不在于"说错了什么"，而在于"没说什么"。S3（意图补充）步骤通过分类清单（UI / backend / content / config）主动探查用户可能遗漏的边界条件：

- "深色模式是否也需要支持？"——通常被遗忘
- "旧接口是否需要向后兼容？"——决定完全不同的实现路径
- "改动是一次性还是可重复执行？"——影响是否需要幂等设计

这些问题如果在执行后才暴露，代价是完整的重构；在澄清阶段暴露，代价是一句话的回答。

---

### B.4 汇总

| 场景 | 无澄清 token | 有 AskSancho token | 节省比 | 说明 |
|---|---|---|---|---|
| 小改动 | ~5,000 | ~8,500 | **-70%（亏损）** | 五步协议对极小任务过重 |
| 中型功能 | ~17,000 | ~10,000 | **+41%** | 一次返工即回本 |
| 大型架构 | ~41,000 | ~11,000 | **+73%** | 方向性错误成本极高 |
| v9.4.0 事件（实例） | ~72,000 | ~10,000 | **+83%** | Phase 7 全回滚的真实成本 |

**使用建议**：对预计执行时间 < 2 分钟的任务，直接执行优于走澄清协议。对预计执行时间 > 10 分钟（或任何"大型"/"重构"/"新功能"标签的任务），AskSancho 的固定澄清成本（~6K tokens，~3~5 分钟）几乎必然正收益。

---

*本文档基于 AskSancho 项目代码、git 历史及 AIGP 项目实际事件生成。所有 token 数字为理论估算，仅供量级参考。*
