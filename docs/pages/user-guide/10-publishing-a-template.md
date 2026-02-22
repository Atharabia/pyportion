# Publishing a Template

A PyPortion template is just a Git repository. Once your template is ready, push it to GitHub or GitLab and users can download it immediately.

## Push to Git

```bash
git init
git add .
git commit -m "Initial template"
git remote add origin https://github.com/your-org/my-template
git push -u origin main
```

## Download the Template

Users can download your template with the full URL:

<div class="termynal" data-termynal>
    <span data-ty>portion template download https://github.com/your-org/my-template</span>
</div>

Or using the GitHub shorthand:

<div class="termynal" data-termynal>
    <span data-ty>portion template download gh/your-org/my-template</span>
</div>
