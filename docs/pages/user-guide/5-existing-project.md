# Adding PyPortion to an Existing Project

If you have an existing Python project you want to manage with PyPortion, you don't need to start from scratch. The `init` command adds PyPortion to any existing project directory.

## Initialize the Project

Navigate into your project directory and run:

<div class="termynal" data-termynal>
    <span data-ty>portion init &lt;project-name&gt;</span>
</div>

**Example:**

<div class="termynal" data-termynal>
    <span data-ty>portion init my-existing-app</span>
</div>

This creates a `.pyportion.yml` configuration file in the current directory. No existing files are modified.

## Attach a Template

Once the project is initialized, attach one or more templates to it:

<div class="termynal" data-termynal>
    <span data-ty>portion add &lt;template-name&gt;</span>
</div>

**Example:**

<div class="termynal" data-termynal>
    <span data-ty>portion add cli-template</span>
</div>

The template is registered in `.pyportion.yml`. Its portions are now available to use in the project.

## Build Portions

With a template attached, scaffold new code using its portions:

<div class="termynal" data-termynal>
    <span data-ty>portion build &lt;portion-name&gt;</span>
</div>

**Example:**

<div class="termynal" data-termynal>
    <span data-ty>portion build command</span>
</div>

## Next Steps

- [Cloning a PyPortion Project](6-syncing-templates.md) — Work with a PyPortion project after cloning it from GitHub
- [Template Creation](7-template-creation.md) — Build and publish your own custom templates
