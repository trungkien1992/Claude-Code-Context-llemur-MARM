#!/usr/bin/env python3
"""
main.py - Extended Claude context management with MARM memory layer

@ai-context: Primary CLI entry point for Claude Code AI-readable development
@architecture: Modular CLI with notebook, compilation, and AI session management
@integration: Extends context-llemur with MARM memory + AI workflow capabilities
@usage-pattern: ctx [notebook|compile|ai] [command] [args]
@security: Graceful degradation when context-llemur unavailable
@performance: Lazy imports prevent startup delays with missing dependencies

ARCHITECTURE OVERVIEW:
- Extends context-llemur with MARM memory capabilities
- Three core features: notebook management + context compilation + AI sessions
- Lazy imports avoid dependency issues during development

EXTENSION POINTS:
- Add new @main.command() for top-level commands
- Add new @notebook.command() for notebook operations  
- Add new @ai.command() for AI workflow operations
- ContextCompiler handles all portable snapshot logic

AI-READABLE DEVELOPMENT FEATURES:
- Structured AI development sessions with goal tracking
- Context-aware preparation for Claude Code integration
- Session management with progress documentation
- Pattern libraries for consistent AI guidance
"""

# @fetch https://click.palletsprojects.com/en/8.1.x/api/#click.group
# Click group documentation for CLI structure patterns
import click
from pathlib import Path

# @fetch https://github.com/jerpint/context-llemur
# Core context management - provides CtxCore.get_active_ctx_path()
from src.memory.notebook import NotebookManager
from src.memory.compiler import ContextCompiler
from src.cli_utils import get_context_path_or_exit, copy_to_clipboard, require_context_llemur

# @implement: Integrate context management at startup
# - Context resolution now handled by shared utilities
# - Graceful degradation when context-llemur unavailable
# - CLI commands handle context resolution individually

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

@main.group()
def ai():
    """AI development context management (Claude Code integration)"""
    pass

# === NOTEBOOK OPERATIONS ===
# Pattern: All notebook commands follow ctx_core -> NotebookManager -> operation
# Add similar commands: get, list, delete, export (see notebook.py:cli for examples)

@notebook.command('add')
@click.argument('key')
@click.argument('value')
@require_context_llemur  
def notebook_add(ctx_path, key, value):
    """Add entry to notebook with MARM compliance validation
    
    @ai-context: Core MARM memory operation - stores persistent knowledge for AI sessions
    @usage-example: ctx notebook add "api_endpoint" "https://api.service.com/v1" 
    @limits: 30 entries max, 2048 chars per entry, 30KB total (MARM compliance)
    @error-handling: Validates key format, entry size, and notebook capacity
    @integration: Works with AI sessions for storing development context
    @security: Input sanitization, no sensitive data exposure in error messages
    
    @fetch https://github.com/jerpint/context-llemur/blob/main/README.md#notebook-management
    @refactored: Now uses shared CLI utilities for context resolution
    @pattern Command https://refactoring.guru/design-patterns/command
    """
    manager = NotebookManager(ctx_path)
    success, message = manager.add(key, value)
    click.echo(f"✅ {message}" if success else f"❌ {message}")

# === CONTEXT COMPILATION ===
# MARM's core innovation: portable context blocks for cross-session sharing
# Output format must remain stable for compatibility

@main.command()
@click.argument('name', required=False)
@click.option('--fields', help='Fields to include')
@require_context_llemur
def compile(ctx_path, name, fields):
    """Compile context into portable snapshot (MARM innovation)
    
    @fetch https://github.com/jerpint/context-llemur/blob/main/README.md#context-compilation
    @fetch https://docs.python.org/3/library/json.html#json.dumps
    @refactored: Now uses shared CLI utilities for context resolution
    @ai-context: Core MARM feature - creates portable context blocks for sharing across sessions
    @pattern Builder https://refactoring.guru/design-patterns/builder
    """
    compiler = ContextCompiler(ctx_path)
    compilation = compiler.compile(name, fields.split(',') if fields else None)
    reseed_block = compiler.create_reseed_block(compilation)
    click.echo(reseed_block)
    copy_to_clipboard(reseed_block, "✅ Reseed block copied to clipboard!")

# === AI CONTEXT OPERATIONS ===
# Integration with Claude Code for AI-readable development

