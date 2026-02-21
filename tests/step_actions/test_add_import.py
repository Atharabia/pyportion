from pathlib import Path

from portion.core import Logger
from portion.models import OperationTypes
from portion.models import ProjectTemplate
from portion.models import TemplateAddImportStep
from portion.step_actions.add_import import AddImportAction

add_import_action = AddImportAction(
    step=TemplateAddImportStep(
        type=OperationTypes.ADD_IMPORT,
        path=["$project_dir", "main.py"],
        import_statement="import $module"
    ),
    project_template=ProjectTemplate(name="Sample Template", link="", tag=""),
    memory={"project_dir": "myproject", "module": "os"},
    logger=Logger()
)


def test_add_import_action_prepare():
    add_import_action.prepare()
    assert add_import_action.step.path == ["myproject", "main.py"]
    assert add_import_action.step.import_statement == "import os"


def test_add_import_action_apply(tmp_path: Path):
    py_file = tmp_path / "main.py"
    py_file.write_text("x = 1\n")

    add_import_action.step.path = [str(tmp_path), "main.py"]
    add_import_action.step.import_statement = "import os"
    add_import_action.apply()

    content = py_file.read_text()
    assert "import os" in content
