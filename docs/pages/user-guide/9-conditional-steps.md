# Conditional Steps <span class="md-tag">Added in v1.4.0</span>

Any step may include an optional `when` field. If it is present and evaluates to false, the step is skipped.

The value is a string expression made of one or more comparisons, combined with `and` and `or`. Only **`==`** and **`!=`** are supported. Each side of a comparison is either:

- a memory reference: `$variable_name` (values come from `ask`, `ask_options`, `set_var`, and earlier steps) 
- a literal string **without quotes** (for example `true`, `yes`, `production`).

```yaml
- type: set_var
  key: use_cli
  value: "yes"

- type: copy
  when: $use_cli == yes
  from_path: ["cli.py"]
  to_path: ["src", "cli.py"]

- type: copy
  when: $use_cli != yes
  from_path: ["minimal.py"]
  to_path: ["src", "minimal.py"]
```

| Field | Description |
|---|---|
| `when` | If omitted or empty, the step always runs. Otherwise must be a valid `==` / `!=` expression as above. |