@ai.command()
@click.argument('goal')
@click.option('--focus', help='Focus area for the session')
@require_context_llemur
def start_session(ctx_path, goal, focus):
    """Start new AI development session with structured context preparation
    
    @ai-context: Primary entry point for structured AI development with Claude Code
    @workflow: Initializes session -> prepares context -> displays for Claude Code use
    @usage-example: ctx ai start-session "Implement user auth" --focus "backend_api"
    @output: Session tracking info + formatted context for immediate Claude Code use
    @integration: Creates MARM notebook entries for session persistence
    @productivity: Structures development for 20-55% efficiency improvement
    @refactored: Now uses shared CLI utilities for context resolution
    """
    from src.ai_context import AIContextManager
    
    manager = AIContextManager(ctx_path)
    success, message = manager.start_ai_session(goal, focus)
    
    if success:
        click.echo(f"✅ {message}")
        context = manager.prepare_claude_context()
        click.echo("\n" + context)
    else:
        click.echo(f"❌ {message}")

@ai.command()
@click.argument('summary')
@click.option('--next-steps', help='Next steps for future sessions')
@require_context_llemur
def end_session(ctx_path, summary, next_steps):
    """End current AI session with summary"""
    from src.ai_context import AIContextManager
    
    manager = AIContextManager(ctx_path)
    success, message = manager.end_ai_session(summary, next_steps)
    click.echo(f"✅ {message}" if success else f"❌ {message}")

@ai.command()
@click.option('--copy', is_flag=True, help='Copy to clipboard')
@require_context_llemur
def context(ctx_path, copy):
    """Prepare context for Claude Code session"""
    from src.ai_context import AIContextManager
    
    manager = AIContextManager(ctx_path)
    context_content = manager.prepare_claude_context()
    
    click.echo(context_content)
    
    if copy:
        copy_to_clipboard(context_content, "✅ Context copied to clipboard for Claude Code!")

@ai.command('smart-context')
@click.option('--learning/--no-learning', default=True, help='Include learning insights')
@click.option('--patterns/--no-patterns', default=True, help='Include pattern suggestions')
@click.option('--relationships/--no-relationships', default=True, help='Include knowledge relationships')
@click.option('--insights/--no-insights', default=True, help='Include recent insights')
@click.option('--copy', is_flag=True, help='Copy to clipboard')
@require_context_llemur
def generate_smart_context(ctx_path, learning, patterns, relationships, insights, copy):
    """Generate intelligent AI context with all enhancements"""
    from src.ai_context import AIContextManager
    
    manager = AIContextManager(ctx_path)
    context = manager.prepare_intelligent_context(
        include_learning=learning,
        include_patterns=patterns,
        include_relationships=relationships,
        include_insights=insights
    )
    
    click.echo(context)
    
    if copy:
        copy_to_clipboard(context, "✅ Smart context copied to clipboard!")

@ai.command('capture')
@click.argument('type', type=click.Choice(['solution', 'pattern', 'failure', 'insight']))
@click.argument('problem')
@click.argument('solution')
@click.option('--outcome', default='success', type=click.Choice(['success', 'failure', 'partial']))
@require_context_llemur
def capture_learning(ctx_path, type, problem, solution, outcome):
    """Capture learning from development session"""
    from src.ai_context import AIContextManager
    
    manager = AIContextManager(ctx_path)
    manager.capture_interaction(type, problem, solution, outcome)
    
    click.echo(f"✅ Learning captured: {type} with outcome {outcome}")

# === INTELLIGENCE COMMAND GROUPS ===

@main.group()
def learn():
    """Learning and intelligence commands"""
    pass

@learn.command('search')
@click.argument('query')
@require_context_llemur
def search_learning(ctx_path, query):
    """Search for relevant learning"""
    from src.intelligence.learning import LearningCapture
    
    lc = LearningCapture(ctx_path)
    results = lc.get_relevant_learning(query)
    
    if results:
        click.echo(f"Found {len(results)} relevant items:\n")
        for item in results:
            if item["type"] == "solution":
                click.echo(f"• Solution: {item['data']['solution'][:100]}...")
            elif item["type"] == "pattern":
                click.echo(f"• Pattern: {item['pattern']} (used {item['usage_count']} times)")
            elif item["type"] == "failure":
                click.echo(f"• Previous Failure: {item['data']['attempted_solution'][:100]}...")
    else:
        click.echo("No relevant learning found")

@learn.command('stats')
@require_context_llemur
def learning_stats(ctx_path):
    """Show learning statistics"""
    from src.intelligence.learning import LearningCapture
    
    lc = LearningCapture(ctx_path)
    stats = lc.get_learning_stats()
    
    if "error" in stats:
        click.echo(f"❌ {stats['error']}")
        return
    
    click.echo("📊 Learning Statistics")
    click.echo(f"• Total Sessions: {stats['total_sessions']}")
    click.echo(f"• Solutions Captured: {stats['total_solutions']}")
    click.echo(f"• Failures Documented: {stats['total_failures']}")
    click.echo(f"• Patterns Identified: {stats['total_patterns']}")
    click.echo(f"• Success Rate: {stats['success_rate']:.1%}")
    
    if stats['top_patterns']:
        click.echo("\n🔥 Top Patterns:")
        for pattern in stats['top_patterns']:
            click.echo(f"  • {pattern['pattern']}: {pattern['usage_count']} uses")

