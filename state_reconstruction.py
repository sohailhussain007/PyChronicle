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


print("State 1:")
print(reconstruct_state(DATABASE_FILE, 0))

print("\nState 2:")
print(reconstruct_state(DATABASE_FILE, 1))

print("\nState 3:")
print(reconstruct_state(DATABASE_FILE, 2))