# Claude Code Context llemur

MARM Memory Layer Implementation with Context-llemur integration

## 🚨 DEVELOPMENT GUIDELINES - READ FIRST 🚨

### MANDATORY SESSION START CHECKLIST:
- [ ] ✅ Read [CLAUDE_CODE_RULES.md](./CLAUDE_CODE_RULES.md) BEFORE any code changes
- [ ] ⚡ Remember: **PRESERVE BEFORE MODIFY** - Never recreate user code
- [ ] 🎯 Fix specific issues only - no wholesale rewrites  
- [ ] 🤝 Ask before making significant changes

### Violation Prevention
**This rule exists because Claude recreated complete user code instead of fixing a simple encoding issue. This must not happen again.**

## Project Structure

```
src/
├── memory/
│   ├── notebook.py    # MARM notebook management with CLI
│   ├── compiler.py    # Context compilation with reseed blocks
│   └── session.py     # Session management (TBD)
tests/
├── test_notebook.py   # Notebook functionality tests
└── test_compiler.py   # Compiler tests (TBD)
```

## Installation

```bash
# Install with memory extras
pip install -e ".[memory]"

# Or using uv  
uv pip install -e ".[memory]"
```

## CLI Usage

```bash
# Notebook commands
ctx-notebook add "key" "value"
ctx-notebook get "key" 
ctx-notebook list
ctx-notebook delete "key"
ctx-notebook export

# Compiler commands  
ctx-compile snapshot-name
ctx-compile load snapshot-name
ctx-compile list
ctx-compile delete snapshot-name
```