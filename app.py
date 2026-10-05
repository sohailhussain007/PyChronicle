from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label
from textual.binding import Binding

from storage.state_storage import SQLiteStateStorage


class PyChronicleApp(App):

    BINDINGS = [
        Binding("left", "previous_line", "Previous"),
        Binding("right", "next_line", "Next"),
    ]

    CSS = """
    #main-area {
        height: 1fr;
    }

    #code-panel {
        width: 70%;
        border: solid green;
        padding: 1;
    }

    #watch-panel {
        width: 30%;
        border: solid blue;
        padding: 1;
    }

    .code-line {
        padding: 0 1;
    }

    .current-line {
        background: yellow;
        color: black;
    }

    #timeline-label {
        padding: 1;
        height: 3;
    }
    """

    def __init__(self):
        super().__init__()

        self.current_line = 1
        self.current_state = 0

        self.storage = SQLiteStateStorage(
            "pychronicle.db"
        )

        self.states = self.storage.get_states()

        with open("trace_test.py", "r") as file:
            self.source_lines = file.readlines()

    def compose(self) -> ComposeResult:
        yield Header()

        yield Horizontal(
            Vertical(
                Static("CODE VIEW"),

                *[
                    Static(
                        f"{number}  {line.rstrip()}",
                        id=f"line-{number}",
                        classes="code-line"
                    )
                    for number, line in enumerate(
                        self.source_lines,
                        start=1
                    )
                ],

                id="code-panel",
            ),

            Vertical(
                Static("WATCH VARIABLES"),

                Static(
                    "x = 10\n"
                    "y = --\n"
                    "z = --",
                    id="watch-variables"
                ),

                id="watch-panel",
            ),

            id="main-area",
        )

        yield Label(
            "Timeline: Line 1",
            id="timeline-label"
        )

        yield Footer()

    def action_next_line(self):
        if self.current_state < len(self.states) - 1:
            self.current_state += 1

            self.current_line = self.states[
                self.current_state
            ][1]

        self.update_ui()

    def action_previous_line(self):
        if self.current_state > 0:
            self.current_state -= 1

            self.current_line = self.states[
                self.current_state
            ][1]

        self.update_ui()

    def set_current_line(self, line_number):
        self.current_line = line_number
        self.update_ui()

    def get_current_variables(self):
        variables = {}

        for state in self.states[:self.current_state + 1]:
            variable_name = state[2]
            variable_value = state[3]

            variables[variable_name] = variable_value

        return variables

    def update_ui(self):

        label = self.query_one(
            "#timeline-label",
            Label
        )

        # Get current historical state
        current_state = self.states[self.current_state]

        line_number = current_state[1]
        variable_name = current_state[2]
        variable_value = current_state[3]

        label.update(
            f"State {self.current_state + 1} | "
            f"Line {line_number} | "
            f"{variable_name} = {variable_value}"
        )

        # Remove old highlighting from all source lines
        for number in range(1, len(self.source_lines) + 1):
            line = self.query_one(
                f"#line-{number}"
            )

            line.remove_class("current-line")

        # Highlight current source line
        current = self.query_one(
            f"#line-{self.current_line}"
        )

        current.add_class("current-line")

        variables = self.query_one(
            "#watch-variables",
            Static
        )

        # Get historical variables
        current_variables = self.get_current_variables()

        if current_variables:
            variables_text = "\n".join(
                f"{name} = {value}"
                for name, value in current_variables.items()
            )

            variables.update(variables_text)

        else:
            variables.update(
                "No variables available"
            )


if __name__ == "__main__":
    app = PyChronicleApp()
    app.run()