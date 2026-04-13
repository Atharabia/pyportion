from dataclasses import dataclass


class Message:
    @dataclass
    class Init:
        CHECKING_INIT = "Checking current path: {path}"

        PROJECT_EXIST = "This project is already a portion project"

        INITIALIZED = ("[bold #47ba47]({project_name})[/] project has "
                       "been initialized successfully")

    @dataclass
    class Add:
        CHECKING_TEMPLATE = "checking template: {template_name}"
        VALIDATE_TEMPALTE = "Validate given template"
        CHECKING_USED_TEMPLATES = "Checking used templates in current project"
        ADDING_TEMPLATE = "Adding {template_name} to the current project"

        TEMPLATE_EXIST = "The given template is not exist"
        TEMPLATE_ALREADY_ADDED = "The template is already added"
        CHOOSE_VERSION = ("Which version of {template_name} "
                          "do you want to add?")

        TEMPLATE_ADDED = ("[bold #47ba47]({template_name})[/] has "
                          "been added successfully")

    @dataclass
    class Build:
        READING_CONFIG = "Reading configuration"
        COLLECTING_PORTIONS = "Collecting all portions"
        NO_PORTION = "There is no portion called {portion_name}"
        RUNNING_STEP = "Running step: {step_type}"
        SKIP_STEP = "Skipping step: {step_type} (when is false)"
        CONFIRMATION = "Do you want to continue?"
        ABORT = "[bold red]Aborted[/]"

    @dataclass
    class Install:
        READING_CONFIGURATION = "Reading project configuration"
        DOWNLOADING_TEMPALTE = ("Downloading template: {template_name} "
                                "from {template_link}@{template_version}")

        VERSION_ALREADY_EXISTS = ("{template_name}@{template_version} "
                                  "is already downloaded, skipping")
        DOWNLOADED = ("{template_name}@{template_version} "
                      "is successfully downloaded")
        COULD_NOT_DOWNLOAD = ("Could not download "
                              "{template_name}@{template_version}")

    @dataclass
    class New:
        PROJECT_CHECK = "Checking current project"
        TEMPLATE_CHECK = "Checking given template"
        PROJECT_EXIST = "The project is already exist"
        TEMPLATE_NOT_EXIST = "The template is not exist"
        CHOOSE_VERSION = ("Which version of {template_name} "
                          "do you want to use?")

        READING_TEMPLATE_CONFIG = ("Reading template configuration: "
                                   "{template_name}")

        CREATING_PROJECT = "Creating new project: {project_name}"

        CREATED = ("[bold #47ba47]{project_name}[/] project is "
                   "successfully created")

    @dataclass
    class Remove:
        CHECKING_TEMPLATES = "Checking templates in current project"
        TEMPLATE_NOT_FOUND = "The template isn't exist in this project"
        TEMPLATE_REMOVED = ("([bold #47ba47]{template_name})[/] has been "
                            "removed successfully")

    @dataclass
    class Template:
        INVALID_LINK = "The link is not valid"
        TEMPLATE_EXIST = "The given template is already exist"
        VERSION_EXIST = ("{template_name}@{version} "
                         "is already downloaded")
        NOT_PORTION_TEMPLATE = "The given template is not a portion template"
        DOWNLOAD_FAILED = "Failed to download the template"
        DOWNLOADED = ("[bold #47ba47]{template_name}@{version}[/] "
                      "has been downloaded successfully")

        INVALID_NAME = "The template name is not valid"
        TEMPLATE_NOT_EXIST = ("The template ([bold]{template_name}[/]) "
                              "is not exist")
        CHOOSE_VERSION = "Which version do you want to use?"

        VERSION_DELETED = ("[bold #47ba47]{template_name}@{version}[/] "
                           "has been deleted")
        TEMPLATE_DELETED = ("The template ([bold #47ba47]{template_name}[/]) "
                            "has been deleted")

        NO_TEMPLATES = "There are no templates"

    @dataclass
    class Version:
        DISPLAY = "PyPortion: {version}"
