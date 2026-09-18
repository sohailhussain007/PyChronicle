import sys
import copy

from ast_rewriter import rewrite_source


TARGET_FILE = "trace_test.py"

previous_variables = {}
execution_history = []
captured_states = []


def serialize_value(value):
    return repr(value)


def capture_state(variable_name, variable_value, line_number):
    captured_states.append({
        "variable_name": variable_name,
        "variable_value": serialize_value(variable_value),
        "line_number": line_number
    })

    execution_history.append({
        "line_number": line_number,
        "changes": {
            variable_name: serialize_value(variable_value)
        }
    })

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

            # execution_state = {
            #     "line_number": frame.f_lineno,
            #     "changes": changes
            # }

            # execution_history.append(execution_state)

            previous_variables[frame_id] = copy.deepcopy(
                current_variables
            )

    elif event == "exception":

        filename = frame.f_code.co_filename

        if filename.endswith(TARGET_FILE):

            exception_type, exception_value, traceback = arg

            execution_state = {
                "line_number": frame.f_lineno,
                "event": "exception",
                "exception_type": exception_type.__name__,
                "exception_message": str(exception_value)
            }

            execution_history.append(execution_state)

    elif event == "return":

        frame_id = id(frame)

        previous_variables.pop(frame_id, None)

    return trace_function


# -----------------------------------
# Read original Python file
# -----------------------------------

with open(TARGET_FILE, "r") as file:
    source_code = file.read()


# -----------------------------------
# Rewrite code using AST Rewriter
# -----------------------------------

rewritten_code = rewrite_source(source_code)

print("Rewritten Code:\n")
print(rewritten_code)


# -----------------------------------
# Provide capture_state() to rewritten code
# -----------------------------------

namespace = {
    "capture_state": capture_state
}


# -----------------------------------
# Execute rewritten code with tracer
# -----------------------------------

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


# -----------------------------------
# AST captured states
# -----------------------------------

print("\nAST Captured States:")

for state in captured_states:
    print(state)


# -----------------------------------
# Execution history
# -----------------------------------

print("\nExecution History:")

for state in execution_history:
    print(state)