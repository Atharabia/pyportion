from pathlib import PosixPath

from portion.core import TemplateManager

VERSION = "v1.0.0"
VERSION_DIR = VERSION.lstrip("v")


def create_template(mock_user_data_dir: PosixPath,
                    template_name: str) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)
    base_path = version_path / "base"
    base_path.mkdir()

    config_str = f"""\
    name: {template_name}
    source: https://github.com/test/template
    version: {VERSION}
    description: A test template
    author: Test Author
    type: test
    """
    config_file = version_path / ".pyportion.yml"
    config_file.write_text(config_str)
    (base_path / ".pyportion.yml").touch()


def create_template_without_source(mock_user_data_dir: PosixPath,
                                   template_name: str) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)
    base_path = version_path / "base"
    base_path.mkdir()

    config_str = f"""\
    name: {template_name}
    version: {VERSION}
    description: A test template without source
    author: Test Author
    type: test
    """

    config_file = version_path / ".pyportion.yml"
    config_file.write_text(config_str)
    (base_path / ".pyportion.yml").touch()


def create_template_with_portions(mock_user_data_dir: PosixPath,
                                  template_name: str) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)
    base_path = version_path / "base"
    base_path.mkdir()

    config_str = f"""\
    name: {template_name}
    source: https://github.com/test/template
    version: {VERSION}
    description: A test template with multiple portions
    author: Test Author
    type: test
    portions:
      - name: feature1
        steps:
          - type: copy
            from_path: ["feature1.py"]
            to_path: ["feature1.py"]
      - name: feature2
        steps:
          - type: copy
            from_path: ["feature2.py"]
            to_path: ["feature2.py"]
    """

    config_file = version_path / ".pyportion.yml"
    config_file.write_text(config_str)
    (base_path / ".pyportion.yml").touch()

    portions_dir = version_path / ".portions"
    portions_dir.mkdir()
    (portions_dir / "feature1.py").write_text("# Feature 1")
    (portions_dir / "feature2.py").write_text("# Feature 2")


def create_template_with_conditional_steps(mock_user_data_dir: PosixPath,
                                           template_name: str) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)
    base_path = version_path / "base"
    base_path.mkdir()

    config_str = f"""\
    name: {template_name}
    source: https://github.com/test/template
    version: {VERSION}
    description: A test template with when steps
    author: Test Author
    type: test
    portions:
      - name: cond
        steps:
          - type: set_var
            key: flag
            value: "yes"
          - type: copy
            when: $flag == no
            from_path: ["skipped_only.py"]
            to_path: ["skipped_only.py"]
          - type: copy
            when: $flag == yes
            from_path: ["feature1.py"]
            to_path: ["kept.py"]
    """

    config_file = version_path / ".pyportion.yml"
    config_file.write_text(config_str)
    (base_path / ".pyportion.yml").touch()

    portions_dir = version_path / ".portions"
    portions_dir.mkdir()
    (portions_dir / "skipped_only.py").write_text("# skipped")
    (portions_dir / "feature1.py").write_text("# kept")


def create_template_with_setup(mock_user_data_dir: PosixPath,
                               template_name: str) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)
    base_path = version_path / "base"
    base_path.mkdir()

    config_str = f"""\
    name: {template_name}
    source: https://github.com/test/template
    version: {VERSION}
    description: A test template with setup
    author: Test Author
    type: test
    setup:
      - name: basic_setup
        steps:
          - type: set_var
            key: setup_key
            value: setup_value
    """

    config_file = version_path / ".pyportion.yml"
    config_file.write_text(config_str)
    (base_path / ".pyportion.yml").touch()


def create_template_with_setup_and_conditional(mock_user_data_dir: PosixPath,
                                               template_name: str) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()

    version_path = (mock_user_data_dir / "pyportion"
                    / template_name / VERSION_DIR)
    version_path.mkdir(parents=True)
    base_path = version_path / "base"
    base_path.mkdir()

    config_str = f"""\
    name: {template_name}
    source: https://github.com/test/template
    version: {VERSION}
    description: A test template with conditional setup
    author: Test Author
    type: test
    setup:
      - name: conditional_setup
        steps:
          - type: set_var
            key: flag
            value: "no"
          - type: set_var
            when: $flag == yes
            key: skipped_key
            value: skipped_value
    """

    config_file = version_path / ".pyportion.yml"
    config_file.write_text(config_str)
    (base_path / ".pyportion.yml").touch()


def create_template_with_two_versions(mock_user_data_dir: PosixPath,
                                      template_name: str) -> None:
    tm = TemplateManager()
    tm.create_pyportion_dir()

    for ver_str, ver_tag in [("1.0.0", "v1.0.0"), ("2.0.0", "v2.0.0")]:
        version_path = (mock_user_data_dir / "pyportion"
                        / template_name / ver_str)
        version_path.mkdir(parents=True)
        base_path = version_path / "base"
        base_path.mkdir()

        config_str = f"""\
    name: {template_name}
    source: https://github.com/test/template
    version: {ver_tag}
    description: A test template
    author: Test Author
    type: test
    """
        (version_path / ".pyportion.yml").write_text(config_str)
        (base_path / ".pyportion.yml").touch()
