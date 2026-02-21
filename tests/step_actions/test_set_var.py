from portion.core import Logger
from portion.models import OperationTypes
from portion.models import ProjectTemplate
from portion.models import TemplateSetVar
from portion.step_actions.set_var import SetVarAction


def test_set_var_action_prepare_no_mode():
    memory: dict[str, str] = {"source": "hello world"}
    action = SetVarAction(
        step=TemplateSetVar(
            type=OperationTypes.SET_VAR,
            key="result",
            value="$source",
            mode=None
        ),
        project_template=ProjectTemplate(
            name="Sample Template", link="", tag=""),
        memory=memory,
        logger=Logger()
    )
    action.prepare()
    assert memory["result"] == "hello world"


def test_set_var_action_prepare_with_mode():
    memory: dict[str, str] = {"source": "hello world"}
    action = SetVarAction(
        step=TemplateSetVar(
            type=OperationTypes.SET_VAR,
            key="result",
            value="$source",
            mode="uppercase"
        ),
        project_template=ProjectTemplate(name="Sample Template",
                                         link="", tag=""),
        memory=memory,
        logger=Logger()
    )
    action.prepare()
    assert memory["result"] == "HELLO WORLD"
