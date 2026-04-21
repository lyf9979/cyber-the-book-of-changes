#!/bin/bash
# merge-skill.sh
# 将 skill/SKILL.md + references/*.md 合并为单一系统提示词
# 用于接入不支持文件引用的 LLM 平台（如 ChatGPT 网页、国产模型等）

set -e

OUTPUT="${1:-merged-system-prompt.md}"

cd "$(dirname "$0")/.."

echo "合并 Cyber Book of Changes Skill..."
echo "输出文件：$OUTPUT"
echo ""

cat > "$OUTPUT" <<'EOF'
# Cyber Book of Changes · 赛博周易（系统提示词）

> 本文件是本项目所有规则的合并版本，可直接作为任意 LLM 的 system prompt 使用。

---

EOF

echo "## 主 Skill 定义" >> "$OUTPUT"
echo "" >> "$OUTPUT"
cat skill/SKILL.md >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "---" >> "$OUTPUT"
echo "" >> "$OUTPUT"

for ref in references/*.md; do
    filename=$(basename "$ref" .md)
    echo "## 参考文档：$filename" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    cat "$ref" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    echo "---" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
done

WORD_COUNT=$(wc -w < "$OUTPUT")
CHAR_COUNT=$(wc -m < "$OUTPUT")
LINE_COUNT=$(wc -l < "$OUTPUT")

echo "✅ 合并完成"
echo ""
echo "📄 文件：$OUTPUT"
echo "📊 统计："
echo "   - 行数：$LINE_COUNT"
echo "   - 字符：$CHAR_COUNT"
echo "   - 词数：$WORD_COUNT"
echo ""
echo "💡 使用方法："
echo "   1. 打开目标 LLM 平台（ChatGPT / 通义 / 文心 / 豆包 等）"
echo "   2. 在自定义 GPT / 智能体 的 Instructions 中粘贴 $OUTPUT 的内容"
echo "   3. 测试输入：2001.11.28 00:53 男 算一下八字"
