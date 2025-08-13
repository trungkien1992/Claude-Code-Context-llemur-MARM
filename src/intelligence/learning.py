#!/usr/bin/env python3
"""
Session Learning Capture - Convert AI interactions into knowledge
@implement: Capture, distill, and persist learning from each session
@ai-context: Core intelligence component that builds institutional memory
@architecture: JSON-based storage with categorized learning and insights
@integration: Works with AI sessions to capture and retrieve development patterns
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import re

class LearningCapture:
    """Captures and persists learning from AI development sessions"""
    
    def __init__(self, ctx_path: Path):
        self.ctx_path = ctx_path
        self.memory_dir = ctx_path / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.learning_file = self.memory_dir / "learning.json"
        self.insights_file = self.memory_dir / "insights.json"
        self._init_storage()
    
    def _init_storage(self):
        """Initialize learning storage"""
        if not self.learning_file.exists():
            self.learning_file.write_text(json.dumps({
                "sessions": {},
                "patterns": {},
                "solutions": {},
                "failures": {},
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "total_sessions": 0,
                    "total_learnings": 0
                }
            }, indent=2))
        
        if not self.insights_file.exists():
            self.insights_file.write_text(json.dumps({
                "technical": [],
                "architectural": [],
                "debugging": [],
                "optimization": [],
                "security": [],
                "testing": []
            }, indent=2))
    
    def capture_session_learning(self, session_id: str, 
                                interaction_type: str,
                                problem: str,
                                solution: str,
                                outcome: str,
                                metadata: Dict[str, Any] = None):
        """Capture learning from a development session"""
        with open(self.learning_file, 'r') as f:
            learning = json.load(f)
        
        # Create session entry
        session_learning = {
            "timestamp": datetime.now().isoformat(),
            "type": interaction_type,
            "problem": problem,
            "solution": solution,
            "outcome": outcome,
            "metadata": metadata or {},
            "tags": self._extract_tags(problem + " " + solution),
            "difficulty": self._assess_difficulty(problem, solution),
            "reusability": self._assess_reusability(solution)
        }
        
        # Store by session
        if session_id not in learning["sessions"]:
            learning["sessions"][session_id] = []
        learning["sessions"][session_id].append(session_learning)
        
        # Update metadata
        learning["metadata"]["total_sessions"] = len(learning["sessions"])
        learning["metadata"]["total_learnings"] = sum(len(s) for s in learning["sessions"].values())
        learning["metadata"]["last_updated"] = datetime.now().isoformat()
        
        # Categorize learning
        if outcome == "success":
            solution_key = self._generate_solution_key(problem)
            learning["solutions"][solution_key] = {
                "problem": problem,
                "solution": solution,
                "session": session_id,
                "timestamp": datetime.now().isoformat(),
                "tags": session_learning["tags"],
                "difficulty": session_learning["difficulty"],
                "reusability": session_learning["reusability"]
            }
        elif outcome == "failure":
            failure_key = self._generate_failure_key(problem)
            learning["failures"][failure_key] = {
                "problem": problem,
                "attempted_solution": solution,
                "session": session_id,
                "timestamp": datetime.now().isoformat(),
                "tags": session_learning["tags"],
                "lessons": self._extract_failure_lessons(problem, solution)
            }
        
        # Extract and store patterns
        patterns = self._extract_patterns(solution)
        for pattern in patterns:
            if pattern not in learning["patterns"]:
                learning["patterns"][pattern] = []
            learning["patterns"][pattern].append({
                "session": session_id,
                "context": problem[:100],
                "outcome": outcome,
                "timestamp": datetime.now().isoformat()
            })
            # Keep only last 20 entries per pattern
            learning["patterns"][pattern] = learning["patterns"][pattern][-20:]
        
        with open(self.learning_file, 'w') as f:
            json.dump(learning, f, indent=2)
        
        # Generate insights
        self._generate_insights(interaction_type, problem, solution, outcome)
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from text"""
        # Common technical terms to look for
        tech_terms = [
            "api", "auth", "authentication", "authorization", "cache", "caching",
            "database", "db", "sql", "nosql", "deploy", "deployment", "docker",
            "kubernetes", "error", "exception", "function", "git", "http", "https",
            "import", "json", "jwt", "logging", "memory", "network", "optimization",
            "performance", "query", "redis", "security", "test", "testing",
            "validation", "async", "await", "promise", "middleware", "frontend",
            "backend", "fullstack", "react", "node", "python", "javascript",
            "typescript", "css", "html", "microservice", "monolith", "session",
            "cookie", "cors", "csrf", "xss", "sql-injection", "encryption",
            "decryption", "hash", "salt", "oauth", "jwt", "rest", "graphql",
            "websocket", "serverless", "lambda", "cloud", "aws", "azure", "gcp"
        ]
        
        text_lower = text.lower()
        tags = [term for term in tech_terms if term in text_lower]
        
        # Add pattern-based tags
        if re.search(r'\b(crud|create.*read.*update.*delete)\b', text_lower):
            tags.append("crud")
        if re.search(r'\b(mvc|model.*view.*controller)\b', text_lower):
            tags.append("mvc")
        if re.search(r'\b(solid|single.*responsibility|open.*closed|liskov|interface.*segregation|dependency.*inversion)\b', text_lower):
            tags.append("solid-principles")
        
        return list(set(tags))  # Remove duplicates
    
    def _extract_patterns(self, solution: str) -> List[str]:
        """Extract reusable patterns from solution"""
        patterns = []
        solution_lower = solution.lower()
        
        # Pattern indicators
        pattern_mapping = {
            "async": "async_pattern",
            "cache": "caching_pattern", 
            "retry": "retry_pattern",
            "validate": "validation_pattern",
            "middleware": "middleware_pattern",
            "factory": "factory_pattern",
            "singleton": "singleton_pattern",
            "observer": "observer_pattern",
            "strategy": "strategy_pattern",
            "decorator": "decorator_pattern",
            "adapter": "adapter_pattern",
            "facade": "facade_pattern",
            "proxy": "proxy_pattern",
            "builder": "builder_pattern",
            "command": "command_pattern",
            "state": "state_pattern",
            "template": "template_pattern"
        }
        
        for keyword, pattern in pattern_mapping.items():
            if keyword in solution_lower:
                patterns.append(pattern)
        
        # Advanced pattern detection
        if re.search(r'try.*catch|try.*except', solution_lower):
            patterns.append("error_handling_pattern")
        if re.search(r'log|logging|console\.log', solution_lower):
            patterns.append("logging_pattern")
        if re.search(r'config|configuration|env', solution_lower):
            patterns.append("configuration_pattern")
        if re.search(r'test|spec|mock|stub', solution_lower):
            patterns.append("testing_pattern")
        
        return patterns
    
    def _assess_difficulty(self, problem: str, solution: str) -> str:
        """Assess the difficulty of the problem/solution"""
        # Simple heuristic based on content complexity
        complexity_indicators = [
            ("algorithm", 2), ("optimization", 2), ("architecture", 3),
            ("design pattern", 2), ("security", 3), ("performance", 2),
            ("integration", 2), ("migration", 3), ("refactoring", 2),
            ("debugging", 1), ("configuration", 1), ("deployment", 2)
        ]
        
        text = (problem + " " + solution).lower()
        score = 0
        
        for indicator, weight in complexity_indicators:
            if indicator in text:
                score += weight
        
        # Also consider length and technical terms
        tech_terms = len(self._extract_tags(text))
        score += tech_terms * 0.5
        
        if score < 2:
            return "simple"
        elif score < 5:
            return "moderate"
        else:
            return "complex"
    
    def _assess_reusability(self, solution: str) -> str:
        """Assess how reusable the solution is"""
        reusability_indicators = [
            "function", "class", "module", "library", "pattern",
            "template", "utility", "helper", "service", "component"
        ]
        
        solution_lower = solution.lower()
        matches = sum(1 for indicator in reusability_indicators if indicator in solution_lower)
        
        if matches >= 3:
            return "high"
        elif matches >= 1:
            return "medium"
        else:
            return "low"
    
    def _extract_failure_lessons(self, problem: str, solution: str) -> List[str]:
        """Extract lessons from failed attempts"""
        lessons = []
        
        # Common failure patterns and lessons
        failure_patterns = {
            "permission": "Check file/directory permissions and user access rights",
            "timeout": "Consider increasing timeout values or optimizing performance",
            "connection": "Verify network connectivity and service availability",
            "authentication": "Validate credentials and authentication flow",
            "validation": "Implement proper input validation and error handling",
            "memory": "Monitor memory usage and implement proper cleanup",
            "deadlock": "Review locking strategies and transaction isolation",
            "race condition": "Implement proper synchronization mechanisms"
        }
        
        text = (problem + " " + solution).lower()
        for pattern, lesson in failure_patterns.items():
            if pattern in text:
                lessons.append(lesson)
        
        return lessons
    
    def _generate_solution_key(self, problem: str) -> str:
        """Generate a searchable key for a solution"""
        # Use first few words of problem as key
        words = re.sub(r'[^a-zA-Z0-9\s]', '', problem.lower()).split()[:5]
        return "_".join(words)
    
    def _generate_failure_key(self, problem: str) -> str:
        """Generate a searchable key for a failure"""
        words = re.sub(r'[^a-zA-Z0-9\s]', '', problem.lower()).split()[:5]
        return "fail_" + "_".join(words)
    
    def _generate_insights(self, interaction_type: str, problem: str, 
                          solution: str, outcome: str):
        """Generate insights from learning"""
        with open(self.insights_file, 'r') as f:
            insights = json.load(f)
        
        # Categorize insight
        category = self._categorize_insight(problem, solution)
        
        # Create insight
        insight = {
            "timestamp": datetime.now().isoformat(),
            "interaction_type": interaction_type,
            "problem_summary": problem[:100],
            "solution_summary": solution[:100],
            "outcome": outcome,
            "lesson": self._extract_lesson(problem, solution, outcome),
            "tags": self._extract_tags(problem + " " + solution)[:5]  # Top 5 tags
        }
        
        insights[category].append(insight)
        
        # Keep only recent insights (last 50 per category)
        insights[category] = insights[category][-50:]
        
        with open(self.insights_file, 'w') as f:
            json.dump(insights, f, indent=2)
    
    def _categorize_insight(self, problem: str, solution: str) -> str:
        """Categorize insight by type"""
        text = (problem + " " + solution).lower()
        
        if any(word in text for word in ["architecture", "design", "pattern", "structure"]):
            return "architectural"
        elif any(word in text for word in ["debug", "error", "fix", "bug", "issue"]):
            return "debugging"
        elif any(word in text for word in ["performance", "optimize", "speed", "memory", "efficiency"]):
            return "optimization"
        elif any(word in text for word in ["security", "auth", "encrypt", "vulnerability", "safe"]):
            return "security"
        elif any(word in text for word in ["test", "spec", "mock", "unit", "integration"]):
            return "testing"
        else:
            return "technical"
    
    def _extract_lesson(self, problem: str, solution: str, outcome: str) -> str:
        """Extract key lesson from interaction"""
        if outcome == "success":
            return f"Solution '{solution[:50]}...' successfully addressed '{problem[:50]}...'"
        elif outcome == "failure":
            return f"Approach '{solution[:50]}...' was unsuccessful for '{problem[:50]}...'"
        else:
            return f"Partial progress made on '{problem[:50]}...' using '{solution[:50]}...'"
    
    def get_relevant_learning(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve learning relevant to a query"""
        with open(self.learning_file, 'r') as f:
            learning = json.load(f)
        
        relevant = []
        query_lower = query.lower()
        query_tags = self._extract_tags(query)
        
        # Search solutions
        for key, solution in learning["solutions"].items():
            relevance_score = self._calculate_relevance(solution, query_tags, query_lower)
            if relevance_score > 0:
                relevant.append({
                    "type": "solution",
                    "data": solution,
                    "relevance": relevance_score
                })
        
        # Search failures (to avoid repeating mistakes)
        for key, failure in learning["failures"].items():
            relevance_score = self._calculate_relevance(failure, query_tags, query_lower)
            if relevance_score > 0:
                relevant.append({
                    "type": "failure",
                    "data": failure,
                    "relevance": relevance_score
                })
        
        # Search patterns
        for pattern, contexts in learning["patterns"].items():
            if any(word in pattern for word in query_lower.split()):
                relevant.append({
                    "type": "pattern",
                    "pattern": pattern,
                    "usage_count": len(contexts),
                    "relevance": 0.7,  # Static relevance for pattern matches
                    "recent_contexts": contexts[-3:]  # Last 3 uses
                })
        
        # Sort by relevance
        relevant.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        return relevant[:limit]
    
    def _calculate_relevance(self, item: Dict[str, Any], query_tags: List[str], query_lower: str) -> float:
        """Calculate relevance score for an item"""
        relevance = 0.0
        
        # Tag overlap
        item_tags = item.get("tags", [])
        tag_overlap = len(set(query_tags) & set(item_tags))
        relevance += tag_overlap * 0.3
        
        # Text similarity in problem
        problem_text = item.get("problem", "").lower()
        query_words = set(query_lower.split())
        problem_words = set(problem_text.split())
        word_overlap = len(query_words & problem_words)
        relevance += (word_overlap / max(len(query_words), 1)) * 0.4
        
        # Boost for high reusability
        if item.get("reusability") == "high":
            relevance += 0.2
        elif item.get("reusability") == "medium":
            relevance += 0.1
        
        return relevance
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get statistics about captured learning"""
        try:
            with open(self.learning_file, 'r') as f:
                learning = json.load(f)
            
            with open(self.insights_file, 'r') as f:
                insights = json.load(f)
            
            # Calculate statistics
            stats = {
                "total_sessions": len(learning["sessions"]),
                "total_solutions": len(learning["solutions"]),
                "total_failures": len(learning["failures"]),
                "total_patterns": len(learning["patterns"]),
                "total_insights": sum(len(category) for category in insights.values()),
                "success_rate": 0.0,
                "top_patterns": [],
                "recent_activity": []
            }
            
            # Calculate success rate
            total_learnings = sum(len(session) for session in learning["sessions"].values())
            if total_learnings > 0:
                successful_learnings = sum(
                    1 for session in learning["sessions"].values()
                    for item in session if item["outcome"] == "success"
                )
                stats["success_rate"] = successful_learnings / total_learnings
            
            # Top patterns by usage
            pattern_usage = [
                {"pattern": pattern, "usage_count": len(contexts)}
                for pattern, contexts in learning["patterns"].items()
            ]
            pattern_usage.sort(key=lambda x: x["usage_count"], reverse=True)
            stats["top_patterns"] = pattern_usage[:5]
            
            # Recent activity (last 10 items)
            recent_items = []
            for session_id, session_items in learning["sessions"].items():
                for item in session_items:
                    recent_items.append({
                        "session": session_id,
                        "timestamp": item["timestamp"],
                        "type": item["type"],
                        "outcome": item["outcome"]
                    })
            
            recent_items.sort(key=lambda x: x["timestamp"], reverse=True)
            stats["recent_activity"] = recent_items[:10]
            
            return stats
        except (FileNotFoundError, json.JSONDecodeError):
            return {"error": "No learning data available"}
    
    def export_learning(self) -> Dict[str, Any]:
        """Export all learning data for sharing or backup"""
        try:
            with open(self.learning_file, 'r') as f:
                learning = json.load(f)
            
            with open(self.insights_file, 'r') as f:
                insights = json.load(f)
            
            return {
                "export_timestamp": datetime.now().isoformat(),
                "learning": learning,
                "insights": insights,
                "summary": self.get_learning_stats()
            }
        except (FileNotFoundError, json.JSONDecodeError):
            return {"error": "No learning data available"}