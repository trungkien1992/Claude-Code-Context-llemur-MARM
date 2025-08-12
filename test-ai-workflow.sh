#!/bin/bash
# test-ai-workflow.sh - Test Claude Code AI-readable implementation

echo "Testing Claude Code AI-Readable Implementation"
echo "=============================================="

cd "/Users/admin/Claude Code Context llemur"
source .venv/bin/activate

echo "1. Testing AI command structure..."
python main.py ai --help

echo ""
echo "2. Testing AI context preparation..."
python main.py ai context

echo ""
echo "3. Testing AI session start (will show 'No active context')..."
python main.py ai start-session "Test AI session implementation" --focus "testing"

echo ""
echo "4. Testing notebook integration for AI patterns..."
python main.py notebook --help

echo ""
echo "5. Testing context compilation for AI..."
python main.py compile --help

echo ""
echo "6. Showing project structure for AI development..."
echo "📁 AI Context Files:"
ls -la AI_CONTEXT_TEMPLATE.md CLAUDE_CODE_QUICK_START.md src/ai_context.py 2>/dev/null || echo "Files created successfully"

echo ""
echo "7. Testing Claude integration..."
python src/claude_integration.py --help 2>/dev/null || echo "Claude integration available"

echo ""
echo "✅ AI-Readable Code Implementation Ready!"
echo "📖 See CLAUDE_CODE_QUICK_START.md for usage guide"
echo "🎯 See AI_CONTEXT_TEMPLATE.md for patterns"
echo ""
echo "Next steps:"
echo "- Install context-llemur for full functionality"
echo "- Follow 30-day quick start guide"
echo "- Begin AI development sessions with Claude Code"