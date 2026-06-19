from portion.core import Terminal
from portion.models import ActionType
from portion.models import ProjectTemplate
from portion.models import TemplateSetVarAction
from portion.step_actions.set_var import SetVarAction


def test_set_var_action_prepare_no_mode():
    memory: dict[str, str] = {"source": "hello world"}
    action = SetVarAction(
        step=TemplateSetVarAction(
            type=ActionType.SET_VAR,
            key="result",
            value="$source",
            mode=None
        ),
        project_template=ProjectTemplate(
            name="Sample Template", source="", version=""),
        memory=memory,
        terminal=Terminal()
    )
    action.prepare()
    assert memory["result"] == "hello world"


def test_set_var_action_prepare_with_mode():
    memory: dict[str, str] = {"source": "hello world"}
    action = SetVarAction(
        step=TemplateSetVarAction(
            type=ActionType.SET_VAR,
            key="result",
            value="$source",
            mode="uppercase"
        ),
        project_template=ProjectTemplate(name="Sample Template",
                                         source="", version=""),
        memory=memory,
        terminal=Terminal()
    )
    action.prepare()
    assert memory["result"] == "HELLO WORLD"


def test_set_var_action_prepare_with_prefix():
    memory: dict[str, str] = {"source": "world"}
    action = SetVarAction(
        step=TemplateSetVarAction(
            type=ActionType.SET_VAR,
            key="result",
            value="$source",
            prefix="hello_"
        ),
        project_template=ProjectTemplate(name="Sample Template",
                                         source="", version=""),
        memory=memory,
        terminal=Terminal()
    )
    action.prepare()
    assert memory["result"] == "hello_world"


def test_set_var_action_prepare_with_suffix():
    memory: dict[str, str] = {"source": "hello"}
    action = SetVarAction(
        step=TemplateSetVarAction(
            type=ActionType.SET_VAR,
            key="result",
            value="$source",
            suffix="_world"
        ),
        project_template=ProjectTemplate(name="Sample Template",
                                         source="", version=""),
        memory=memory,
        terminal=Terminal()
    )
    action.prepare()
    assert memory["result"] == "hello_world"


def test_set_var_action_prepare_with_prefix_and_suffix():
    memory: dict[str, str] = {"source": "world"}
    action = SetVarAction(
        step=TemplateSetVarAction(
            type=ActionType.SET_VAR,
            key="result",
            value="$source",
            prefix="hello_",
            suffix="!"
        ),
        project_template=ProjectTemplate(name="Sample Template",
                                         source="", version=""),
        memory=memory,
        terminal=Terminal()
    )
    action.prepare()
    assert memory["result"] == "hello_world!"


def test_set_var_action_prepare_with_variable_prefix():
    memory: dict[str, str] = {"source": "world", "pre": "hello_"}
    action = SetVarAction(
        step=TemplateSetVarAction(
            type=ActionType.SET_VAR,
            key="result",
            value="$source",
            prefix="$pre"
        ),
        project_template=ProjectTemplate(name="Sample Template",
                                         source="", version=""),
        memory=memory,
        terminal=Terminal()
    )
    action.prepare()
    assert memory["result"] == "hello_world"


def test_set_var_action_prepare_with_variable_suffix():
    memory: dict[str, str] = {"source": "hello", "suf": "_world"}
    action = SetVarAction(
        step=TemplateSetVarAction(
            type=ActionType.SET_VAR,
            key="result",
            value="$source",
            suffix="$suf"
        ),
        project_template=ProjectTemplate(name="Sample Template",
                                         source="", version=""),
        memory=memory,
        terminal=Terminal()
    )
    action.prepare()
    assert memory["result"] == "hello_world"
