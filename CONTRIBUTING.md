# 贡献指南 Contributing Guide

感谢你对 **赛博周易 Cyber Book of Changes** 项目的兴趣！

## 贡献方式

### 1. 报告问题（Issue）

如果你发现：
- 排盘结果错误（如日柱算错、起运岁数偏差）
- 命理分析建议不合理
- 文档错别字或理解歧义
- Agent 平台接入失败

请在 [Issues](https://github.com/lyf9979/cyber-the-book-of-changes/issues) 页面反馈。

**Issue 模板**：

```
### 问题描述


### 复现步骤


### 预期行为


### 实际行为


### 环境
- 平台：（Claude / Codex / ChatGPT ...）
- 模型版本：
- OS：
```

### 2. 提交代码（PR）

#### 工作流

1. Fork 本仓库
2. 创建分支：`git checkout -b feat/my-feature`
3. 提交改动：`git commit -m "feat: 增加 xxx"`
4. 推送：`git push origin feat/my-feature`
5. 在 GitHub 提交 Pull Request

#### Commit 规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档改动
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 杂项

示例：
```
feat: 在 ten-dimensions.md 中增加配偶年龄差分析方法
fix: 修复 sxtwl 节气索引错误导致的起运岁数偏差
docs: 完善 Cursor 平台接入步骤
```

### 3. 改进命理知识库

修改 `references/` 下任何文档时：
- **必须附带理论依据**（引用经典典籍、学术论文、权威流派）
- 避免引入个人玄学观点或无依据的主观判断
- 不引入商业导向内容（风水产品、开光物品等）

**参考典籍白名单**：
- 《渊海子平》《三命通会》《滴天髓》《子平真诠》《穷通宝鉴》
- 《命理探源》《子平粹言》《精选命理约言》
- 学术期刊关于传统命理文化研究的论文

### 4. 添加新平台适配

若你发现本项目还未适配某个 Agent 平台（如新的国产模型、新发布的 AI IDE），欢迎：

1. 在 `docs/integration.md` 中新增一节
2. 按现有格式说明接入方式
3. 提供一个可工作的最小示例
4. 在 `AGENTS.md` 的平台对照表中补齐

### 5. 添加分析示例

欢迎在 `examples/` 目录添加更多示例：

文件命名：`example-<编号>.md`（如 `example-02.md`）
内容要求：
- 完整覆盖十大维度 + 近三年流年
- 排盘数据来自本项目的 `bazi_calculator.py`
- 隐去真实个人隐私（可虚构命例，但要注明"演示用例"）
- 字数控制在 3000–6000 字

## 代码规范

### Python 代码

- 遵循 PEP 8
- 使用 type hints
- 关键函数需 docstring
- 新增功能需添加示例用法

### 文档规范

- Markdown 遵循 CommonMark
- 中文与英文/数字之间留空格（如"乙木 日主 生于 亥 月"）
- 表格对齐清晰
- 大段文本分段清晰，避免"墙一样"的段落

## 禁忌

以下内容不会被接受：

1. ❌ 推广任何商业风水/命理产品
2. ❌ 宣扬"绝对命定论"或贬低个人努力
3. ❌ 添加可能伤害使用者的内容（如鼓励自残、诅咒他人）
4. ❌ 未经充分理论支撑的"个人流派"私货
5. ❌ 大段引用未授权的版权内容（古籍除外，古籍为公有领域）

## 社区准则

- 保持理性讨论，尊重不同命理流派（子平、盲派、新派、滴天髓派等）
- 不人身攻击、不歧视、不煽动对立
- 讨论限于学术与工程层面，不进行"算命预言"贸然断事
- 欢迎学术辩论，拒绝人身诋毁

## 许可

贡献的内容将以 [MIT License](./LICENSE) 发布。提交 PR 即表示你同意以 MIT 协议授权你的贡献。

---

再次感谢你的贡献！🌿
