
from portion.core import Terminal
from portion.models import OperationTypes
from portion.models import ProjectTemplate
from portion.models.template import TemplateAskStep
from portion.step_actions import create_action
from portion.step_actions.ask import AskAction


def test_create_ask_action():
    step = TemplateAskStep(
        type=OperationTypes.ASK,
        question="What is your name?",
        variable="user_name"
    )
    project_template = ProjectTemplate(name="Test Template",
                                       link="", tag="")
    memory: dict[str, str] = {}
    logger = Terminal()
    action = create_action(step, project_template, memory, logger)
    assert isinstance(action, AskAction)
