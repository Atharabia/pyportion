from pathlib import Path

from portion.base import CommandBase
from portion.core import ProjectManager
from portion.models import Message


class InitCommand(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        self.project_manager = ProjectManager()

    def init(self, project_name: str) -> None:
        path = Path.cwd()

        self.terminal.pulse(Message.Init.CHECKING_INIT, path=str(path))
        if self.project_manager.is_project_initalized(path):
            self.terminal.error(Message.Init.PROJECT_EXIST)
            return None

        self.project_manager.initialize_project(path, project_name)
        self.terminal.info(Message.Init.INITIALIZED, project_name=project_name)
