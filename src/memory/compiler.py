#!/usr/bin/env python3
"""
src/memory/compiler.py - Context compilation and reseeding
Implements MARM's portable context blocks

@fetch https://docs.python.org/3/library/json.html
@fetch https://gitpython.readthedocs.io/en/stable/tutorial.html
@ai-context: MARM's core innovation - portable context blocks for cross-session sharing
"""

# @fetch https://docs.python.org/3/library/json.html#json.dumps
# JSON serialization for compilation data
import json
from datetime import datetime
# @fetch https://docs.python.org/3/library/pathlib.html#pathlib.Path
# Path operations for file system management
from pathlib import Path
from typing import Any, Dict, List, Optional

# @fetch https://click.palletsprojects.com/en/8.1.x/
# CLI framework for command-line interface
import click
from ..cli_utils import require_context_llemur, copy_to_clipboard
# @fetch https://gitpython.readthedocs.io/en/stable/reference.html#git.repo.base.Repo
# Git repository operations for context information
try:
    from git import Repo
    HAS_GIT = True
except ImportError:
    HAS_GIT = False


class ContextCompiler:
    """Compiles context into portable snapshots

    CRITICAL: This implements MARM's core innovation - portable context blocks
    that can be shared across different Claude sessions and contexts.
    """

    def __init__(self, ctx_path: Path):
        self.ctx_path = ctx_path
        self.memory_dir = ctx_path / "memory"
        self.compilations_dir = self.memory_dir / "compilations"
        self._ensure_structure()

    def _ensure_structure(self):
        """Ensure compilations directory exists"""
        self.memory_dir.mkdir(exist_ok=True)
        self.compilations_dir.mkdir(exist_ok=True)

    def compile(
        self, name: Optional[str] = None, fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compile current context into portable snapshot
        This is MARM's key innovation - portable context blocks

        @implement:
            1. Generate timestamp-based name if not provided
            2. Collect static files (goals.txt, rules.txt, ctx.txt)
            3. Include notebook entries from memory/notebook.json
            4. Extract git information (branch, recent commits)
            5. Calculate metadata (entry counts, total size)
            6. Apply field filtering if specified
            7. Save compilation to disk and return data structure
        @ai-context: Output format must remain compatible with create_reseed_block()
        @pattern Builder https://refactoring.guru/design-patterns/builder
        """
        if not name:
            name = f"snapshot-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        compilation = {
            "name": name,
            "created": datetime.now().isoformat(),
            "context_path": str(self.ctx_path),
            "static_files": {},
            "notebook": {},
            "git_info": {},
            "metadata": {},
        }

        # 1. Collect static files - standard Claude context files
        static_files = ["goals.txt", "rules.txt", "ctx.txt"]
        for filename in static_files:
            filepath = self.ctx_path / filename
            if filepath.exists():
                compilation["static_files"][filename] = filepath.read_text()

        # 2. Collect notebook entries - MARM memory layer
        notebook_path = self.memory_dir / "notebook.json"
        if notebook_path.exists():
            compilation["notebook"] = json.loads(notebook_path.read_text())

        # 3. Collect git information
        if HAS_GIT:
            try:
                repo = Repo(self.ctx_path)
                compilation["git_info"] = {
                    "current_branch": repo.active_branch.name,
                    "recent_commits": [],
                }

                # Get last 10 commits
                for commit in list(repo.iter_commits("HEAD", max_count=10)):
                    compilation["git_info"]["recent_commits"].append(
                        {
                            "sha": commit.hexsha[:7],
                            "message": commit.message.strip(),
                            "author": str(commit.author),
                            "date": commit.committed_datetime.isoformat(),
                        }
                    )
            except Exception as e:
                compilation["git_info"] = {"error": str(e)}
        else:
            compilation["git_info"] = {"error": "Git not available"}

        # 4. Add metadata
        compilation["metadata"] = {
            "total_notebook_entries": len(compilation["notebook"]),
            "total_static_files": len(compilation["static_files"]),
            "compilation_size": 0,  # Will calculate after
        }

        # Apply field filter if specified
        if fields:
            filtered = {}
            for field in fields:
                if field in compilation:
                    filtered[field] = compilation[field]
            compilation = filtered

        # Calculate size
        compilation_json = json.dumps(compilation)
        if "metadata" in compilation:
            compilation["metadata"]["compilation_size"] = len(compilation_json)

        # Save compilation
        compilation_path = self.compilations_dir / f"{name}.json"
        compilation_path.write_text(json.dumps(compilation, indent=2))

        return compilation

    def create_reseed_block(self, compilation: Dict[str, Any]) -> str:
        """
        Create portable text block that can be pasted anywhere
        This is the core MARM innovation - human-readable context sharing

        @implement:
            1. Create bordered header with compilation metadata
            2. Add static files section with content previews
            3. Include notebook entries in bullet format
            4. Show git context (branch, recent commits)
            5. Add metadata summary (counts, sizes)
            6. Include usage instructions at bottom
        @ai-context: Format must be parseable by humans and compatible with Claude
        @pattern Template Method https://refactoring.guru/design-patterns/template-method
        """
        block = "=" * 70 + "\n"
        block += "📋 PORTABLE CONTEXT BLOCK\n"
        block += f"📋 Created: {compilation.get('created', 'Unknown')}\n"
        block += f"📋 Name: {compilation.get('name', 'Unknown')}\n"
        block += "=" * 70 + "\n\n"

        # Static files section
        if "static_files" in compilation and compilation["static_files"]:
            block += "📋 STATIC CONTEXT FILES:\n"
            block += "-" * 40 + "\n"
            for filename, content in compilation["static_files"].items():
                # Show first 200 chars of each file
                preview = content[:200] + "..." if len(content) > 200 else content
                block += f"\n[{filename}]\n{preview}\n"
            block += "\n"

        # Notebook entries section
        if "notebook" in compilation and compilation["notebook"]:
            block += "📋 NOTEBOOK ENTRIES:\n"
            block += "-" * 40 + "\n"
            for key, entry in compilation["notebook"].items():
                value = entry["value"] if isinstance(entry, dict) else entry
                block += f"• {key}: {value}\n"
            block += "\n"

        # Git information section
        if "git_info" in compilation and compilation["git_info"]:
            git = compilation["git_info"]
            block += "<? GIT CONTEXT:\n"
            block += "-" * 40 + "\n"
            block += f"Current Branch: {git.get('current_branch', 'unknown')}\n"

            if "recent_commits" in git and git["recent_commits"]:
                block += "\nRecent Commits:\n"
                for commit in git["recent_commits"][:5]:
                    block += f"  {commit['sha']}: {commit['message'][:50]}\n"
            block += "\n"

        # Metadata section
        if "metadata" in compilation:
            meta = compilation["metadata"]
            block += "📋 METADATA:\n"
            block += "-" * 40 + "\n"
            block += f"Notebook Entries: {meta.get('total_notebook_entries', 0)}\n"
            block += f"Static Files: {meta.get('total_static_files', 0)}\n"
            block += f"Total Size: {meta.get('compilation_size', 0)} bytes\n"

        block += "\n" + "=" * 70 + "\n"
        block += "📋 To load this context: ctx load-compilation <name>\n"
        block += "=" * 70

        return block

    def load(self, name: str) -> tuple[bool, str, Optional[Dict]]:
        """Load a previously compiled context - merges with existing notebook"""
        compilation_path = self.compilations_dir / f"{name}.json"

        if not compilation_path.exists():
            available = [f.stem for f in self.compilations_dir.glob("*.json")]
            return (
                False,
                f"Compilation '{name}' not found. Available: {', '.join(available)}",
                None,
            )

        try:
            compilation = json.loads(compilation_path.read_text())

            # Restore notebook entries if present
            if "notebook" in compilation and compilation["notebook"]:
                notebook_path = self.memory_dir / "notebook.json"
                current_notebook = {}

                if notebook_path.exists():
                    current_notebook = json.loads(notebook_path.read_text())

                # Merge with existing notebook - preserves current entries
                for key, entry in compilation["notebook"].items():
                    if key not in current_notebook:  # No overwrite - safer for users
                        current_notebook[key] = entry

                notebook_path.write_text(json.dumps(current_notebook, indent=2))

            return True, f"Loaded compilation: {name}", compilation

        except Exception as e:
            return False, f"Error loading compilation: {e}", None

    def list_compilations(self) -> List[Dict[str, Any]]:
        """List all available compilations"""
        compilations = []

        for compilation_file in self.compilations_dir.glob("*.json"):
            try:
                data = json.loads(compilation_file.read_text())
                compilations.append(
                    {
                        "name": compilation_file.stem,
                        "created": data.get("created", "Unknown"),
                        "size": compilation_file.stat().st_size,
                        "notebook_entries": len(data.get("notebook", {})),
                        "static_files": len(data.get("static_files", {})),
                    }
                )
            except:
                continue

        return sorted(compilations, key=lambda x: x["created"], reverse=True)

    def export_to_markdown(self, compilation: Dict[str, Any]) -> str:
        """Export compilation as markdown

        @fetch https://daringfireball.net/projects/markdown/syntax Markdown syntax reference
        @implement:
            1. Create structured markdown document with headers
            2. Include metadata table with compilation info
            3. Add static files as code blocks with language hints
            4. Format notebook entries as definition list
            5. Include git information as nested lists
            6. Add footer with export timestamp and instructions
        @ai-context: Markdown format enables easy sharing and version control
        @pattern Template Method https://refactoring.guru/design-patterns/template-method
        """
        md = f"# Context Compilation: {compilation.get('name', 'Unnamed')}\n\n"

        # Metadata table
        md += "## Metadata\n\n"
        md += "| Property | Value |\n"
        md += "|----------|-------|\n"
        md += f"| Created | {compilation.get('created', 'Unknown')} |\n"
        md += f"| Context Path | `{compilation.get('context_path', 'Unknown')}` |\n"

        if "metadata" in compilation:
            meta = compilation["metadata"]
            md += f"| Notebook Entries | {meta.get('total_notebook_entries', 0)} |\n"
            md += f"| Static Files | {meta.get('total_static_files', 0)} |\n"
            md += f"| Total Size | {meta.get('compilation_size', 0)} bytes |\n"

        md += "\n"

        # Static files section
        if "static_files" in compilation and compilation["static_files"]:
            md += "## Static Context Files\n\n"
            for filename, content in compilation["static_files"].items():
                md += f"### {filename}\n\n"
                md += "```\n"
                md += content
                md += "\n```\n\n"

        # Notebook entries section
        if "notebook" in compilation and compilation["notebook"]:
            md += "## Notebook Entries\n\n"
            for key, entry in compilation["notebook"].items():
                value = entry["value"] if isinstance(entry, dict) else entry
                created = (
                    entry.get("created", "Unknown")
                    if isinstance(entry, dict)
                    else "Unknown"
                )
                md += f"**{key}**\n: {value}\n: *Created: {created}*\n\n"

        # Git information section
        if "git_info" in compilation and compilation["git_info"]:
            git = compilation["git_info"]
            md += "## Git Context\n\n"
            md += f"**Current Branch:** {git.get('current_branch', 'unknown')}\n\n"

            if "recent_commits" in git and git["recent_commits"]:
                md += "**Recent Commits:**\n\n"
                for commit in git["recent_commits"]:
                    md += f"- `{commit['sha']}` {commit['message']} *(by {commit['author']})*\n"
                md += "\n"

        # Footer
        md += "---\n\n"
        md += f"*Exported: {datetime.now().isoformat()}*\n\n"
        md += "**Usage:** Save this file and reference during development or paste into Claude Code for context.\n"

        return md

    def import_from_claude_artifacts(self, artifacts_json: str) -> tuple[bool, str]:
        """Import context from Claude artifacts

        @fetch https://docs.anthropic.com/claude/docs/artifacts Claude artifacts documentation
        @implement:
            1. Parse artifacts JSON structure (id, type, title, content)
            2. Extract relevant context from code artifacts
            3. Create notebook entries from artifact metadata
            4. Generate new compilation with imported data
            5. Validate imported data against MARM limits
            6. Save as new compilation with artifact-based name
        @ai-context: Enables importing Claude-generated code and context back into MARM system
        @pattern Adapter https://refactoring.guru/design-patterns/adapter
        """
        try:
            artifacts = json.loads(artifacts_json)
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {e}"

        # Handle both single artifact and array of artifacts
        if not isinstance(artifacts, list):
            artifacts = [artifacts]

        imported_entries = {}
        static_files = {}

        for i, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                continue

            artifact_id = artifact.get("id", f"artifact_{i}")
            artifact_type = artifact.get("type", "unknown")
            title = artifact.get("title", f"Untitled {artifact_type}")
            content = artifact.get("content", "")

            # Create notebook entry for artifact metadata
            notebook_key = f"artifact_{artifact_id}"
            imported_entries[notebook_key] = {
                "value": f"Type: {artifact_type}, Title: {title}",
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
            }

            # If it's a code artifact, save as static file
            if artifact_type in ["code", "text", "markdown"] and content:
                # Sanitize filename
                filename = f"{artifact_id}_{artifact_type}.txt"
                static_files[filename] = content

        # Create compilation from imported data
        compilation_name = f"claude_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        compilation = {
            "name": compilation_name,
            "created": datetime.now().isoformat(),
            "context_path": str(self.ctx_path),
            "static_files": static_files,
            "notebook": imported_entries,
            "git_info": {"source": "claude_artifacts_import"},
            "metadata": {
                "total_notebook_entries": len(imported_entries),
                "total_static_files": len(static_files),
                "import_source": "claude_artifacts",
                "original_artifact_count": len(artifacts),
            },
        }

        # Validate against MARM limits
        if len(imported_entries) > 30:  # NotebookManager.MAX_ENTRIES
            return (
                False,
                f"Too many entries ({len(imported_entries)}). MARM limit is 30.",
            )

        total_size = len(json.dumps(compilation))
        if total_size > 30000:  # NotebookManager.MAX_TOTAL_SIZE
            return (
                False,
                f"Compilation too large ({total_size} bytes). MARM limit is 30,000.",
            )

        # Save compilation
        compilation_path = self.compilations_dir / f"{compilation_name}.json"
        compilation_path.write_text(json.dumps(compilation, indent=2))

        # Optionally merge into current notebook (ask user via return message)
        return (
            True,
            f"Imported {len(artifacts)} artifacts as compilation '{compilation_name}'. Use 'ctx compile load {compilation_name}' to merge into current context.",
        )

    def delete(self, name: str) -> tuple[bool, str]:
        """Delete a compilation"""
        compilation_path = self.compilations_dir / f"{name}.json"

        if not compilation_path.exists():
            return False, f"Compilation '{name}' not found"

        compilation_path.unlink()
        return True, f"Deleted compilation: {name}"


# CLI Commands - Entry points defined in pyproject.toml [project.scripts]
@click.group()
def cli():
    """Context compilation commands"""
    pass


@cli.command()
@click.argument("name", required=False)
@click.option("--fields", help="Comma-separated fields to include")
@require_context_llemur
def compile(ctx_path, name, fields):
    """Compile current context into portable snapshot"""
    compiler = ContextCompiler(ctx_path)

    fields_list = fields.split(",") if fields else None
    compilation = compiler.compile(name, fields_list)

    # Create and display reseed block - core MARM feature
    reseed_block = compiler.create_reseed_block(compilation)
    click.echo(reseed_block)

    # Copy to clipboard using shared utility
    copy_to_clipboard(reseed_block, "✅ Reseed block copied to clipboard!")


@cli.command()
@click.argument("name")
@require_context_llemur
def load(ctx_path, name):
    """Load a previously compiled context"""
    compiler = ContextCompiler(ctx_path)
    success, message, compilation = compiler.load(name)

    if success:
        click.echo(f" {message}")
        if compilation:
            reseed_block = compiler.create_reseed_block(compilation)
            click.echo("\n" + reseed_block)
    else:
        click.echo(f"❌ {message}")


@cli.command("list")
@require_context_llemur
def list_compilations(ctx_path):
    """List all available compilations"""
    compiler = ContextCompiler(ctx_path)
    compilations = compiler.list_compilations()

    if not compilations:
        click.echo("📋 No compilations found")
        return

    click.echo("📋 Available Compilations:\n")
    for comp in compilations:
        click.echo(f"• {comp['name']}")
        click.echo(f"  Created: {comp['created']}")
        click.echo(f"  Size: {comp['size']} bytes")
        click.echo(f"  Notebook: {comp['notebook_entries']} entries")
        click.echo(f"  Static: {comp['static_files']} files")
        click.echo()


@cli.command()
@click.argument("name")
@require_context_llemur
def delete(ctx_path, name):
    """Delete a compilation"""
    if not click.confirm(f"Delete compilation '{name}'?"):
        return

    compiler = ContextCompiler(ctx_path)
    success, message = compiler.delete(name)

    if success:
        click.echo(f" {message}")
    else:
        click.echo(f"❌ {message}")


@cli.command()
@click.argument("name")
@click.option("--output", "-o", help="Output file path")
@require_context_llemur
def export_md(ctx_path, name, output):
    """Export compilation as markdown

    @implement: Load compilation and convert to markdown format with proper CLI integration
    @ai-context: Provides markdown export for documentation and sharing
    """
    compiler = ContextCompiler(ctx_path)
    compilation_path = compiler.compilations_dir / f"{name}.json"

    if not compilation_path.exists():
        click.echo(f"❌ Compilation '{name}' not found")
        return

    try:
        compilation = json.loads(compilation_path.read_text())
        markdown = compiler.export_to_markdown(compilation)

        if output:
            output_path = Path(output)
            output_path.write_text(markdown)
            click.echo(f"✅ Markdown exported to {output_path}")
        else:
            click.echo(markdown)

        copy_to_clipboard(markdown, "✅ Markdown copied to clipboard!")

    except Exception as e:
        click.echo(f"❌ Error exporting: {e}")


@cli.command()
@click.argument("artifacts_file", type=click.Path(exists=True))
@require_context_llemur
def import_artifacts(ctx_path, artifacts_file):
    """Import context from Claude artifacts JSON file

    @implement: Read artifacts file and import into MARM system with validation
    @ai-context: Enables Claude artifacts to be imported back into memory system
    """
    try:
        artifacts_json = Path(artifacts_file).read_text()
        compiler = ContextCompiler(ctx_path)
        success, message = compiler.import_from_claude_artifacts(artifacts_json)

        if success:
            click.echo(f"✅ {message}")
        else:
            click.echo(f"❌ {message}")

    except Exception as e:
        click.echo(f"❌ Error importing artifacts: {e}")


if __name__ == "__main__":
    cli()
