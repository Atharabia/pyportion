from portion.base import ActionBase
from portion.core import TemplateManager
from portion.core import Terminal
from portion.models import ProjectTemplate
from portion.models import TemplateCopyStep
from portion.utils import Resolver


class CopyAction(ActionBase[TemplateCopyStep]):
    def __init__(self,
                 step: TemplateCopyStep,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 logger: Terminal) -> None:
        super().__init__(step, project_template, memory, logger)
        self.template_manager = TemplateManager()

    def prepare(self) -> None:
        self.step.to_path = Resolver.resolve(self.memory,
                                             self.step.to_path)

    def apply(self) -> None:
        self.template_manager.copy_portion(self.project_template.name,
                                           self.project_template.version,
                                           self.step.from_path,
                                           self.step.to_path)
