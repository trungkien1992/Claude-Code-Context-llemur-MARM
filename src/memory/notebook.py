#!/usr/bin/env python3
"""
src/memory/notebook.py - Runtime notebook management
Implements MARM's user-controlled knowledge layer

@fetch https://docs.python.org/3/library/json.html
@fetch https://docs.python.org/3/library/pathlib.html
@ai-context: Core MARM memory component - enables persistent knowledge across Claude sessions
"""

# @fetch https://docs.python.org/3/library/json.html#json.loads
# JSON operations for notebook persistence
import json
from datetime import datetime
# @fetch https://docs.python.org/3/library/pathlib.html#pathlib.Path
# Path operations for file system management
from pathlib import Path
from typing import Any, Dict, Optional

# @fetch https://click.palletsprojects.com/en/8.1.x/
# CLI framework for command-line interface
import click
from ..cli_utils import require_context_llemur, copy_to_clipboard


class NotebookManager:
    """Manages runtime notebook entries - MARM's key innovation

    CRITICAL: These limits are MARM specification requirements.
    Changing them breaks compatibility with Claude's memory system.
    """

    # MARM compliance limits - DO NOT MODIFY without updating MARM spec
    MAX_ENTRIES = 30  # Maximum number of notebook entries
    MAX_TOTAL_SIZE = 30000  # Total JSON size limit (chars)
    MAX_ENTRY_SIZE = 2048  # Individual entry value limit (chars)

    def __init__(self, ctx_path: Path):
        self.ctx_path = ctx_path
        self.memory_dir = ctx_path / "memory"
        self.notebook_path = self.memory_dir / "notebook.json"
        self._ensure_structure()

    def _ensure_structure(self):
        """Create memory directory and notebook file if they don't exist"""
        self.memory_dir.mkdir(exist_ok=True)
        if not self.notebook_path.exists():
            self.notebook_path.write_text("{}")

    def _load(self) -> Dict[str, Any]:
        """Load notebook from disk"""
        try:
            return json.loads(self.notebook_path.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save(self, notebook: Dict[str, Any]):
        """Save notebook to disk"""
        self.notebook_path.write_text(json.dumps(notebook, indent=2))

    def add(self, key: str, value: str) -> tuple[bool, str]:
        """Add entry to notebook with MARM-compliant validation

        @implement:
            1. Validate key format (1-64 chars, reasonable memory usage)
            2. Validate value size against MAX_ENTRY_SIZE limit
            3. Check notebook capacity against MAX_ENTRIES limit
            4. Verify total size won't exceed MAX_TOTAL_SIZE
            5. Create entry with timestamp metadata
            6. Save to disk and return success/error message
        @ai-context: Critical MARM compliance - limits ensure Claude memory compatibility
        """
        # Key validation - 64 char limit ensures reasonable memory usage
        if not key or len(key) > 64:
            return False, "Key must be 1-64 characters"

        # Value size check - prevents individual entries from being too large
        if not value or len(value) > self.MAX_ENTRY_SIZE:
            return False, f"Value must be 1-{self.MAX_ENTRY_SIZE} characters"

        notebook = self._load()

        # MARM limit enforcement - critical for Claude memory compatibility
        if len(notebook) >= self.MAX_ENTRIES:
            return False, f"Notebook full ({self.MAX_ENTRIES} entries max)"

        # Total size check prevents notebook from growing beyond MARM limits
        current_size = len(json.dumps(notebook))
        new_size = len(json.dumps({key: value}))
        if current_size + new_size > self.MAX_TOTAL_SIZE:
            return (
                False,
                f"Notebook size limit reached ({self.MAX_TOTAL_SIZE} chars max)",
            )

        # Entry structure - timestamps enable tracking for memory management
        notebook[key] = {
            "value": value,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),  # Always set on creation
        }

        self._save(notebook)
        return True, f"Stored '{key}' in notebook"

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get entry from notebook"""
        notebook = self._load()
        return notebook.get(key)

    def list_all(self) -> Dict[str, Any]:
        """List all notebook entries"""
        return self._load()

    def delete(self, key: str) -> tuple[bool, str]:
        """Delete entry from notebook"""
        notebook = self._load()
        if key not in notebook:
            return False, f"Entry '{key}' not found"

        del notebook[key]
        self._save(notebook)
        return True, f"Deleted '{key}' from notebook"

    def update(self, key: str, value: str) -> tuple[bool, str]:
        """Update existing entry - preserves created timestamp"""
        notebook = self._load()
        if key not in notebook:
            return False, f"Entry '{key}' not found"

        # Same size limit as add() - maintains MARM compliance
        if len(value) > self.MAX_ENTRY_SIZE:
            return False, f"Value too large (max {self.MAX_ENTRY_SIZE} chars)"

        notebook[key]["value"] = value
        notebook[key]["updated"] = datetime.now().isoformat()  # Track modifications

        self._save(notebook)
        return True, f"Updated '{key}' in notebook"

    def export(self) -> str:
        """Export notebook as portable text - format must match import_from_text()

        @implement:
            1. Load all notebook entries from disk
            2. Generate markdown-formatted output with ## headers
            3. Include export timestamp for version tracking
            4. Format entries with creation timestamps
            5. Return formatted string suitable for cross-context sharing
        @ai-context: Enables notebook portability across different contexts and sessions
        @pattern Template Method https://refactoring.guru/design-patterns/template-method
        """
        notebook = self._load()
        if not notebook:
            return "# Empty notebook"

        # Format designed for cross-context sharing and backup/restore
        output = "# Notebook Entries\n"
        output += f"# Exported: {datetime.now().isoformat()}\n\n"

        for key, entry in notebook.items():
            output += f"## {key}\n"  # Markdown header - import parser depends on this
            output += f"{entry['value']}\n"
            output += f"_Created: {entry['created']}_\n\n"

        return output

    def import_from_text(self, text: str) -> tuple[bool, str]:
        """Import notebook from text format - parses export() output format"""
        # IMPORTANT: Parser must handle export() format exactly (## headers, _Created: lines)
        lines = text.strip().split("\n")
        current_key = None
        current_value = []
        imported_count = 0

        for line in lines:
            if line.startswith("## "):
                # Save previous entry if exists
                if current_key and current_value:
                    value_text = "\n".join(current_value).strip()
                    if value_text and not value_text.startswith("_Created:"):
                        success, _ = self.add(
                            current_key, value_text
                        )  # Uses MARM validation
                        if success:
                            imported_count += 1

                # Start new entry - extract key from markdown header
                current_key = line[3:].strip()
                current_value = []
            elif (
                current_key
                and not line.startswith("#")
                and not line.startswith("_Created:")
            ):
                current_value.append(line)

        # Process final entry
        if current_key and current_value:
            value_text = "\n".join(current_value).strip()
            if value_text:
                success, _ = self.add(current_key, value_text)
                if success:
                    imported_count += 1

        return True, f"Imported {imported_count} entries"


# CLI Commands - Entry points defined in pyproject.toml [project.scripts]
@click.group()
def cli():
    """Notebook management commands"""
    pass


@cli.command()
@click.argument("key")
@click.argument("value")
@require_context_llemur
def add(ctx_path, key, value):
    """Add entry to notebook"""
    manager = NotebookManager(ctx_path)
    success, message = manager.add(key, value)

    if success:
        click.echo(f"✅ {message}")
    else:
        click.echo(f"❌ {message}")


@cli.command()
@click.argument("key")
@require_context_llemur
def get(ctx_path, key):
    """Get entry from notebook"""
    manager = NotebookManager(ctx_path)
    entry = manager.get(key)

    if entry:
        click.echo(f"📝 {key}: {entry['value']}")
        click.echo(f"   Updated: {entry['updated']}")
    else:
        click.echo(f"❌ Entry '{key}' not found")


@cli.command("list")
@require_context_llemur
def list_entries(ctx_path):
    """List all notebook entries"""
    manager = NotebookManager(ctx_path)
    notebook = manager.list_all()

    if not notebook:
        click.echo("📔 Notebook is empty")
        return

    click.echo(
        f"📔 Notebook Entries ({len(notebook)}/{NotebookManager.MAX_ENTRIES}):\n"
    )

    for key, entry in notebook.items():
        value_preview = (
            entry["value"][:50] + "..." if len(entry["value"]) > 50 else entry["value"]
        )
        click.echo(f"• {key}: {value_preview}")


@cli.command()
@click.argument("key")
@require_context_llemur
def delete(ctx_path, key):
    """Delete entry from notebook"""
    if not click.confirm(f"Delete '{key}' from notebook?"):
        return

    manager = NotebookManager(ctx_path)
    success, message = manager.delete(key)

    if success:
        click.echo(f"✅ {message}")
    else:
        click.echo(f"❌ {message}")


@cli.command()
@require_context_llemur
def export(ctx_path):
    """Export notebook as text"""
    manager = NotebookManager(ctx_path)
    output = manager.export()

    click.echo(output)
    copy_to_clipboard(output)


if __name__ == "__main__":
    cli()
