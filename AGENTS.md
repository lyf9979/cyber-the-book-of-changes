# AGENTS.md

> 此文件为 **OpenAI Codex CLI / ChatGPT Agents / 通用 LLM Agents** 提供项目入口指令。
> Claude 用户请直接参考 `skill/SKILL.md`。

## 项目定位

**赛博周易 · Cyber Book of Changes** 是一个基于传统子平术（四柱八字）的多场景命理分析 skill/prompt 工程项目，为各大 Agent 平台提供即插即用的命理工具箱能力。

## 触发条件

当用户满足以下任一条件时，启动本项目的分析流程：

1. 提供了出生年月日时（公历或农历）和性别
2. 使用关键词："算命""批八字""看命盘""四柱""周易""命理""生辰"
3. 请求分析"我的命运""我的运势""我的事业/感情/财运"等
4. 请求"合婚""姻缘配对""结婚吉日""择日""备孕""起名""手相""面相""跳槽择时""财运择时""太岁""梦境解读"等扩展场景

## 执行流程（Agent 必须严格按此顺序）

### Step 0: 判断模式

根据用户意图选择模式，再加载对应文档：

| 模式 | 场景 | 参考文档 |
|------|------|---------|
| `single_bazi` | 单人八字深度报告 | `bazi-calculation.md`、`yongshen-rules.md`、`ten-dimensions.md`、`liunian-analysis.md` |
| `compatibility` | 两人姻缘合婚 | `compatibility-rules.md`、`couple-dimensions.md` |
| `wedding_date` | 结婚/订婚/领证择日 | `wedding-selection.md` |
| `child_planning` | 生育规划、属相月份时辰 | `child-conception.md`、`child-dimensions.md` |
| `palm_face` | 手相/面相图片分析 | `palm-face-rules.md` |
| `quick_flow` | 流年速测 | `quick-flow.md` |
| `naming` | 起名/改名 | `naming-rules.md`、`name-database.md` |
| `fengshui` | 家居/办公风水方位 | `fengshui-positions.md` |
| `career_pivot` | 跳槽/转型择时 | `career-pivot.md` |
| `wealth_timing` | 财运/投资/大额支出择时 | `wealth-timing.md` |
| `taisui` | 本命年/太岁提醒 | `taisui-rules.md` |
| `dream` | 梦境与八字综合解读 | `dream-symbols.md` |
| `consultation` | 已有报告后的追问 | 复用已生成报告与相关文档 |

### Step 1: 信息收集

确认以下信息完整，缺一不可：
- [ ] 出生日期（公历还是农历需明确）
- [ ] 出生时间（精确到时辰，模糊则追问）
- [ ] 性别
- [ ] 出生地（可选）

若不完整，**先追问再开始**。

### Step 2: 读取参考文档

按需加载以下参考文档（位于 `references/` 目录）：

| 文档 | 用途 |
|------|------|
| `bazi-calculation.md` | 排盘算法与藏干、十神规则 |
| `yongshen-rules.md` | 格局与用神判定 |
| `ten-dimensions.md` | 十大维度分析框架 |
| `liunian-analysis.md` | 流年大运分析方法 |
| `html-template.md` | 默认单文件 HTML 输出模板 |
| `output-template.md` | 仅在用户明确要求 Markdown/纯文本时使用 |
| `compatibility-rules.md` | 合婚评分与双盘规则 |
| `couple-dimensions.md` | 合婚八维分析 |
| `wedding-selection.md` | 结婚择日 |
| `child-conception.md` | 生育规划 |
| `child-dimensions.md` | 子女简化十维 |
| `palm-face-rules.md` | 手相面相交叉分析 |
| `quick-flow.md` | 流年速测 |
| `naming-rules.md` / `name-database.md` | 起名改名 |
| `fengshui-positions.md` | 风水方位 |
| `career-pivot.md` | 事业转型择时 |
| `wealth-timing.md` | 财运择时 |
| `taisui-rules.md` | 太岁本命年 |
| `dream-symbols.md` | 梦境综合解读 |

### Step 3: 排盘

1. 计算四柱（年月日时）
2. 列出藏干
3. 标注十神
4. 统计五行
5. 排大运（7–8 步）
6. 可选：标注神煞

排盘工具与降级规则：
- `scripts/bazi_calculator.py` 是可选高精度工具，不是普通用户运行 skill 的必要条件。
- Agent 不得反复要求用户安装 Python、C++ 构建环境或 `sxtwl`，也不得循环执行安装命令消耗 token。
- 本地排盘最多尝试一次；若脚本不可用、依赖缺失、构建失败或用户环境不支持，立即停止工具尝试并降级。
- 降级顺序：优先使用用户提供的完整四柱；若用户未提供，则按 `references/bazi-calculation.md` 做 LLM 近似排盘。
- 最终 HTML 必须标注排盘来源：`sxtwl local`、`user provided` 或 `LLM approximate`，并写明置信度。

### Step 4: 格局与用神判定

- 日主强弱
- 格局类型
- 喜用神、忌神
- 命局特点总结

### Step 5: 十大维度分析

**顺序不可调换**：
1. 性格特质
2. 感情运势
3. 家庭与六亲
4. 财富格局
5. 健康倾向
6. 事业方向
7. 配偶特征
8. 居住与风水
9. 学业 / 考试 / 名气
10. 人生事件节点

深度要求：
- 每个维度至少 500 字
- 每个维度都要包含：命盘依据、现实表现、风险点、优化建议

### Step 6: 近三年流年趋势（2026–2028）

- 2026 年（按月总结）
- 2027 年（按月总结）
- 2028 年（按月总结）

