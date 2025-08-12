#!/usr/bin/env python3
"""
AI Context Management for Claude Code Integration

@fetch https://docs.anthropic.com/en/docs/claude-code Claude Code documentation
@implement: AI-readable code context management with MARM integration
@ai-context: Extends MARM system specifically for AI development workflows
@pattern Command https://refactoring.guru/design-patterns/command
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import click

from .memory.notebook import NotebookManager
from .memory.compiler import ContextCompiler


class AIContextManager:
    """Manages AI-specific context patterns for Claude Code integration
    
    @implement:
        1. Standardized AI context templates and patterns
        2. Session-based development workflow management  
        3. Integration with MARM notebook and compilation systems
        4. Automated context preparation for Claude Code sessions
    @ai-context: Bridges human development intent with AI understanding
    """
    
    def __init__(self, ctx_path: Path):
        self.ctx_path = ctx_path
        self.notebook = NotebookManager(ctx_path)
        self.compiler = ContextCompiler(ctx_path)
        self.ai_context_dir = ctx_path / '.ai-context'
        self._ensure_structure()
    
    def _ensure_structure(self):
        """Create AI context directory structure"""
        self.ai_context_dir.mkdir(exist_ok=True)
        
        # Create template files if they don't exist
        templates = {
            'session-template.md': self._get_session_template(),
            'architecture-template.md': self._get_architecture_template(),
            'coding-standards.md': self._get_coding_standards_template()
        }
        
        for filename, content in templates.items():
            template_path = self.ai_context_dir / filename
            if not template_path.exists():
                template_path.write_text(content)
    
    def start_ai_session(self, goal: str, focus_area: Optional[str] = None) -> tuple[bool, str]:
        """Start new AI development session with structured context
        
        @implement:
            1. Create session timestamp and goal tracking
            2. Prepare current project context for AI
            3. Set up session-specific notebook entries
            4. Generate session compilation for reference
        @ai-context: Structures development sessions for optimal AI collaboration
        """
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        session_name = f"ai_session_{session_id}"
        
        # Store session metadata
        success, msg = self.notebook.add(f"session_{session_id}_goal", goal)
        if not success:
            return False, f"Failed to create session: {msg}"
        
        if focus_area:
            self.notebook.add(f"session_{session_id}_focus", focus_area)
        
        self.notebook.add(f"session_{session_id}_start", datetime.now().isoformat())
        self.notebook.add("current_session", session_id)
        
        # Create session compilation
        compilation = self.compiler.compile(session_name)
        
        return True, f"Started AI session {session_id} with goal: {goal}"
    
    def end_ai_session(self, summary: str, next_steps: Optional[str] = None) -> tuple[bool, str]:
        """End current AI session with documentation
        
        @implement: Record session outcomes and prepare for next session
        @ai-context: Captures learning and progress for continuous development
        """
        # Get current session
        current_session_entry = self.notebook.get("current_session")
        if not current_session_entry:
            return False, "No active AI session found"
        
        session_id = current_session_entry['value']
        
        # Store session outcomes
        self.notebook.add(f"session_{session_id}_summary", summary)
        self.notebook.add(f"session_{session_id}_end", datetime.now().isoformat())
        
        if next_steps:
            self.notebook.add(f"session_{session_id}_next", next_steps)
        
        # Remove current session marker
        self.notebook.delete("current_session")
        
        # Create final session compilation
        session_name = f"ai_session_{session_id}_completed"
        self.compiler.compile(session_name)
        
        return True, f"Ended AI session {session_id}"
    
    def prepare_claude_context(self, include_history: bool = True) -> str:
        """Prepare comprehensive context specifically for Claude Code
        
        @implement:
            1. Gather current project state and active session info
            2. Include relevant historical context if requested
            3. Format for optimal Claude Code consumption
            4. Add AI-specific guidance and patterns
        @ai-context: Optimized context format for Claude Code sessions
        """
        context = "# Claude Code AI Development Context\n\n"
        
        # Current session info
        current_session = self.notebook.get("current_session")
        if current_session:
            session_id = current_session['value']
            goal_entry = self.notebook.get(f"session_{session_id}_goal")
            focus_entry = self.notebook.get(f"session_{session_id}_focus")
            
            context += "## Active Session\n"
            context += f"- **Session ID**: {session_id}\n"
            if goal_entry:
                context += f"- **Goal**: {goal_entry['value']}\n"
            if focus_entry:
                context += f"- **Focus Area**: {focus_entry['value']}\n"
            context += "\n"
        
        # Project context from notebook
        notebook_data = self.notebook.list_all()
        if notebook_data:
            context += "## Project Knowledge Base\n"
            
            # Categorize entries
            categories = {
                'Architecture': [],
                'Development': [],
                'Configuration': [],
                'Session History': [],
                'Other': []
            }
            
            for key, entry in notebook_data.items():
                value = entry['value'] if isinstance(entry, dict) else entry
                
                if any(term in key.lower() for term in ['arch', 'design', 'pattern']):
                    categories['Architecture'].append(f"- **{key}**: {value}")
                elif any(term in key.lower() for term in ['session_', 'current_', 'active_']):
                    categories['Session History'].append(f"- **{key}**: {value}")
                elif any(term in key.lower() for term in ['config', 'env', 'setup']):
                    categories['Configuration'].append(f"- **{key}**: {value}")
                elif any(term in key.lower() for term in ['dev', 'code', 'implement']):
                    categories['Development'].append(f"- **{key}**: {value}")
                else:
                    categories['Other'].append(f"- **{key}**: {value}")
            
            for category, items in categories.items():
                if items:
                    context += f"\n### {category}\n"
                    context += "\n".join(items) + "\n"
        
        # Add AI guidance
        context += "\n## AI Development Guidance\n"
        context += "- Focus on the current session goal\n"
        context += "- Follow established project patterns and conventions\n"
        context += "- Consider security and performance implications\n"
        context += "- Suggest testing approaches for new functionality\n"
        context += "- Update context as development progresses\n"
        
        return context
    
    def add_ai_pattern(self, pattern_name: str, pattern_description: str, 
                      code_example: Optional[str] = None) -> tuple[bool, str]:
        """Add reusable AI coding pattern to project knowledge
        
        @implement: Store coding patterns for consistent AI guidance
        @ai-context: Builds library of project-specific AI guidance patterns
        """
        pattern_key = f"ai_pattern_{pattern_name}"
        pattern_value = pattern_description
        
        if code_example:
            pattern_value += f"\n\nExample:\n```\n{code_example}\n```"
        
        return self.notebook.add(pattern_key, pattern_value)
    
    def _get_session_template(self) -> str:
        """Session template for AI development"""
        return """# AI Development Session Template

