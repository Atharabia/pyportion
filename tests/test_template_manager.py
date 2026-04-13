import os
from pathlib import Path
from pathlib import PosixPath
from unittest.mock import MagicMock

import pytest
from rich.panel import Panel

from portion.core.template_manager import TemplateManager
from portion.models.template import TemplateConfig
from portion.models.template import TemplatePortion

VERSION = "v1.0.0"
VERSION_DIR = VERSION.lstrip("v")


def test_create_pyportion_dir(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    path = mock_user_data_dir / "pyportion"

    assert os.path.exists(path) is False
    tm.create_pyportion_dir()
    assert os.path.exists(path) is True


def test_download_template(mock_user_data_dir: PosixPath,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    template_name = "pyportion-template"
    link = f"https://github.com/test/{template_name}"
    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)

    def mock_repo_clone(_url, path, **_kwargs) -> None:
        os.makedirs(path, exist_ok=True)
        config = (f"version: {VERSION}\n"
                  f"name: {template_name}\n"
                  "source: https://github.com/\n"
                  "description: test\n"
                  "author: test\n"
                  "type: test\n")
        (Path(path) / ".pyportion.yml").write_text(config)

    tm = TemplateManager()
    monkeypatch.setattr("portion.core.template_manager.Repo.clone_from",
                        mock_repo_clone)

    tm.create_pyportion_dir()
    assert version_path.exists() is False
    assert tm.is_template_exists(template_name) is False

    result = tm.download_template(link)

    assert result == VERSION
    assert version_path.exists() is True
    assert tm.is_template_exists(template_name) is True


def test_download_template_wrong_link(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    result = tm.download_template("invalid_link")
    assert result is None


def test_delete_if_not_template(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)

    assert tm.delete_if_not_template(template_name, VERSION) is True
    assert version_path.exists() is False

    template_path = mock_user_data_dir / "pyportion" / template_name
    assert template_path.exists() is False

    version_path.mkdir(parents=True)
    portion_json_path = version_path / ".pyportion.yml"
    portion_json_path.touch()

    assert tm.delete_if_not_template(template_name, VERSION) is False
    assert version_path.exists() is True


def test_delete_template(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"

    assert tm.delete_template(template_name, VERSION) is False

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)

    assert tm.delete_template(template_name, VERSION) is True
    assert version_path.exists() is False


def test_get_templates(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"

    assert len(tm.get_templates()) == 0

    template_path = (mock_user_data_dir / "pyportion" / template_name)
    template_path.mkdir()

    templates = tm.get_templates()
    assert len(templates) == 1
    assert template_name in templates


def test_copy_template(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"
    project_name = "pyportion-project"

    base_path = (mock_user_data_dir / "pyportion"
                 / template_name / VERSION_DIR / "base")
    base_path.mkdir(parents=True)
    (base_path / ".pyportion.yml").touch()

    project_path = (mock_user_data_dir / project_name)

    assert project_path.exists() is False
    tm.copy_template(template_name, VERSION, str(project_path))
    assert project_path.exists() is True
    assert (project_path / ".pyportion.yml").exists() is True


def test_copy_portion(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"
    project_name = "pyportion-project"

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)
    (version_path / "base").mkdir()

    portion_dir = version_path / ".portions"
    portion_dir.mkdir()
    (portion_dir / "portion.py").touch()

    dest_path = mock_user_data_dir / project_name
    assert dest_path.exists() is False
    dest_path.mkdir()

    tm.copy_portion(template_name,
                    VERSION,
                    portion_path=["portion.py"],
                    dest_path=list(dest_path.parts) + ["portion.py"])

    assert dest_path.exists() is True
    assert (dest_path / "portion.py").exists() is True


def test_read_template_config(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)

    config_str = """\
name: Test Template
source: https://github.com/
version: 1.0.0
description: A test template
author: Test Author
type: test
"""

    (version_path / ".pyportion.yml").write_text(config_str)
    config = tm.read_configuration(template_name, VERSION)

    assert config is not None
    assert config.name == "Test Template"
    assert config.version == "1.0.0"
    assert config.description == "A test template"
    assert config.author == "Test Author"
    assert config.type == "test"


def test_update_configuration(mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "pyportion-template"

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)

    config_str = """\
name: Test Template
source: https://github.com/
version: 1.0.0
description: A test template
author: Test Author
type: test
"""

    (version_path / ".pyportion.yml").write_text(config_str)
    config = tm.read_configuration(template_name, VERSION)
    assert config is not None
    assert config.author == "Test Author"

    config.author = "Updated Author"
    tm.update_configuration(template_name, VERSION, config)
    updated_config = tm.read_configuration(template_name, VERSION)

    assert updated_config is not None
    assert updated_config.author == "Updated Author"


def test_get_template_versions_path_not_exist(
        mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    assert tm.get_template_versions("nonexistent-template") == []


def test_download_template_with_version_already_exists(
        mock_user_data_dir: PosixPath) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "my-template"

    version_path = (mock_user_data_dir / "pyportion" /
                    template_name / VERSION_DIR)

    version_path.mkdir(parents=True)

    result = tm.download_template(f"https://github.com/test/{template_name}",
                                  VERSION)
    assert result is None


def test_download_template_with_version_success(
        mock_user_data_dir: PosixPath,
        monkeypatch: pytest.MonkeyPatch) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "my-template"

    def mock_clone(_url, path, **_kwargs) -> None:
        os.makedirs(path, exist_ok=True)

    monkeypatch.setattr("portion.core.template_manager.Repo.clone_from",
                        mock_clone)

    result = tm.download_template(f"https://github.com/test/{template_name}",
                                  VERSION)
    assert result == VERSION


def test_download_template_with_version_clone_fails(
        mock_user_data_dir: PosixPath,
        monkeypatch: pytest.MonkeyPatch) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "my-template"

    def mock_clone(*args, **kwargs):
        raise Exception("Clone failed")

    monkeypatch.setattr("portion.core.template_manager.Repo.clone_from",
                        mock_clone)

    result = tm.download_template(f"https://github.com/test/{template_name}",
                                  VERSION)
    assert result is None


def test_download_template_no_portion_file(
        mock_user_data_dir: PosixPath,
        monkeypatch: pytest.MonkeyPatch) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "my-template"

    def mock_clone(_url, path, **_kwargs) -> None:
        os.makedirs(path, exist_ok=True)

    monkeypatch.setattr("portion.core.template_manager.Repo.clone_from",
                        mock_clone)

    result = tm.download_template(f"https://github.com/test/{template_name}")
    assert result is None


def test_download_template_no_version_in_data(
        mock_user_data_dir: PosixPath,
        monkeypatch: pytest.MonkeyPatch) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "my-template"

    def mock_clone(_url, path, **_kwargs) -> None:
        os.makedirs(path, exist_ok=True)
        (Path(path) / ".pyportion.yml").write_text("name: test\n")

    monkeypatch.setattr("portion.core.template_manager.Repo.clone_from",
                        mock_clone)

    result = tm.download_template(f"https://github.com/test/{template_name}")
    assert result is None


def test_download_template_version_already_exists_in_data(
        mock_user_data_dir: PosixPath,
        monkeypatch: pytest.MonkeyPatch) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()
    template_name = "my-template"

    version_path = (mock_user_data_dir / "pyportion" /
                    template_name / VERSION_DIR)
    version_path.mkdir(parents=True)

    def mock_clone(_url, path, **_kwargs) -> None:
        os.makedirs(path, exist_ok=True)
        (Path(path) / ".pyportion.yml").write_text(
            f"name: {template_name}\nversion: {VERSION}\n")

    monkeypatch.setattr("portion.core.template_manager.Repo.clone_from",
                        mock_clone)

    result = tm.download_template(f"https://github.com/test/{template_name}")
    assert result is None


def test_get_template_info_no_string_metadata() -> None:
    tm = TemplateManager()
    mock_config = MagicMock()
    mock_config.model_dump.return_value = {"portions": [], "count": 42}
    panel = tm.get_template_info(mock_config)
    assert isinstance(panel, Panel)


def test_get_template_info() -> None:
    tm = TemplateManager()
    template_config = TemplateConfig(
        name="Test Template",
        source="https://github.com/",
        version="1.0.0",
        description="A test template",
        author="Test Author",
        type="test",
        portions=[
            TemplatePortion(name="portion1", steps=[]),
            TemplatePortion(name="portion2", steps=[]),
        ]
    )

    panel = tm.get_template_info(template_config)
    assert isinstance(panel, Panel)
