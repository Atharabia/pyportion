# Variables

Variables collected via `ask` or derived via `set_var` can be referenced anywhere in step fields using the `$variable_name` syntax.

## Usage

Reference a variable by prefixing its name with `$`:

```yaml
- type: copy
  from_path: ["command.py"]
  to_path: ["cli", "commands", "$command_name.py"]
```

Variables are substituted before the step runs, so the file will be placed at the resolved path.

## Case Transformations

The `replace` and `set_var` steps accept an optional `mode` field that transforms the variable value before it is used.

| Mode | Input | Output |
|---|---|---|
| `pascalcase` | `my command` | `MyCommand` |
| `camelcase` | `my command` | `myCommand` |
| `titlecase` | `my command` | `My Command` |
| `uppercase` | `my command` | `MY COMMAND` |
| `lowercase` | `My Command` | `my command` |

### Example

```yaml
- type: set_var
  key: command_class
  value: $command_name
  mode: pascalcase

- type: replace
  path: ["cli", "commands", "$command_name.py"]
  replacements:
      - keyword: COMMAND_CLASS_NAME
        value: $command_class
```

Here `$command_name` is collected from the user and `$command_class` is derived from it in PascalCase. Both are then available to all following steps.
