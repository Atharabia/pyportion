# Developer Guide

This guide explains the internal structure of PyPortion so you can understand, modify, and extend the codebase.

## Project Structure

```
pyportion/
├── portion/                # Main source package
│   ├── __main__.py         # Entry point
│   ├── portion.py          # Root CLI app (Typer)
│   ├── base/               # Abstract base classes
│   ├── commands/           # Business logic per command
│   ├── core/               # Singleton managers (logger, template, project)
│   ├── handler/            # CLI binding layer
│   ├── models/             # Pydantic data models
│   ├── step_actions/       # Step implementations
│   └── utils/              # Resolver and Transformer helpers
├── tests/                  # pytest test suite
└── docs/                   # MkDocs documentation
```

---

## Architecture

PyPortion uses a three-layer pattern:

```
CLI input
   │
   ▼
Handler        ← registers the command with Typer, parses CLI args
   │
   ▼
Command        ← orchestrates business logic, talks to managers
   │
   ▼
Action         ← executes a single step (copy, replace, ask…)
```

### Handlers

Handlers live in `portion/handler/`. Each one subclasses `HandlerBase` and registers one or more Typer commands. They are loaded at startup by `load_handlers()` in `portion/handler/__init__.py`.

Handlers only deal with CLI concerns: parsing arguments, printing errors, calling the corresponding command. No business logic lives here.

### Commands

Commands live in `portion/commands/`. Each one subclasses `CommandBase` and holds the business logic for a feature. Commands call core managers (`TemplateManager`, `ProjectManager`) to read/write files and templates.

### Step Actions

Step actions live in `portion/step_actions/`. Each one subclasses `ActionBase` and implements two methods:

- `prepare()` — resolve variables, validate inputs
- `apply()` — execute the change (copy file, replace text, etc.)

The factory function `create_action()` in `portion/step_actions/__init__.py` maps a step type string to the correct action class.

---

## Core Modules

### `Logger` — `portion/core/logger.py`

