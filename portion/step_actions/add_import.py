from portion.base import ActionBase
from portion.core import Logger
from portion.core import ProjectManager
from portion.models import ProjectTemplate
from portion.models import TemplateAddImportStep
from portion.utils import Resolver


class AddImportAction(ActionBase[TemplateAddImportStep]):
    def __init__(self,
                 step: TemplateAddImportStep,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 logger: Logger) -> None:
        super().__init__(step, project_template, memory, logger)
        self.project_manager = ProjectManager()

    def prepare(self) -> None:
        self.step.path = Resolver.resolve(self.memory,
                                          self.step.path)

        self.step.import_statement = Resolver.resolve_variable(
            self.memory,
            self.step.import_statement)

    def apply(self) -> None:
        self.project_manager.add_import(self.step.path,
                                        self.step.import_statement)
