#!/usr/bin/env python3
"""
Knowledge Graph Engine - Relationships between concepts
@implement: Transform flat notebook into interconnected knowledge web
@ai-context: Core intelligence component that builds semantic relationships
@architecture: Dual storage (JSON for compatibility, SQLite for advanced features)
@integration: Works with existing notebook while adding relationship tracking
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import sqlite3

# Optional dependencies for enhanced features
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

class KnowledgeGraph:
    """Manages relationships and semantic connections between knowledge entries"""
    
    def __init__(self, ctx_path: Path):
        self.ctx_path = ctx_path
        self.memory_dir = ctx_path / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        
        # Dual storage: JSON for compatibility, SQLite for advanced features
        self.graph_file = self.memory_dir / "knowledge_graph.json"
        self.db_file = self.memory_dir / "knowledge.db"
        
        self._init_structures()
        
    def _init_structures(self):
        """Initialize both JSON and SQLite structures"""
        # JSON structure for basic relationships
        if not self.graph_file.exists():
            initial = {
                "entries": {},      # Enhanced notebook entries
                "relationships": [], # Connections between entries
                "patterns": {},     # Recognized patterns
                "sessions": {},     # Session metadata
                "evolution": []     # Change history
            }
            self.graph_file.write_text(json.dumps(initial, indent=2))
        
        # SQLite for vectorization and semantic search
        conn = sqlite3.connect(self.db_file)
        conn.execute('''CREATE TABLE IF NOT EXISTS entries (
            key TEXT PRIMARY KEY,
            value TEXT,
            type TEXT,
            tags TEXT,
            vector BLOB,
            created TIMESTAMP,
            updated TIMESTAMP
        )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            target TEXT,
            relation_type TEXT,
            strength REAL,
            context TEXT,
            created TIMESTAMP,
            FOREIGN KEY (source) REFERENCES entries(key),
            FOREIGN KEY (target) REFERENCES entries(key)
        )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS patterns (
            name TEXT PRIMARY KEY,
            description TEXT,
            usage_count INTEGER DEFAULT 0,
            success_rate REAL,
            last_used TIMESTAMP,
            vector BLOB
        )''')
        
        conn.commit()
        conn.close()
    
    def add_entry_with_relationships(self, key: str, value: str, 
                                    entry_type: str = "knowledge",
                                    tags: List[str] = None,
                                    related_to: List[Tuple[str, str]] = None):
        """Add entry with automatic relationship detection"""
        # Load current graph
        with open(self.graph_file, 'r') as f:
            graph = json.load(f)
        
        # Add to graph with metadata
        graph["entries"][key] = {
            "value": value,
            "type": entry_type,
            "tags": tags or [],
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat()
        }
        
        # Auto-detect relationships based on content similarity
        if related_to:
            for target_key, relation_type in related_to:
                if target_key in graph["entries"]:
                    graph["relationships"].append({
                        "source": key,
                        "target": target_key,
                        "type": relation_type,
                        "strength": self._calculate_similarity(value, 
                                     graph["entries"][target_key]["value"]),
                        "created": datetime.now().isoformat()
                    })
        
        # Save enhanced graph
        with open(self.graph_file, 'w') as f:
            json.dump(graph, f, indent=2)
        
        # Also store in SQLite with vector
        self._store_in_db(key, value, entry_type, tags)
        
        return True
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between texts"""
        # Simple Jaccard similarity for now
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _store_in_db(self, key: str, value: str, entry_type: str, tags: List[str]):
        """Store entry in SQLite with vector representation"""
        conn = sqlite3.connect(self.db_file)
        
        # Generate vector if numpy available
        vector_bytes = None
        if HAS_NUMPY:
            vector = self._generate_vector(value)
            vector_bytes = vector.tobytes()
        
        conn.execute('''INSERT OR REPLACE INTO entries 
                       (key, value, type, tags, vector, created, updated)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (key, value, entry_type, json.dumps(tags or []),
                     vector_bytes, datetime.now(), datetime.now()))
        
        conn.commit()
        conn.close()
    
    def _generate_vector(self, text: str):
        """Generate semantic vector for text"""
        if not HAS_NUMPY:
            return None
            
        # Simplified vectorization - in production use proper embeddings
        words = text.lower().split()
        # Create fixed-size vector based on word hashes
        vector = np.zeros(128)
        for word in words:
            idx = hash(word) % 128
            vector[idx] += 1
        
        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
            
        return vector
    
    def find_related(self, key: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Find entries related to a given key"""
        with open(self.graph_file, 'r') as f:
            graph = json.load(f)
        
        related = []
        
        # Direct relationships
        for rel in graph["relationships"]:
            if rel["source"] == key:
                target = graph["entries"].get(rel["target"])
                if target:
                    related.append({
                        "key": rel["target"],
                        "entry": target,
                        "relation": rel["type"],
                        "strength": rel.get("strength", 0.5)
                    })
        
        # Sort by strength and limit results
        related.sort(key=lambda x: x["strength"], reverse=True)
        return related[:max_results]
    
    def find_similar_semantic(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Find semantically similar entries using vector search"""
        if not HAS_NUMPY:
            # Fallback to keyword search
            return self._keyword_search(query, max_results)
            
        query_vector = self._generate_vector(query)
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.execute("SELECT key, value, vector FROM entries")
        
        similarities = []
        for row in cursor:
            key, value, vector_bytes = row
            if vector_bytes:
                entry_vector = np.frombuffer(vector_bytes, dtype=np.float64)
                similarity = np.dot(query_vector, entry_vector)
                similarities.append({
                    "key": key,
                    "value": value,
                    "similarity": similarity
                })
        
        conn.close()
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:max_results]
    
    def _keyword_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Fallback keyword search when numpy not available"""
        with open(self.graph_file, 'r') as f:
            graph = json.load(f)
        
        query_words = set(query.lower().split())
        matches = []
        
        for key, entry in graph["entries"].items():
            entry_words = set(entry["value"].lower().split())
            overlap = len(query_words.intersection(entry_words))
            if overlap > 0:
                matches.append({
                    "key": key,
                    "value": entry["value"],
                    "similarity": overlap / len(query_words.union(entry_words))
                })
        
        matches.sort(key=lambda x: x["similarity"], reverse=True)
        return matches[:max_results]
    
    def add_relationship(self, source: str, target: str, relation_type: str, 
                        strength: float = 0.5, context: str = ""):
        """Add explicit relationship between entries"""
        with open(self.graph_file, 'r') as f:
            graph = json.load(f)
        
        # Check if entries exist
        if source not in graph["entries"] or target not in graph["entries"]:
            return False, "Source or target entry does not exist"
        
        # Add relationship
        graph["relationships"].append({
            "source": source,
            "target": target,
            "type": relation_type,
            "strength": strength,
            "context": context,
            "created": datetime.now().isoformat()
        })
        
        with open(self.graph_file, 'w') as f:
            json.dump(graph, f, indent=2)
        
        return True, "Relationship added successfully"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge graph statistics"""
        with open(self.graph_file, 'r') as f:
            graph = json.load(f)
        
        return {
            "total_entries": len(graph["entries"]),
            "total_relationships": len(graph["relationships"]),
            "entry_types": self._count_entry_types(graph["entries"]),
            "relationship_types": self._count_relationship_types(graph["relationships"]),
            "has_numpy": HAS_NUMPY
        }
    
    def _count_entry_types(self, entries: Dict) -> Dict[str, int]:
        """Count entries by type"""
        counts = {}
        for entry in entries.values():
            entry_type = entry.get("type", "unknown")
            counts[entry_type] = counts.get(entry_type, 0) + 1
        return counts
    
    def _count_relationship_types(self, relationships: List) -> Dict[str, int]:
        """Count relationships by type"""
        counts = {}
        for rel in relationships:
            rel_type = rel.get("type", "unknown")
            counts[rel_type] = counts.get(rel_type, 0) + 1
        return counts