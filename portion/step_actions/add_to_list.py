from portion.base import ActionBase
from portion.core import Logger
from portion.core import ProjectManager
from portion.models import ProjectTemplate
from portion.models import TemplateAddToListStep
from portion.utils import Resolver


class AddToListAction(ActionBase[TemplateAddToListStep]):
    def __init__(self,
                 step: TemplateAddToListStep,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 logger: Logger) -> None:
        super().__init__(step, project_template, memory, logger)
        self.project_manager = ProjectManager()

    def prepare(self) -> None:
        self.step.path = Resolver.resolve(self.memory,
                                          self.step.path)

        self.step.list_name = Resolver.resolve_variable(self.memory,
                                                        self.step.list_name)

        if isinstance(self.step.value, str):
            self.step.value = Resolver.resolve_variable(self.memory,
                                                        self.step.value)

    def apply(self) -> None:
        self.project_manager.add_to_list(self.step.path,
                                         self.step.list_name,
                                         self.step.value)
