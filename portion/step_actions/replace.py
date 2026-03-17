from portion.base import ActionBase
from portion.core import ProjectManager
from portion.core import Terminal
from portion.models import ProjectTemplate
from portion.models import TemplateReplaceAction
from portion.utils import Resolver
from portion.utils import Transformer


class ReplaceAction(ActionBase[TemplateReplaceAction]):
    def __init__(self,
                 step: TemplateReplaceAction,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 logger: Terminal) -> None:
        super().__init__(step, project_template, memory, logger)
        self.project_manager = ProjectManager()

    def prepare(self) -> None:
        self.step.path = Resolver.resolve(self.memory, self.step.path)

        for replace in self.step.replacements:
            memory_value = Resolver.resolve_variable(self.memory,
                                                     replace.value)

            value = Transformer.transform(memory_value, replace.mode)
            replace.value = value

    def apply(self) -> None:
        self.project_manager.replace_in_file(self.step.path,
                                             self.step.replacements)
