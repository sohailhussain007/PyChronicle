# PyChronicle
### AST-Powered Time-Travel Debugger for Python

PyChronicle is a Python debugging tool that records program execution states and allows developers to inspect historical variable values without rerunning the program.

## 🚀 Features

- **AST-Based Code Rewriting:** Adds state-capturing hooks to Python code.
- **Execution Tracking:** Monitors program execution using Python's `sys.settrace()`.
- **Variable State Tracking:** Captures variable values during execution.
- **Delta Compression:** Records changes in variable states.
- **SQLite Storage:** Stores recorded states for later inspection.
- **State Reconstruction:** Reconstructs historical program states.
- **Interactive Terminal UI:** Navigate through recorded states using the Textual interface.
- **Watch Variables:** Track a specific variable through the CLI.
- **Exception Tracking:** Captures runtime exception information.

## 🛠️ Technology Stack

- Python
- Python AST
- `sys.settrace()`
- SQLite
- Textual
- Click

## 📂 Project Structure

```text
PyChronicle/
├── ast_rewriter.py
├── execution_engine.py
├── delta_compression.py
├── state_reconstruction.py
├── storage/
│   └── state_storage.py
├── app.py
├── cli.py
├── trace_test.py
├── test_delta_compression.py
├── test_state_reconstruction.py
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd PyChronicle
```

Install the required libraries:

```bash
pip install click textual
```

## ▶️ Usage

### Run a Python program

```bash
python cli.py run trace_test.py
```

### Watch a specific variable

```bash
python cli.py run trace_test.py --watch total
```

### Launch the Textual UI

```bash
python app.py
```

Use the **Left and Right arrow keys** to navigate through recorded execution states in the UI.

## 🧪 Testing

Run the automated tests:

```bash
python -m pytest
```

The project was tested with **14 passing automated tests**.

## 👥 Team Contribution

This project was developed collaboratively as a team project.

My contributions included:
- Execution Engine development using `sys.settrace()`
- Delta compression and state reconstruction
- Testing and debugging
- Textual UI and execution workflow integration
- Team coordination and final GitHub integration

## 🎯 Objective

The objective of PyChronicle is to make Python debugging more informative by recording execution history and allowing developers to inspect previous program states.

---

**Project:** PyChronicle — AST-Powered Time-Travel Debugger for Python
