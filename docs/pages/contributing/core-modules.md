# Core Modules

Core modules live in `portion/core/` and are all singletons — call the class to get the shared instance from anywhere in the codebase.

---

## `Logger` — `portion/core/logger.py`

Wraps [Rich](https://rich.readthedocs.io) for all terminal output. Respects the global `verbose` flag from `cli_state`.

```python
from portion.core.logger import Logger

logger = Logger()
logger.info("Template downloaded.")
```

| <div style="min-width:160px">Method</div> | Purpose |
|---|---|
| `info(msg)` | Print an informational message |
| `warn(msg)` | Print a warning |
| `error(msg)` | Print an error and exit |
| `prompt(msg)` | Ask the user for input and return the answer |
| `pulse(msg)` | Show a spinner while a task runs |

---

## `TemplateManager` — `portion/core/template_manager.py`

Handles all template file operations. Templates are stored in the OS user data directory via [platformdirs](https://platformdirs.readthedocs.io).

```python
from portion.core.template_manager import TemplateManager

tm = TemplateManager()
tm.download_template("https://github.com/org/my-template")
```

| <div style="min-width:290px">Method</div> | Purpose |
|---|---|
| `download_template(link)` | Git-clone a template from a URL |
| `copy_template(name, project_name)` | Copy `base/` into a new project directory |
| `copy_portion(template, portion_path, dest)` | Copy a file from `.portions/` into the project |
| `read_configuration(name)` | Load and parse a template's `.pyportion.yml` |
| `delete_template(name)` | Delete a template from disk |

---

## `ProjectManager` — `portion/core/project_manager.py`

Handles all project file operations. Uses [RedBaron](https://redbaron.readthedocs.io) for AST-based Python file modification, which means it parses the actual Python syntax tree rather than doing raw text replacement.

```python
from portion.core.project_manager import ProjectManager

pm = ProjectManager()
pm.add_import(["cli", "__init__.py"], "from .my_cmd import my_cmd")
```

| <div style="min-width:270px">Method</div> | Purpose |
|---|---|
| `initialize_project(path, name)` | Create a `.pyportion.yml` in the project |
| `read_configuration(path)` | Load and parse the project's `.pyportion.yml` |
| `replace_in_file(path, replacements)` | Do text substitution inside a file |
| `add_import(path, import_statement)` | Append an import to a Python file |
| `add_to_list(path, list_name, value)` | Append a value to a Python list variable |
