from portion.base import ActionBase
from portion.core import ProjectManager
from portion.core import Terminal
from portion.models import Message
from portion.models import ProjectTemplate
from portion.models import TemplateAddImportAction
from portion.utils import Resolver


class AddImportAction(ActionBase[TemplateAddImportAction]):
    def __init__(self,
                 step: TemplateAddImportAction,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 terminal: Terminal) -> None:
        super().__init__(step, project_template, memory, terminal)
        self.project_manager = ProjectManager()

    def prepare(self) -> None:
        self.step.path = Resolver.resolve(self.memory,
                                          self.step.path)

        self.step.import_statement = Resolver.resolve_variable(
            self.memory,
            self.step.import_statement)

    def get_summary(self) -> str | None:
        return Message.Step.IMPORT_ADDED.format(
            import_statement=self.step.import_statement,
            path=self.step.path
        )

    def apply(self) -> None:
        self.project_manager.add_import(self.step.path,
                                        self.step.import_statement)
