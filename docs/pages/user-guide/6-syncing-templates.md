# Cloning a PyPortion Project

When you clone a PyPortion project from GitHub, the project's `.pyportion.yml` already lists the templates it uses — but those templates are not included in the repository. You need to download them locally before you can build portions.

## Download All Templates

From inside the cloned project directory, run:

<div class="termynal" data-termynal>
    <span data-ty>portion template download</span>
</div>

Running `portion template download` without any arguments reads your project's `.pyportion.yml` and downloads every template listed there to your local machine.

## Build Portions

Once the templates are downloaded, you can scaffold code as usual:

<div class="termynal" data-termynal>
    <span data-ty>portion build &lt;portion-name&gt;</span>
</div>

**Example:**

<div class="termynal" data-termynal>
    <span data-ty>portion build command</span>
</div>

## Typical Workflow After Cloning

<div class="termynal" data-termynal>
    <span data-ty="input">git clone https://github.com/your-org/my-awesome-app</span>
    <span data-ty="input">cd my-awesome-app</span>
    <span data-ty="input">portion template download</span>
    <span data-ty="input">portion build command</span>
</div>

## Next Steps

- [Template Creation](7-template-creation.md) — Build and publish your own custom templates
