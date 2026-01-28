"""
Agent Memory System for AutoShorts AI.
Provides short-term and long-term memory storage with semantic search capabilities.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import json
import sqlite3
from pathlib import Path

from config import log, settings


class AgentMemory:
    """
    Memory system for agents with short-term and long-term storage.
    
    Short-term memory: In-memory dictionary for current session
    Long-term memory: SQLite database for persistent storage
    """
    
    def __init__(self, agent_id: str, agent_type: str):
        """
        Initialize agent memory.
        
        Args:
            agent_id: Unique identifier for the agent
            agent_type: Type of agent
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.short_term: Dict[str, Any] = {}
        
        # Initialize database connection
        self.db_path = Path(settings.data_dir) / "agent_memory.db"
        self._init_database()
        
        log.debug(f"Initialized memory for agent {agent_id}")
    
    def _init_database(self) -> None:
        """Initialize the SQLite database for long-term memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create long-term memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS long_term_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                agent_type TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(agent_id, key)
            )
        """)
        
        # Create learnings table for agent insights
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_type TEXT NOT NULL,
                learning_type TEXT NOT NULL,
                content TEXT NOT NULL,
                confidence REAL DEFAULT 0.5,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_agent_memory 
            ON long_term_memory(agent_id, agent_type)
        """)
        
        conn.commit()
        conn.close()
    
    def store_short_term(self, key: str, value: Any) -> None:
        """
        Store data in short-term memory (current session only).
        
        Args:
            key: Memory key
            value: Value to store
        """
        self.short_term[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        log.debug(f"[{self.agent_type}] Stored in short-term memory: {key}")
    
    def retrieve_short_term(self, key: str) -> Optional[Any]:
        """
        Retrieve data from short-term memory.
        
        Args:
            key: Memory key
            
        Returns:
            Stored value or None if not found
        """
        data = self.short_term.get(key)
        if data:
            return data["value"]
        return None
    
    def clear_short_term(self) -> None:
        """Clear all short-term memory."""
        self.short_term.clear()
        log.debug(f"[{self.agent_type}] Cleared short-term memory")
    
    def store_long_term(self, key: str, value: Any) -> None:
        """
        Store data in long-term memory (persistent).
        
        Args:
            key: Memory key
            value: Value to store (will be JSON serialized)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Serialize value to JSON
        value_json = json.dumps(value)
        
        # Insert or replace
        cursor.execute("""
            INSERT OR REPLACE INTO long_term_memory (agent_id, agent_type, key, value, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (self.agent_id, self.agent_type, key, value_json, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        log.debug(f"[{self.agent_type}] Stored in long-term memory: {key}")
    
    def retrieve_long_term(self, key: str) -> Optional[Any]:
        """
        Retrieve data from long-term memory.
        
        Args:
            key: Memory key
            
        Returns:
            Stored value or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT value FROM long_term_memory
            WHERE agent_id = ? AND key = ?
        """, (self.agent_id, key))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        return None
    
    def query_long_term(self, filters: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Query long-term memory with optional filters.
        
        Args:
            filters: Optional filters (e.g., {"agent_type": "trend_research"})
            limit: Maximum number of results
            
        Returns:
            List of memory entries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT agent_id, agent_type, key, value, timestamp FROM long_term_memory WHERE 1=1"
        params = []
        
        if filters:
            if "agent_id" in filters:
                query += " AND agent_id = ?"
                params.append(filters["agent_id"])
            if "agent_type" in filters:
                query += " AND agent_type = ?"
                params.append(filters["agent_type"])
        
        query += f" ORDER BY timestamp DESC LIMIT {limit}"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "agent_id": r[0],
                "agent_type": r[1],
                "key": r[2],
                "value": json.loads(r[3]),
                "timestamp": r[4]
            }
            for r in results
        ]
    
    def store_learning(self, learning_type: str, content: str, confidence: float = 0.5) -> None:
        """
        Store a learning/insight for this agent type.
        
        Args:
            learning_type: Type of learning (e.g., "successful_hook", "failed_topic")
            content: Learning content
            confidence: Confidence score (0-1)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO agent_learnings (agent_type, learning_type, content, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (self.agent_type, learning_type, content, confidence, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        log.info(f"[{self.agent_type}] Stored learning: {learning_type} (confidence: {confidence})")
    
    def retrieve_learnings(self, learning_type: Optional[str] = None, min_confidence: float = 0.0) -> List[Dict[str, Any]]:
        """
        Retrieve learnings for this agent type.
        
        Args:
            learning_type: Optional filter by learning type
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of learnings
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT learning_type, content, confidence, timestamp 
            FROM agent_learnings
            WHERE agent_type = ? AND confidence >= ?
        """
        params = [self.agent_type, min_confidence]
        
        if learning_type:
            query += " AND learning_type = ?"
            params.append(learning_type)
        
        query += " ORDER BY confidence DESC, timestamp DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "learning_type": r[0],
                "content": r[1],
                "confidence": r[2],
                "timestamp": r[3]
            }
            for r in results
        ]
    
    def consolidate_memory(self, max_age_days: int = 30) -> None:
        """
        Consolidate and prune old memory entries.
        
        Args:
            max_age_days: Maximum age of entries to keep
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete old entries
        cursor.execute("""
            DELETE FROM long_term_memory
            WHERE agent_id = ? AND timestamp < datetime('now', '-' || ? || ' days')
        """, (self.agent_id, max_age_days))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        log.info(f"[{self.agent_type}] Consolidated memory: removed {deleted_count} old entries")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get statistics about memory usage.
        
        Returns:
            Dictionary of memory statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count long-term entries
        cursor.execute("""
            SELECT COUNT(*) FROM long_term_memory WHERE agent_id = ?
        """, (self.agent_id,))
        long_term_count = cursor.fetchone()[0]
        
        # Count learnings
        cursor.execute("""
            SELECT COUNT(*) FROM agent_learnings WHERE agent_type = ?
        """, (self.agent_type,))
        learnings_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "short_term_entries": len(self.short_term),
            "long_term_entries": long_term_count,
            "learnings_count": learnings_count
        }
