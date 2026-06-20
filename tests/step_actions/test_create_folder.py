from pathlib import Path

from portion.core import Terminal
from portion.models import ActionType
from portion.models import ProjectTemplate
from portion.models import TemplateCreateFolderAction
from portion.step_actions import CreateFolderAction


def make_create_folder_action(path: list[str]) -> CreateFolderAction:
    return CreateFolderAction(
        step=TemplateCreateFolderAction(
            type=ActionType.CREATE_FOLDER,
            path=path,
        ),
        project_template=ProjectTemplate(name="Test", source="", version=""),
        memory={},
        terminal=Terminal(),
    )


def test_create_folder_prepare():
    action = make_create_folder_action(["$base", "subdir"])
    action.memory["base"] = "myproject"
    action.prepare()
    assert action.step.path == ["myproject", "subdir"]


def test_create_folder_get_summary():
    action = make_create_folder_action(["src", "utils"])
    expected = "Created folder [bold #47ba47]src/utils[/]"
    assert action.get_summary() == expected


def test_create_folder_apply(tmp_path: Path):
    target = tmp_path / "src" / "utils"
    action = make_create_folder_action([str(tmp_path), "src", "utils"])
    action.apply()
    assert target.exists()
    assert target.is_dir()


def test_create_folder_apply_already_exists(tmp_path: Path):
    target = tmp_path / "existing"
    target.mkdir()
    action = make_create_folder_action([str(tmp_path), "existing"])
    action.apply()
    assert target.exists()
