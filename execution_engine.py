import sys
import sys
import copy
import time

from ast_rewriter import rewrite_source
from storage.state_storage import SQLiteStateStorage
from delta_compression import calculate_delta


TARGET_FILE = "trace_test.py"
DATABASE_FILE = "pychronicle.db"

previous_variables = {}
previous_captured_state = {}

execution_history = []
captured_states = []

storage = SQLiteStateStorage(DATABASE_FILE)
storage.clear()


def serialize_value(value):
    return repr(value)


def capture_state(variable_name, variable_value, line_number):
    global previous_captured_state

    serialized_value = serialize_value(variable_value)

    current_state = {
        variable_name: serialized_value
    }

    delta = calculate_delta(
        previous_captured_state,
        current_state
    )

    captured_states.append({
        "variable_name": variable_name,
        "variable_value": serialized_value,
        "line_number": line_number
    })

    if delta:
        execution_history.append({
            "line_number": line_number,
            "changes": delta
        })

        storage.save_state(
            timestamp=time.time(),
            line_number=line_number,
            variable_name=variable_name,
            value=variable_value
        )

    previous_captured_state.update(current_state)


def trace_function(frame, event, arg):

    if event == "line":

        filename = frame.f_code.co_filename

        if filename.endswith(TARGET_FILE):

            frame_id = id(frame)

            if frame_id not in previous_variables:
                previous_variables[frame_id] = {}

            old_variables = previous_variables[frame_id]

            current_variables = {
                name: value
                for name, value in frame.f_locals.items()
                if not name.startswith("__")
                and name != "capture_state"
            }

            changes = {}

            for name, value in current_variables.items():

                if name not in old_variables:
                    changes[name] = serialize_value(value)

                elif old_variables[name] != value:
                    changes[name] = serialize_value(value)

            previous_variables[frame_id] = copy.deepcopy(
                current_variables
            )

    elif event == "exception":

        filename = frame.f_code.co_filename

        if filename.endswith(TARGET_FILE):

            exception_type, exception_value, traceback = arg

            execution_history.append({
                "line_number": frame.f_lineno,
                "event": "exception",
                "exception_type": exception_type.__name__,
                "exception_message": str(exception_value)
            })

    elif event == "return":

        frame_id = id(frame)
        previous_variables.pop(frame_id, None)

    return trace_function


# Read target Python file
with open(TARGET_FILE, "r") as file:
    source_code = file.read()


# Rewrite source code using AST
rewritten_code = rewrite_source(source_code)

print("Rewritten Code:\n")
print(rewritten_code)


# Provide capture_state to rewritten program
namespace = {
    "capture_state": capture_state
}


# Run target program
sys.settrace(trace_function)

try:

    compiled_code = compile(
        rewritten_code,
        TARGET_FILE,
        "exec"
    )

    exec(compiled_code, namespace)

except Exception as error:

    print(
        "Program stopped:",
        type(error).__name__,
        "-",
        str(error)
    )

finally:

    sys.settrace(None)
    storage.close()


print("\nAST Captured States:")

for state in captured_states:
    print(state)


print("\nDelta Execution History:")

for state in execution_history:
    print(state)


print("\nSQLite States:")

read_storage = SQLiteStateStorage(DATABASE_FILE)

states = read_storage.get_states()

for state in states:
    print(state)

read_storage.close()