## Session Goal
[What do you want to accomplish in this session?]

## Focus Area
- [ ] New feature implementation
- [ ] Bug fixing
- [ ] Refactoring
- [ ] Testing
- [ ] Documentation

## Context Checklist
- [ ] Current state documented in notebook
- [ ] Related code files identified
- [ ] Dependencies and constraints noted
- [ ] Success criteria defined

## Session Notes
[Track progress, decisions, and insights during the session]

## Outcomes
[What was accomplished?]

## Next Steps
[What should be done in the next session?]
"""
    
    def _get_architecture_template(self) -> str:
        """Architecture documentation template"""
        return """# AI Architecture Context

## System Overview
[High-level system architecture]

## Key Components
- Component 1: [Description]
- Component 2: [Description]

## Data Flow
[How data moves through the system]

## Integration Points
[External systems and APIs]

## AI Development Patterns
[Specific patterns for AI to follow in this codebase]
"""
    
    def _get_coding_standards_template(self) -> str:
        """Coding standards template"""
        return """# AI Coding Standards

## Language Conventions
[Language-specific conventions]

## Framework Patterns
[Framework-specific patterns to follow]

## Error Handling
[How errors should be handled]

## Testing Approach
[Testing patterns and requirements]

## Security Guidelines
[Security considerations for AI to follow]

