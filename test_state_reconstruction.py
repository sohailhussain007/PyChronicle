import sqlite3
import pickle

from state_reconstruction import (
    reconstruct_state,
    get_reconstructed_timeline,
    get_state_by_number,
    get_timeline_for_ui,
    get_ui_state_by_number
)


DATABASE_FILE = "test_state_reconstruction.db"


def create_test_database():
    connection = sqlite3.connect(DATABASE_FILE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS variable_states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            line_number INTEGER NOT NULL,
            variable_name TEXT NOT NULL,
            serialized_value BLOB NOT NULL
        )
    """)

    connection.execute("DELETE FROM variable_states")

    states = [
        (1.0, 1, "x", 10),
        (2.0, 2, "x", 20),
        (3.0, 3, "y", 30),
    ]

    for timestamp, line_number, variable_name, value in states:
        connection.execute(
            """
            INSERT INTO variable_states
            (timestamp, line_number, variable_name, serialized_value)
            VALUES (?, ?, ?, ?)
            """,
            (
                timestamp,
                line_number,
                variable_name,
                pickle.dumps(value)
            )
        )

    connection.commit()
    connection.close()


def test_reconstruct_state():
    create_test_database()

    result = reconstruct_state(
        DATABASE_FILE,
        1
    )

    assert result == {
        "x": 20
    }


def test_reconstructed_timeline():
    create_test_database()

    timeline = get_reconstructed_timeline(
        DATABASE_FILE
    )

    assert len(timeline) == 3

    assert timeline[0]["state"] == {
        "x": 10
    }

    assert timeline[1]["state"] == {
        "x": 20
    }

    assert timeline[2]["state"] == {
        "x": 20,
        "y": 30
    }


def test_get_state_by_number():
    create_test_database()

    result = get_state_by_number(
        DATABASE_FILE,
        2
    )

    assert result["state_number"] == 2
    assert result["line_number"] == 2
    assert result["state"] == {
        "x": 20
    }


def test_ui_timeline():
    create_test_database()

    result = get_timeline_for_ui(
        DATABASE_FILE
    )

    assert result[0] == {
        "state_number": 1,
        "line_number": 1,
        "state": {
            "x": 10
        }
    }


def test_ui_state_by_number():
    create_test_database()

    result = get_ui_state_by_number(
        DATABASE_FILE,
        3
    )

    assert result == {
        "state_number": 3,
        "line_number": 3,
        "state": {
            "x": 20,
            "y": 30
        }
    }


def test_invalid_state_number():
    create_test_database()

    result = get_ui_state_by_number(
        DATABASE_FILE,
        999
    )

    assert result is None