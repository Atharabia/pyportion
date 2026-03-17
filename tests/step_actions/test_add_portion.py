from pathlib import Path

from portion.core import Terminal
from portion.models import OperationTypes
from portion.models import ProjectTemplate
from portion.models import TemplateAddPortionStep
from portion.step_actions.add_portion import AddPortion

add_portion_action = AddPortion(
    step=TemplateAddPortionStep(
        type=OperationTypes.ADD_IMPORT,
        path=["$project_dir", "main.py"],
        value="$module"),
    project_template=ProjectTemplate(
        name="Sample Template",
        source="",
        version=""),
    memory={
        "project_dir": "myproject",
        "module": "some_module"},
    logger=Terminal())


def test_add_portion_prepare():
    add_portion_action.prepare()
    assert add_portion_action.step.path == ["myproject", "main.py"]


def test_add_portion_apply(tmp_path: Path):
    py_file = tmp_path / "main.py"
    py_file.write_text("x = 1\n")

    add_portion_action.step.path = [str(tmp_path), "main.py"]
    add_portion_action.step.value = "y = 2"
    add_portion_action.apply()

    content = py_file.read_text()
    assert "x = 1" in content
    assert "y = 2" in content