每年包含：总评、关键维度、行动建议、1–12 月逐月表（主线/风险/动作/优先级）。

### Step 7: 综合建议收尾

必须输出“总结与执行清单”：
- 30 天执行清单
- 90 天执行清单
- 年度执行清单
- 每月/每季度复盘机制

### Step 8: 扩展场景输出

- 合婚：输出总分、8 维对比、协同点、摩擦点、未来三年共同节点。
- 择日：输出 Top 10 日期、月度热度、避开日期、现实档期提醒。
- 生育：输出候选月份、受孕窗口、属相合冲、子女简化十维；不得涉及性别选择。
- 手相/面相：先描述可见特征，再与八字做印证/补充/矛盾对照。
- 起名：输出 5–10 个候选名，包含五行补益、音律、字义与风险提示。
- 事业/财运择时：输出月度窗口表与行动清单；不构成职业或投资建议。
- 风水：只给方位、颜色、空间节律建议，不推荐实物商品。

## 输出约束

- **总字数**：建议 9000–15000 字
- **格式**：
  - 默认：严格按照 `references/html-template.md` 生成完整单文件 HTML，从 `<!doctype html>` 开始
  - 文件优先：在 Codex、Claude Code、Cursor、Windsurf 等具备文件系统能力的环境中，必须写入 `outputs/<YYYYMMDD-HHMMSS>-<mode>-report.html`
  - 最终回复：只返回生成的 HTML 文件路径和一句简短说明，不要在控制台/聊天中粘贴整份 HTML
  - 全场景：无论使用哪个 reference，最终都必须用可打开的 HTML 文件呈现，不以控制台式 Markdown 作为最终报告
  - 无文件系统兜底：若平台不能写入文件，则生成 HTML Artifact / Canvas / 附件；仍不支持时，才输出带文件名提示的完整 HTML 代码块
  - 例外：仅当用户明确要求 Markdown、纯文本、调试文本或不要 HTML 时，才使用 `references/output-template.md`
- **语言**：中文，专业中带温度
- **禁止**：
  - 绝对化预言（"一定""必定""注定"）
  - 玄学黑话（"前世因果""天定"）
  - 恐吓式表达
  - 推荐具体风水消费产品
  - 诊断疾病
  - 承诺特定结果
  - 性别选择、寿命判断、容貌评价

## 适配的 Agent 平台

| 平台 | 入口文件 | 说明 |
|------|---------|------|
| **Claude（API / claude.ai / Claude Code）** | `skill/SKILL.md` | 原生 skill 格式 |
| **OpenAI Codex CLI** | `AGENTS.md`（本文件） + `~/.codex/config.toml` | 可作为项目级指令 |
| **ChatGPT Custom GPT** | `skill/SKILL.md` 内容作为 Instructions | 需手动粘贴 |
| **Cursor** | `.cursorrules` | 引用本文件 |
| **Windsurf** | `.windsurfrules` | 引用本文件 |
| **Gemini / Copilot Chat** | 将 `skill/SKILL.md` 作为 system prompt | 需手动配置 |
| **国产模型（通义、文心、豆包、智谱等）** | 将 `skill/SKILL.md` 内容作为系统提示 | 需手动配置 |

详细配置方法见 `docs/integration.md`。

## 目录结构

```
cyber-the-book-of-changes/
├── AGENTS.md                     # 本文件，Codex / 通用 Agent 入口
├── README.md                     # 项目说明
├── LICENSE                       # 开源协议（MIT）
├── skill/
│   └── SKILL.md                  # Claude skill 入口
├── references/                   # 知识库
│   ├── bazi-calculation.md       # 排盘算法
│   ├── yongshen-rules.md         # 用神规则
│   ├── ten-dimensions.md         # 十大维度
│   ├── liunian-analysis.md       # 流年分析
│   ├── output-template.md        # 输出模板
│   ├── html-template.md          # HTML 输出模板
│   ├── compatibility-rules.md    # 合婚规则
│   ├── couple-dimensions.md      # 合婚八维
│   ├── wedding-selection.md      # 结婚择日
│   ├── child-conception.md       # 生育规划
│   ├── child-dimensions.md       # 子女简化十维
│   ├── palm-face-rules.md        # 手相面相
│   ├── quick-flow.md             # 流年速测
│   ├── naming-rules.md           # 起名规则
│   ├── name-database.md          # 五行字库
│   ├── fengshui-positions.md     # 风水方位
│   ├── career-pivot.md           # 事业择时
│   ├── wealth-timing.md          # 财运择时
│   ├── taisui-rules.md           # 太岁规则
│   └── dream-symbols.md          # 梦境解读
├── examples/                     # 示例命盘分析
│   ├── example-01.md
│   └── example-01.html
├── scripts/                      # 辅助脚本（可选）
│   └── bazi_calculator.py
├── docs/
│   └── integration.md            # 多平台接入指南
└── .github/
    └── workflows/
        └── lint.yml              # CI 检查
```

## 禁忌（所有 Agent 必须遵守）

1. **不替代医生**：健康部分只提倾向，不诊断
2. **不替代法律/金融顾问**：重大决策提醒咨询专业人士
3. **不推销风水产品**：不推荐开光、化煞物品消费
4. **不预言生死**：对寿元等敏感话题保持克制
5. **尊重用户**：不因命局差而唱衰，不因命局好而过度吹捧
6. **保持理性**：传统文化解读不应成为逃避现实的借口

## 贡献指南

欢迎提交 PR 改进此项目。修改 `references/` 下文档需附带说明与理论依据。

## 开源协议

MIT License — 详见 `LICENSE` 文件。
