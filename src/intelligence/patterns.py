#!/usr/bin/env python3
"""
Pattern Recognition and Evolution Engine
@implement: Identify, track, and evolve development patterns
@ai-context: Core intelligence component that learns from code and development patterns
@architecture: JSON-based storage with pattern detection rules and effectiveness tracking
@integration: Works with AI sessions to capture and suggest proven patterns
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import defaultdict
import re

class PatternEngine:
    """Recognizes and evolves patterns from development sessions"""
    
    def __init__(self, ctx_path: Path):
        self.ctx_path = ctx_path
        self.memory_dir = ctx_path / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.patterns_file = self.memory_dir / "patterns.json"
        self.usage_file = self.memory_dir / "pattern_usage.json"
        self._init_patterns()
    
    def _init_patterns(self):
        """Initialize pattern storage"""
        if not self.patterns_file.exists():
            self.patterns_file.write_text(json.dumps({}, indent=2))
        if not self.usage_file.exists():
            self.usage_file.write_text(json.dumps({}, indent=2))
    
    def extract_patterns(self, content: str, context: Dict[str, Any]) -> List[str]:
        """Extract patterns from session content"""
        patterns = []
        
        # Pattern detection rules
        pattern_rules = [
            (r"@pattern\s+(\w+)", "explicit_pattern"),
            (r"TODO:\s*(.*)", "todo_pattern"),
            (r"FIXME:\s*(.*)", "fix_pattern"),
            (r"jwt|token|auth", "auth_pattern"),
            (r"redis|cache|memcache", "cache_pattern"),
            (r"async|await|promise", "async_pattern"),
            (r"test|spec|mock", "testing_pattern"),
            (r"docker|kubernetes|deploy", "deployment_pattern"),
            (r"api|endpoint|rest", "api_pattern"),
            (r"database|db|sql", "database_pattern"),
            (r"validation|validate|schema", "validation_pattern"),
            (r"error|exception|try.*catch", "error_handling_pattern"),
            (r"retry|backoff|timeout", "retry_pattern"),
            (r"log|logging|debug", "logging_pattern"),
            (r"config|configuration|settings", "config_pattern"),
            (r"security|encrypt|decrypt", "security_pattern")
        ]
        
        for regex, pattern_type in pattern_rules:
            if re.search(regex, content, re.IGNORECASE):
                patterns.append(pattern_type)
        
        # Store patterns with context
        self._store_patterns(patterns, context)
        
        return patterns
    
    def _store_patterns(self, patterns: List[str], context: Dict[str, Any]):
        """Store identified patterns with context"""
        with open(self.patterns_file, 'r') as f:
            all_patterns = json.load(f)
        
        for pattern in patterns:
            if pattern not in all_patterns:
                all_patterns[pattern] = {
                    "first_seen": datetime.now().isoformat(),
                    "occurrences": 0,
                    "contexts": []
                }
            
            all_patterns[pattern]["occurrences"] += 1
            all_patterns[pattern]["last_seen"] = datetime.now().isoformat()
            all_patterns[pattern]["contexts"].append({
                "timestamp": datetime.now().isoformat(),
                "session": context.get("session_id"),
                "goal": context.get("goal")
            })
            
            # Keep only last 10 contexts for each pattern
            all_patterns[pattern]["contexts"] = all_patterns[pattern]["contexts"][-10:]
        
        with open(self.patterns_file, 'w') as f:
            json.dump(all_patterns, f, indent=2)
    
    def track_pattern_usage(self, pattern: str, outcome: str, 
                           effectiveness: float = 0.5):
        """Track how patterns are used and their effectiveness"""
        with open(self.usage_file, 'r') as f:
            usage = json.load(f)
        
        if pattern not in usage:
            usage[pattern] = {
                "total_uses": 0,
                "successful_uses": 0,
                "failed_uses": 0,
                "modified_uses": 0,
                "average_effectiveness": 0.0,
                "evolution": []
            }
        
        usage[pattern]["total_uses"] += 1
        
        if outcome == "success":
            usage[pattern]["successful_uses"] += 1
        elif outcome == "failed":
            usage[pattern]["failed_uses"] += 1
        elif outcome == "modified":
            usage[pattern]["modified_uses"] += 1
        
        # Update effectiveness rolling average
        old_avg = usage[pattern]["average_effectiveness"]
        n = usage[pattern]["total_uses"]
        new_avg = ((n - 1) * old_avg + effectiveness) / n
        usage[pattern]["average_effectiveness"] = new_avg
        
        # Track evolution
        usage[pattern]["evolution"].append({
            "timestamp": datetime.now().isoformat(),
            "outcome": outcome,
            "effectiveness": effectiveness
        })
        
        # Keep only last 20 evolution entries
        usage[pattern]["evolution"] = usage[pattern]["evolution"][-20:]
        
        with open(self.usage_file, 'w') as f:
            json.dump(usage, f, indent=2)
    
    def suggest_patterns(self, context: str) -> List[Dict[str, Any]]:
        """Suggest relevant patterns based on context"""
        with open(self.patterns_file, 'r') as f:
            all_patterns = json.load(f)
        
        with open(self.usage_file, 'r') as f:
            usage = json.load(f)
        
        suggestions = []
        context_lower = context.lower()
        
        for pattern_name, pattern_data in all_patterns.items():
            # Check if pattern might be relevant
            relevance_score = 0.0
            
            # Check pattern name relevance
            pattern_words = pattern_name.replace("_", " ").split()
            if any(word in context_lower for word in pattern_words):
                relevance_score += 0.5
            
            # Check effectiveness if available
            if pattern_name in usage:
                effectiveness = usage[pattern_name]["average_effectiveness"]
                relevance_score += effectiveness * 0.5
                
                # Boost patterns with high success rate
                success_rate = usage[pattern_name]["successful_uses"] / max(usage[pattern_name]["total_uses"], 1)
                relevance_score += success_rate * 0.3
            
            if relevance_score > 0.3:
                suggestions.append({
                    "pattern": pattern_name,
                    "relevance": relevance_score,
                    "occurrences": pattern_data["occurrences"],
                    "effectiveness": usage.get(pattern_name, {}).get("average_effectiveness", 0.5),
                    "success_rate": usage.get(pattern_name, {}).get("successful_uses", 0) / max(usage.get(pattern_name, {}).get("total_uses", 1), 1)
                })
        
        # Sort by relevance
        suggestions.sort(key=lambda x: x["relevance"], reverse=True)
        return suggestions[:5]
    
    def get_pattern_details(self, pattern_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific pattern"""
        try:
            with open(self.patterns_file, 'r') as f:
                all_patterns = json.load(f)
            
            with open(self.usage_file, 'r') as f:
                usage = json.load(f)
            
            if pattern_name not in all_patterns:
                return None
            
            pattern_info = all_patterns[pattern_name].copy()
            if pattern_name in usage:
                pattern_info["usage"] = usage[pattern_name]
            
            return pattern_info
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def get_top_patterns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top patterns by effectiveness or usage"""
        try:
            with open(self.patterns_file, 'r') as f:
                all_patterns = json.load(f)
            
            with open(self.usage_file, 'r') as f:
                usage = json.load(f)
            
            pattern_list = []
            for pattern_name, pattern_data in all_patterns.items():
                effectiveness = usage.get(pattern_name, {}).get("average_effectiveness", 0.0)
                total_uses = usage.get(pattern_name, {}).get("total_uses", 0)
                success_rate = usage.get(pattern_name, {}).get("successful_uses", 0) / max(total_uses, 1)
                
                # Calculate composite score
                score = (effectiveness * 0.5) + (success_rate * 0.3) + (min(total_uses / 10, 1) * 0.2)
                
                pattern_list.append({
                    "pattern": pattern_name,
                    "score": score,
                    "effectiveness": effectiveness,
                    "success_rate": success_rate,
                    "total_uses": total_uses,
                    "occurrences": pattern_data["occurrences"]
                })
            
            pattern_list.sort(key=lambda x: x["score"], reverse=True)
            return pattern_list[:limit]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def analyze_pattern_trends(self) -> Dict[str, Any]:
        """Analyze trends in pattern usage and effectiveness"""
        try:
            with open(self.usage_file, 'r') as f:
                usage = json.load(f)
            
            trends = {
                "most_used": [],
                "most_effective": [],
                "trending_up": [],
                "needs_improvement": []
            }
            
            for pattern_name, pattern_data in usage.items():
                total_uses = pattern_data["total_uses"]
                effectiveness = pattern_data["average_effectiveness"]
                success_rate = pattern_data["successful_uses"] / max(total_uses, 1)
                
                # Most used patterns
                trends["most_used"].append({
                    "pattern": pattern_name,
                    "total_uses": total_uses
                })
                
                # Most effective patterns
                trends["most_effective"].append({
                    "pattern": pattern_name,
                    "effectiveness": effectiveness
                })
                
                # Patterns needing improvement
                if effectiveness < 0.4 and total_uses > 2:
                    trends["needs_improvement"].append({
                        "pattern": pattern_name,
                        "effectiveness": effectiveness,
                        "total_uses": total_uses
                    })
                
                # Check if trending up (recent effectiveness > average)
                if len(pattern_data["evolution"]) >= 3:
                    recent_effectiveness = sum(e["effectiveness"] for e in pattern_data["evolution"][-3:]) / 3
                    if recent_effectiveness > effectiveness:
                        trends["trending_up"].append({
                            "pattern": pattern_name,
                            "recent_effectiveness": recent_effectiveness,
                            "average_effectiveness": effectiveness
                        })
            
            # Sort each category
            trends["most_used"].sort(key=lambda x: x["total_uses"], reverse=True)
            trends["most_effective"].sort(key=lambda x: x["effectiveness"], reverse=True)
            trends["trending_up"].sort(key=lambda x: x["recent_effectiveness"] - x["average_effectiveness"], reverse=True)
            trends["needs_improvement"].sort(key=lambda x: x["effectiveness"])
            
            # Limit results
            for key in trends:
                trends[key] = trends[key][:5]
            
            return trends
        except (FileNotFoundError, json.JSONDecodeError):
            return {"error": "No pattern data available"}
    
    def export_patterns(self) -> Dict[str, Any]:
        """Export all pattern data for sharing or backup"""
        try:
            with open(self.patterns_file, 'r') as f:
                patterns = json.load(f)
            
            with open(self.usage_file, 'r') as f:
                usage = json.load(f)
            
            return {
                "export_timestamp": datetime.now().isoformat(),
                "patterns": patterns,
                "usage": usage,
                "summary": {
                    "total_patterns": len(patterns),
                    "total_usages": sum(u.get("total_uses", 0) for u in usage.values()),
                    "average_effectiveness": sum(u.get("average_effectiveness", 0) for u in usage.values()) / max(len(usage), 1)
                }
            }
        except (FileNotFoundError, json.JSONDecodeError):
            return {"error": "No pattern data available"}