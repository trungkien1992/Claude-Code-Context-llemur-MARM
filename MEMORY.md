# Memory Layer for Context-Llemur

## Overview
This enhancement adds MARM's memory innovations to Context-Llemur:
- **Runtime Notebook**: User-controlled knowledge base
- **Context Compilation**: Portable context snapshots
- **Claude Integration**: Enhanced context for Claude Code

## New Commands

### Notebook Management
```bash
ctx notebook add <key> <value>    # Add entry
ctx notebook get <key>            # Get entry
ctx notebook list                 # List all entries
ctx notebook delete <key>         # Delete entry
ctx notebook export               # Export as text
```

### Context Compilation
```bash
ctx compile [name]                # Create snapshot
ctx compile --fields key1,key2    # Compile specific fields
ctx compile list                  # List all compilations
ctx compile load <name>           # Load compilation
ctx compile delete <name>         # Delete compilation
ctx compile export-md <name>      # Export as markdown
ctx compile import-artifacts <file> # Import Claude artifacts
```

### Claude Integration
```bash
python src/claude_integration.py     # Prepare Claude context
python src/claude_integration.py --copy  # Copy to clipboard
```

## Architecture

### Memory Components
- `src/memory/notebook.py` - MARM-compliant notebook management
- `src/memory/compiler.py` - Context compilation with git integration
- `src/claude_integration.py` - Claude Code context preparation

### MARM Compliance
- Max 30 notebook entries
- 30,000 character total limit
- 2,048 characters per entry
- Timestamp tracking for all entries

### Data Persistence
```
context/
├── memory/
│   ├── notebook.json       # Runtime notebook entries
│   └── snapshots/          # Compiled context snapshots
└── ...
```

## Usage Examples

### Basic Workflow
```bash
# Set up context
ctx new my-project

# Add to notebook
ctx notebook add "api_key" "sk-test-12345"
ctx notebook add "endpoint" "https://api.example.com"
ctx notebook add "bug_status" "Fixed authentication issue"

# Create snapshot
ctx compile "auth-fix-v1"

# Prepare for Claude Code
python src/claude_integration.py --copy
```

### Advanced Usage
```bash
# Export notebook for backup
ctx notebook export > backup.md

# Compile specific fields only
ctx compile snapshot-name --fields api_key,endpoint

# Export compilation as markdown for documentation
ctx compile export-md my-snapshot --output snapshot.md

# Import Claude artifacts back into system
ctx compile import-artifacts artifacts.json

# Check notebook usage
ctx notebook list  # Shows 3/30 entries

# List all compilations
ctx compile list
```

## Integration Points

### With Context-Llemur
- Extends existing context management
- Preserves all original functionality  
- Adds memory layer on top

### With Claude Code
- Provides comprehensive context
- Includes git status and project structure
- Formats output for optimal Claude understanding

### With MARM Systems
- Compatible with MARM memory specifications
- Supports cross-session knowledge sharing
- Maintains compliance limits

## Development Notes

### AI Annotations
The codebase uses standardized AI annotations:
- `@fetch` - Documentation references
- `@implement` - Implementation guidance
- `@ai-context` - AI understanding context
- `@pattern` - Design pattern references

Extract annotations with:
```bash
./extract-annotations.sh
```

### Testing
```bash
./test-workflow.sh    # Comprehensive system test
```

### Dependencies
- `context-llemur>=0.2.2` - Base system
- `click` - CLI framework  
- `GitPython` - Git integration
- `pyperclip` - Clipboard support (optional)

## Troubleshooting

### Common Issues
1. **"No active context"** - Run `ctx new project-name` first
2. **"context-llemur not available"** - Install with `pip install context-llemur`
3. **CLI commands not found** - Install package with `pip install -e .`

### Verification
```bash
# Check CLI is working
python main.py --help

# Test Claude integration
python src/claude_integration.py

# Verify annotations
./extract-annotations.sh | head -20
```

## New Features Added

### Markdown Export
Export any compilation as structured markdown for documentation:
```bash
ctx compile export-md my-snapshot
ctx compile export-md my-snapshot --output docs/context.md
```

### Claude Artifacts Import
Import Claude-generated artifacts back into the MARM system:
```bash
# Save Claude artifacts as JSON file, then:
ctx compile import-artifacts my-artifacts.json
```

This creates a new compilation with:
- Notebook entries for artifact metadata
- Static files for code content
- MARM compliance validation
- Automatic timestamping

### Enhanced AI Annotations
The codebase now includes comprehensive AI annotations:
- `@fetch` - Documentation references
- `@implement` - Implementation guidance  
- `@ai-context` - AI understanding context
- `@pattern` - Design pattern references

Extract all annotations:
```bash
./extract-annotations.sh
```

## Future Enhancements
- Session management (`src/memory/session.py`)
- Multi-context notebook sharing
- Advanced compilation filters
- Cloud synchronization support
- Real-time collaboration features
- Enhanced Claude integration