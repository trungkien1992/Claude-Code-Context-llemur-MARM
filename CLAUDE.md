# Claude Code Context - MARM Memory Layer

## CRITICAL: Development Rules
🚨 **BEFORE ANY CODE MODIFICATIONS**: Read [CLAUDE_CODE_RULES.md](./CLAUDE_CODE_RULES.md)

**Key Enforcement Rule**: 
- NEVER recreate user-provided complete code
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