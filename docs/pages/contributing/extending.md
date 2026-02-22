# Extending PyPortion

## Adding a New CLI Command

Follow these four steps to add a new top-level command.

**1. Create the command** in `portion/commands/my_command.py`:

```python
from portion.base.command import CommandBase

class MyCommand(CommandBase):
    def run(self, arg: str) -> None:
        self.logger.info(f"Running with {arg}")
```

**2. Create the handler** in `portion/handler/my_command.py`:

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

**3. Register the handler** in `portion/handler/__init__.py`:

```python
from portion.handler.my_command import MyCommandHandler

def load_handlers(cli: typer.Typer) -> None:
    ...
    MyCommandHandler().register(cli)
```

**4. Add a test** in `tests/commands/test_my_command.py`.

---

## Adding a New Step Action

Follow these four steps to add a new step type.

**1. Define the step model** in `portion/models/template.py`:

```python
class MyStep(BaseModel):
    type: Literal["my_step"]
    my_field: str
```

Then add `MyStep` to the `TemplatePortionStepsType` union and add `"my_step"` to the `OperationTypes` enum.

**2. Create the action** in `portion/step_actions/my_step.py`:

```python
from portion.base.action import ActionBase
from portion.models.template import MyStep

class MyStepAction(ActionBase[MyStep]):
    def prepare(self) -> None:
        # Resolve variables, validate inputs
        pass

    def apply(self) -> None:
        # Execute the change
        pass
```

**3. Register the action** in `portion/step_actions/__init__.py`:

```python
from portion.step_actions.my_step import MyStepAction

def create_action(step, ...):
    ...
    if step.type == "my_step":
        return MyStepAction(step, ...)
```

**4. Add a test** in `tests/step_actions/test_my_step.py`.
