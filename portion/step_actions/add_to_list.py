from portion.base import ActionBase
from portion.core import ProjectManager
from portion.core import Terminal
from portion.models import ProjectTemplate
from portion.models import TemplateAddToListAction
from portion.utils import Resolver


class AddToListAction(ActionBase[TemplateAddToListAction]):
    def __init__(self,
                 step: TemplateAddToListAction,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 terminal: Terminal) -> None:
        super().__init__(step, project_template, memory, terminal)
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
                                         self.step.value,
                                         as_identifier=self.step.as_identifier)
