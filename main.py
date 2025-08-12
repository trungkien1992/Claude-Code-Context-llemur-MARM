#!/usr/bin/env python3
"""
main.py - Extended Claude context management with MARM memory layer

ARCHITECTURE OVERVIEW:
- Extends context-llemur with MARM memory capabilities
- Two core features: notebook management + context compilation
- Lazy imports avoid dependency issues during development

EXTENSION POINTS:
- Add new @main.command() for top-level commands
- Add new @notebook.command() for notebook operations
- ContextCompiler handles all portable snapshot logic
"""

# @fetch https://click.palletsprojects.com/en/8.1.x/api/#click.group
# Click group documentation for CLI structure patterns
import click

# @fetch https://github.com/jerpint/context-llemur
# Core context management - provides CtxCore.get_active_ctx_path()
from src.memory.notebook import NotebookManager
from src.memory.compiler import ContextCompiler

# @implement: Integrate context management at startup
# - Import CtxCore from context_llemur (assuming it's installed)
# - Use CtxCore.get_active_ctx_path() to load the active context path
# - If no active context, default to creating one with ctx new 'default'
# - Initialize NotebookManager and ContextCompiler with the active path
# - Handle errors gracefully, e.g., echo a message if context not found
try:
    from context_llemur import CtxCore
    ctx_core = CtxCore()
    active_path = ctx_core.get_active_ctx_path()
    if active_path is None:
        click.echo("No active context found. Creating default.")
        # Logic to create and set active context would go here
except ImportError:
    active_path = None
    click.echo("context-llemur not available")

# === CLI STRUCTURE ===
# main() -> root group (extendable with @main.command())
# notebook() -> sub-group (extendable with @notebook.command())

# @implement: Define the main CLI group using @click.group()
# - Set invoke_without_command=True to allow running without subcommands (e.g., show help)
# - Add a result_callback if needed for processing subcommand results
# - Follow multi-command pattern: Allow adding subcommands like 'notebook' later
# - Use context_settings={'help_option_names': ['-h', '--help']} for custom help
@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """Claude context management with MARM memory layer"""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@main.group()
def notebook():
    """Manage runtime notebook (MARM innovation)"""
    pass

# === NOTEBOOK OPERATIONS ===
# Pattern: All notebook commands follow ctx_core -> NotebookManager -> operation
# Add similar commands: get, list, delete, export (see notebook.py:cli for examples)

@notebook.command('add')
@click.argument('key')
@click.argument('value')
def notebook_add(key, value):
    """Add entry to notebook
    
    @fetch https://github.com/jerpint/context-llemur/blob/main/README.md#notebook-management
    @implement:
        1. Validate key format (alphanumeric, underscore, dash only)
        2. Check value length against MARM limits (see NotebookManager.MAX_ENTRY_SIZE)
        3. Use lazy import pattern for context_llemur dependency
        4. Get active context path via CtxCore.get_active_ctx_path()
        5. Create NotebookManager instance and call add(key, value)
        6. Display success/error with appropriate emoji feedback
    @ai-context: Part of MARM memory layer - entries persist across Claude sessions
    @pattern Command https://refactoring.guru/design-patterns/command
    """
    # Lazy import pattern - prevents startup failures if context-llemur missing
    try:
        from context_llemur import CtxCore
        ctx_core = CtxCore()
    except ImportError:
        click.echo("❌ context-llemur not available. Install with: pip install context-llemur")
        return
    
    ctx_path = ctx_core.get_active_ctx_path()
    if not ctx_path:
        click.echo("❌ No active context")
        return
    
    manager = NotebookManager(ctx_path)
    success, message = manager.add(key, value)
    click.echo(f"✅ {message}" if success else f"❌ {message}")

# === CONTEXT COMPILATION ===
# MARM's core innovation: portable context blocks for cross-session sharing
# Output format must remain stable for compatibility

@main.command()
@click.argument('name', required=False)
@click.option('--fields', help='Fields to include')
def compile(name, fields):
    """Compile context into portable snapshot (MARM innovation)
    
    @fetch https://github.com/jerpint/context-llemur/blob/main/README.md#context-compilation
    @fetch https://docs.python.org/3/library/json.html#json.dumps
    @implement:
        1. Auto-generate timestamp-based name if not provided
        2. Validate fields parameter format (comma-separated string)
        3. Get active context using CtxCore.get_active_ctx_path()
        4. Create ContextCompiler instance with context path
        5. Call compiler.compile() with parsed fields list
        6. Generate portable reseed block using create_reseed_block()
        7. Output reseed block to console (consider clipboard integration)
    @ai-context: Core MARM feature - creates portable context blocks for sharing across sessions
    @pattern Builder https://refactoring.guru/design-patterns/builder
    """
    try:
        from context_llemur import CtxCore
        ctx_core = CtxCore()
    except ImportError:
        click.echo("❌ context-llemur not available. Install with: pip install context-llemur")
        return
    
    ctx_path = ctx_core.get_active_ctx_path()
    if not ctx_path:
        click.echo("❌ No active context")
        return
    
    compiler = ContextCompiler(ctx_path)
    compilation = compiler.compile(name, fields.split(',') if fields else None)
    reseed_block = compiler.create_reseed_block(compilation)
    click.echo(reseed_block)

# === ENTRY POINTS ===
# cli_main() allows standalone execution: python main.py
# For distribution, use pyproject.toml [project.scripts]

def cli_main():
    """Entry point for standalone usage"""
    main()

if __name__ == "__main__":
    cli_main()
