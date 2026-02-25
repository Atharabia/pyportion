from pathlib import Path

from portion.core import Terminal
from portion.models import OperationTypes
from portion.models import ProjectTemplate
from portion.models import TemplateReplacement
from portion.models import TemplateReplaceStep
from portion.step_actions import ReplaceAction

replace_action = ReplaceAction(
    step=TemplateReplaceStep(
        type=OperationTypes.REPLACE,
        path=["source", "file.txt"],
        replacements=[TemplateReplacement(
            keyword="PLACEHOLDER",
            value="$new_value",
            mode="uppercase"
        )
        ]
    ),
    project_template=ProjectTemplate(name="Sample Template",
                                     link="",
                                     tag=""),
    memory={"new_value": "hello world"},
    logger=Terminal()
)


def test_replace_action_prepare():
    replace_action.prepare()
    assert replace_action.step.path == ["source", "file.txt"]
    assert replace_action.step.replacements[0].value == "HELLO WORLD"


def test_replace_action_apply(tmp_path: Path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    source_file = source_dir / "file.txt"
    source_file.write_text("This is a PLACEHOLDER in the file.")

    replace_action.step.path = [str(source_dir), "file.txt"]
    replace_action.apply()

    updated_content = source_file.read_text()
    assert updated_content == "This is a HELLO WORLD in the file."
