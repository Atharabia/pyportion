
## Working with Templates

Templates define the structure and configuration of your projects. PyPortion provides built-in templates and supports custom templates.

### List Available Templates

View all templates currently available on your system:

<div class="termynal" data-termynal>
    <span data-ty>portion template list</span>
</div>


### PyPortion Official Templates

It makes sense that you start without any templates. PyPortion provides a set of official templates maintained by the team that you can download and use right away.

| Template | Description | URL |
|---|---|---|
| `cli-template` | A ready-to-use structure for building Python CLI applications | `https://github.com/Atharabia/cli-template` |

View all official templates [here](../official-templates.md)

### Download a Template

Download a template from a remote repository:

<div class="termynal" data-termynal>
    <span data-ty>portion template download &lt;template-url&gt; [version]</span>
</div>

Replace `<template-url>` with the URL of the template repository. The optional `[version]` argument pins a specific branch or tag — omitting it downloads the latest version as declared in the template's `.pyportion.yml`:

<div class="termynal" data-termynal>
    <span data-ty>portion template download https://github.com/Atharabia/cli-template</span>
</div>

To download a specific version:

<div class="termynal" data-termynal>
    <span data-ty>portion template download https://github.com/Atharabia/cli-template v1.2.0</span>
</div>

Multiple versions of the same template can be installed side by side.

### Link Alias

You can also use shorthand aliases instead of full URLs:

<div class="termynal" data-termynal>
    <span data-ty>portion template download gh/Atharabia/cli-template</span>
</div>

### View Template Info

Inspect a template's metadata and available portions:

<div class="termynal" data-termynal>
    <span data-ty>portion template info &lt;template-name&gt;</span>
</div>

**Example:**

<div class="termynal" data-termynal>
    <span data-ty>portion template info cli-template</span>
</div>

If multiple versions of the template are installed, you will be prompted to choose which one to inspect.

### Remove a Template

Delete a specific version of a template from your local system:

<div class="termynal" data-termynal>
    <span data-ty>portion template remove &lt;template-name&gt;</span>
</div>

**Example:**

<div class="termynal" data-termynal>
    <span data-ty>portion template remove cli-template</span>
</div>

If multiple versions are installed, you will be prompted to select which version to remove. The template directory is deleted automatically once no versions remain.

## Next Steps

- [Project Creation](4-project-creation.md) — Create a new project from a downloaded template
- [Template Creation](7-template-creation.md) — Build and publish your own custom templates
