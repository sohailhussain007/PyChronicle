from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label
from textual.binding import Binding

from storage.state_storage import SQLiteStateStorage
from state_reconstruction import get_timeline_for_ui


DATABASE_FILE = "pychronicle.db"


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

        self.storage = SQLiteStateStorage(DATABASE_FILE)

        self.timeline = get_timeline_for_ui(DATABASE_FILE)

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
                    "Loading...",
                    id="watch-variables"
                ),

                id="watch-panel",
            ),

            id="main-area",
        )

        yield Label(
            "Timeline: Loading...",
            id="timeline-label"
        )

        yield Footer()

    def on_mount(self):
        if self.timeline:
            self.current_line = self.timeline[0]["line_number"]

        self.update_ui()

    def action_next_line(self):
        if self.current_state < len(self.timeline) - 1:
            self.current_state += 1

            self.current_line = self.timeline[
                self.current_state
            ]["line_number"]

            self.update_ui()

    def action_previous_line(self):
        if self.current_state > 0:
            self.current_state -= 1

            self.current_line = self.timeline[
                self.current_state
            ]["line_number"]

            self.update_ui()

    def update_ui(self):

        if not self.timeline:
            return

        current_state = self.timeline[self.current_state]

        line_number = current_state["line_number"]
        variables_state = current_state["state"]

        label = self.query_one(
            "#timeline-label",
            Label
        )

        label.update(
            f"State {current_state['state_number']} | "
            f"Line {line_number}"
        )

        # Remove old highlighting
        for number in range(
            1,
            len(self.source_lines) + 1
        ):
            line = self.query_one(
                f"#line-{number}"
            )

            line.remove_class("current-line")

        # Highlight current line
        current = self.query_one(
            f"#line-{line_number}"
        )

        current.add_class("current-line")

        # Update watch variables
        variables = self.query_one(
            "#watch-variables",
            Static
        )

        if variables_state:
            variables_text = "\n".join(
                f"{name} = {value}"
                for name, value in variables_state.items()
            )

            variables.update(variables_text)

        else:
            variables.update(
                "No variables available"
            )


if __name__ == "__main__":
    app = PyChronicleApp()
    app.run()