# Step Actions

Step actions live in `portion/step_actions/`. Each one maps to a `type` value in a portion's `steps` list and is responsible for executing one unit of work during a `portion build` run.

---

## How They Work

All actions subclass `ActionBase[TStep]` and implement two methods:

```python
class MyAction(ActionBase[MyStep]):
    def prepare(self) -> None:
        # Resolve variables, validate fields
        ...

    def apply(self) -> None:
        # Execute the change
        ...
```

Steps in a portion share a `memory` dict — a plain `dict[str, str]` that is passed through every action in the run. `ask` and `set_var` write to it; all other actions read from it through the `Resolver`.

The factory function `create_action()` in `portion/step_actions/__init__.py` maps a step type string to the correct action class.

---

## Available Actions

| <div style="min-width:120px">Type</div> | <div style="min-width:170px">Class</div> | What it does |
|---|---|---|
| `ask` | `AskAction` | Prompts the user and stores the answer in `memory` |
| `set_var` | `SetVarAction` | Derives a new variable from a fixed value or an existing one and stores it in `memory` |
| `copy` | `CopyAction` | Copies a file from `.portions/` into the project |
| `replace` | `ReplaceAction` | Replaces keyword placeholders in a file |
| `add_import` | `AddImportAction` | Appends an import statement to a Python file |
| `add_to_list` | `AddToListAction` | Appends a value to a Python list variable in a file |

---

## File Map

| <div style="min-width:200px">File</div> | Class |
|---|---|
| `step_actions/ask.py` | `AskAction` |
| `step_actions/set_var.py` | `SetVarAction` |
| `step_actions/copy.py` | `CopyAction` |
| `step_actions/replace.py` | `ReplaceAction` |
| `step_actions/add_import.py` | `AddImportAction` |
| `step_actions/add_to_list.py` | `AddToListAction` |
| `step_actions/__init__.py` | `create_action()` factory |
