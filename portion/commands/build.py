from pathlib import Path

from portion.base import CommandBase
from portion.core import ProjectManager
from portion.core import TemplateManager
from portion.models import Message
from portion.models import ProjectTemplate
from portion.models import TemplatePortion
from portion.models import cli_state
from portion.step_actions import create_action


class BuildCommand(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        self.project_manager = ProjectManager()
        self.template_manager = TemplateManager()
        self.memory: dict[str, str] = {}

    def _find_portion(self,
                      portions: list[tuple[ProjectTemplate, TemplatePortion]],
                      portion_name: str,
                      ) -> tuple[ProjectTemplate, TemplatePortion] | None:
        for template, portion in portions:
            if portion.name == portion_name:
                return template, portion
        return None

    def build(self, portion_name: str) -> None:
        path = Path.cwd()

        self.terminal.pulse(Message.Build.READING_CONFIG)
        pconfig = self.project_manager.read_configuration(path)

        self.terminal.pulse(Message.Build.COLLECTING_PORTIONS)
        portions = [(t, portion)
                    for t in pconfig.templates
                    for portion in
                    self.template_manager.read_configuration(
                        t.name, t.version).portions]

        template_portion = self._find_portion(portions, portion_name)

        if not template_portion:
            self.terminal.error(Message.Build.NO_PORTION,
                                portion_name=portion_name)
            return None

        template, portion = template_portion

        actions = [create_action(step, template, self.memory, self.terminal)
                   for step in portion.steps]

        for action in actions:
            action.prepare()

        if not cli_state.auto_confirm:
            if not self.terminal.prompt(Message.Build.CONFIRMATION):
                self.terminal.info(Message.Build.ABORT)
                return None

        for action in actions:
            self.terminal.pulse(Message.Build.RUNNING_STEP,
                                step_type=action.step.type.value)
            action.apply()
