# Template Creation

This guide walks you through creating a custom PyPortion template that you can share and reuse across projects.

## Template Structure

A PyPortion template is a Git repository with the following layout:

```
my-template/
├── .pyportion.yml
├── base/
│   └── ...
└── .portions/
    └── ...
```

| <div style="min-width:130px">Path</div> | Purpose |
|---|---|
| `.pyportion.yml` | Describes the template and defines its portions |
| `base` | Files that are copied into a new project directory when running `portion new` |
| `.portions` | File snippets that portions can copy and transform into the project |

You will build the template structure, files, and steps manually.

## Template Configuration

The `.pyportion.yml` file has two sections: **metadata** and **portions**.

```yaml
name: my-template
version: 1.0.0
description: A short description of what this template does.
author: Your Name
type: cli

source:
    link: https://github.com/your-org/my-template
    tag: main

portions:
    - name: command
      steps:
          - ...
```

### Metadata Fields

| Field | Description |
|---|---|
| `name` | Template identifier (must match the repository name) |
| `version` | Semantic version of the template |
| `description` | Short description shown in `portion template info` |
| `author` | Author or team name |
| `type` | Category label (e.g. `cli`, `api`, `library`) |
| `source.link` | Git URL of the template repository |
| `source.tag` | Branch or tag to track |

## Portions

A **portion** is a named sequence of steps that generates or modifies files inside a project. Portions are triggered with `portion build <portion-name>`.

Each portion has a `name` and a list of `steps`. Here is a simple example that copies a file from `.portions/` into the project:

```yaml
portions:
    - name: command
      steps:
          - type: copy
            from_path: ["command.py"]
            to_path: ["cli", "commands", "command.py"]
```

Steps run in order. You can chain as many steps as needed — see the [Steps Reference](8-steps-reference.md) for the full list.

## The `base` Directory

The `base` directory contains files that are copied into a new project when a user runs `portion new`. Think of it as the starting scaffold — things like a `README.md`, a `pyproject.toml`, a default folder structure, or any other file every new project should begin with.

```
base/
├── README.md
├── pyproject.toml
└── src/
    └── __init__.py
```

Files in `base` are not processed or transformed — they are copied as-is.

## The `.portions` Directory

The `.portions` directory holds the file snippets that your portions work with. When a portion runs a `copy` step, it pulls the source file from here and places it into the user's project.

```
.portions/
└── command.py
```

The files inside can contain placeholder keywords that the `replace` step will substitute with real values at build time. This is how you turn a generic snippet into a project-specific file.

## Next Steps

- [Steps Reference](8-steps-reference.md) — all available step types and their fields
- [Variables](9-variable-substitution.md) — how to use variables across steps
- [Publishing a Template](10-publishing-a-template.md) — how to share your template with others
