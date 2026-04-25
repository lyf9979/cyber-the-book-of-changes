# Cyber Book of Changes · 赛博周易

> 面向 Claude、Codex、ChatGPT、Cursor、Windsurf 与通用 LLM Agent 的多场景中文命理分析 skill。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-orange.svg)](./skill/SKILL.md)
[![Codex Compatible](https://img.shields.io/badge/Codex-Compatible-green.svg)](./AGENTS.md)
[![Release](https://img.shields.io/github/v/release/lyf9979/cyber-the-book-of-changes)](https://github.com/lyf9979/cyber-the-book-of-changes/releases)
[![NPX Ready](https://img.shields.io/badge/NPX-ready-brightgreen)](./package.json)
[![Contributors](https://img.shields.io/badge/contributors-welcome-blue)](./CONTRIBUTORS.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

---

## 这是什么

**Cyber Book of Changes（赛博周易）** 原本是一个单人八字深度分析 skill，现在已扩写为多场景命理工具箱。它以传统子平术（四柱八字）为基础，复用排盘、用神、十神、流年、大运等核心能力，再按不同用户场景加载对应 reference 文档，默认生成可直接打开的 `.html` 报告文件。

本项目强调三条边界：

- 传统文化解读，不做绝对预言。
- 不替代医疗、法律、金融、心理治疗或重大人生决策。
- 不推荐开光、护符、化煞物品等消费。

---

## 核心能力

| 模式 | 场景 | 输出 |
|---|---|---|
| `single_bazi` | 单人八字深度分析 | 十大维度 + 2026–2028 逐月趋势 + 执行清单 |
| `compatibility` | 两人姻缘合婚 | 合婚评分、8 维关系分析、协同点与摩擦点 |
| `wedding_date` | 结婚 / 订婚 / 领证择日 | Top 10 推荐日期、月度热度、避开日期 |
| `child_planning` | 生育规划 | 属相、出生月份、时辰倾向、受孕窗口区间 |
| `palm_face` | 手相 / 面相 + 八字 | 图像特征、八字交叉验证、印证/补充/矛盾标签 |
| `quick_flow` | 流年速测 | 当前年/月速读评分与行动建议 |
| `naming` | 宝宝起名 / 成人改名 | 5–10 个候选名、五行补益、音形义分析 |
| `fengshui` | 家居 / 办公方位 | 喜用方位、空间布局、颜色材质建议 |
| `career_pivot` | 跳槽 / 转型择时 | 未来 12 个月行动窗口与准备清单 |
| `wealth_timing` | 财运 / 大额支出择时 | 未来 24 个月财务窗口与避险提醒 |
| `taisui` | 本命年 / 太岁 | 未来 12 年太岁时间线与行为清单 |
| `dream` | 梦境 + 八字综合 | 梦境符号、流年流月关联、现实提醒 |
| `consultation` | AI 命理顾问追问 | 基于已生成报告回答具体问题 |

---

## 快速开始

### npx 一键安装

需要 Node.js 18+。

```bash
# 安装到 Claude skills
npx github:lyf9979/cyber-the-book-of-changes install --target claude

# 安装到 Codex skills
npx github:lyf9979/cyber-the-book-of-changes install --target codex

# 同时安装到 Claude + Codex
npx github:lyf9979/cyber-the-book-of-changes install --target all
```

当 npm 包发布后，也可使用：

```bash
npx cyber-bazi-skill install --target all
```

### Claude

```bash
git clone https://github.com/lyf9979/cyber-the-book-of-changes.git
cp -r cyber-the-book-of-changes/skill ~/.claude/skills/cyber-bazi-divination
```

Claude.ai Projects 可将 [skill/SKILL.md](./skill/SKILL.md) 作为 Project Instructions，并上传 `references/` 目录作为知识文件。

### OpenAI Codex CLI

```bash
git clone https://github.com/lyf9979/cyber-the-book-of-changes.git
cd cyber-the-book-of-changes
codex
```

Codex 会读取项目根目录 [AGENTS.md](./AGENTS.md)。

### ChatGPT / Gemini / 国产模型

将 [skill/SKILL.md](./skill/SKILL.md) 与 `references/` 下的文档合并后作为系统提示词。也可使用：

```bash
bash scripts/merge-skill.sh
```

更多平台接入见 [docs/integration.md](./docs/integration.md)。

---

## 使用示例

```text
1988.06.15 09:30 女 算一下我的八字
```

```text
我和对象想合婚：A 是 1993-04-20 08:30 男，B 是 1995-08-15 19:20 女
```

```text
我们准备 2027 年结婚，帮我们挑几个适合领证和办婚礼的日子
```

```text
想 2026-2028 之间备孕，看看哪个出生月份更适合我们家庭
```

```text
根据八字和这张手相图，交叉看一下近期状态
```

---

## 输出形式

默认输出可打开的 HTML 文件：

- 命盘排列
- 格局与用神
- 场景专属分析
- 近三年或指定时间范围趋势
- 总结与执行清单
- 合规声明
- 零 CDN
- 可离线打开
- 响应式
- 可打印
- 支持双盘对比、日历视图、热力矩阵、评分圆环、八方位罗盘等组件

文件输出约定：

- 有文件系统能力的 Agent 必须保存到 `outputs/` 目录。
- 推荐命名：`outputs/<YYYYMMDD-HHMMSS>-<mode>-report.html`。
- 生成后必须在控制台/最终回复中打印：`HTML 报告已生成：<文件路径>`。
- 路径优先使用绝对路径，方便用户直接复制到浏览器或文件管理器打开。
- 最终回复只给 HTML 文件路径和简短说明，不把整份 HTML 粘贴到聊天窗口。
- Claude / ChatGPT 等不能直接写文件的平台，应优先创建 HTML Artifact、Canvas 或附件。
- 只有用户明确要求“Markdown / 纯文本 / 调试文本 / 不要 HTML”时，才使用 Markdown 输出模板。

无论单人八字、合婚、择日、起名、风水、梦境等哪个场景，默认最终报告都应是一个能打开看的 HTML 文件。

示例：

- [examples/example-01.md](./examples/example-01.md)
- [examples/example-01.html](./examples/example-01.html)

---

## 项目结构

```text
cyber-the-book-of-changes/
├── AGENTS.md
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CONTRIBUTORS.md
├── package.json
├── bin/
│   └── cyber-bazi-skill.js
├── skill/
│   └── SKILL.md
├── references/
│   ├── bazi-calculation.md
│   ├── yongshen-rules.md
│   ├── ten-dimensions.md
│   ├── liunian-analysis.md
│   ├── output-template.md
│   ├── html-template.md
│   ├── compatibility-rules.md
│   ├── couple-dimensions.md
│   ├── wedding-selection.md
│   ├── child-conception.md
│   ├── child-dimensions.md
│   ├── palm-face-rules.md
│   ├── quick-flow.md
│   ├── naming-rules.md
│   ├── name-database.md
│   ├── fengshui-positions.md
│   ├── career-pivot.md
│   ├── wealth-timing.md
│   ├── taisui-rules.md
│   └── dream-symbols.md
├── scripts/
│   ├── bazi_calculator.py
│   ├── merge-skill.sh
│   └── requirements.txt
├── outputs/
│   └── .gitkeep
├── examples/
│   ├── example-01.md
│   └── example-01.html
├── docs/
│   └── integration.md
└── .github/workflows/
    ├── lint.yml
    └── release.yml
```

---

## 扩展路线

本次扩写参考本地《skill 扩展方案》中的四阶段路线：

| 阶段 | 功能 | 状态 |
|---|---|---|
| 第一波 | 手相面相、流年速测、AI 顾问问答 | 已加入 skill 规则与 reference |
| 第二波 | 姻缘合婚、起名改名、事业择时、财运择时 | 已加入 skill 规则与 reference |
| 第三波 | 结婚择日、梦境解读 | 已加入 skill 规则与 reference |
| 第四波 | 生育规划、风水方位、太岁提醒 | 已加入 skill 规则与 reference |

说明：当前版本已完成 prompt/skill 知识层扩写。日期扫描、生育枚举、起名候选生成等场景后续可继续增强为 Python 脚本。

---

## 无环境可用

普通用户不需要安装 Python、C++ 编译环境或 `sxtwl` 才能使用本 skill。Agent 应按下面的降级策略工作，避免反复提示安装依赖造成 token 消耗：

- 优先使用本地 `scripts/bazi_calculator.py` 做一次高精度排盘。
- 如果本地没有 Python、缺少 `sxtwl`、缺少 C++ 构建工具或脚本运行失败，立即停止安装尝试。
- 若用户已经提供完整四柱，直接按用户四柱分析，并标注“user provided”。
- 若用户只提供出生时间，则按 reference 规则做 LLM 近似排盘，并标注“LLM approximate / 近似排盘”。
- 最终 HTML 报告必须写明排盘来源与置信度。

---

## 推荐安装高精度排盘依赖

如果你希望每次排盘尽量准确，推荐在使用前先安装 Python 依赖。这样 Agent 可以直接调用本地 `sxtwl` 历法库完成高精度四柱排盘，不需要靠近似推算。

### 1. 确认已安装 Python

```bash
python --version
```

如果提示找不到 `python`，请先安装 Python 3.9+，然后重新打开终端。

### 2. 安装依赖

在项目根目录运行：

```bash
pip install -r scripts/requirements.txt
```

如果你只想单独安装排盘核心依赖，也可以运行：

```bash
pip install sxtwl
```

### 3. 验证排盘工具

```bash
python scripts/bazi_calculator.py --date 1988-06-15 --time 09:30 --gender female
```

能看到四柱、藏干、十神、大运等信息，就说明高精度排盘工具可用。

如果安装失败，不要反复重试或让 Agent 一直安装依赖。直接继续使用 skill 即可，系统会降级为用户提供四柱或 LLM 近似排盘，并在 HTML 报告里标注排盘来源与置信度。

---

## 可选 Python 排盘工具

```bash
pip install -r scripts/requirements.txt
python scripts/bazi_calculator.py --date 1988-06-15 --time 09:30 --gender female
```

排盘工具基于 `sxtwl`，用于精确生成四柱、藏干、十神、大运、流年等基础数据。它是增强能力，不是使用 skill 的硬性前置条件。

---

## 合规声明

本项目内容属于传统命理文化解读，仅供文化体验、自我反思与娱乐参考。

本项目不构成：

- 医疗诊断或治疗建议
- 法律、金融、投资建议
- 心理治疗建议
- 婚姻、生育、职业等重大人生决策结论
- 寿命判断、性别选择、容貌评价

涉及现实重大决策时，请结合现实条件、专业意见与个人意愿综合判断。

---

## Contributors

| Contributor | Role |
|---|---|
| [@lyf9979](https://github.com/lyf9979) | Creator / Maintainer |
| Claude (Anthropic) | AI-assisted drafting and documentation collaboration |
| Codex (OpenAI) | Repository implementation and release automation support |

更多见 [CONTRIBUTORS.md](./CONTRIBUTORS.md)。

---

## Releases

本项目支持 GitHub Releases。维护者推送语义化 tag 后会自动生成 release 资产：

```bash
git tag v0.2.0
git push origin v0.2.0
```

---

## License

MIT License，详见 [LICENSE](./LICENSE)。
