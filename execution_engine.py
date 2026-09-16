import sys
import runpy
import copy

TARGET_FILE = "trace_test.py"

previous_variables = {}
execution_history = []


def serialize_value(value):
    return repr(value)


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
            }

            changes = {}

            for name, value in current_variables.items():

                if name not in old_variables:
                    changes[name] = serialize_value(value)

                elif old_variables[name] != value:
                    changes[name] = serialize_value(value)

            execution_state = {
                "line_number": frame.f_lineno,
                "changes": changes
            }

            execution_history.append(execution_state)

            previous_variables[frame_id] = copy.deepcopy(current_variables)

    elif event == "return":
        frame_id = id(frame)
        previous_variables.pop(frame_id, None)

    return trace_function


sys.settrace(trace_function)

runpy.run_path(TARGET_FILE)

sys.settrace(None)


print("\nExecution History:")

for state in execution_history:
    print(state)