from typing import Generic
from typing import TypeVar

from portion.core import Terminal
from portion.models import ProjectTemplate

TStep = TypeVar("TStep")


class ActionBase(Generic[TStep]):
    def __init__(self,
                 step: TStep,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 terminal: Terminal) -> None:
        self.step = step
        self.project_template = project_template
        self.memory = memory
        self.terminal = terminal
        self.skipped = False

    def prepare(self) -> None:
        ...

    def apply(self) -> None:
        ...
