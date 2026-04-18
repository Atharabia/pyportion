import subprocess

from portion.base import ActionBase
from portion.core import Terminal
from portion.models import Message
from portion.models import ProjectTemplate
from portion.models import TemplateBashCommand
from portion.models import cli_state
from portion.utils import Resolver


class BashAction(ActionBase[TemplateBashCommand]):
    def __init__(self,
                 step: TemplateBashCommand,
                 project_template: ProjectTemplate,
                 memory: dict[str, str],
                 terminal: Terminal) -> None:
        super().__init__(step, project_template, memory, terminal)

    def prepare(self) -> None:
        ...

    def apply(self) -> None:
        message = Message.General.RUNNING_BASH.format(self.step.command)
        self.terminal.info(message)
        if not cli_state.auto_confirm:
            if not self.terminal.prompt(Message.Build.CONFIRMATION):
                self.terminal.info(Message.Build.ABORT)
                return None

        self.step.command = Resolver.resolve_variable(self.memory,
                                                      self.step.command)

        result = subprocess.run(
            self.step.command.split(" "),
            capture_output=True,
            text=True,
            check=True
        )

        self.memory[self.step.variable] = result.stdout
