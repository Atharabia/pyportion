import os

from portion.base import ActionBase
from portion.core import Terminal
from portion.models import Message
from portion.models import ProjectTemplate
from portion.models import TemplateCreateFolderAction
from portion.utils import Resolver


class CreateFolderAction(ActionBase[TemplateCreateFolderAction]):
    def __init__(self,
                 step: TemplateCreateFolderAction,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 terminal: Terminal) -> None:
        super().__init__(step, project_template, memory, terminal)

    def prepare(self) -> None:
        self.step.path = Resolver.resolve(self.memory, self.step.path)

    def get_summary(self) -> str | None:
        return Message.Step.FOLDER_CREATED.format(
            path="/".join(self.step.path)
        )

    def apply(self) -> None:
        os.makedirs(os.path.join(*self.step.path), exist_ok=True)
