"""
Storage layer for autoresearch experiments.
Supports SQLite (preferred) with automatic fallback to file-based storage.
"""

import json
import os
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class StorageInterface(ABC):
    """Abstract interface for experiment storage."""

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize storage. Returns True if successful."""
        pass

    @abstractmethod
    def record_experiment(self, experiment: Dict[str, Any]) -> int:
        """Record an experiment. Returns experiment ID."""
        pass

    @abstractmethod
    def query_experiments(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Query experiments with optional filters."""
        pass

    @abstractmethod
    def get_best_experiments(self, metric: str, n: int = 10, objective: str = "maximize") -> List[Dict]:
        """Get top N experiments by metric."""
        pass

    @abstractmethod
    def get_recent_experiments(self, n: int = 10) -> List[Dict]:
        """Get N most recent experiments."""
        pass

    @abstractmethod
    def get_experiment_by_id(self, exp_id: int) -> Optional[Dict]:
        """Get specific experiment by ID."""
        pass

    @abstractmethod
    def get_pareto_front(self, metrics: List[str]) -> List[Dict]:
        """Get pareto-optimal experiments (for multi-objective)."""
        pass

    @abstractmethod
    def count_experiments(self, status: Optional[str] = None) -> int:
        """Count experiments, optionally filtered by status."""
        pass


