# 🔮 Cyber Book of Changes · 赛博周易

> 一个面向多 Agent 平台的开源命理分析 skill —— 让 AI 像老先生一样，把八字给你批得明明白白。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-orange.svg)](./skill/SKILL.md)
[![Codex Compatible](https://img.shields.io/badge/Codex-Compatible-green.svg)](./AGENTS.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

---

## ✨ 这是什么

**Cyber Book of Changes（赛博周易）** 是一个基于传统子平术（四柱八字）的 **结构化命理分析 skill**，可直接加载到 Claude、Codex、ChatGPT、Cursor 等主流 Agent 平台，让 LLM 具备全维度命盘分析能力。

### 核心特性

- ✅ **十大维度覆盖**：性格、感情、家庭、财富、健康、事业、配偶、居住/风水、学业考试名气、事件节点
- ✅ **近三年流年建议**：基于当前大运流年输出可操作的具体建议
- ✅ **结构化输出**：排盘 → 格局 → 十大维度 → 流年 → 综合建议，层次清晰
- ✅ **双格式输出**：默认直接文本输出 + 可选精美 HTML 展示
- ✅ **多平台适配**：Claude Skill / OpenAI Codex / ChatGPT / Cursor / Windsurf / 通用 LLM
- ✅ **可追溯**：每个结论都回溯到命盘具体干支，拒绝"玄学黑话"
- ✅ **文化向 + 理性**：纯传统文化解读，不推销、不恐吓、不替代专业决策

---

## 🚀 快速开始

### 方式 1：Claude（推荐）

**Claude Code / Claude.ai Pro**：

```bash
# 克隆项目
git clone https://github.com/lyf9979/cyber-the-book-of-changes.git

# 将 skill/ 目录放入你的 skills 路径
cp -r cyber-the-book-of-changes/skill ~/.claude/skills/cyber-bazi-divination
```

或者在 Claude.ai 的项目中，将 `skill/SKILL.md` 的内容作为 Project Instructions 粘贴。

### 方式 2：OpenAI Codex CLI

将本仓库克隆到本地后：

```bash
cd cyber-the-book-of-changes
# Codex 会自动读取 AGENTS.md 作为项目级 instructions
codex
```

或在 `~/.codex/config.toml` 中添加：

```toml
[projects.bazi]
path = "/path/to/cyber-the-book-of-changes"
instructions_file = "AGENTS.md"
```

### 方式 3：ChatGPT Custom GPT

1. 打开 ChatGPT → 创建 GPT
2. 将 `skill/SKILL.md` 的内容粘贴到 **Instructions**
3. 上传 `references/` 下的文档作为 Knowledge Files
4. 发布即可使用

### 方式 4：Cursor / Windsurf

```bash
# 在项目根目录创建规则文件
cp AGENTS.md .cursorrules
# 或
cp AGENTS.md .windsurfrules
```

### 方式 5：其他 LLM（通义、文心、豆包、智谱、Gemini 等）

将 `skill/SKILL.md` + `references/` 下所有内容合并后作为系统提示词（System Prompt）加载。

详细接入指南见 [`docs/integration.md`](./docs/integration.md)。

---

## 💡 使用示例

**用户输入**：

```
1988.06.15 09:30 女 算一下我的八字
```

**AI 输出结构**：

```
┌─ 一、命盘排列
│   ├─ 四柱八字（表格）
│   ├─ 大运排布
│   ├─ 五行统计
│   └─ 神煞
├─ 二、格局判定
│   ├─ 日主强弱
│   ├─ 格局类型
│   └─ 喜用神 / 忌神
├─ 三、十大维度分析
│   ├─ 1. 性格特质
│   ├─ 2. 感情运势
│   ├─ 3. 家庭与六亲
│   ├─ 4. 财富格局
│   ├─ 5. 健康倾向
│   ├─ 6. 事业方向
│   ├─ 7. 配偶特征
│   ├─ 8. 居住与风水
│   ├─ 9. 学业 / 考试 / 名气
│   └─ 10. 人生事件节点
├─ 四、近三年发展趋势建议
│   ├─ 📅 2026 年（当前流年）
│   ├─ 📅 2027 年
│   └─ 📅 2028 年
└─ 五、综合建议
```

完整示例见 [`examples/example-01.md`](./examples/example-01.md)。
精美 HTML 示例见 [`examples/example-01.html`](./examples/example-01.html)。

---

## 📚 项目结构

```
cyber-the-book-of-changes/
├── AGENTS.md                     # 通用 Agent 入口（Codex 等）
├── README.md                     # 本文件
├── LICENSE                       # MIT 开源协议
├── CONTRIBUTING.md               # 贡献指南
├── skill/
│   └── SKILL.md                  # Claude Skill 入口
├── references/                   # 命理知识库
│   ├── bazi-calculation.md       # 排盘算法
│   ├── yongshen-rules.md         # 格局与用神
│   ├── ten-dimensions.md         # 十大维度分析框架
│   ├── liunian-analysis.md       # 流年大运方法
│   ├── output-template.md        # 文本输出模板
│   └── html-template.md          # HTML 输出模板
├── examples/                     # 分析示例
│   ├── example-01.md             # 文本示例（虚构案例）
│   └── example-01.html           # 精美 HTML 示例（虚构案例）
├── scripts/                      # 辅助脚本
│   └── bazi_calculator.py        # Python 排盘工具
├── docs/
│   └── integration.md            # 多平台接入指南
└── .github/
    └── workflows/
        └── lint.yml              # CI 检查
```

---

## 🎯 十大分析维度

| # | 维度 | 说明 |
|---|------|------|
| 1 | 性格特质 | 基于日主 + 日支 + 月令 + 透干十神 |
| 2 | 感情运势 | 配偶星旺衰 + 配偶宫字性 + 桃花神煞 |
| 3 | 家庭与六亲 | 年月日时柱分别对应祖辈/父母/自身/子女 |
| 4 | 财富格局 | 财星旺衰 + 身财对比 + 食伤生财通道 |
| 5 | 健康倾向 | 五行偏枯对应脏腑 + 冲克刑害 |
| 6 | 事业方向 | 喜用神五行对应行业 + 十神组合 |
| 7 | 配偶特征 | 配偶星五行 + 配偶宫 + 位置远近 |
| 8 | 居住与风水 | 喜用神方位、颜色、环境要素 |
| 9 | 学业 / 考试 / 名气 | 印星 + 官星 + 食伤 + 文昌神煞 |
| 10 | 人生事件节点 | 大运流年的重大节点预测 |

---

## 🔧 Python 排盘工具（可选）

`scripts/bazi_calculator.py` 提供命令行工具：

```bash
python scripts/bazi_calculator.py --date 1988-06-15 --time 09:30 --gender female
```

输出四柱、藏干、十神、大运等核心信息。

> 注：LLM 自身也可完成排盘，此脚本用于需要高精度或批量处理时。

---

## ⚖️ 重要声明

1. **仅为文化传承与研究**：本项目内容属传统命理文化解读，**不构成任何形式的命运预言、人生指导或专业建议**。
2. **不替代专业决策**：涉及健康、法律、金融、婚姻等重大事项，请咨询相应领域的专业人士。
3. **尊重理性与科学**：传统命理不应成为逃避现实、放弃努力的借口。命由己造，相由心生。
4. **不涉及迷信活动**：本项目拒绝推荐任何风水产品、化煞开光等消费行为。

---

## 🤝 贡献

欢迎提交 Issue 与 PR！特别欢迎：

- 完善命理理论细节（附理论依据）
- 增加更多 Agent 平台适配
- 补充分析示例
- 翻译成其他语言
- 改进排盘算法

贡献指南见 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。

---

## 📖 参考典籍

本项目命理理论主要参考：

- 《渊海子平》（宋·徐子平）
- 《三命通会》（明·万民英）
- 《滴天髓》（明·刘伯温 / 清·任铁樵）
- 《子平真诠》（清·沈孝瞻）
- 《穷通宝鉴》（明·余春台）

---

## 📄 License

本项目基于 [MIT License](./LICENSE) 开源。自由使用、修改、分发。

---

## 🌟 Star History

如果这个项目对你有帮助，欢迎 Star ⭐️ 支持！

---

**「命由天定，运由己造；知命者不忧，尽人事以听天命。」**
