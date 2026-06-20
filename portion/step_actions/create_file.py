import os

from portion.base import ActionBase
from portion.core import Terminal
from portion.models import Message
from portion.models import ProjectTemplate
from portion.models import TemplateCreateFileAction
from portion.utils import Resolver


class CreateFileAction(ActionBase[TemplateCreateFileAction]):
    def __init__(self,
                 step: TemplateCreateFileAction,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 terminal: Terminal) -> None:
        super().__init__(step, project_template, memory, terminal)

    def prepare(self) -> None:
        self.step.path = Resolver.resolve(self.memory, self.step.path)
        self.step.content = Resolver.resolve_variable(self.memory,
                                                      self.step.content)

    def get_summary(self) -> str | None:
        return Message.Step.FILE_CREATED.format(
            path="/".join(self.step.path)
        )

    def apply(self) -> None:
        file_path = os.path.join(*self.step.path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(self.step.content)
