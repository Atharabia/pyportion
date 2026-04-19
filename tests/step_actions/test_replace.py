from pathlib import Path

from portion.core import Terminal
from portion.models import ActionType
from portion.models import ProjectTemplate
from portion.models import TemplateReplaceAction
from portion.models import TemplateReplacement
from portion.step_actions import ReplaceAction

replace_action = ReplaceAction(
    step=TemplateReplaceAction(
        type=ActionType.REPLACE,
        path=["source", "file.txt"],
        replacements=[TemplateReplacement(
            keyword="PLACEHOLDER",
            value="$new_value",
            mode="uppercase"
        )
        ]
    ),
    project_template=ProjectTemplate(name="Sample Template",
                                     source="",
                                     version=""),
    memory={"new_value": "hello world"},
    terminal=Terminal()
)


def test_replace_action_prepare():
    replace_action.prepare()
    assert replace_action.step.path == ["source", "file.txt"]
    assert replace_action.step.replacements[0].value == "HELLO WORLD"


def test_replace_action_prepare_no_mode():
    action = ReplaceAction(
        step=TemplateReplaceAction(
            type=ActionType.REPLACE,
            path=["source", "file.txt"],
            replacements=[TemplateReplacement(
                keyword="PLACEHOLDER",
                value="$new_value",
            )]
        ),
        project_template=ProjectTemplate(name="Sample Template",
                                         source="",
                                         version=""),
        memory={"new_value": "hello world"},
        terminal=Terminal()
    )
    action.prepare()
    assert action.step.replacements[0].value == "hello world"


def test_replace_action_get_summary():
    replace_action.step.path = ["source", "file.txt"]
    expected = ("Replaced [bold #47ba47]1[/] value(s) in "
                "[bold #47ba47]['source', 'file.txt'][/]")
    assert replace_action.get_summary() == expected


def test_replace_action_apply(tmp_path: Path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    source_file = source_dir / "file.txt"
    source_file.write_text("This is a PLACEHOLDER in the file.")

    replace_action.step.path = [str(source_dir), "file.txt"]
    replace_action.apply()

    updated_content = source_file.read_text()
    assert updated_content == "This is a HELLO WORLD in the file."
