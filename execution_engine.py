import sys
import runpy

TARGET_FILE = "trace_test.py"

previous_variables = {}


def trace_function(frame, event, arg):
    global previous_variables

    if event == "line":
        filename = frame.f_code.co_filename

        if filename.endswith(TARGET_FILE):

            current_variables = {
                name: value
                for name, value in frame.f_locals.items()
                if not name.startswith("__")
            }

            changes = {}

            for name, value in current_variables.items():
                if name not in previous_variables:
                    changes[name] = value
                elif previous_variables[name] != value:
                    changes[name] = value

            execution_state = {
                "line_number": frame.f_lineno,
                "changes": changes
            }

            print("Execution State:", execution_state)

            previous_variables = current_variables.copy()

    return trace_function


sys.settrace(trace_function)

runpy.run_path(TARGET_FILE)

sys.settrace(None)