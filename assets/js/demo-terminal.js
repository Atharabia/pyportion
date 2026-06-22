const terminal = document.getElementById("terminal");
const explorerPanel = document.getElementById("explorerPanel");
const replayBtn = document.getElementById("replayBtn");
let allTimeouts = [];
let currentExplorerState = {
    folders: {},
    files: []
};

const animationSteps = [
    { type: "prompt", delay: 1000 },
    {
        type: "command",
        text: "portion new flask-app blog-app",
        delay: 2500,
        typeSpeed: 80,
    },
    {
        type: "output",
        text: "Creating new Flask project...",
        delay: 800,
        class: "info",
    },
    {
        type: "output",
        text: "Setting up project structure...",
        delay: 600,
        class: "info",
    },
    {
        type: "output",
        text: "✨ Project created successfully!",
        delay: 800,
        class: "success",
    },
    { type: "output", text: "", delay: 300 },
    { type: "addFile", path: "src/app.py", status: "new", delay: 200 },
    { type: "addFile", path: "src/__init__.py", status: "new", delay: 200 },
    { type: "addFile", path: "config/settings.py", status: "new", delay: 200 },
    { type: "addFile", path: "tests/__init__.py", status: "new", delay: 200 },
    { type: "addFile", path: "requirements.txt", status: "new", delay: 200 },
    { type: "addFile", path: ".pyportion.yml", status: "new", delay: 200 },
    { type: "addFile", path: "README.md", status: "new", delay: 200 },
    { type: "output", text: "", delay: 800 },

    { type: "prompt", delay: 1000 },
    {
        type: "command",
        text: "portion build blueprint",
        delay: 2500,
        typeSpeed: 80,
    },
    {
        type: "output",
        text: "Reading configuration...",
        delay: 800,
        class: "info",
    },
    {
        type: "output",
        text: "Found portion: blueprint",
        delay: 500,
        class: "success",
    },
    { type: "output", text: "", delay: 300 },
    { type: "output", text: "Running step: ask", delay: 400, class: "info" },
    {
        type: "output",
        text: "What is your blueprint name?",
        delay: 1000,
    },
    {
        type: "command",
        text: " auth",
        delay: 1200,
    },
    { type: "output", text: "", delay: 300 },
    {
        type: "output",
        text: "Do you want to include authentication?",
        delay: 1000,
    },
    {
        type: "command",
        text: " yes",
        delay: 1000,
    },
    { type: "output", text: "", delay: 300 },
    { type: "output", text: "Running step: copy", delay: 400, class: "info" },
    { type: "output", text: "  Creating blueprint files...", delay: 600 },
    {
        type: "file",
        text: "  ✓ Created: src/blueprints/auth.py",
        delay: 400,
        class: "file-new",
    },
    { type: "addFile", path: "src/blueprints/auth.py", status: "new", delay: 100 },
    {
        type: "file",
        text: "  ✓ Created: src/blueprints/__init__.py",
        delay: 400,
        class: "file-new",
    },
    { type: "addFile", path: "src/blueprints/__init__.py", status: "new", delay: 100 },
    {
        type: "file",
        text: "  ✓ Created: src/templates/auth/login.html",
        delay: 400,
        class: "file-new",
    },
    { type: "addFile", path: "src/templates/auth/login.html", status: "new", delay: 100 },
    {
        type: "file",
        text: "  ✓ Created: src/templates/auth/register.html",
        delay: 400,
        class: "file-new",
    },
    { type: "addFile", path: "src/templates/auth/register.html", status: "new", delay: 100 },
    { type: "output", text: "", delay: 300 },
    {
        type: "output",
        text: "Running step: replace",
        delay: 400,
        class: "info",
    },
    { type: "output", text: "  Updating project files...", delay: 600 },
    {
        type: "file",
        text: "  ✓ Modified: src/app.py",
        delay: 400,
        class: "file-modified",
    },
    { type: "addFile", path: "src/app.py", status: "modified", delay: 100 },
    {
        type: "file",
        text: "  ✓ Modified: config/settings.py",
        delay: 400,
        class: "file-modified",
    },
    { type: "addFile", path: "config/settings.py", status: "modified", delay: 100 },
    { type: "output", text: "", delay: 500 },
    {
        type: "output",
        text: "✨ Build completed successfully!",
        delay: 800,
        class: "success",
    },
    { type: "output", text: "", delay: 300 },
    { type: "prompt", delay: 1000 },
];

function createLine(content, className = "") {
    const line = document.createElement("div");
    line.className = `terminal-line ${className}`;
    line.innerHTML = content;
    return line;
}

function typeText(element, text, speed = 50) {
    return new Promise((resolve) => {
        let i = 0;
        const cursor = document.createElement("span");
        cursor.className = "cursor";
        element.appendChild(cursor);

        const interval = setInterval(() => {
            if (i < text.length) {
                const textNode = document.createTextNode(text[i]);
                element.insertBefore(textNode, cursor);
                i++;
            } else {
                clearInterval(interval);
                cursor.remove();
                resolve();
            }
        }, speed);
    });
}

