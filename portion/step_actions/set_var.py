from portion.base import ActionBase
from portion.core import Terminal
from portion.models import ProjectTemplate
from portion.models import TemplateSetVarAction
from portion.utils import Resolver
from portion.utils import Transformer


class SetVarAction(ActionBase[TemplateSetVarAction]):
    def __init__(self,
                 step: TemplateSetVarAction,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 terminal: Terminal) -> None:
        super().__init__(step, project_template, memory, terminal)

    def prepare(self) -> None:
        value = Resolver.resolve_variable(self.memory,
                                          self.step.value)

        if self.step.mode:
            value = Transformer.transform(value, self.step.mode)

        self.memory[self.step.key] = value

    def apply(self) -> None:
        ...
