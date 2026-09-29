import sqlite3
import pickle


DATABASE_FILE = "pychronicle.db"


def reconstruct_state(database_path, target_state_index):
    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT line_number, variable_name, serialized_value
        FROM variable_states
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()

    connection.close()

    current_state = {}

    for index, row in enumerate(rows):
        if index > target_state_index:
            break

        line_number, variable_name, serialized_value = row

        value = pickle.loads(serialized_value)

        current_state[variable_name] = value

    return current_state


def reconstruct_state_at_line(database_path, target_line_number):
    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT line_number, variable_name, serialized_value
        FROM variable_states
        WHERE line_number <= ?
        ORDER BY id ASC
    """, (target_line_number,))

    rows = cursor.fetchall()

    connection.close()

    current_state = {}

    for line_number, variable_name, serialized_value in rows:
        value = pickle.loads(serialized_value)
        current_state[variable_name] = value

    return {
        "line_number": target_line_number,
        "state": current_state
    }

def get_reconstructed_timeline(database_path):
    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, line_number
        FROM variable_states
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()

    connection.close()

    timeline = []

    for state_number, (database_id, line_number) in enumerate(rows, start=1):
        state = reconstruct_state(
            database_path,
            state_number - 1
        )

        timeline.append({
            "state_number": state_number,
            "database_id": database_id,
            "line_number": line_number,
            "state": state
        })

    return timeline

def get_state_by_number(database_path, state_number):
    timeline = get_reconstructed_timeline(database_path)

    for item in timeline:
        if item["state_number"] == state_number:
            return item

    return None

def get_timeline_for_ui(database_path):
    timeline = get_reconstructed_timeline(database_path)

    ui_timeline = []

    for item in timeline:
        ui_timeline.append({
            "state_number": item["state_number"],
            "line_number": item["line_number"],
            "state": item["state"]
        })

    return ui_timeline