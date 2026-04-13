
from portion.core import Terminal
from portion.models import ActionType
from portion.models import ProjectTemplate
from portion.models.template import TemplateAskAction
from portion.models.template import TemplateAskOptionsAction
from portion.step_actions import create_action
from portion.step_actions.ask import AskAction
from portion.step_actions.ask import AskOptionsAction


def test_create_ask_action():
    step = TemplateAskAction(
        type=ActionType.ASK,
        question="What is your name?",
        variable="user_name"
    )
    project_template = ProjectTemplate(name="Test Template",
                                       source="", version="")
    memory: dict[str, str] = {}
    logger = Terminal()
    action = create_action(step, project_template, memory, logger)
    assert isinstance(action, AskAction)


def test_create_ask_options_action():
    step = TemplateAskOptionsAction(
        type=ActionType.ASK_OPTIONS,
        question="Choose:",
        variable="choice",
        options=["a", "b"],
    )
    project_template = ProjectTemplate(name="Test Template",
                                       source="", version="")
    memory: dict[str, str] = {}
    logger = Terminal()
    action = create_action(step, project_template, memory, logger)
    assert isinstance(action, AskOptionsAction)
