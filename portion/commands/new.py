from portion.base import CommandBase
from portion.core import ProjectManager
from portion.core import TemplateManager
from portion.models import Message
from portion.models import ProjectTemplate
from portion.models import cli_state
from portion.step_actions import create_action
from portion.utils import evaluate_when


class NewCommand(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        self.project_manager = ProjectManager()
        self.template_manager = TemplateManager()

    def _run_setup(self, setup, project_template: ProjectTemplate) -> None:
        self.terminal.pulse(Message.New.RUNNING_SETUP)
        memory: dict[str, str] = {}

        actions = [create_action(step, project_template, memory, self.terminal)
                   for step in setup]

        for action in actions:
            if evaluate_when(action.step.when, memory):
                action.prepare()
            else:
                action.skipped = True
                if cli_state.verbose:
                    self.terminal.info(Message.New.SKIP_SETUP_STEP,
                                       step_type=action.step.type.value)

        for action in actions:
            if action.skipped:
                continue
            self.terminal.pulse(Message.New.RUNNING_SETUP_STEP,
                                step_type=action.step.type.value)
            action.apply()

    def new(self, template_name: str, project_name: str) -> None:
        self.terminal.pulse(Message.New.PROJECT_CHECK)
        if self.project_manager.is_project_exist(project_name):
            self.terminal.error(Message.New.PROJECT_EXIST)
            return None

        self.terminal.pulse(Message.New.TEMPLATE_CHECK)
        if not self.template_manager.is_template_exists(template_name):
            self.terminal.error(Message.New.TEMPLATE_NOT_EXIST)
            return None

        versions = self.template_manager.get_template_versions(template_name)
        if len(versions) == 1:
            version = versions[0]
        else:
            version = self.terminal.choose(Message.New.CHOOSE_VERSION,
                                           versions,
                                           template_name=template_name)

        self.terminal.pulse(Message.New.READING_TEMPLATE_CONFIG,
                            template_name=template_name)

        tconfig = self.template_manager.read_configuration(template_name,
                                                           version)

        self.terminal.pulse(Message.New.CREATING_PROJECT,
                            project_name=project_name)
        self.project_manager.create_project(project_name)
        self.template_manager.copy_template(template_name,
                                            version,
                                            project_name)
        self.project_manager.initialize_project(project_name, project_name)

        project_template = ProjectTemplate(name=tconfig.name,
                                           source=tconfig.source,
                                           version=version)
        pconfig = self.project_manager.read_configuration(project_name)
        pconfig.templates.append(project_template)
        self.project_manager.update_configuration(project_name, pconfig)

        if tconfig.setup:
            self._run_setup(tconfig.setup, project_template)

        self.terminal.info(Message.New.CREATED, project_name=project_name)
