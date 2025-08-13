#!/usr/bin/env python3
"""
Knowledge Graph Visualization
@implement: Create visual representations of knowledge relationships
@ai-context: Provides insights into knowledge structure and evolution
@architecture: Mermaid and text-based visualization generators
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class GraphVisualizer:
    """Generate visualizations of knowledge graph"""
    
    def __init__(self, ctx_path: Path):
        self.ctx_path = ctx_path
        self.memory_dir = ctx_path / "memory"
        self.graph_file = self.memory_dir / "knowledge_graph.json"
    
    def generate_mermaid_graph(self, max_nodes: int = 20) -> str:
        """Generate Mermaid diagram of knowledge graph"""
        if not self.graph_file.exists():
            return "graph TD\n    A[\"No knowledge graph data available\"]"
            
        try:
            with open(self.graph_file, 'r') as f:
                graph = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return "graph TD\n    A[\"Error loading graph data\"]"
        
        mermaid = "graph TD\n"
        
        # Add nodes
        nodes = list(graph["entries"].keys())[:max_nodes]
        for node in nodes:
            entry = graph["entries"][node]
            # Truncate value for display and escape special characters
            display_value = entry["value"][:30].replace("\n", " ").replace('"', "'")
            safe_node = node.replace("-", "_").replace(".", "_")
            mermaid += f'    {safe_node}["{node}<br/>{display_value}..."]\n'
        
        # Add relationships
        safe_nodes = {node: node.replace("-", "_").replace(".", "_") for node in nodes}
        for rel in graph["relationships"]:
            source_safe = safe_nodes.get(rel["source"])
            target_safe = safe_nodes.get(rel["target"])
            
            if source_safe and target_safe:
                strength = rel.get("strength", 0.5)
                if strength > 0.7:
                    arrow = "==>"
                elif strength > 0.4:
                    arrow = "-->"
                else:
                    arrow = "-.->"
                
                relation_type = rel["type"].replace("-", "_")
                mermaid += f'    {source_safe} {arrow}|{relation_type}| {target_safe}\n'
        
        # Add styling
        mermaid += "\n    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px;\n"
        mermaid += "    classDef pattern fill:#e1f5fe,stroke:#01579b,stroke-width:2px;\n"
        mermaid += "    classDef solution fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;\n"
        
        return mermaid
    
    def generate_evolution_timeline(self) -> str:
        """Generate timeline of knowledge evolution"""
        if not self.graph_file.exists():
            return "# Knowledge Evolution Timeline\n\nNo knowledge graph data available."
            
        try:
            with open(self.graph_file, 'r') as f:
                graph = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return "# Knowledge Evolution Timeline\n\nError loading graph data."
        
        timeline = "# Knowledge Evolution Timeline\n\n"
        
        # Collect all timestamped events
        events = []
        
        for key, entry in graph["entries"].items():
            if "created" in entry:
                events.append({
                    "timestamp": entry["created"],
                    "type": "entry_created",
                    "key": key,
                    "value": entry["value"][:50]
                })
        
        for rel in graph["relationships"]:
            if "created" in rel:
                events.append({
                    "timestamp": rel["created"],
                    "type": "relationship_created",
                    "source": rel["source"],
                    "target": rel["target"],
                    "relation": rel["type"]
                })
        
        if not events:
            return timeline + "No evolution events found."
        
        # Sort by timestamp
        events.sort(key=lambda x: x["timestamp"])
        
        # Generate timeline
        current_date = None
        for event in events[-20:]:  # Last 20 events
            try:
                event_date = event["timestamp"][:10]
            except (IndexError, TypeError):
                event_date = "unknown"
            
            if event_date != current_date:
                timeline += f"\n## {event_date}\n\n"
                current_date = event_date
            
            if event["type"] == "entry_created":
                timeline += f"- **Added**: `{event['key']}` - {event['value']}...\n"
            elif event["type"] == "relationship_created":
                timeline += f"- **Linked**: `{event['source']}` → `{event['target']}` ({event['relation']})\n"
        
        return timeline
    
    def generate_pattern_effectiveness_report(self) -> str:
        """Generate report on pattern effectiveness"""
        usage_file = self.memory_dir / "pattern_usage.json"
        
        if not usage_file.exists():
            return "# Pattern Effectiveness Report\n\nNo pattern usage data available."
        
        try:
            with open(usage_file, 'r') as f:
                usage = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return "# Pattern Effectiveness Report\n\nError loading pattern data."
        
        if not usage:
            return "# Pattern Effectiveness Report\n\nNo patterns have been tracked yet."
        
        report = "# Pattern Effectiveness Report\n\n"
        
        # Sort patterns by effectiveness
        patterns = []
        for pattern_name, data in usage.items():
            total_uses = data.get("total_uses", 0)
            if total_uses > 0:
                patterns.append({
                    "name": pattern_name,
                    "effectiveness": data.get("average_effectiveness", 0),
                    "total_uses": total_uses,
                    "success_rate": data.get("successful_uses", 0) / total_uses
                })
        
        patterns.sort(key=lambda x: x["effectiveness"], reverse=True)
        
        # Generate report
        if patterns:
            report += "## Top Performing Patterns\n\n"
            for pattern in patterns[:5]:
                report += f"### {pattern['name']}\n"
                report += f"- **Effectiveness**: {pattern['effectiveness']:.2%}\n"
                report += f"- **Success Rate**: {pattern['success_rate']:.2%}\n"
                report += f"- **Total Uses**: {pattern['total_uses']}\n\n"
            
            # Patterns needing improvement
            poor_patterns = [p for p in patterns if p["effectiveness"] < 0.5]
            if poor_patterns:
                report += "## Patterns Needing Improvement\n\n"
                for pattern in poor_patterns[-3:]:
                    report += f"- **{pattern['name']}**: {pattern['effectiveness']:.2%} effectiveness\n"
        else:
            report += "No pattern data available for analysis."
        
        return report
    
    def generate_learning_summary(self) -> str:
        """Generate summary of learning activities"""
        learning_file = self.memory_dir / "learning.json"
        insights_file = self.memory_dir / "insights.json"
        
        if not learning_file.exists():
            return "# Learning Summary\n\nNo learning data available."
        
        try:
            with open(learning_file, 'r') as f:
                learning = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return "# Learning Summary\n\nError loading learning data."
        
        summary = "# Learning Summary\n\n"
        
        # Overview statistics
        total_sessions = len(learning.get("sessions", {}))
        total_solutions = len(learning.get("solutions", {}))
        total_failures = len(learning.get("failures", {}))
        total_patterns = len(learning.get("patterns", {}))
        
        summary += "## Overview\n\n"
        summary += f"- **Total Sessions**: {total_sessions}\n"
        summary += f"- **Solutions Captured**: {total_solutions}\n"
        summary += f"- **Failures Documented**: {total_failures}\n"
        summary += f"- **Patterns Identified**: {total_patterns}\n\n"
        
        # Calculate success rate
        all_learnings = []
        for session_items in learning.get("sessions", {}).values():
            all_learnings.extend(session_items)
        
        if all_learnings:
            successful = sum(1 for item in all_learnings if item.get("outcome") == "success")
            success_rate = successful / len(all_learnings)
            summary += f"- **Success Rate**: {success_rate:.1%}\n\n"
        
        # Recent solutions
        solutions = learning.get("solutions", {})
        if solutions:
            summary += "## Recent Solutions\n\n"
            recent_solutions = sorted(
                solutions.items(),
                key=lambda x: x[1].get("timestamp", ""),
                reverse=True
            )[:5]
            
            for key, solution in recent_solutions:
                summary += f"- **{solution.get('problem', 'Unknown')[:50]}...**\n"
                summary += f"  Solution: {solution.get('solution', 'Unknown')[:100]}...\n\n"
        
        # Top patterns
        patterns = learning.get("patterns", {})
        if patterns:
            summary += "## Most Used Patterns\n\n"
            pattern_usage = [
                (pattern, len(contexts)) for pattern, contexts in patterns.items()
            ]
            pattern_usage.sort(key=lambda x: x[1], reverse=True)
            
            for pattern, usage_count in pattern_usage[:5]:
                summary += f"- **{pattern}**: {usage_count} uses\n"
        
        # Add insights if available
        if insights_file.exists():
            try:
                with open(insights_file, 'r') as f:
                    insights = json.load(f)
                
                summary += "\n## Recent Insights\n\n"
                all_insights = []
                for category, items in insights.items():
                    all_insights.extend([(category, item) for item in items[-2:]])
                
                for category, insight in all_insights[-5:]:
                    summary += f"- **[{category}]** {insight.get('lesson', 'No lesson available')}\n"
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return summary
    
    def generate_knowledge_map(self) -> str:
        """Generate a text-based knowledge map"""
        if not self.graph_file.exists():
            return "# Knowledge Map\n\nNo knowledge graph data available."
            
        try:
            with open(self.graph_file, 'r') as f:
                graph = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return "# Knowledge Map\n\nError loading graph data."
        
        knowledge_map = "# Knowledge Map\n\n"
        
        # Group entries by type
        entries_by_type = {}
        for key, entry in graph["entries"].items():
            entry_type = entry.get("type", "unknown")
            if entry_type not in entries_by_type:
                entries_by_type[entry_type] = []
            entries_by_type[entry_type].append((key, entry))
        
        for entry_type, entries in entries_by_type.items():
            knowledge_map += f"## {entry_type.title()} ({len(entries)} entries)\n\n"
            
            for key, entry in entries[:10]:  # Limit to 10 per type
                knowledge_map += f"### {key}\n"
                knowledge_map += f"{entry['value'][:150]}...\n\n"
                
                # Show related entries
                related = []
                for rel in graph["relationships"]:
                    if rel["source"] == key:
                        related.append(f"{rel['target']} ({rel['type']})")
                
                if related:
                    knowledge_map += f"**Related to**: {', '.join(related[:3])}\n\n"
            
            if len(entries) > 10:
                knowledge_map += f"... and {len(entries) - 10} more entries\n\n"
        
        return knowledge_map