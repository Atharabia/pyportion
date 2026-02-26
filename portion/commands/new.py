from portion.base import CommandBase
from portion.core import ProjectManager
from portion.core import TemplateManager
from portion.models import Message
from portion.models import ProjectTemplate


class NewCommand(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        self.project_manager = ProjectManager()
        self.template_manager = TemplateManager()

    def new(self, template_name: str, project_name: str) -> None:
        self.terminal.pulse(Message.New.PROJECT_CHECK)
        if self.project_manager.is_project_exist(project_name):
            self.terminal.error(Message.New.PROJECT_EXIST)
            return None

        self.terminal.pulse(Message.New.TEMPLATE_CHECK)
        if not self.template_manager.is_template_exists(template_name):
            self.terminal.error(Message.New.TEMPLATE_NOT_EXIST)
            return None

        self.terminal.pulse(Message.New.READING_TEMPLATE_CONFIG,
                            template_name=template_name)

        tconfig = self.template_manager.read_configuration(template_name)

        self.terminal.pulse(Message.New.CREATING_PROJECT,
                            project_name=project_name)
        self.project_manager.create_project(project_name)
        self.template_manager.copy_template(template_name, project_name)
        self.project_manager.initialize_project(project_name, project_name)

        pconfig = self.project_manager.read_configuration(project_name)
        pconfig.templates.append(ProjectTemplate(name=tconfig.name,
                                                 source=tconfig.source,
                                                 version=tconfig.version))
        self.project_manager.update_configuration(project_name, pconfig)

        self.terminal.info(Message.New.CREATED, project_name=project_name)
