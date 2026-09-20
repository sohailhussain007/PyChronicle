from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label
from textual.binding import Binding


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

    def compose(self) -> ComposeResult:
        yield Header()

        yield Horizontal(
            Vertical(
                Static("CODE VIEW"),

                Static(
                    "1  x = 10",
                    id="line-1",
                    classes="code-line"
                ),

                Static(
                    "2  y = 20",
                    id="line-2",
                    classes="code-line"
                ),

                Static(
                    "3  z = x + y",
                    id="line-3",
                    classes="code-line"
                ),

                Static(
                    "4  print(z)",
                    id="line-4",
                    classes="code-line"
                ),

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
        if self.current_line < 4:
            self.current_line += 1

        self.update_ui()

    def action_previous_line(self):
        if self.current_line > 1:
            self.current_line -= 1

        self.update_ui()

    def set_current_line(self, line_number):
        self.current_line = line_number
        self.update_ui()

    def update_ui(self):

        label = self.query_one(
            "#timeline-label",
            Label
        )

        label.update(
            f"Timeline: Line {self.current_line}"
        )

        for number in range(1, 5):
            line = self.query_one(
                f"#line-{number}"
            )

            line.remove_class("current-line")

        current = self.query_one(
            f"#line-{self.current_line}"
        )

        current.add_class("current-line")

        variables = self.query_one(
            "#watch-variables",
            Static
        )

        if self.current_line == 1:
            variables.update(
                "x = 10\n"
                "y = --\n"
                "z = --"
            )

        elif self.current_line == 2:
            variables.update(
                "x = 10\n"
                "y = 20\n"
                "z = --"
            )

        elif self.current_line == 3:
            variables.update(
                "x = 10\n"
                "y = 20\n"
                "z = 30"
            )

        elif self.current_line == 4:
            variables.update(
                "x = 10\n"
                "y = 20\n"
                "z = 30"
            )


if __name__ == "__main__":
    app = PyChronicleApp()
    app.run()   