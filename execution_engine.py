import sys
from ast_rewriter import rewrite_source
TARGET_FILE = "test_target.py"
previous_variables = {}
execution_history = []
capture_events = []
def capture_state(variable_name, variable_value):
    """Called by the AST Rewriter after each assignment."""
    caller_frame = sys._getframe(1)
    capture_events.append({
        "line_number": caller_frame.f_lineno,
        "variable_name": variable_name,
        "value": variable_value
    })
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
            execution_history.append(execution_state)
            previous_variables = current_variables.copy()
    return trace_function
# Read the target Python program
with open(TARGET_FILE, "r", encoding="utf-8") as file:
    source_code = file.read()
# Rewrite the target program using AST Rewriter
rewritten_code = rewrite_source(source_code)
print("Rewritten Code:")
print("----------------")
print(rewritten_code)
# Execute rewritten code with tracing enabled
sys.settrace(trace_function)
try:
    exec(
        compile(rewritten_code, TARGET_FILE, "exec"),
        {
            "__name__": "__main__",
            "capture_state": capture_state
        }
    )
finally:
    sys.settrace(None)
print("\nCapture Events:")
print("----------------")
for event in capture_events:
    print(event)
print("\nExecution History:")
print("----------------")
for state in execution_history:
    print(state)