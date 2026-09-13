"""
PyChronicle State Storage Module

This module provides the foundation for storing
chronological variable states during program execution.
"""


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