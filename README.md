# Claude Code Context-Llemur with MARM Memory Layer

Enhanced Context-Llemur with MARM's memory innovations for persistent knowledge management across Claude sessions.

## 🚀 Features

### Core MARM Memory System
- **Runtime Notebook**: User-controlled knowledge base with 30 entries, 30KB limit
- **Context Compilation**: Portable snapshots with git integration
- **Claude Code Integration**: Enhanced context preparation for Claude Code
- **Markdown Export**: Documentation-ready format export
- **Artifacts Import**: Import Claude-generated artifacts back into system

### Enhanced Capabilities
- MARM-compliant memory limits for optimal Claude compatibility
- Comprehensive AI annotations throughout codebase
- Graceful degradation when dependencies are unavailable
- Professional code formatting and testing

## 📦 Installation

### Method 1: Install from PyPI (Recommended)
```bash
pip install claude-code-context-llemur
```

### Method 2: Development Installation
```bash
git clone https://github.com/trungkien1992/Claude-Code-Context-llemur-MARM.git
cd Claude-Code-Context-llemur-MARM
pip install -e ".[memory]"
```

### Dependencies
- **Required**: `context-llemur>=0.2.2`, `click`, `GitPython`
- **Optional**: `pyperclip` (for clipboard integration)

## 🎯 Quick Start

### 1. Create a New Context
```bash
ctx new my-project
```

### 2. Add Knowledge to Notebook
```bash
ctx notebook add "api_key" "sk-test-12345"
ctx notebook add "endpoint" "https://api.example.com"
ctx notebook add "current_task" "Implementing authentication"
```

### 3. List Notebook Entries
```bash
ctx notebook list
# Shows: 📔 Notebook Entries (3/30)
```

### 4. Create Context Compilation
```bash
ctx compile "auth-implementation"
# Creates portable context block
```

### 5. Prepare Context for Claude Code
```bash
python -m claude_integration --copy
# Copies comprehensive context to clipboard
```

## 📖 Complete CLI Reference

### Notebook Management
```bash
ctx notebook add <key> <value>       # Add entry (max 2048 chars)
ctx notebook get <key>               # Get specific entry
ctx notebook list                    # List all entries
ctx notebook delete <key>            # Delete entry
ctx notebook export                  # Export as markdown
```

### Context Compilation
```bash
ctx compile [name]                   # Create snapshot
ctx compile --fields key1,key2       # Compile specific fields
ctx compile list                     # List all compilations
ctx compile load <name>              # Load compilation
ctx compile delete <name>            # Delete compilation
ctx compile export-md <name>         # Export as markdown
ctx compile import-artifacts <file>  # Import Claude artifacts
```

### Claude Integration
```bash
python -m claude_integration         # Show context
python -m claude_integration --copy  # Copy to clipboard
```

## 🔧 Advanced Usage

### Export for Documentation
```bash
# Export compilation as structured markdown
ctx compile export-md my-snapshot --output docs/context.md
```

### Import Claude Artifacts
```bash
# Save Claude artifacts as JSON, then import
ctx compile import-artifacts my-artifacts.json
```

### Backup and Restore
```bash
# Export notebook for backup
ctx notebook export > backup.md

# Check MARM compliance
ctx notebook list  # Shows current usage: (15/30 entries)
```

## 🏗️ Project Structure

```
src/
├── memory/
│   ├── notebook.py       # MARM notebook management
│   ├── compiler.py       # Context compilation with git integration
│   └── session.py        # Session management (future)
├── claude_integration.py # Claude Code integration
tests/
├── test_notebook.py      # Notebook functionality tests
└── test_compiler.py      # Compiler tests
docs/
├── MEMORY.md             # Complete usage guide
├── AI-annotations.md     # AI annotation system
└── CLAUDE_CODE_RULES.md  # Development guidelines
```

## 💡 Use Cases

### For Developers
- Maintain context across long coding sessions
- Share project state with team members
- Document API keys and configurations
- Track current bugs and solutions

### For Claude Code Users
- Enhanced context preparation
- Persistent memory across sessions
- Import/export Claude artifacts
- Structured documentation generation

### For Teams
- Share compiled contexts via markdown export
- Maintain project knowledge base
- Track development progress
- Document architectural decisions

## 🔍 Examples

### Example 1: API Development
```bash
ctx notebook add "base_url" "https://api.myservice.com/v1"
ctx notebook add "auth_header" "Authorization: Bearer ${TOKEN}"
ctx notebook add "current_endpoint" "POST /users - Creating user registration"
ctx compile "user-api-v1"
```

### Example 2: Bug Tracking
```bash
ctx notebook add "bug_id" "#1234"
ctx notebook add "symptoms" "Login fails with 403 on prod"
ctx notebook add "hypothesis" "Token validation issue in middleware"
ctx notebook add "solution" "Updated token refresh logic in auth.py"
```

### Example 3: Documentation Workflow
```bash
# Work on features
ctx notebook add "feature" "Dark mode toggle"
ctx notebook add "files_modified" "src/components/ThemeToggle.tsx, src/styles/themes.css"

# Compile and export
ctx compile "dark-mode-implementation"
ctx compile export-md "dark-mode-implementation" --output docs/features/dark-mode.md
```

## 🧪 Testing

```bash
# Run unit tests
pytest tests/ -v

# Run integration tests
./test-workflow.sh

# Extract AI annotations
./extract-annotations.sh
```

## 🔗 Integration with Context-Llemur

This project extends [context-llemur](https://github.com/jerpint/context-llemur) with MARM memory capabilities:
- Preserves all original context-llemur functionality
- Adds memory layer on top of existing system  
- Graceful fallback when context-llemur is unavailable
- Compatible with existing workflows

## 📚 Documentation

- **[MEMORY.md](./MEMORY.md)** - Complete feature guide and examples
- **[AI-annotations.md](./AI-annotations.md)** - AI annotation system documentation
- **[CLAUDE_CODE_RULES.md](./CLAUDE_CODE_RULES.md)** - Development guidelines

## 🤝 Contributing

1. Read [CLAUDE_CODE_RULES.md](./CLAUDE_CODE_RULES.md) for development guidelines
2. Run the complete test suite: `pytest tests/ -v && ./test-workflow.sh`
3. Ensure code formatting: `black src/ && isort src/`
4. Submit PR with comprehensive description

## 📄 License

This project extends context-llemur and maintains compatibility with its licensing terms.

## 🔄 Version History

- **v2.0.0**: Enhanced MARM memory layer with markdown export and Claude artifacts import
- **v1.0.0**: Initial MARM memory implementation