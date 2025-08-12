#!/bin/bash
# extract-annotations.sh - Extract AI annotations from codebase
#
# @fetch https://www.gnu.org/software/grep/manual/grep.html Grep manual
# @implement: Extract @fetch, @implement, @ai-context annotations from all source files
# @ai-context: Helps maintain documentation and AI guidance across the project

echo "# AI Annotations Report"
echo "Generated: $(date)"
echo ""

echo "## Found Annotations:"
echo ""

find . -name "*.py" -o -name "*.sh" -o -name "*.md" | \
grep -v ".venv" | \
grep -v "__pycache__" | \
xargs grep -n -H "@fetch\|@implement\|@ai-context\|@pattern" | \
while IFS=: read -r file line content; do
    echo "**File:** $file:$line"
    echo "**Content:** $content"
    echo ""
done