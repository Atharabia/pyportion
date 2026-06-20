from pathlib import Path

from portion.core import Terminal
from portion.models import ActionType
from portion.models import ProjectTemplate
from portion.models import TemplateCreateFileAction
from portion.step_actions import CreateFileAction


def make_create_file_action(path: list[str],
                             content: str = "") -> CreateFileAction:
    return CreateFileAction(
        step=TemplateCreateFileAction(
            type=ActionType.CREATE_FILE,
            path=path,
            content=content,
        ),
        project_template=ProjectTemplate(name="Test", source="", version=""),
        memory={},
        terminal=Terminal(),
    )


def test_create_file_prepare():
    action = make_create_file_action(["$dir", "$name.py"], "hello $name")
    action.memory["dir"] = "src"
    action.memory["name"] = "main"
    action.prepare()
    assert action.step.path == ["src", "main.py"]
    assert action.step.content == "hello main"


def test_create_file_get_summary():
    action = make_create_file_action(["src", "main.py"])
    expected = "Created file [bold #47ba47]src/main.py[/]"
    assert action.get_summary() == expected


def test_create_file_apply_creates_file(tmp_path: Path):
    file_path = tmp_path / "output.txt"
    action = make_create_file_action([str(tmp_path), "output.txt"],
                                     content="hello world")
    action.apply()
    assert file_path.exists()
    assert file_path.read_text() == "hello world"


def test_create_file_apply_creates_parent_dirs(tmp_path: Path):
    file_path = tmp_path / "nested" / "deep" / "file.py"
    action = make_create_file_action(
        [str(tmp_path), "nested", "deep", "file.py"]
    )
    action.apply()
    assert file_path.exists()


def test_create_file_apply_empty_content(tmp_path: Path):
    file_path = tmp_path / "empty.txt"
    action = make_create_file_action([str(tmp_path), "empty.txt"])
    action.apply()
    assert file_path.exists()
    assert file_path.read_text() == ""
