from portion.base import ActionBase
from portion.core import Logger
from portion.models import ProjectTemplate
from portion.models import TemplateSetVar
from portion.utils import Resolver
from portion.utils import Transformer


class SetVarAction(ActionBase[TemplateSetVar]):
    def __init__(self,
                 step: TemplateSetVar,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 logger: Logger) -> None:
        super().__init__(step, project_template, memory, logger)

    def prepare(self) -> None:
        value = Resolver.resolve_variable(self.memory,
                                          self.step.value)

        if self.step.mode:
            value = Transformer.transform(value, self.step.mode)

        self.memory[self.step.key] = value

    def apply(self) -> None:
        ...