A singleton wrapping [Rich](https://rich.readthedocs.io) for all terminal output.

| Method | Purpose |
|---|---|
| `info(msg)` | Print an informational message |
| `warn(msg)` | Print a warning |
| `error(msg)` | Print an error |
| `prompt(msg)` | Ask the user for input |
| `pulse(msg)` | Show a spinner while a task runs |

Obtain the instance anywhere with `Logger()`.

### `TemplateManager` — `portion/core/template_manager.py`

A singleton that handles all template file operations. Templates are stored in the OS user data directory (via [platformdirs](https://platformdirs.readthedocs.io)).

| Method | Purpose |
|---|---|
| `download_template(link)` | Git-clone a template from a URL |
| `copy_template(name, project_name)` | Copy `base/` into a new project directory |
| `copy_portion(template, portion_path, dest)` | Copy a file from `.portions/` into the project |
| `read_configuration(name)` | Load and parse a template's `.pyportion.yml` |
| `delete_template(name)` | Delete a template from disk |

### `ProjectManager` — `portion/core/project_manager.py`

A singleton that handles all project file operations. Uses [RedBaron](https://redbaron.readthedocs.io) for AST-based Python file modification.

| Method | Purpose |
|---|---|
| `initialize_project(path, name)` | Create a `.pyportion.yml` in the project |
| `read_configuration(path)` | Load and parse the project's `.pyportion.yml` |
| `replace_in_file(path, replacements)` | Do text substitution inside a file |
| `add_import(path, import_statement)` | Append an import to a Python file |
| `add_to_list(path, list_name, value)` | Append a value to a Python list variable |

---

## Step Actions

Each step action corresponds to a `type` value in a portion's `steps` list.

| Type | Class | What it does |
|---|---|---|
| `ask` | `AskAction` | Prompts the user and stores the answer in memory |
| `set_var` | `SetVarAction` | Derives a new variable from a fixed value or an existing one |
| `copy` | `CopyAction` | Copies a file from `.portions/` into the project |
| `replace` | `ReplaceAction` | Replaces keyword placeholders in a file |
| `add_import` | `AddImportAction` | Appends an import statement to a Python file |
| `add_to_list` | `AddToListAction` | Appends a value to a Python list in a file |

Steps share a `memory` dict — a plain `dict[str, str]` passed through all actions in a portion run. `ask` and `set_var` write to it; `copy`, `replace`, `add_import`, and `add_to_list` read from it via the `Resolver`.

---

## Models

Models live in `portion/models/` and are Pydantic dataclasses.

| File | Models | Purpose |
|---|---|---|
| `template.py` | `TemplateConfig`, `TemplatePortion`, step types | Parsed `.pyportion.yml` of a template |
| `project.py` | `PortionConfig`, `ProjectTemplate` | Parsed `.pyportion.yml` of a project |
| `state.py` | `cli_state` | Global CLI flags (`verbose`, `auto_confirm`) |
| `message.py` | `Message` | All user-facing strings in one place |
| `config.py` | `Config` | Static configuration (app name, paths) |

---

## Utils

### `Resolver` — `portion/utils/resolver.py`

Resolves `$variable` references in strings and path lists using the `memory` dict.

```python
resolver = Resolver(memory={"name": "hello"})
resolver.resolve("$name_command")  # → "hello_command"
resolver.resolve_path(["cli", "$name.py"])  # → ["cli", "hello.py"]
```

### `Transformer` — `portion/utils/transformer.py`

Applies case transformations to a string.

```python
Transformer.transform("my command", "pascalcase")  # → "MyCommand"
Transformer.transform("my command", "camelcase")   # → "myCommand"
```

Supported modes: `pascalcase`, `camelcase`, `titlecase`, `uppercase`, `lowercase`.

---

## Adding a New CLI Command

1. **Create the command** in `portion/commands/my_command.py`:

    ```python
    from portion.base.command import CommandBase

    class MyCommand(CommandBase):
        def run(self, arg: str) -> None:
            self.logger.info(f"Running with {arg}")
    ```

2. **Create the handler** in `portion/handler/my_command.py`:

    ```python
    import typer
    from portion.base.handler import HandlerBase
    from portion.commands.my_command import MyCommand

    class MyCommandHandler(HandlerBase):
        def register(self, cli: typer.Typer) -> None:
            @cli.command("my-command")
            def my_command(arg: str = typer.Argument(...)):
                MyCommand().run(arg)
    ```

3. **Register the handler** in `portion/handler/__init__.py`:

    ```python
    from portion.handler.my_command import MyCommandHandler

    def load_handlers(cli: typer.Typer) -> None:
        ...
        MyCommandHandler().register(cli)
    ```

4. **Add a test** in `tests/commands/test_my_command.py`.

---

## Adding a New Step Action

1. **Define the step model** in `portion/models/template.py`:

    ```python
    class MyStep(BaseModel):
        type: Literal["my_step"]
        my_field: str
    ```

    Add `MyStep` to the `TemplatePortionStepsType` union and `OperationTypes` enum.

2. **Create the action** in `portion/step_actions/my_step.py`:

    ```python
    from portion.base.action import ActionBase
    from portion.models.template import MyStep

    class MyStepAction(ActionBase[MyStep]):
        def prepare(self) -> None:
            # resolve variables, validate
            pass

        def apply(self) -> None:
            # do the work
            pass
    ```

3. **Register the action** in `portion/step_actions/__init__.py`:

    ```python
    from portion.step_actions.my_step import MyStepAction

    def create_action(step, ...):
        ...
        if step.type == "my_step":
            return MyStepAction(step, ...)
    ```

4. **Add a test** in `tests/step_actions/test_my_step.py`.

---

## Running Tests

```bash
poetry run pytest
```

With coverage:

```bash
poetry run pytest --cov=portion --cov-report=term-missing
```

Type checking:

```bash
poetry run mypy portion/
```

Lint:

```bash
poetry run flake8 portion/
```
