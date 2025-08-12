#!/usr/bin/env python3
"""
Claude Code integration - prepares context for Claude

@fetch https://docs.anthropic.com/en/docs/claude-code Claude Code documentation
@fetch https://click.palletsprojects.com/en/8.1.x/ Click CLI framework
@implement:
    1. Gather context from multiple sources (git, notebook, files)
    2. Format output for Claude Code consumption
    3. Support clipboard integration for easy sharing
    4. Handle missing dependencies gracefully
@ai-context: Core integration point between MARM memory system and Claude Code
@pattern Facade https://refactoring.guru/design-patterns/facade
"""

import json
from pathlib import Path
import click
from datetime import datetime

def prepare_claude_context():
    """Prepare complete context for Claude Code
    
    @implement:
        1. Check for context-llemur availability and active context
        2. Load notebook entries from memory/notebook.json
        3. Extract git information (branch, commits) 
        4. Generate project structure summary
        5. Format everything for Claude Code consumption
    @ai-context: Output format must be stable for Claude Code compatibility
    """
    output = "=" * 70 + "\n"
    output += "CLAUDE CODE CONTEXT\n"
    output += "=" * 70 + "\n\n"
    
    # Try to get active context, but work without it
    ctx_path = None
    try:
        from context_llemur import CtxCore
        core = CtxCore()
        ctx_path = core.get_active_ctx_path()
    except ImportError:
        output += "⚠️  context-llemur not available - showing project structure instead\n\n"
        ctx_path = Path.cwd()
    
    if not ctx_path:
        output += "❌ No active context\n"
        return output
    
    # 1. Static files (goals.txt, rules.txt)
    for filename in ['goals.txt', 'rules.txt']:
        filepath = ctx_path / filename
        if filepath.exists():
            output += f"[{filename}]\n"
            output += filepath.read_text() + "\n\n"
    
    # 2. Notebook entries (if available)
    notebook_path = ctx_path / 'memory' / 'notebook.json'
    if notebook_path.exists():
        try:
            notebook_data = json.loads(notebook_path.read_text())
            if notebook_data:
                output += "📔 RUNTIME NOTEBOOK:\n"
                output += "-" * 40 + "\n"
                for key, entry in notebook_data.items():
                    value = entry.get('value', entry) if isinstance(entry, dict) else entry
                    output += f"• {key}: {value}\n"
                output += "\n"
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # 3. Current git status (if in git repo)
    try:
        from git import Repo
        repo = Repo(ctx_path)
        output += f"🌿 Current Branch: {repo.active_branch.name}\n"
        
        # Recent commits
        try:
            commits = list(repo.iter_commits('HEAD', max_count=5))
            if commits:
                output += "\nRecent Activity:\n"
                for commit in commits:
                    output += f"  {commit.hexsha[:7]}: {commit.message.strip()[:50]}\n"
            else:
                output += "\n📝 No commits yet\n"
        except Exception:
            output += "\n📝 No commits yet\n"
    except Exception:
        output += "📁 Not a git repository or git not available\n"
    
    # 4. Project structure
    output += f"\n📊 Project Structure (from {ctx_path}):\n"
    output += "-" * 40 + "\n"
    
    # Show key files
    key_files = ['README.md', 'CLAUDE.md', 'main.py', 'pyproject.toml']
    for filename in key_files:
        filepath = ctx_path / filename
        if filepath.exists():
            output += f"✅ {filename}\n"
    
    # Show src structure
    src_path = ctx_path / 'src'
    if src_path.exists():
        output += "\nSource files:\n"
        for py_file in src_path.rglob('*.py'):
            rel_path = py_file.relative_to(ctx_path)
            output += f"  📄 {rel_path}\n"
    
    output += f"\n⏰ Generated: {datetime.now().isoformat()}\n"
    
    return output

@click.command()
@click.option('--copy', is_flag=True, help='Copy to clipboard')
def claude(copy):
    """Prepare context for Claude Code"""
    context = prepare_claude_context()
    click.echo(context)
    
    if copy:
        try:
            import pyperclip
            pyperclip.copy(context)
            click.echo("\n✅ Copied to clipboard!")
        except ImportError:
            click.echo("\n💡 Install pyperclip: pip install pyperclip")

if __name__ == '__main__':
    claude()