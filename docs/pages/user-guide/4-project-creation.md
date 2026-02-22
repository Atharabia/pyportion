# Creating a New Project

Once you have a template downloaded, scaffold a new project with the `new` command:

<div class="termynal" data-termynal>
    <span data-ty>portion new &lt;template-name&gt; &lt;project-name&gt;</span>
</div>

**Parameters:**

- `<template-name>` — Name of the downloaded template to use
- `<project-name>` — Name for the new project directory

**Example:**

<div class="termynal" data-termynal>
    <span data-ty>portion new cli-template my-awesome-app</span>
</div>

This creates a `my-awesome-app/` directory pre-populated with the structure defined in `cli-template`.

## Adding More Templates

A project can use more than one template. To attach an additional template to a project you've already created:

<div class="termynal" data-termynal>
    <span data-ty>portion add &lt;template-name&gt;</span>
</div>

**Example:**

<div class="termynal" data-termynal>
    <span data-ty>portion add cli-template</span>
</div>

This registers the template in your project's `.pyportion.yml`, making its portions available for use.

### Remove a Template

To detach a template from your project:

<div class="termynal" data-termynal>
    <span data-ty>portion remove &lt;template-name&gt;</span>
</div>

This removes the template reference from `.pyportion.yml`. It does not delete any previously generated files.

### View Project Info

Display the current project configuration and its attached templates:

<div class="termynal" data-termynal>
    <span data-ty>portion info</span>
</div>

## Building Portions

A **portion** is a named, reusable code-generation recipe defined inside a template. Once a template is attached to your project, run any of its portions to scaffold new code:

<div class="termynal" data-termynal>
    <span data-ty>portion build &lt;portion-name&gt;</span>
</div>

**Example** — scaffold a new command using the `cli-template`:

<div class="termynal" data-termynal>
    <span data-ty>portion build command</span>
</div>

PyPortion prompts you for any required inputs, shows a summary of the changes it will make, and asks for confirmation before applying them.

Use the `-y` flag to skip the confirmation prompt:

<div class="termynal" data-termynal>
    <span data-ty>portion -y build command</span>
</div>

## Next Steps

- [Existing Project](5-existing-project.md) — Add PyPortion to a project you've already started
- [Cloning a PyPortion Project](6-syncing-templates.md) — Work with a PyPortion project after cloning it from GitHub
- [Template Creation](7-template-creation.md) — Build and publish your own custom templates