@main.group()
def graph():
    """Knowledge graph commands"""
    pass

@graph.command('relate')
@click.argument('source')
@click.argument('target')
@click.argument('relation_type')
@require_context_llemur
def create_relationship(ctx_path, source, target, relation_type):
    """Create relationship between knowledge entries"""
    from src.knowledge.graph import KnowledgeGraph
    
    kg = KnowledgeGraph(ctx_path)
    success, message = kg.add_relationship(source, target, relation_type)
    
    if success:
        click.echo(f"✅ Related {source} to {target} via {relation_type}")
    else:
        click.echo(f"❌ {message}")

@graph.command('find')
@click.argument('key')
@require_context_llemur
def find_related(ctx_path, key):
    """Find entries related to a key"""
    from src.knowledge.graph import KnowledgeGraph
    
    kg = KnowledgeGraph(ctx_path)
    related = kg.find_related(key)
    
    if related:
        click.echo(f"Entries related to '{key}':\n")
        for item in related:
            click.echo(f"• {item['key']} ({item['relation']}): {item['entry']['value'][:50]}...")
    else:
        click.echo(f"No related entries found for '{key}'")

@graph.command('search')
@click.argument('query')
@require_context_llemur
def semantic_search(ctx_path, query):
    """Search for semantically similar entries"""
    from src.knowledge.graph import KnowledgeGraph
    
    kg = KnowledgeGraph(ctx_path)
    results = kg.find_similar_semantic(query)
    
    if results:
        click.echo(f"Similar entries to '{query}':\n")
        for item in results:
            click.echo(f"• {item['key']} (similarity: {item['similarity']:.2f}): {item['value'][:50]}...")
    else:
        click.echo("No similar entries found")

@graph.command('stats')
@require_context_llemur
def graph_stats(ctx_path):
    """Show knowledge graph statistics"""
    from src.knowledge.graph import KnowledgeGraph
    
    kg = KnowledgeGraph(ctx_path)
    stats = kg.get_stats()
    
    click.echo("🧠 Knowledge Graph Statistics")
    click.echo(f"• Total Entries: {stats['total_entries']}")
    click.echo(f"• Total Relationships: {stats['total_relationships']}")
    click.echo(f"• Vector Search Available: {'✅' if stats['has_numpy'] else '❌'}")
    
    if stats['entry_types']:
        click.echo("\n📊 Entry Types:")
        for entry_type, count in stats['entry_types'].items():
            click.echo(f"  • {entry_type}: {count}")
    
    if stats['relationship_types']:
        click.echo("\n🔗 Relationship Types:")
        for rel_type, count in stats['relationship_types'].items():
            click.echo(f"  • {rel_type}: {count}")

@main.group()
def patterns():
    """Pattern management commands"""
    pass

@patterns.command('track')
@click.argument('pattern')
@click.argument('outcome', type=click.Choice(['success', 'failed', 'modified']))
@click.option('--effectiveness', default=0.5, type=float, help='Effectiveness score (0.0-1.0)')
@require_context_llemur
def track_pattern(ctx_path, pattern, outcome, effectiveness):
    """Track pattern usage and effectiveness"""
    from src.intelligence.patterns import PatternEngine
    
    pe = PatternEngine(ctx_path)
    pe.track_pattern_usage(pattern, outcome, effectiveness)
    
    click.echo(f"✅ Tracked {pattern} usage with outcome: {outcome}")

@patterns.command('suggest')
@click.argument('context')
@require_context_llemur
def suggest_patterns(ctx_path, context):
    """Get pattern suggestions for context"""
    from src.intelligence.patterns import PatternEngine
    
    pe = PatternEngine(ctx_path)
    suggestions = pe.suggest_patterns(context)
    
    if suggestions:
        click.echo("💡 Suggested patterns:\n")
        for sug in suggestions:
            click.echo(f"• {sug['pattern']}: relevance={sug['relevance']:.2f}, effectiveness={sug['effectiveness']:.2f}")
    else:
        click.echo("No pattern suggestions available")

@patterns.command('list')
@click.option('--limit', default=10, type=int, help='Number of patterns to show')
@require_context_llemur
def list_patterns(ctx_path, limit):
    """List top patterns by effectiveness"""
    from src.intelligence.patterns import PatternEngine
    
    pe = PatternEngine(ctx_path)
    top_patterns = pe.get_top_patterns(limit)
    
    if top_patterns:
        click.echo(f"🏆 Top {len(top_patterns)} Patterns:\n")
        for i, pattern in enumerate(top_patterns, 1):
            click.echo(f"{i}. {pattern['pattern']}")
            click.echo(f"   Score: {pattern['score']:.2f} | Uses: {pattern['total_uses']} | Success: {pattern['success_rate']:.1%}")
    else:
        click.echo("No patterns available")

