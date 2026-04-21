# 多平台接入指南

本 skill 设计为可被任意 LLM Agent 平台接入。以下是主流平台的具体接入方法。

## 目录

- [Claude](#claude)
- [OpenAI Codex CLI](#openai-codex-cli)
- [ChatGPT Custom GPT](#chatgpt-custom-gpt)
- [Cursor](#cursor)
- [Windsurf](#windsurf)
- [GitHub Copilot Chat](#github-copilot-chat)
- [Google Gemini](#google-gemini)
- [国产模型（通义、文心、豆包、智谱等）](#国产模型)
- [通用 API 集成](#通用-api-集成)

---

## Claude

### 方式 1：Claude Code（本地）

Claude Code 原生支持 skill 格式：

```bash
git clone https://github.com/lyf9979/cyber-the-book-of-changes.git
mkdir -p ~/.claude/skills
cp -r cyber-the-book-of-changes/skill ~/.claude/skills/cyber-bazi-divination
```

重启 Claude Code，skill 即可自动被触发。

### 方式 2：Claude.ai Projects

1. 登录 claude.ai
2. 创建一个 Project
3. 将 `skill/SKILL.md` 的内容粘贴到 "Project Instructions"
4. 将 `references/` 目录下所有文件通过 "Add files" 上传至 Project Knowledge

### 方式 3：Anthropic API

```python
import anthropic

# 加载 skill 内容
with open("skill/SKILL.md") as f:
    skill_content = f.read()

# 加载参考文档
reference_docs = {}
for name in ["bazi-calculation", "yongshen-rules", "ten-dimensions",
             "liunian-analysis", "output-template"]:
    with open(f"references/{name}.md") as f:
        reference_docs[name] = f.read()

system_prompt = f"""
{skill_content}

## 参考文档

### bazi-calculation.md
{reference_docs['bazi-calculation']}

### yongshen-rules.md
{reference_docs['yongshen-rules']}

### ten-dimensions.md
{reference_docs['ten-dimensions']}

### liunian-analysis.md
{reference_docs['liunian-analysis']}

### output-template.md
{reference_docs['output-template']}
"""

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=8000,
    system=system_prompt,
    messages=[{"role": "user", "content": "2001.11.28 00:53 男 算一下"}]
)
print(response.content[0].text)
```

---

## OpenAI Codex CLI

Codex CLI 会自动读取项目根目录的 `AGENTS.md` 作为 project-level instructions。

### 方式 1：作为工作目录

```bash
git clone https://github.com/lyf9979/cyber-the-book-of-changes.git
cd cyber-the-book-of-changes
codex
# Codex 会自动加载 AGENTS.md
```

### 方式 2：全局配置

在 `~/.codex/AGENTS.md` 中添加：

```markdown
# 全局指令

当用户请求算命、批八字、看命盘时，请遵循以下项目的规则：
[引用本项目 AGENTS.md 全部内容]
```

### 方式 3：按项目配置

在 `~/.codex/config.toml` 中添加：

```toml
[projects.bazi-divination]
name = "赛博周易"
instructions = "/path/to/cyber-the-book-of-changes/AGENTS.md"
```

---

## ChatGPT Custom GPT

### 步骤

1. 访问 https://chat.openai.com/gpts/editor
2. 点击 "Create a GPT"
3. 在 **Configure** 标签页：
   - **Name**: 赛博周易
   - **Description**: 传统八字命理全维度分析
   - **Instructions**: 粘贴 `skill/SKILL.md` 的全部内容
4. **Knowledge**：上传 `references/` 目录下所有 `.md` 文件
5. **Capabilities**：可关闭 Web Browsing 和 DALL·E，保留 Code Interpreter（可选）
6. **Conversation starters** 建议：
   - "帮我算八字：[生日] [时间] [性别]"
   - "看看我未来三年的运势"
   - "我的事业方向适合什么行业？"
7. 保存并发布

---

## Cursor

Cursor 支持项目级 AI 指令文件 `.cursorrules`。

```bash
cd cyber-the-book-of-changes
cp AGENTS.md .cursorrules
```

或者在任意项目中引用：

```bash
# 在你的项目根目录
cat > .cursorrules <<EOF
# 引用赛博周易 skill
[粘贴 AGENTS.md 内容]
EOF
```

---

## Windsurf

Windsurf 类似 Cursor：

```bash
cp AGENTS.md .windsurfrules
```

---

## GitHub Copilot Chat

Copilot Chat 目前对项目级指令支持有限。推荐方式：

1. 在 VS Code 中打开本项目
2. 使用 `@workspace` 引用本项目作为上下文
3. 或在 Copilot Chat 设置中添加 custom instructions，内容为 `AGENTS.md` 的核心要点

---

## Google Gemini

### Gemini API

```python
import google.generativeai as genai

# 加载所有文档
with open("skill/SKILL.md") as f:
    system_prompt = f.read()

# ... 拼接 references 同 Claude 示例

model = genai.GenerativeModel(
    model_name="gemini-2.0-pro",
    system_instruction=system_prompt
)

response = model.generate_content("2001.11.28 00:53 男")
print(response.text)
```

### Gemini Web（gemini.google.com）

将 `skill/SKILL.md` + 所有 `references/` 合并后粘贴到对话开头作为系统指令。

### Gemini Gem

创建一个自定义 Gem，将 `skill/SKILL.md` 内容作为 Instructions。

---

## 国产模型

### 通义千问

1. 访问 https://tongyi.aliyun.com/
2. 创建"智能体"，将 `skill/SKILL.md` + `references/*` 合并作为系统提示
3. 发布使用

### 文心一言 / 百度智能云

使用百度千帆平台，将合并后的内容作为 Prompt 模板。

### 豆包（字节）

在扣子（Coze）平台创建 Bot，将内容作为 Persona Prompt。

### 智谱清言（ChatGLM）

在智能体平台创建"命理分析师"角色，加载本项目内容。

### DeepSeek / Kimi / 讯飞星火

同样方式：合并所有 markdown 文件内容作为系统提示词。

---

## 通用 API 集成

### 合并文档的 Shell 脚本

```bash
#!/bin/bash
# merge-skill.sh - 将所有 skill 文档合并为单个系统提示词

OUTPUT="merged-system-prompt.md"

echo "# Cyber Book of Changes - Merged System Prompt" > $OUTPUT
echo "" >> $OUTPUT

cat skill/SKILL.md >> $OUTPUT
echo -e "\n\n---\n\n" >> $OUTPUT

for ref in references/*.md; do
    echo "## 参考文档：$(basename $ref)" >> $OUTPUT
    echo "" >> $OUTPUT
    cat $ref >> $OUTPUT
    echo -e "\n\n---\n\n" >> $OUTPUT
done

echo "合并完成，输出至 $OUTPUT"
echo "总字数：$(wc -w < $OUTPUT)"
```

使用：

```bash
chmod +x merge-skill.sh
./merge-skill.sh
# 然后将 merged-system-prompt.md 作为任意 LLM 的系统提示
```

### 注意事项

1. **上下文长度**：合并后文档约 15K–20K tokens，大部分现代模型（Claude/GPT-4/Gemini Pro）都能容纳
2. **温度参数**：建议 `temperature=0.7` 以平衡稳定性与文采
3. **max_tokens**：建议设置 4000+ 以保证完整输出
4. **流式输出**：长文本建议开启流式输出改善用户体验

---

## 测试验证

接入后使用以下标准输入测试：

```
请分析：2001.11.28 00:53 男
```

检查输出应包含：
- ✅ 四柱排盘（辛巳 己亥 戊寅 壬子）
- ✅ 十大维度全部覆盖
- ✅ 近三年流年建议
- ✅ 综合建议收尾
- ✅ 不含绝对预言和玄学黑话

---

## 问题反馈

接入过程中遇到问题，请在项目 Issues 中反馈：
https://github.com/lyf9979/cyber-the-book-of-changes/issues
