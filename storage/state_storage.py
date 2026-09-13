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


def _validate_state(timestamp, line_number, variable_name):
    """Validate common state information."""
    if not isinstance(timestamp, (int, float)):
        raise TypeError("timestamp must be a number")

    if not isinstance(line_number, int):
        raise TypeError("line_number must be an integer")

    if line_number < 1:
        raise ValueError("line_number must be greater than or equal to 1")

    if not isinstance(variable_name, str):
        raise TypeError("variable_name must be a string")

    if not variable_name:
        raise ValueError("variable_name cannot be empty")


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
        _validate_state(timestamp, line_number, variable_name)

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

    def clear(self):
        """Remove all stored variable states."""
        self.connection.execute("DELETE FROM variable_states")
        self.connection.commit()

    def close(self):
        """Close the database connection.""" 
        self.connection.close()


class InMemoryStateStorage(StateStorage):
    """In-memory storage for chronological variable states."""

    def __init__(self):
        """Initialize an empty in-memory state list."""
        self.states = []

    def save_state(
        self,
        timestamp,
        line_number,
        variable_name,
        value,
    ):
        """Serialize and store a variable state in memory."""
        _validate_state(timestamp, line_number, variable_name)

        serialized_value = pickle.dumps(value)

        self.states.append(
            (
                timestamp,
                line_number,
                variable_name,
                serialized_value,
            )
        )

    def get_states(self):
        """Return all stored variable states chronologically."""
        ordered_states = sorted(
            self.states,
            key=lambda state: state[0],
        )

        return [
            (
                timestamp,
                line_number,
                variable_name,
                pickle.loads(serialized_value),
            )
            for timestamp, line_number, variable_name, serialized_value
            in ordered_states
        ]

    def clear(self):
        """Remove all stored states from memory."""
        self.states = []