# Steps Reference

Steps are the building blocks of a portion. They run in order and can read and write variables, copy files, and modify project files.

---

## `ask`

Prompt the user for a value and store it in a variable for use in later steps.

```yaml
- type: ask
  question: What is the command name?
  variable: command_name
```

| Field | Description |
|---|---|
| `question*` | The prompt shown to the user |
| `variable*` | Variable name to store the answer (referenced with `$variable_name`) |

---

## `set_var`

Derive a new variable from a fixed value or an existing variable, optionally applying a case transformation.

```yaml
- type: set_var
  key: command_class
  value: $command_name
  mode: titlecase
```

| Field | Description |
|---|---|
| `key*` | Name of the new variable |
| `value*` | Source value (can reference an existing variable) |
| `mode` | Transformation to apply: `pascalcase`, `camelcase`, `titlecase`, `uppercase`, `lowercase` |

---

## `copy`

Copy a file from `.portions/` into the project directory.

```yaml
- type: copy
  from_path: ["command.py"]
  to_path: ["cli", "commands", "$command_name.py"]
```

| <div style="min-width:160px">Field</div> | Description |
|---|---|
| `from_path*` | Path segments relative to `.portions/` |
| `to_path*` | Destination path segments in the project (supports variable substitution) |

---

## `replace`

Replace keyword placeholders inside a file with variable values.

```yaml
- type: replace
  path: ["cli", "commands", "$command_name.py"]
  replacements:
      - keyword: COMMAND_CLASS_NAME
        value: $command_name
        mode: pascalcase
```

| Field | Description |
|---|---|
| `path*` | Path segments to the file in the project |
| `replacements*` | List of keyword/value pairs |
| `replacements[].keyword*` | Literal string to search for in the file |
| `replacements[].value*` | Replacement value (supports variable substitution) |
| `replacements[].mode` | Case transformation applied to the replacement value |

---

## `add_import`

Append an import statement to a Python file.

```yaml
- type: add_import
  path: ["cli", "commands", "__init__.py"]
  import_statement: "from .$command_name import $command_class"
```

| Field | Description |
|---|---|
| `path*` | Path segments to the target Python file |
| `import_statement*` | The import line to add (supports variable substitution) |

---

## `add_to_list`

Append a value to a Python list variable in a file.

```yaml
- type: add_to_list
  path: ["cli", "commands", "__init__.py"]
  list_name: "__all__"
  value: "$command_class"
```

| Field | Description |
|---|---|
| `path*` | Path segments to the target Python file |
| `list_name*` | Name of the list variable to append to |
| `value*` | Value to append (supports variable substitution) |
