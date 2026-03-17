from pathlib import Path

from portion.core import Terminal
from portion.models import ActionType
from portion.models import ProjectTemplate
from portion.models import TemplateCopyAction
from portion.step_actions import CopyAction

copy_action = CopyAction(
    step=TemplateCopyAction(
        type=ActionType.COPY,
        from_path=["source", "file.txt"],
        to_path=["$destination", "file.txt"]
    ),
    project_template=ProjectTemplate(name="Sample Template",
                                     source="",
                                     version=""),
    memory={"destination": "dest_folder"},
    logger=Terminal()
)


def test_copy_action_prepare():
    copy_action.prepare()
    assert copy_action.step.to_path == ["dest_folder", "file.txt"]


def test_copy_action_apply(tmp_path: Path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    source_file = source_dir / "file.txt"
    source_file.write_text("Sample content")

    dest_dir = tmp_path / "dest_folder"
    dest_dir.mkdir()

    copy_action.step.from_path = [str(source_dir), "file.txt"]
    copy_action.step.to_path = [str(tmp_path / "dest_folder"), "file.txt"]
    copy_action.apply()

    dest_file = tmp_path / "dest_folder" / "file.txt"
    assert dest_file.exists()
    assert dest_file.read_text() == "Sample content"
