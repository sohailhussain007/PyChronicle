from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label

from storage.state_storage import SQLiteStateStorage


DATABASE_FILE = "pychronicle.db"
TARGET_FILE = "trace_test.py"


class PyChronicleApp(App):

    BINDINGS = [
        ("left", "previous_state", "Previous"),
        ("right", "next_state", "Next"),
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

    #state-label {
        padding: 1;
    }
    """

    def __init__(self):
        super().__init__()

        self.states = []
        self.code_lines = []
        self.current_state = 0
        self.current_variables = {}

        self.load_data()

    def load_data(self):
        # Load source code
        with open(TARGET_FILE, "r") as file:
            self.code_lines = file.readlines()

        # Load states from SQLite
        storage = SQLiteStateStorage(DATABASE_FILE)

        try:
            self.states = storage.get_states()
        finally:
            storage.close()

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
                    for number, line in enumerate(self.code_lines, start=1)
                ],

                id="code-panel",
            ),

            Vertical(
                Static("WATCH VARIABLES"),

                Static(
                    "No state selected",
                    id="watch-variables"
                ),

                id="watch-panel",
            ),

            id="main-area",
        )

        yield Label(
            "Timeline: State 1",
            id="timeline-label"
        )

        yield Label(
            "No states loaded",
            id="state-label"
        )

        yield Footer()

    def on_mount(self):
        if self.states:
            self.update_ui()

    def action_next_state(self):
        if not self.states:
            return

        if self.current_state < len(self.states) - 1:
            self.current_state += 1

        self.update_ui()

    def action_previous_state(self):
        if not self.states:
            return

        if self.current_state > 0:
            self.current_state -= 1

        self.update_ui()

    def update_ui(self):

        if not self.states:
            return

        # Reconstruct variables from beginning up to current state
        variables = {}

        for index in range(self.current_state + 1):
            _, _, variable_name, value = self.states[index]
            variables[variable_name] = value

        self.current_variables = variables

        # Current state
        timestamp, line_number, variable_name, value = self.states[
            self.current_state
        ]

        # Timeline label
        timeline = self.query_one(
            "#timeline-label",
            Label
        )

        timeline.update(
            f"Timeline: State {self.current_state + 1} / {len(self.states)}"
        )

        # State information
        state_label = self.query_one(
            "#state-label",
            Label
        )

        state_label.update(
            f"Line {line_number} | {variable_name} = {value}"
        )

        # Remove previous line highlighting
        for number in range(1, len(self.code_lines) + 1):
            line = self.query_one(
                f"#line-{number}"
            )

            line.remove_class("current-line")

        # Highlight current line
        current_line = self.query_one(
            f"#line-{line_number}"
        )

        current_line.add_class("current-line")

        # Update watch variables
        variables_widget = self.query_one(
            "#watch-variables",
            Static
        )

        if variables:
            variable_text = "\n".join(
                f"{name} = {value}"
                for name, value in variables.items()
            )

            variables_widget.update(variable_text)
        else:
            variables_widget.update("No variables")


if __name__ == "__main__":
    app = PyChronicleApp()
    app.run()