# Architecture

## Project Structure

```
pyportion/
├── portion/                # Main source package
│   ├── __main__.py         # Entry point — calls Portion().run()
│   ├── portion.py          # Root CLI app (Typer) and global flags
│   ├── base/               # Abstract base classes (CommandBase, HandlerBase, ActionBase)
│   ├── commands/           # Business logic — one file per command
│   ├── core/               # Singleton managers (Logger, TemplateManager, ProjectManager)
│   ├── handler/            # CLI binding — registers commands with Typer
│   ├── models/             # Pydantic data models
│   ├── step_actions/       # Step implementations (copy, replace, ask, …)
│   └── utils/              # Resolver and Transformer helpers
├── tests/                  # pytest test suite
└── docs/                   # MkDocs documentation
```

---

## The Three-Layer Pattern

Every CLI command flows through three layers:

```
CLI input
   │
   ▼
Handler        ← registers the command with Typer, parses CLI args
   │
   ▼
Command        ← orchestrates business logic, calls core managers
   │
   ▼
Action         ← executes a single step (copy, replace, ask, …)
```

### Handlers (`portion/handler/`)

Each handler subclasses `HandlerBase` and registers one or more Typer commands. They are loaded at startup by `load_handlers()` in `portion/handler/__init__.py`.

Handlers deal only with CLI concerns: parsing arguments, calling the command, printing top-level errors. No business logic lives here.

### Commands (`portion/commands/`)

Each command subclasses `CommandBase` and holds the business logic for one feature. Commands call core managers (`TemplateManager`, `ProjectManager`) to read and write files and templates.

### Actions (`portion/step_actions/`)

Each action subclasses `ActionBase` and implements two methods:

- `prepare()` — resolve variables, validate inputs
- `apply()` — execute the change (copy file, replace text, etc.)

The factory function `create_action()` in `portion/step_actions/__init__.py` maps a step `type` string to the correct action class.

---

## Models (`portion/models/`)

All data structures are Pydantic models.

| <div style="min-width:120px">File</div> | <div style="min-width:240px">Models</div> | Purpose |
|---|---|---|
| `template.py` | `TemplateConfig`, `TemplatePortion`, step types | Parsed `.pyportion.yml` of a template |
| `project.py` | `PortionConfig`, `ProjectTemplate` | Parsed `.pyportion.yml` of a project |
| `state.py` | `cli_state` | Global CLI flags (`verbose`, `auto_confirm`) |
| `message.py` | `Message` | All user-facing strings in one place |
| `config.py` | `Config` | Static configuration (app name, paths) |

---

## Utils (`portion/utils/`)

### `Resolver` — `portion/utils/resolver.py`

Resolves `$variable` references in strings and path lists using the shared `memory` dict.

```python
resolver = Resolver(memory={"name": "hello"})
resolver.resolve("$name_command")               # → "hello_command"
resolver.resolve_path(["cli", "$name.py"])      # → ["cli", "hello.py"]
```

### `Transformer` — `portion/utils/transformer.py`

Applies case transformations to a string.

```python
Transformer.transform("my command", "pascalcase")  # → "MyCommand"
Transformer.transform("my command", "camelcase")   # → "myCommand"
```

Supported modes: `pascalcase`, `camelcase`, `titlecase`, `uppercase`, `lowercase`.
