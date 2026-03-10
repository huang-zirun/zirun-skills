# Claude 技能构建完整指南

## 目录

- [简介](#简介)
- [第 1 章：基础](#第-1-章基础)
- [第 2 章：规划与设计](#第-2-章规划与设计)
- [第 3 章：测试与迭代](#第-3-章测试与迭代)
- [第 4 章：分发与共享](#第-4-章分发与共享)
- [第 5 章：模式与故障排除](#第-5-章模式与故障排除)
- [第 6 章：资源与参考](#第-6-章资源与参考)
- [附录 A：快速检查清单](#附录-a快速检查清单)
- [附录 B：YAML frontmatter](#附录-byaml-frontmatter)
- [附录 C：完整技能示例](#附录-c完整技能示例)

---

## 简介

**技能（skill）** 是一组指令，以简单文件夹的形式打包，用于教 Claude 如何完成特定任务或工作流。技能是让 Claude 按你的需求定制的有力方式之一：不必在每次对话里重复说明偏好、流程和领域知识，只需教一次，即可在每次使用中生效。

当你有可重复的工作流时，技能尤其有用：根据规格生成前端设计、用统一方法做调研、按团队版式创建文档，或编排多步骤流程。它们与 Claude 的内置能力（如代码执行、文档生成）配合良好；若你在做 MCP 集成，技能还能在工具访问之上增加一层，把原始工具调用变成可靠、优化的工作流。

本指南涵盖构建有效技能所需的一切：从规划与结构到测试与分发。无论你是为自己、团队还是社区做技能，都能在文中找到实用模式和真实示例。

### 你将学到

- 技能结构的技术要求与最佳实践
- 独立技能与 MCP 增强工作流的模式
- 在不同场景下验证有效的模式
- 如何测试、迭代和分发你的技能

### 适用对象

- 希望 Claude 稳定遵循特定工作流的开发者
- 希望 Claude 遵循特定工作流的高级用户
- 希望在全组织内统一 Claude 使用方式的团队

### 两条阅读路径

**只做独立技能？** 重点看「基础」「规划与设计」以及类别 1–2。

**在现有 MCP 上增强？** 「Skills + MCP」小节和类别 3 适合你。

两条路径共享同一套技术要求，按你的使用场景选读即可。

**读完本指南你能做到：** 一次坐下来就能做出一个可用的技能。用 skill-creator 从零到第一个可运行技能，大约需要 15–30 分钟。

开始吧。

---

## 第 1 章：基础

### 什么是技能？

技能是一个文件夹，包含：

- **SKILL.md**（必选）：带 YAML frontmatter 的 Markdown 说明
- **scripts/**（可选）：可执行代码（Python、Bash 等）
- **references/**（可选）：按需加载的文档
- **assets/**（可选）：输出中用到的模板、字体、图标等

### 核心设计原则

#### 渐进式披露（Progressive Disclosure）

技能采用三级结构：

- **第一级（YAML frontmatter）：** 始终加载进 Claude 的系统提示，只提供「何时该用这个技能」的信息，无需把全部内容放进上下文。
- **第二级（SKILL.md 正文）：** 当 Claude 判断该技能与当前任务相关时加载，包含完整说明与指引。
- **第三级（链接文件）：** 技能目录内打包的额外文件，Claude 仅在需要时浏览和发现。

这种渐进式披露在保持专业能力的同时，减少 token 消耗。

#### 可组合性（Composability）

Claude 可同时加载多个技能。你的技能应能与其他技能良好共存，而不是假设自己是唯一能力。

#### 可移植性（Portability）

技能在 Claude.ai、Claude Code 和 API 中行为一致。一次创建，在所有界面通用，只要环境满足技能所需的依赖即可。

### 面向 MCP 开发者：Skills + 连接器

> 💡 不涉及 MCP、只做独立技能？可跳到「规划与设计」，之后随时回来看本节。

若你已有可用的 MCP server，最难的部分已经完成。技能是之上的「知识层」——把你已知的工作流和最佳实践固化下来，让 Claude 稳定执行。

#### 厨房类比

- **MCP** 提供专业厨房：工具、食材和设备。
- **技能** 提供菜谱：一步步做出有价值成果的说明。

二者结合，用户无需自己摸索每一步就能完成复杂任务。

#### 如何配合

| MCP（连接） | 技能（知识） |
|-------------|--------------|
| 将 Claude 连接到你的服务（Notion、Asana、Linear 等） | 教 Claude 如何有效使用你的服务 |
| 提供实时数据访问与工具调用 | 固化工作流与最佳实践 |
| **Claude 能做什么** | **Claude 该怎么去做** |

#### 对 MCP 用户的意义

**没有技能时：**

- 用户连上 MCP 却不知道下一步做什么
- 大量「如何用你们的集成做 X」的工单
- 每次对话从零开始
- 因提示方式不同而结果不一致
- 用户把问题归咎于连接器，而实际缺的是工作流指引

**有技能时：**

- 预置工作流在需要时自动激活
- 一致、可靠地使用工具
- 每次交互都嵌入最佳实践
- 集成学习成本更低

---

## 第 2 章：规划与设计

### 从用例出发

在写任何代码之前，先明确技能要支持的 2–3 个具体用例。

**好的用例定义示例：**

- **用例：** 项目冲刺规划
- **触发：** 用户说「帮我规划这次冲刺」或「创建冲刺任务」
- **步骤：**
  1. 通过 MCP 从 Linear 获取当前项目状态
  2. 分析团队速率与容量
  3. 建议任务优先级
  4. 在 Linear 中创建带标签与估时的任务
- **结果：** 规划好的冲刺及已创建任务

**自问：**

- 用户想达成什么？
- 需要哪些多步骤工作流？
- 需要哪些工具（内置还是 MCP）？
- 应嵌入哪些领域知识或最佳实践？

### 常见技能用例类别

在 Anthropic，我们观察到三类常见用例：

#### 类别 1：文档与资产创建

**用于：** 产出一致、高质量的文档、演示、应用、设计、代码等。

**真实示例：** frontend-design 技能（另见 docx、pptx、xlsx、ppt 相关技能）

> "Create distinctive, production-grade frontend interfaces with high design quality. Use when building web components, pages, artifacts, posters, or applications."

**常用手法：**

- 内嵌风格指南与品牌规范
- 统一输出的模板结构
- 定稿前质量检查清单
- 无需外部工具，依赖 Claude 内置能力

#### 类别 2：工作流自动化

**用于：** 需要统一方法的多步骤流程，包括跨多个 MCP server 的协调。

**真实示例：** skill-creator 技能

> "Interactive guide for creating new skills. Walks the user through use case definition, frontmatter generation, instruction writing, and validation."

**常用手法：**

- 带校验节点的分步工作流
- 通用结构模板
- 内置审查与改进建议
- 迭代精炼循环

#### 类别 3：MCP 增强

**用于：** 在 MCP 提供的工具访问之上，增加工作流指引。

**真实示例：** sentry-code-review 技能（来自 Sentry）

> "Automatically analyzes and fixes detected bugs in GitHub Pull Requests using Sentry's error monitoring data via their MCP server."

**常用手法：**

- 按顺序协调多次 MCP 调用
- 嵌入领域知识
- 提供用户本需自己补充的上下文
- 针对常见 MCP 问题的错误处理

### 定义成功标准

如何判断技能在起作用？

以下可作为目标参考——是粗略基准而非精确阈值。尽量严谨，但接受会存在一定主观判断。我们正在完善更可靠的度量指引与工具。

**可量化指标：**

- **在约 90% 的相关查询下触发**
  - 做法：跑 10–20 条本应触发该技能的测试查询，统计自动加载与需显式调用的比例。
- **在 X 次工具调用内完成工作流**
  - 做法：对比同一任务在开启/关闭技能时的工具调用次数与总 token 消耗。
- **每条工作流 0 次失败 API 调用**
  - 做法：在测试中查看 MCP server 日志，统计重试与错误码。

**定性指标：**

- **用户不必反复提示下一步**
  - 评估：测试时记录需要纠正或澄清的频率，向 beta 用户收集反馈。
- **工作流无需用户修正即可完成**
  - 评估：同一请求跑 3–5 次，比较输出的结构一致性与质量。
- **跨会话结果一致**
  - 评估：新用户能否在最少指引下首次就完成任务？

### 技术要求

#### 文件结构

```
your-skill-name/
├── SKILL.md       # 必选 - 主技能文件
├── scripts/       # 可选 - 可执行代码
│   ├── process_data.py   # 示例
│   └── validate.sh       # 示例
├── references/    # 可选 - 文档
│   ├── api-guide.md      # 示例
│   └── examples/        # 示例
└── assets/        # 可选 - 模板等
    └── report-template.md   # 示例
```

#### 硬性规则

**SKILL.md 命名：**

- 必须严格为 **SKILL.md**（区分大小写）
- 不接受 SKILL.MD、skill.md 等变体

**技能文件夹命名：**

- 使用 kebab-case：`notion-project-setup` ✅
- 不要空格：`Notion Project Setup` ❌
- 不要下划线：`notion_project_setup` ❌
- 不要大写：`NotionProjectSetup` ❌

**不要 README.md：**

- 技能文件夹内不要放 README.md
- 所有说明放在 SKILL.md 或 references/
- 说明：通过 GitHub 分发时，仓库级仍需 README 给人看——见「分发与共享」。

#### YAML frontmatter：最关键部分

YAML frontmatter 决定 Claude 是否加载你的技能，务必写对。

**最少必需格式：**

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

有这些就可以起步。

**字段要求：**

- **name**（必填）：
  - 仅 kebab-case
  - 无空格、无大写
  - 建议与文件夹名一致

- **description**（必填）：
  - 必须同时包含：技能做什么 + 何时使用（触发条件）
  - 不超过 1024 字符
  - 不得含 XML 标签（`<` 或 `>`）
  - 包含用户可能说的具体任务
  - 若与文件类型相关，请写明

- **license**（可选）：
  - 开源时可写
  - 常见：MIT、Apache-2.0

- **compatibility**（可选）：
  - 1–500 字符
  - 说明环境要求：如目标产品、系统依赖、网络需求等

- **metadata**（可选）：
  - 任意自定义键值
  - 建议：author、version、mcp-server
  - 示例：

    ```yaml
    metadata:
      author: ProjectHub
      version: 1.0.0
      mcp-server: projecthub
    ```

**安全限制**

frontmatter 中禁止：

- XML 尖括号（`<` `>`）
- 名称中含 "claude" 或 "anthropic" 的技能（保留字）

原因：frontmatter 会进入 Claude 系统提示，恶意内容可能注入指令。

### 写出有效技能

#### description 字段

Anthropic 工程博客指出：「这些元数据……只提供足够信息，让 Claude 知道何时使用每个技能，而无需把全部内容加载进上下文。」这是渐进式披露的第一级。

**结构：** [做什么] + [何时用] + [关键能力]

**良好 description 示例：**

```yaml
# 好 - 具体可执行
description: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".

# 好 - 含触发短语
description: Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".

# 好 - 价值清晰
description: End-to-end customer onboarding workflow for PayFlow. Handles account creation, payment setup, and subscription management. Use when user says "onboard new customer", "set up subscription", or "create PayFlow account".
```

**不良 description 示例：**

```yaml
# 太泛
description: Helps with projects.

# 缺触发条件
description: Creates sophisticated multi-page documentation systems.

# 偏技术、无用户触发
description: Implements the Project entity model with hierarchical relationships.
```

#### 撰写正文说明

frontmatter 之后，用 Markdown 写实际说明。

**推荐结构：**

按你的技能替换方括号内容即可。

    ---
    name: your-skill
    description: [--.]
    ---

    # Your Skill Name

    ## Instructions

    ### Step 1: [First Major Step]
    Clear explanation of what happens.

    Example:
        python scripts/fetch_data.py --project-id PROJECT_ID
    Expected output: [describe what success looks like]

    (Add more steps as needed)

    ## Examples

    ### Example 1: [common scenario]
    User says: "Set up a new marketing campaign"
    Actions:
    1. Fetch existing campaigns via MCP
    2. Create new campaign with provided parameters
    Result: Campaign created with confirmation link

    (Add more examples as needed)

    ## Troubleshooting

    ### Error: [Common error message]
    Cause: [Why it happens]
    Solution: [How to fix]

    (Add more error cases as needed)

#### 说明撰写最佳实践

**具体且可执行**

✅ 好：

- 运行 `python scripts/validate.py --input {filename}` 检查数据格式。
- 若校验失败，常见原因包括：
  - 缺少必填字段（补全到 CSV）
  - 日期格式无效（使用 YYYY-MM-DD）

❌ 差：

- 进行前先校验数据。

**包含错误处理**

```markdown
## Common Issues

### MCP Connection Failed
If you see "Connection refused":
1. Verify MCP server is running: Check Settings > Extensions
2. Confirm API key is valid
3. Try reconnecting: Settings > Extensions > [Your Service] > Reconnect
```

**明确引用打包资源**

在写查询前，查阅 `references/api-patterns.md` 了解：

- 限流说明
- 分页方式
- 错误码与处理

**善用渐进式披露**

SKILL.md 聚焦核心说明，详细文档放到 `references/` 并做链接。（三级系统见「核心设计原则」。）

---

## 第 3 章：测试与迭代

可根据需求选择不同严格程度的测试方式：

- **在 Claude.ai 中手动测试** — 直接提问、观察行为，迭代快、无需配置。
- **在 Claude Code 中脚本化测试** — 用自动化用例在改动间做可重复验证。
- **通过 skills API 程序化测试** — 针对既定测试集系统化运行评估。

选择与质量要求和技能可见范围匹配的方式。小团队内部用的技能，与面向大量企业用户部署的技能，测试需求不同。

> **建议：先在一个任务上迭代，再扩展**  
> 我们发现，最有效的做法是：先在一个难任务上反复试，直到 Claude 稳定成功，再把成功做法抽成技能。这样利用 Claude 的上下文学习，比泛泛测试更快得到信号。基础稳固后，再扩展到多用例做覆盖。

### 推荐测试思路

根据早期经验，有效测试通常覆盖三块：

#### 1. 触发测试

**目标：** 确保技能在正确时机加载。

**测试点：**

- ✅ 在明显相关任务上触发
- ✅ 在换一种说法时仍触发
- ❌ 在无关主题上不触发

**示例测试集：**

- **应触发：**
  - "Help me set up a new ProjectHub workspace"
  - "I need to create a project in ProjectHub"
  - "Initialize a ProjectHub project for Q4 planning"
- **不应触发：**
  - "What's the weather in San Francisco?"
  - "Help me write Python code"
  - "Create a spreadsheet"（除非 ProjectHub 技能处理表格）

#### 2. 功能测试

**目标：** 验证技能产出正确结果。

**测试点：**

- 产出有效输出
- API 调用成功
- 错误处理正常
- 边界情况覆盖

**示例：**

- **测试：** 创建含 5 个任务的项目
- **给定：** 项目名 "Q4 Planning"，5 条任务描述
- **当：** 技能执行工作流
- **则：**
  - 在 ProjectHub 中创建项目
  - 创建 5 个任务且属性正确
  - 任务均关联到项目
  - 无 API 错误

#### 3. 性能对比

**目标：** 证明相对基线，技能带来改进。

使用「定义成功标准」中的指标。对比可类似下面这样。

**基线对比：**

| | 无技能 | 有技能 |
|---|--------|--------|
| 每次都要用户给指令 | 工作流自动执行 |
| 15 轮来回消息 | 仅 2 次澄清问题 |
| 3 次失败 API 需重试 | 0 次失败 API |
| 消耗 12,000 token | 消耗 6,000 token |

### 使用 skill-creator 技能

**skill-creator 技能** — 在 Claude.ai 通过插件目录获取，或为 Claude Code 下载 — 可帮助你构建和迭代技能。若已有 MCP server 并清楚前 2–3 个工作流，通常 15–30 分钟内就能搭建并验证一个可用技能。

**创建技能：**

- 从自然语言描述生成技能
- 产出格式正确的 SKILL.md 与 frontmatter
- 建议触发短语与结构

**审查技能：**

- 标出常见问题（描述含糊、缺触发、结构问题）
- 指出过度/不足触发的风险
- 根据技能声明的用途建议测试用例

**迭代改进：**

- 使用技能时遇到边界或失败，把案例带回 skill-creator
- 示例："Use the issues & solution identified in this chat to improve how the skill handles [specific edge case]"

**使用方式：**

> "Use the skill-creator skill to help me build a skill for [your use case]"

> **说明：** skill-creator 协助设计与打磨技能，但不执行自动化测试套件，也不产出量化评估结果。

### 根据反馈迭代

技能是活文档，可按以下信号迭代：

**触发不足：**

- 该加载时未加载
- 用户经常手动启用
- 支持问题集中在「什么时候用」

**对策：** 在 description 中增加细节与 nuance，包括技术术语关键词

**触发过多：**

- 无关查询也加载
- 用户主动关闭
- 对用途产生困惑

**对策：** 增加负面触发说明，收窄范围

**执行问题：**

- 结果不稳定
- API 调用失败
- 需要用户纠正

**对策：** 改进说明、补充错误处理

---

## 第 4 章：分发与共享

技能让你的 MCP 集成更完整。用户在比较各种连接器时，带技能的方案能更快产生价值，相对「仅 MCP」更有优势。

### 当前分发方式（2026 年 1 月）

**个人用户获取技能：**

1. 下载技能文件夹
2. 如需则打成 zip
3. 在 Claude.ai 通过 设置 > Capabilities > Skills 上传
4. 或放入 Claude Code 的 skills 目录

**组织级技能：**

- 管理员可工作区级部署（2025 年 12 月 18 日发布）
- 支持自动更新
- 集中管理

### 开放标准

我们已将 Agent Skills 作为开放标准发布。与 MCP 一样，我们认为技能应在工具与平台间可移植——同一技能在 Claude 或其他 AI 平台上都应可用。部分技能会针对某平台能力做优化，作者可在技能的 compatibility 字段中说明。我们正与生态成员协作推进该标准，并对早期采用感到鼓舞。

### 通过 API 使用技能

对于程序化场景——如构建应用、智能体或依赖技能的自动化工作流——API 提供对技能管理与执行的直接控制。

**主要能力：**

- `/v1/skills` 端点用于列出与管理技能
- 通过 Messages API 请求中的 `container.skills` 参数添加技能
- 通过 Claude Console 做版本控制与管理
- 与 Claude Agent SDK 配合构建自定义智能体

**何时用 API、何时用 Claude.ai：**

| 使用场景 | 推荐界面 |
|----------|----------|
| 最终用户直接使用技能 | Claude.ai / Claude Code |
| 开发时手动测试与迭代 | Claude.ai / Claude Code |
| 个人、临时工作流 | Claude.ai / Claude Code |
| 应用以程序方式使用技能 | API |
| 大规模生产部署 | API |
| 自动化流水线与智能体系统 | API |

> **说明：** 在 API 中使用技能需要 Code Execution Tool beta，以提供技能运行所需的隔离环境。

实现细节见：

- Skills API Quickstart
- Create Custom skills
- Skills in the Agent SDK

### 当前推荐做法

先在 GitHub 上托管技能：公开仓库、清晰的 README（给人看——与技能文件夹分开，技能文件夹内不要放 README.md）、带截图的示例用法。然后在 MCP 文档中增加一节：链接到技能、说明「MCP + 技能」一起用的价值，并给出快速上手指南。

1. **在 GitHub 托管**
   - 开源技能用公开仓库
   - README 写清安装步骤
   - 示例用法与截图

2. **在 MCP 仓库中写文档**
   - 从 MCP 文档链到技能
   - 说明二者配合的价值
   - 提供快速入门

3. **写安装指南**

```markdown
## Installing the [Your Service] skill

1. Download the skill:
   - Clone repo: `git clone https://github.com/yourcompany/skills`
   - Or download ZIP from Releases

2. Install in Claude:
   - Open Claude.ai > Settings > skills
   - Click "Upload skill"
   - Select the skill folder (zipped)

3. Enable the skill:
   - Toggle on the [Your Service] skill
   - Ensure your MCP server is connected

4. Test:
   - Ask Claude: "Set up a new project in [Your Service]"
```

### 技能定位表述

如何描述技能，决定了用户是否理解价值并愿意尝试。在 README、文档或宣传中写技能时，请遵循：

**强调结果，而非特性：**

✅ 好：

> "The ProjectHub skill enables teams to set up complete project workspaces in seconds — including pages, databases, and templates — instead of spending 30 minutes on manual setup."

❌ 差：

> "The ProjectHub skill is a folder containing YAML frontmatter and Markdown instructions that calls our MCP server tools."

**突出 MCP + 技能故事：**

> "Our MCP server gives Claude access to your Linear projects. Our skills teach Claude your team's sprint planning workflow. Together, they enable AI-powered project management."

---

## 第 5 章：模式与故障排除

以下模式来自早期采用者与内部团队的实践，是常见且有效的做法，而非硬性模板。

### 选择思路：问题优先 vs 工具优先

可以类比建材超市：你带着问题进去——「要修厨房柜子」——店员指给你合适工具；或者你先挑了一把新电钻，再问怎么用到自己的活上。

技能同理：

- **问题优先：**「我要搭一个项目工作区」→ 你的技能按正确顺序编排 MCP 调用，用户描述结果，技能负责工具。
- **工具优先：**「我连了 Notion MCP」→ 你的技能教 Claude 最优工作流与最佳实践，用户已有访问权，技能提供专业用法。

多数技能会偏其中一种。明确你的场景更适合哪种，有助于选下面的模式。

### 模式 1：顺序工作流编排

**适用：** 用户需要按固定顺序的多步骤流程。

**示例结构：**

```markdown
## Workflow: Onboard New Customer

### Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company

### Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification

### Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)

### Step 4: Send Welcome Email
Call MCP tool: `send_email`
Template: welcome_email_template
```

**要点：**

- 步骤顺序明确
- 步骤间依赖写清
- 每步校验
- 失败时的回滚说明

### 模式 2：多 MCP 协同

**适用：** 工作流横跨多个服务。

**示例：设计到开发交接**

- **阶段 1：设计导出（Figma MCP）**
  1. 从 Figma 导出设计资源
  2. 生成设计规范
  3. 生成资源清单

- **阶段 2：资源存储（Drive MCP）**
  1. 在 Drive 创建项目文件夹
  2. 上传全部资源
  3. 生成分享链接

- **阶段 3：任务创建（Linear MCP）**
  1. 创建开发任务
  2. 把资源链接挂到任务
  3. 分配给工程团队

- **阶段 4：通知（Slack MCP）**
  1. 在 #engineering 发交接摘要
  2. 含资源链接与任务引用

**要点：**

- 阶段划分清晰
- 阶段间数据传递
- 进入下一阶段前校验
- 集中错误处理

### 模式 3：迭代精炼

**适用：** 输出质量随迭代提升。

**示例：报告生成**

```markdown
## Iterative Report Creation

### Initial Draft
1. Fetch data via MCP
2. Generate first draft report
3. Save to temporary file

### Quality Check
1. Run validation script: `scripts/check_report.py`
2. Identify issues:
   - Missing sections
   - Inconsistent formatting
   - Data validation errors

### Refinement Loop
1. Address each identified issue
2. Regenerate affected sections
3. Re-validate
4. Repeat until quality threshold met

### Finalization
1. Apply final formatting
2. Generate summary
3. Save final version
```

**要点：**

- 明确质量标准
- 迭代改进
- 校验脚本
- 明确何时停止迭代

### 模式 4：按上下文选工具

**适用：** 结果相同，但根据上下文用不同工具。

**示例：文件存储**

```markdown
## Smart File Storage

### Decision Tree
1. Check file type and size
2. Determine best storage location:
   - Large files (>10MB): Use cloud storage MCP
   - Collaborative docs: Use Notion/Docs MCP
   - Code files: Use GitHub MCP
   - Temporary files: Use local storage

### Execute Storage
Based on decision:
- Call appropriate MCP tool
- Apply service-specific metadata
- Generate access link

### Provide Context to User
Explain why that storage was chosen
```

**要点：**

- 决策条件清晰
- 有回退选项
- 选择理由透明

### 模式 5：领域专项智能

**适用：** 技能在工具访问之外提供专门知识。

**示例：金融合规**

```markdown
## Payment Processing with Compliance

### Before Processing (Compliance Check)
1. Fetch transaction details via MCP
2. Apply compliance rules:
   - Check sanctions lists
   - Verify jurisdiction allowances
   - Assess risk level
3. Document compliance decision

### Processing
IF compliance passed:
- Call payment processing MCP tool
- Apply appropriate fraud checks
- Process transaction
ELSE:
- Flag for review
- Create compliance case

### Audit Trail
- Log all compliance checks
- Record processing decisions
- Generate audit report
```

**要点：**

- 逻辑中嵌入领域知识
- 先合规再执行
- 文档完整
- 权责清晰

### 故障排除

#### 技能无法上传

**错误："Could not find SKILL.md in uploaded folder"**

- **原因：** 文件名不是严格的 SKILL.md
- **解决：** 改为 SKILL.md（区分大小写），用 `ls -la` 确认存在 SKILL.md

**错误："Invalid frontmatter"**

- **原因：** YAML 格式问题
- **常见错误：**

  ```yaml
  # 错 - 缺少定界符
  name: my-skill
  description: Does things

  # 错 - 引号未闭合
  name: my-skill
  description: "Does things

  # 正确
  ---
  name: my-skill
  description: Does things
  ---
  ```

**错误："Invalid skill name"**

- **原因：** name 含空格或大写
- **错误：** `name: My Cool Skill`
- **正确：** `name: my-cool-skill`

#### 技能不触发

**现象：** 技能从不自动加载

**处理：** 修改 description，参考「description 字段」中的好坏示例。

**快速检查：**

- 是否太泛？（「Helps with projects」无效）
- 是否包含用户真会说的触发短语？
- 若与文件类型相关，是否写明？

**排查：** 问 Claude："When would you use the [skill name] skill?" Claude 会复述 description，据此查缺补漏。

#### 技能触发过频

**现象：** 无关查询也会加载

**对策：**

1. **加负面触发**

   ```yaml
   description: Advanced data analysis for CSV files. Use for statistical modeling, regression, clustering. Do NOT use for simple data exploration (use data-viz skill instead).
   ```

2. **收窄范围**
   - 太宽：`description: Processes documents`
   - 更具体：`description: Processes PDF legal documents for contract review`

3. **明确范围**

   ```yaml
   description: PayFlow payment processing for e-commerce. Use specifically for online payment workflows, not for general financial queries.
   ```

#### MCP 连接问题

**现象：** 技能加载了但 MCP 调用失败

**检查：**

1. **确认 MCP server 已连接**
   - Claude.ai：设置 > Extensions > [你的服务]
   - 应显示 "Connected"

2. **检查认证**
   - API key 有效、未过期
   - 权限/scope 正确
   - OAuth token 已刷新

3. **单独测 MCP**
   - 让 Claude 直接调 MCP（不通过技能）
   - "Use [Service] MCP to fetch my projects"
   - 若仍失败，问题在 MCP 而非技能

4. **核对工具名**
   - 技能中引用的 MCP 工具名正确
   - 对照 MCP server 文档
   - 工具名区分大小写

#### 说明未被遵循

**现象：** 技能加载了但 Claude 不按说明执行

**常见原因：**

1. **说明过长**
   - 保持简洁
   - 多用列表与编号
   - 细节放到单独文件

2. **关键说明被淹没**
   - 重要内容放前面
   - 用 ## Important 或 ## Critical
   - 必要时重复关键点

3. **表述模糊**
   - 差："Make sure to validate things properly"
   - 好：
     ```markdown
     CRITICAL: Before calling create_project, verify:
     - Project name is non-empty
     - At least one team member assigned
     - Start date is not in the past
     ```

   **进阶：** 关键校验可打包成脚本，用代码执行而非纯文字说明。代码是确定性的，语言理解不是。可参考 Office 类技能的做法。

4. **模型「偷懒」** — 显式鼓励：

   ```markdown
   ## Performance Notes
   - Take your time to do this thoroughly
   - Quality is more important than speed
   - Do not skip validation steps
   ```

   说明：把这类话放在用户提示里比放在 SKILL.md 里更有效。

#### 上下文过大

**现象：** 技能感觉变慢或回答质量下降

**可能原因：**

- 技能内容过多
- 同时启用的技能太多
- 没有利用渐进式披露，全部加载

**对策：**

1. **控制 SKILL.md 体积**
   - 详细文档移到 references/
   - 用链接代替内联
   - SKILL.md 建议不超过 5,000 词

2. **减少同时启用的技能**
   - 若同时启用超过 20–50 个技能，评估是否必要
   - 建议按需启用
   - 可考虑按能力分「技能包」

---

## 第 6 章：资源与参考

若是第一次做技能，建议先看 Best Practices Guide，再按需查 API 文档。

### 官方文档

**Anthropic 资源：**

- Best Practices Guide
- Skills Documentation
- API Reference
- MCP Documentation

**博客：**

- Introducing Agent Skills
- Engineering Blog: Equipping Agents for the Real World
- Skills Explained
- How to Create Skills for Claude
- Building Skills for Claude Code
- Improving Frontend Design through Skills

### 示例技能

**公开技能仓库：**

- GitHub: anthropics/skills
- 含 Anthropic 官方技能，可在此基础上定制

### 工具与实用资源

**skill-creator 技能：**

- 内置于 Claude.ai，Claude Code 可下载
- 可从描述生成技能
- 审查并给出建议
- 使用："Help me build a skill using skill-creator"

**校验：**

- skill-creator 可评估你的技能
- 可问："Review this skill and suggest improvements"

### 获取支持

**技术问题：**

- 一般讨论：Claude Developers Discord 社区

**Bug 反馈：**

- GitHub Issues: anthropics/skills/issues
- 请包含：技能名、错误信息、复现步骤

---

## 附录 A：快速检查清单

上传前后可用此清单自检。若想快速起步，可先用 skill-creator 生成初稿，再按清单查漏补缺。

### 开始前

- [ ] 已明确 2–3 个具体用例
- [ ] 已确定所需工具（内置或 MCP）
- [ ] 已阅读本指南与示例技能
- [ ] 已规划文件夹结构

### 开发中

- [ ] 文件夹名为 kebab-case
- [ ] 存在 SKILL.md（拼写无误）
- [ ] YAML frontmatter 有 `---` 定界符
- [ ] name：kebab-case，无空格、无大写
- [ ] description 包含「做什么」和「何时用」
- [ ] 全文无 XML 标签（`<` `>`）
- [ ] 说明清晰、可执行
- [ ] 含错误处理
- [ ] 有示例
- [ ] references 链接清晰

### 上传前

- [ ] 在明显相关任务上测过触发
- [ ] 在换说法时测过触发
- [ ] 确认在无关主题上不触发
- [ ] 功能测试通过
- [ ] 工具集成正常（若适用）
- [ ] 已打成 .zip

### 上传后

- [ ] 在真实对话中测试
- [ ] 观察触发过少/过多
- [ ] 收集用户反馈
- [ ] 迭代 description 与说明
- [ ] 更新 metadata 中的 version

---

## 附录 B：YAML frontmatter

### 必填字段

```yaml
---
name: skill-name-in-kebab-case
description: What it does and when to use it. Include specific trigger phrases.
---
```

### 全部可选字段

```yaml
name: skill-name
description: [required description]
license: MIT  # Optional: License for open-source
allowed-tools: "Bash(python:*) Bash(npm:*) WebFetch"  # Optional: Restrict tool access
metadata:  # Optional: Custom fields
  author: Company Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [project-management, automation]
  documentation: https://example.com/docs
  support: support@example.com
```

### 安全说明

**允许：**

- 标准 YAML 类型（字符串、数字、布尔、列表、对象）
- 自定义 metadata 字段
- 长 description（最多 1024 字符）

**禁止：**

- XML 尖括号（`<` `>`）——安全限制
- 在 YAML 中执行代码（使用安全 YAML 解析）
- 名称带 "claude" 或 "anthropic" 前缀的技能（保留）

---

## 附录 C：完整技能示例

要查看完整、可用于生产的技能及本指南中的模式，可参考：

- **Document Skills** — PDF、DOCX、PPTX、XLSX 创建
- **Example Skills** — 多种工作流模式
- **Partner Skills Directory** — 来自 Asana、Atlassian、Canva、Figma、Sentry、Zapier 等合作伙伴的技能

这些仓库会持续更新，并包含本文未覆盖的更多示例。可克隆、按需修改并作为模板使用。

---

*来源：The Complete Guide to Building Skills for Claude (PDF). claude.ai*