## Performance Considerations
[Performance patterns and anti-patterns]
"""


# CLI Commands
@click.group()
def ai():
    """AI context management commands"""
    pass

@ai.command()
@click.argument('goal')
@click.option('--focus', help='Focus area for the session')
def start_session(goal, focus):
    """Start new AI development session
    
    @implement: Initialize session with MARM integration
    @ai-context: Prepares structured environment for AI collaboration
    """
    try:
        from context_llemur import CtxCore
        core = CtxCore()
        ctx_path = core.get_active_ctx_path()
    except ImportError:
        click.echo("❌ context-llemur not available")
        return
    
    if not ctx_path:
        click.echo("❌ No active context. Run 'ctx new' first.")
        return
    
    manager = AIContextManager(ctx_path)
    success, message = manager.start_ai_session(goal, focus)
    
    if success:
        click.echo(f"✅ {message}")
        # Show prepared context
        context = manager.prepare_claude_context()
        click.echo("\n" + context)
    else:
        click.echo(f"❌ {message}")

@ai.command()
@click.argument('summary')
@click.option('--next-steps', help='Next steps for future sessions')
def end_session(summary, next_steps):
    """End current AI session with summary
    
    @implement: Capture session outcomes and learnings
    @ai-context: Documents AI collaboration results for future reference
    """
    try:
        from context_llemur import CtxCore
        core = CtxCore()
        ctx_path = core.get_active_ctx_path()
    except ImportError:
        click.echo("❌ context-llemur not available")
        return
    
    if not ctx_path:
        click.echo("❌ No active context")
        return
    
    manager = AIContextManager(ctx_path)
    success, message = manager.end_ai_session(summary, next_steps)
    
    if success:
        click.echo(f"✅ {message}")
    else:
        click.echo(f"❌ {message}")

@ai.command()
@click.option('--copy', is_flag=True, help='Copy to clipboard')
def context(copy):
    """Prepare context for Claude Code session
    
    @implement: Generate AI-optimized context from current project state
    @ai-context: Primary interface for Claude Code context preparation
    """
    try:
        from context_llemur import CtxCore
        core = CtxCore()
        ctx_path = core.get_active_ctx_path()
    except ImportError:
        click.echo("❌ context-llemur not available")
        return
    
    if not ctx_path:
        click.echo("❌ No active context")
        return
    
    manager = AIContextManager(ctx_path)
    context = manager.prepare_claude_context()
    
    click.echo(context)
    
    if copy:
        try:
            import pyperclip
            pyperclip.copy(context)
            click.echo("\n✅ Context copied to clipboard for Claude Code!")
        except ImportError:
            click.echo("\n💡 Install pyperclip: pip install pyperclip")

@ai.command()
@click.argument('pattern_name')
@click.argument('description')
@click.option('--example', help='Code example for the pattern')
def add_pattern(pattern_name, description, example):
    """Add AI coding pattern to project knowledge
    
    @implement: Store reusable AI guidance patterns
    @ai-context: Builds project-specific AI instruction library
    """
    try:
        from context_llemur import CtxCore
        core = CtxCore()
        ctx_path = core.get_active_ctx_path()
    except ImportError:
        click.echo("❌ context-llemur not available")
        return
    
    if not ctx_path:
        click.echo("❌ No active context")
        return
    
    manager = AIContextManager(ctx_path)
    success, message = manager.add_ai_pattern(pattern_name, description, example)
    
    if success:
        click.echo(f"✅ {message}")
    else:
        click.echo(f"❌ {message}")

if __name__ == '__main__':
    ai()