@patterns.command('trends')
@require_context_llemur
def pattern_trends(ctx_path):
    """Analyze pattern trends"""
    from src.intelligence.patterns import PatternEngine
    
    pe = PatternEngine(ctx_path)
    trends = pe.analyze_pattern_trends()
    
    if "error" in trends:
        click.echo(f"❌ {trends['error']}")
        return
    
    click.echo("📈 Pattern Trends Analysis\n")
    
    if trends["most_effective"]:
        click.echo("🎯 Most Effective:")
        for pattern in trends["most_effective"][:3]:
            click.echo(f"  • {pattern['pattern']}: {pattern['effectiveness']:.1%}")
    
    if trends["trending_up"]:
        click.echo("\n📈 Trending Up:")
        for pattern in trends["trending_up"][:3]:
            click.echo(f"  • {pattern['pattern']}: {pattern['recent_effectiveness']:.1%} (up from {pattern['average_effectiveness']:.1%})")
    
    if trends["needs_improvement"]:
        click.echo("\n⚠️ Needs Improvement:")
        for pattern in trends["needs_improvement"][:3]:
            click.echo(f"  • {pattern['pattern']}: {pattern['effectiveness']:.1%} effectiveness")

@main.group()
def visualize():
    """Visualization and analytics commands"""
    pass

@visualize.command('graph')
@click.option('--max-nodes', default=20, type=int, help='Maximum nodes to show')
@click.option('--output', help='Output file for diagram')
@require_context_llemur
def visualize_graph(ctx_path, max_nodes, output):
    """Generate knowledge graph visualization (Mermaid format)"""
    from src.visualization.graph_viz import GraphVisualizer
    
    viz = GraphVisualizer(ctx_path)
    mermaid = viz.generate_mermaid_graph(max_nodes)
    
    if output:
        output_path = Path(output)
        output_path.write_text(mermaid)
        click.echo(f"✅ Graph saved to {output}")
    else:
        click.echo(mermaid)

@visualize.command('timeline')
@click.option('--output', help='Output file for timeline')
@require_context_llemur
def visualize_timeline(ctx_path, output):
    """Generate knowledge evolution timeline"""
    from src.visualization.graph_viz import GraphVisualizer
    
    viz = GraphVisualizer(ctx_path)
    timeline = viz.generate_evolution_timeline()
    
    if output:
        output_path = Path(output)
        output_path.write_text(timeline)
        click.echo(f"✅ Timeline saved to {output}")
    else:
        click.echo(timeline)

@visualize.command('patterns')
@click.option('--output', help='Output file for report')
@require_context_llemur
def visualize_patterns(ctx_path, output):
    """Generate pattern effectiveness report"""
    from src.visualization.graph_viz import GraphVisualizer
    
    viz = GraphVisualizer(ctx_path)
    report = viz.generate_pattern_effectiveness_report()
    
    if output:
        output_path = Path(output)
        output_path.write_text(report)
        click.echo(f"✅ Pattern report saved to {output}")
    else:
        click.echo(report)

@visualize.command('learning')
@click.option('--output', help='Output file for summary')
@require_context_llemur
def visualize_learning(ctx_path, output):
    """Generate learning activities summary"""
    from src.visualization.graph_viz import GraphVisualizer
    
    viz = GraphVisualizer(ctx_path)
    summary = viz.generate_learning_summary()
    
    if output:
        output_path = Path(output)
        output_path.write_text(summary)
        click.echo(f"✅ Learning summary saved to {output}")
    else:
        click.echo(summary)

@visualize.command('knowledge-map')
@click.option('--output', help='Output file for knowledge map')
@require_context_llemur
def visualize_knowledge_map(ctx_path, output):
    """Generate comprehensive knowledge map"""
    from src.visualization.graph_viz import GraphVisualizer
    
    viz = GraphVisualizer(ctx_path)
    knowledge_map = viz.generate_knowledge_map()
    
    if output:
        output_path = Path(output)
        output_path.write_text(knowledge_map)
        click.echo(f"✅ Knowledge map saved to {output}")
    else:
        click.echo(knowledge_map)

# === ENTRY POINTS ===
# cli_main() allows standalone execution: python main.py
# For distribution, use pyproject.toml [project.scripts]

def cli_main():
    """Entry point for standalone usage"""
    main()

if __name__ == "__main__":
    cli_main()
