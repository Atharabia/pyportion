from portion.base import ActionBase
from portion.core import ProjectManager
from portion.core import Terminal
from portion.models import ProjectTemplate
from portion.models import TemplateAddPortionStep
from portion.utils import Resolver


class AddPortion(ActionBase[TemplateAddPortionStep]):
    def __init__(self,
                 step: TemplateAddPortionStep,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 logger: Terminal) -> None:
        super().__init__(step, project_template, memory, logger)
        self.project_manager = ProjectManager()

    def prepare(self) -> None:
        self.step.path = Resolver.resolve(self.memory,
                                          self.step.path)

    def apply(self) -> None:
        self.project_manager.add_portion(self.step.path,
                                         self.step.value)
