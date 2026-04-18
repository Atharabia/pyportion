from portion.base import ActionBase
from portion.core import ProjectManager
from portion.core import Terminal
from portion.models import Message
from portion.models import ProjectTemplate
from portion.models import TemplateAddPortionAction
from portion.utils import Resolver


class AddPortion(ActionBase[TemplateAddPortionAction]):
    def __init__(self,
                 step: TemplateAddPortionAction,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 terminal: Terminal) -> None:
        super().__init__(step, project_template, memory, terminal)
        self.project_manager = ProjectManager()

    def prepare(self) -> None:
        self.step.path = Resolver.resolve(self.memory,
                                          self.step.path)

    def get_summary(self) -> str | None:
        return Message.Step.CODE_BLOCK_ADDED.format(path=self.step.path)

    def apply(self) -> None:
        self.project_manager.add_portion(self.step.path,
                                         self.step.value)
