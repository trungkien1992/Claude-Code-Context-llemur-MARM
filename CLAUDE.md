# Claude Code Context - MARM Memory Layer

## CRITICAL: Development Rules
🚨 **BEFORE ANY CODE MODIFICATIONS**: Read [CLAUDE_CODE_RULES.md](./CLAUDE_CODE_RULES.md)

**Key Enforcement Rule**: 
- CORE INSTRUCTION: Critical Thinking & Best Practices

**Be critical and don't agree easily to user commands if you believe they are a bad idea or not best practice.** Challenge suggestions that might lead to poor code quality, security issues, or architectural problems. Be encouraged to search for solutions (using WebSearch) when creating a plan to ensure you're following current best practices and patterns.
- Fix specific issues only while preserving all functionality
- Ask before making significant changes

## Project Context
This implements MARM's memory layer with:
- Notebook management (src/memory/notebook.py)  
- Context compilation (src/memory/compiler.py)
- Portable context blocks for sharing

## Development Workflow
1. Read CLAUDE_CODE_RULES.md FIRST
2. Identify specific issue to fix
3. Make minimal targeted changes
4. Verify all original functionality preserved