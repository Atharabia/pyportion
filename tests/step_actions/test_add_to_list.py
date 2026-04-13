from pathlib import Path

from portion.core import Terminal
from portion.models import ActionType
from portion.models import ProjectTemplate
from portion.models import TemplateAddToListAction
from portion.step_actions.add_to_list import AddToListAction

add_to_list_action = AddToListAction(
    step=TemplateAddToListAction(
        type=ActionType.ADD_TO_LIST,
        path=[
            "$project_dir",
            "config.py"],
        list_name="$list_var",
        value="$item_val"),
    project_template=ProjectTemplate(
        name="Sample Template",
        source="",
        version=""),
    memory={
        "project_dir": "myproject",
        "list_var": "INSTALLED_APPS",
                    "item_val": "myapp"},
    logger=Terminal())


def test_add_to_list_action_prepare():
    add_to_list_action.prepare()
    assert add_to_list_action.step.path == ["myproject", "config.py"]
    assert add_to_list_action.step.list_name == "INSTALLED_APPS"
    assert add_to_list_action.step.value == "myapp"


def test_add_to_list_action_apply(tmp_path: Path):
    py_file = tmp_path / "config.py"
    py_file.write_text("INSTALLED_APPS = []\n")

    add_to_list_action.step.path = [str(tmp_path), "config.py"]
    add_to_list_action.step.list_name = "INSTALLED_APPS"
    add_to_list_action.step.value = "myapp"
    add_to_list_action.apply()

    content = py_file.read_text()
    assert '"myapp"' in content


def test_add_to_list_action_apply_as_identifier(tmp_path: Path):
    py_file = tmp_path / "__init__.py"
    py_file.write_text("__all__ = []\n")

    action = AddToListAction(
        step=TemplateAddToListAction(
            type=ActionType.ADD_TO_LIST,
            path=[str(tmp_path), "__init__.py"],
            list_name="__all__",
            value="MyClass",
            as_identifier=True,
        ),
        project_template=ProjectTemplate(
            name="Sample Template",
            source="",
            version="",
        ),
        memory={},
        logger=Terminal(),
    )
    action.apply()
    content = py_file.read_text()
    assert "MyClass" in content
    assert '"MyClass"' not in content