function addFileToExplorer(path, status) {
    const parts = path.split('/');
    const fileName = parts[parts.length - 1];
    const folderPath = parts.slice(0, -1);

    if (!currentExplorerState.folders[folderPath.join('/')]) {
        currentExplorerState.folders[folderPath.join('/')] = {
            files: {},
            subfolders: new Set()
        };
    }

    currentExplorerState.folders[folderPath.join('/')].files[fileName] = status;

    for (let i = 0; i < folderPath.length; i++) {
        const currentPath = folderPath.slice(0, i).join('/');
        const folderName = folderPath[i];
        if (!currentExplorerState.folders[currentPath]) {
            currentExplorerState.folders[currentPath] = {
                files: {},
                subfolders: new Set()
            };
        }
        currentExplorerState.folders[currentPath].subfolders.add(folderName);
    }

    renderFileExplorer();
}

function renderFileExplorer() {
    if (!explorerPanel) {
        return;
    }

    const rootFolder = buildFolderStructure('', 0);
    const isEmpty = !rootFolder || rootFolder.trim() === '';

    if (isEmpty) {
        explorerPanel.innerHTML = `<div class="file-explorer">
<div class="explorer-content">
    <div class="explorer-empty">
        <div class="empty-icon">📂</div>
        <div class="empty-text">No files yet</div>
    </div>
</div>
</div>`;
    } else {
        explorerPanel.innerHTML = `<div class="file-explorer">
<div class="explorer-content">
    <div class="explorer-folder">
        <div class="folder-header" style="color: #fff; font-weight: 600;">📁 blog-app</div>
        <div class="folder-content">
            ${rootFolder}
        </div>
    </div>
</div>
</div>`;
    }
}

function buildFolderStructure(path, depth) {
    const folder = currentExplorerState.folders[path];
    if (!folder) return '';

    let html = '';

    const sortedSubfolders = Array.from(folder.subfolders).sort();
    for (const subfolder of sortedSubfolders) {
        const subfolderPath = path ? `${path}/${subfolder}` : subfolder;
        const subfolderData = currentExplorerState.folders[subfolderPath];
        const hasNewFiles = subfolderData && Object.values(subfolderData.files).includes('new');
        const statusClass = hasNewFiles ? 'explorer-new' : '';

        html += `<div class="explorer-folder ${statusClass}">
            <div class="folder-header">📂 ${subfolder}</div>
            <div class="folder-content">
                ${buildFolderStructure(subfolderPath, depth + 1)}
            </div>
        </div>`;
    }

    const sortedFiles = Object.keys(folder.files).sort();
    for (const file of sortedFiles) {
        const status = folder.files[file];
        const statusClass = status === 'new' ? 'explorer-new' : status === 'modified' ? 'explorer-modified' : '';
        html += `<div class="explorer-file ${statusClass}">📄 ${file}</div>`;
    }

    return html;
}

async function runAnimation() {
    terminal.innerHTML = "";
    explorerPanel.innerHTML = "";
    currentExplorerState = {
        folders: {},
        files: []
    };
    renderFileExplorer();
    let totalDelay = 0;

    for (let i = 0; i < animationSteps.length; i++) {
        const step = animationSteps[i];

        const timeout = setTimeout(async () => {
            if (step.type === "prompt") {
                const line = createLine('<span class="prompt">$ </span>');
                terminal.appendChild(line);
            } else if (step.type === "command") {
                const lastLine = terminal.lastElementChild;
                const commandSpan = document.createElement("span");
                commandSpan.className = "command";
                lastLine.appendChild(commandSpan);
                await typeText(commandSpan, step.text, step.typeSpeed);
            } else if (step.type === "output") {
                const line = createLine(
                    `<span class="${step.class || "output"}">${
                        step.text
                    }</span>`
                );
                terminal.appendChild(line);
            } else if (step.type === "file") {
                const line = createLine(
                    `<span class="${step.class || "file-item"}">${
                        step.text
                    }</span>`
                );
                terminal.appendChild(line);
            } else if (step.type === "addFile") {
                addFileToExplorer(step.path, step.status);
            }

            terminal.scrollTop = terminal.scrollHeight;
        }, totalDelay);

        allTimeouts.push(timeout);
        totalDelay += step.delay;
    }
}

function clearTimeouts() {
    allTimeouts.forEach((timeout) => clearTimeout(timeout));
    allTimeouts = [];
}

replayBtn.addEventListener("click", () => {
    clearTimeouts();
    runAnimation();
});

if (explorerPanel) {
    renderFileExplorer();
}

const demoSection = document.querySelector(".demo-section");
let hasAnimated = false;
const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting && !hasAnimated) {
                hasAnimated = true;
                runAnimation();
            }
        });
    },
    {
        threshold: 0.3,
    }
);

observer.observe(demoSection);
