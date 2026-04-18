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
| `when` | Optional condition; the step runs only if it evaluates to true. |

---

## `ask_options`

<span class="md-tag">Added in v1.5.0</span>

Prompt the user to pick one option from a list and store the chosen value in a variable for use in later steps. The CLI shows an interactive menu (arrow keys and Enter).

```yaml
- type: ask_options
  question: Which web framework?
  variable: framework
  options:
    - django
    - flask
    - fastapi
```

| Field | Description |
|---|---|
| `question*` | The prompt shown to the user |
| `variable*` | Variable name to store the selected option (referenced with `$variable_name`) |
| `options*` | Non-empty list of choices; the exact string of the chosen item is stored |
| `when` | Optional condition; the step runs only if it evaluates to true. |

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
| `when` | Optional condition; the step runs only if it evaluates to true. |

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
| `when` | Optional condition; the step runs only if it evaluates to true. |

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
| `when` | Optional condition; the step runs only if it evaluates to true. |

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
| `when` | Optional condition; the step runs only if it evaluates to true. |

---

## `add_portion`

<span class="md-tag">Added in v1.3.0</span>

Run another portion from within a portion step. Useful for composing reusable portions together.

```yaml
- type: add_portion
  path: ["cli", "commands"]
  value: $portion_name
```

| Field | Description |
|---|---|
| `path*` | Path segments to the target directory or file |
| `value*` | Name of the portion to apply (supports variable substitution) |
| `when` | Optional condition; the step runs only if it evaluates to true. |

---

## `bash`

<span class="md-tag">Added in v1.7.0</span>

Run a shell command and store its output in a variable for use in later steps. If `auto_confirm` is not set, the user is prompted before the command runs.

```yaml
- type: bash
  command: git rev-parse --short HEAD
  variable: git_hash
```

| Field | Description |
|---|---|
| `command*` | Shell command to run (supports variable substitution) |
| `variable*` | Variable name to store the command's stdout output |
| `when` | Optional condition; the step runs only if it evaluates to true. |

---

## `add_to_list`

Append a value to a Python list variable in a file. Values are `str`, `int`, `float`, or `bool`. String values are written as quoted string literals by default.

```yaml
- type: add_to_list
  path: ["cli", "commands", "__init__.py"]
  list_name: "__all__"
  value: "$command_class"
  as_identifier: true
```

| Field | Description |
|---|---|
| `path*` | Path segments to the target Python file |
| `list_name*` | Name of the list variable to append to |
| `value*` | Value to append (for strings, `$name` placeholders are replaced from memory) |
| `as_identifier` | If `true`, string values are written without quotes. Default `false`. `Added in v1.5.0` |
| `when` | Optional condition; the step runs only if it evaluates to true. |
