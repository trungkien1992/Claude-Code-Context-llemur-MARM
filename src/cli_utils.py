#!/usr/bin/env python3
"""
src/cli_utils.py - Shared CLI utilities for context management

@ai-context: Eliminates repeated CLI patterns across the codebase
@refactoring: Consolidates context resolution, clipboard, and error handling
@pattern: DRY (Don't Repeat Yourself) principle implementation
"""

from pathlib import Path
from typing import Optional, Callable, Any
from functools import wraps

import click


def get_context_path_or_exit() -> Optional[Path]:
    """Get active context path with standardized error handling
    
    Returns None and exits with error message if context-llemur unavailable 
    or no active context found.
    
    @ai-context: Central context resolution - replaces 20+ duplicate implementations
    @error-handling: Standardized error messages with appropriate emojis
    @integration: Works with context-llemur's CtxCore.get_active_ctx_path()
    """
    try:
        from context_llemur import CtxCore
        core = CtxCore()
        ctx_path = core.get_active_ctx_path()
        
        if not ctx_path:
            click.echo("❌ No active context. Run 'ctx new' first.")
            return None
            
        return ctx_path
        
    except ImportError:
        # Fallback to mock for testing
        try:
            from .mock_context_llemur import CtxCore
            core = CtxCore()
            ctx_path = core.get_active_ctx_path()
            
            # Check if we have a .ctx marker file
            if (ctx_path / ".ctx").exists():
                return ctx_path
            else:
                click.echo("❌ No context found. Create .ctx file or install context-llemur")
                return None
                
        except Exception:
            click.echo("❌ context-llemur not available. Install with: pip install context-llemur")
            return None


def require_context_llemur(func: Callable) -> Callable:
    """Decorator that ensures context-llemur is available and context is active
    
    @ai-context: Decorator pattern for CLI commands that need context
    @usage: @require_context_llemur above CLI command functions
    @behavior: Returns early with error message if requirements not met
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx_path = get_context_path_or_exit()
        if ctx_path is None:
            return
        
        # Call original function with ctx_path as first argument
        return func(ctx_path, *args, **kwargs)
    
    return wrapper


def copy_to_clipboard(content: str, success_msg: str = "✅ Copied to clipboard!") -> None:
    """Copy content to clipboard with graceful fallback
    
    @ai-context: Standardized clipboard handling - replaces 7 duplicate implementations
    @error-handling: Graceful fallback if pyperclip not available
    @user-experience: Consistent messaging across all CLI commands
    """
    try:
        import pyperclip
        pyperclip.copy(content)
        click.echo(f"\n{success_msg}")
    except ImportError:
        click.echo("\n💡 Install pyperclip to auto-copy: pip install pyperclip")


def get_context_path_with_fallback() -> Path:
    """Get context path with fallback to current directory
    
    Used for functions that can work without context-llemur but prefer it.
    
    @ai-context: Variant for functions that can operate without active context
    @fallback: Uses current working directory if context-llemur unavailable
    """
    try:
        from context_llemur import CtxCore
        core = CtxCore()
        ctx_path = core.get_active_ctx_path()
        
        if ctx_path:
            return ctx_path
        else:
            return Path.cwd()
            
    except ImportError:
        return Path.cwd()


def echo_no_context_warning() -> None:
    """Standard warning message for missing context"""
    click.echo("⚠️  context-llemur not available - showing project structure instead")


def validate_key_format(key: str) -> tuple[bool, str]:
    """Validate notebook key format
    
    @ai-context: Centralized validation for notebook keys
    @security: Prevents problematic characters in keys
    """
    if not key or len(key) > 64:
        return False, "Key must be 1-64 characters"
    
    # Allow alphanumeric, underscore, dash, dot
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.")
    if not all(c in allowed_chars for c in key):
        return False, "Key can only contain letters, numbers, underscore, dash, and dot"
    
    return True, "Valid key"


def detect_unicode_issues(file_path: Path) -> list[tuple[int, str]]:
    """Detect potential Unicode issues in a file
    
    @ai-context: Early detection utility based on refactoring lessons learned
    @usage: Call before attempting string replacements in files
    @returns: List of (line_number, problematic_line) tuples
    """
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                # Find non-ASCII characters that might cause replacement issues
                if any(ord(char) > 127 for char in line):
                    issues.append((i, line.strip()))
    except Exception as e:
        issues.append((0, f"Error reading file: {e}"))
    
    return issues


# Standard error messages for consistency
ERROR_MESSAGES = {
    'no_context_llemur': "❌ context-llemur not available. Install with: pip install context-llemur",
    'no_active_context': "❌ No active context. Run 'ctx new' first.",
    'no_active_context_short': "❌ No active context",
    'compilation_not_found': "❌ Compilation '{}' not found",
    'entry_not_found': "❌ Entry '{}' not found",
}


def echo_error(error_key: str, *args) -> None:
    """Echo standardized error message
    
    @ai-context: Consistent error messaging across all CLI commands
    """
    message = ERROR_MESSAGES.get(error_key, "❌ Unknown error")
    if args:
        message = message.format(*args)
    click.echo(message)