class DatabaseStorage(StorageInterface):
    """SQLite-based storage implementation."""

    def __init__(self, db_path: str = ".autoresearch/experiments.db"):
        self.db_path = db_path
        self.conn = None

    def initialize(self) -> bool:
        """Initialize SQLite database with schema."""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable dict-like access

            cursor = self.conn.cursor()

            # Experiments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    strategy TEXT NOT NULL,

                    -- Version info
                    commit_hash TEXT,
                    snapshot_path TEXT,

                    -- Hypothesis
                    hypothesis TEXT,
                    files_modified TEXT,  -- JSON array
                    diff TEXT,

                    -- Metrics
                    primary_metric_name TEXT,
                    primary_metric_value REAL,
                    auxiliary_metrics TEXT,  -- JSON object

                    -- Constraints
                    hard_constraints_met BOOLEAN,
                    constraint_violations TEXT,  -- JSON array

                    -- Decision
                    status TEXT CHECK(status IN ('keep', 'discard', 'crash', 'timeout')),
                    decision_reason TEXT,

                    -- Metadata
                    execution_time REAL,
                    error_log TEXT
                )
            """)

            # Pareto front table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pareto_front (
                    experiment_id INTEGER,
                    is_dominated BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (experiment_id) REFERENCES experiments(id)
                )
            """)

            # Bandit arms table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bandit_arms (
                    arm_name TEXT PRIMARY KEY,
                    pulls INTEGER DEFAULT 0,
                    total_reward REAL DEFAULT 0.0,
                    avg_reward REAL DEFAULT 0.0,
                    last_updated DATETIME
                )
            """)

            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON experiments(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON experiments(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_primary_metric ON experiments(primary_metric_value)")

            self.conn.commit()
            return True

        except (sqlite3.Error, OSError) as e:
            print(f"Failed to initialize database: {e}")
            if self.conn:
                self.conn.close()
            return False

    def record_experiment(self, experiment: Dict[str, Any]) -> int:
        """Record experiment to database."""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO experiments (
                task_name, strategy, commit_hash, snapshot_path,
                hypothesis, files_modified, diff,
                primary_metric_name, primary_metric_value, auxiliary_metrics,
                hard_constraints_met, constraint_violations,
                status, decision_reason, execution_time, error_log
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            experiment.get("task_name"),
            experiment.get("strategy"),
            experiment.get("commit_hash"),
            experiment.get("snapshot_path"),
            experiment.get("hypothesis"),
            json.dumps(experiment.get("files_modified", [])),
            experiment.get("diff"),
            experiment.get("primary_metric", {}).get("name"),
            experiment.get("primary_metric", {}).get("value"),
            json.dumps(experiment.get("auxiliary_metrics", {})),
            experiment.get("hard_constraints_met"),
            json.dumps(experiment.get("constraint_violations", [])),
            experiment.get("status"),
            experiment.get("decision_reason"),
            experiment.get("execution_time"),
            experiment.get("error_log")
        ))

        self.conn.commit()
        return cursor.lastrowid

    def query_experiments(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Query experiments with filters."""
        cursor = self.conn.cursor()

        query = "SELECT * FROM experiments WHERE 1=1"
        params = []

        if filters:
            if "status" in filters:
                query += " AND status = ?"
                params.append(filters["status"])
            if "min_metric" in filters:
                query += " AND primary_metric_value >= ?"
                params.append(filters["min_metric"])
            if "strategy" in filters:
                query += " AND strategy = ?"
                params.append(filters["strategy"])

        query += " ORDER BY timestamp DESC"

        if filters and "limit" in filters:
            query += " LIMIT ?"
            params.append(filters["limit"])

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_best_experiments(self, metric: str, n: int = 10, objective: str = "maximize") -> List[Dict]:
        """Get top N experiments by metric."""
        cursor = self.conn.cursor()
        order = "DESC" if objective == "maximize" else "ASC"

        cursor.execute(f"""
            SELECT * FROM experiments
            WHERE status = 'keep' AND primary_metric_name = ?
            ORDER BY primary_metric_value {order}
            LIMIT ?
        """, (metric, n))

        return [dict(row) for row in cursor.fetchall()]

    def get_recent_experiments(self, n: int = 10) -> List[Dict]:
        """Get N most recent experiments."""
        return self.query_experiments({"limit": n})

    def get_experiment_by_id(self, exp_id: int) -> Optional[Dict]:
        """Get specific experiment."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM experiments WHERE id = ?", (exp_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_pareto_front(self, metrics: List[str]) -> List[Dict]:
        """Get pareto-optimal experiments."""
        # TODO: Implement pareto dominance calculation
        # For now, return all kept experiments
        return self.query_experiments({"status": "keep"})

    def count_experiments(self, status: Optional[str] = None) -> int:
        """Count experiments."""
        cursor = self.conn.cursor()
        if status:
            cursor.execute("SELECT COUNT(*) FROM experiments WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT COUNT(*) FROM experiments")
        return cursor.fetchone()[0]

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


class FileStorage(StorageInterface):
    """File-based storage implementation (fallback)."""

    def __init__(self, base_dir: str = ".autoresearch"):
        self.base_dir = Path(base_dir)
        self.results_tsv = self.base_dir / "results.tsv"
        self.experiments_dir = self.base_dir / "experiments"

    def initialize(self) -> bool:
        """Initialize file-based storage."""
        try:
            self.base_dir.mkdir(parents=True, exist_ok=True)
            self.experiments_dir.mkdir(exist_ok=True)

            # Create results.tsv if doesn't exist
            if not self.results_tsv.exists():
                with open(self.results_tsv, "w") as f:
                    f.write("id\ttimestamp\tcommit\tprimary_metric\tauxiliary_metrics\t"
                           "status\tdescription\tconstraints_met\texecution_time\n")

            return True

        except OSError as e:
            print(f"Failed to initialize file storage: {e}")
            return False

    def record_experiment(self, experiment: Dict[str, Any]) -> int:
        """Record experiment to files."""
        # Get next ID
        exp_id = self._get_next_id()

        # Write detailed JSON
        exp_file = self.experiments_dir / f"exp_{exp_id:03d}.json"
        with open(exp_file, "w") as f:
            json.dump(experiment, f, indent=2)

        # Append to TSV
        with open(self.results_tsv, "a") as f:
            f.write(f"{exp_id}\t"
                   f"{experiment.get('timestamp', datetime.now().isoformat())}\t"
                   f"{experiment.get('commit_hash', '')}\t"
                   f"{experiment.get('primary_metric', {}).get('value', 0.0)}\t"
                   f"{json.dumps(experiment.get('auxiliary_metrics', {}))}\t"
                   f"{experiment.get('status', 'unknown')}\t"
                   f"{experiment.get('hypothesis', '')}\t"
                   f"{experiment.get('hard_constraints_met', True)}\t"
                   f"{experiment.get('execution_time', 0.0)}\n")

        return exp_id

    def _get_next_id(self) -> int:
        """Get next experiment ID."""
        if not self.results_tsv.exists():
            return 1

        with open(self.results_tsv, "r") as f:
            lines = f.readlines()
            if len(lines) <= 1:  # Header only
                return 1
            last_line = lines[-1]
            last_id = int(last_line.split("\t")[0])
            return last_id + 1

    def query_experiments(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Query experiments from files."""
        experiments = []

        for exp_file in sorted(self.experiments_dir.glob("exp_*.json"), reverse=True):
            with open(exp_file, "r") as f:
                exp = json.load(f)
                experiments.append(exp)

        # Apply filters
        if filters:
            if "status" in filters:
                experiments = [e for e in experiments if e.get("status") == filters["status"]]
            if "limit" in filters:
                experiments = experiments[:filters["limit"]]

        return experiments

    def get_best_experiments(self, metric: str, n: int = 10, objective: str = "maximize") -> List[Dict]:
        """Get top N experiments."""
        experiments = self.query_experiments({"status": "keep"})
        reverse = (objective == "maximize")
        experiments.sort(
            key=lambda e: e.get("primary_metric", {}).get("value", 0),
            reverse=reverse
        )
        return experiments[:n]

    def get_recent_experiments(self, n: int = 10) -> List[Dict]:
        """Get recent experiments."""
        return self.query_experiments({"limit": n})

    def get_experiment_by_id(self, exp_id: int) -> Optional[Dict]:
        """Get specific experiment."""
        exp_file = self.experiments_dir / f"exp_{exp_id:03d}.json"
        if exp_file.exists():
            with open(exp_file, "r") as f:
                return json.load(f)
        return None

    def get_pareto_front(self, metrics: List[str]) -> List[Dict]:
        """Get pareto front."""
        return self.query_experiments({"status": "keep"})

    def count_experiments(self, status: Optional[str] = None) -> int:
        """Count experiments."""
        experiments = self.query_experiments()
        if status:
            return sum(1 for e in experiments if e.get("status") == status)
        return len(experiments)


def get_storage(prefer_database: bool = True) -> StorageInterface:
    """
    Get storage instance with automatic fallback.

    Args:
        prefer_database: Try SQLite first if True

    Returns:
        Initialized storage instance
    """
    if prefer_database:
        try:
            storage = DatabaseStorage()
            if storage.initialize():
                print("Using SQLite database storage")
                return storage
        except Exception as e:
            print(f"SQLite unavailable ({e}), falling back to file storage")

    # Fallback to file storage
    storage = FileStorage()
    storage.initialize()
    print("Using file-based storage")
    return storage
