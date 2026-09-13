"""
PyChronicle State Storage Module

This module provides the foundation for storing
chronological variable states during program execution.
"""

import pickle
import sqlite3


class StateStorage:
    """Base interface for PyChronicle state storage."""

    def save_state(
        self,
        timestamp,
        line_number,
        variable_name,
        serialized_value,
    ):
        """Save a variable state."""
        raise NotImplementedError

    def get_states(self):
        """Return all stored variable states chronologically."""
        raise NotImplementedError

    def clear(self):
        """Clear all stored states."""
        raise NotImplementedError


class SQLiteStateStorage(StateStorage):
    """SQLite-based storage for chronological variable states."""

    def __init__(self, database_path="pychronicle.db"):
        """Initialize the SQLite database."""
        self.database_path = database_path
        self.connection = sqlite3.connect(self.database_path)
        self._create_schema()

    def _create_schema(self):
        """Create the state storage table if it does not exist."""
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS variable_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                line_number INTEGER NOT NULL,
                variable_name TEXT NOT NULL,
                serialized_value BLOB NOT NULL
            )
            """
        )
        self.connection.commit()

    def save_state(
        self,
        timestamp,
        line_number,
        variable_name,
        value,
    ):
        """Serialize and save a variable state to SQLite."""
        serialized_value = pickle.dumps(value)

        self.connection.execute(
            """
            INSERT INTO variable_states
            (timestamp, line_number, variable_name, serialized_value)
            VALUES (?, ?, ?, ?)
            """,
            (
                timestamp,
                line_number,
                variable_name,
                serialized_value,
            ),
        )
        self.connection.commit()

    def get_states(self):
        """Return all stored variable states chronologically."""
        cursor = self.connection.execute(
            """
            SELECT timestamp, line_number, variable_name, serialized_value
            FROM variable_states
            ORDER BY timestamp ASC, id ASC
            """
        )

        rows = cursor.fetchall()

        return [
            (
                timestamp,
                line_number,
                variable_name,
                pickle.loads(serialized_value),
            )
            for timestamp, line_number, variable_name, serialized_value in rows
        ]

    def close(self):
        """Close the database connection."""
        self.connection.close()