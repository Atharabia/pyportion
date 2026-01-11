const terminal = document.getElementById("terminal");
const replayBtn = document.getElementById("replayBtn");
let allTimeouts = [];

const animationSteps = [
    { type: "prompt", delay: 1000 },
    {
        type: "command",
        text: "portion build service",
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
        text: "Collecting all portions...",
        delay: 600,
        class: "info",
    },
    {
        type: "output",
        text: "Found portion: service",
        delay: 500,
        class: "success",
    },
    { type: "output", text: "", delay: 300 },
    { type: "output", text: "Running step: ask", delay: 400, class: "info" },
    {
        type: "output",
        text: "What is your service name?",
        delay: 1000,
    },
    {
        type: "command",
        text: " User",
        delay: 1000,
    },
    { type: "output", text: "", delay: 300 },
    { type: "output", text: "Running step: copy", delay: 400, class: "info" },
    { type: "output", text: "  Copying service template files...", delay: 600 },
    {
        type: "file",
        text: "  ✓ Created: src/services/user_service.py",
        delay: 400,
        class: "success",
    },
    {
        type: "file",
        text: "  ✓ Created: src/services/__init__.py",
        delay: 400,
        class: "success",
    },
    {
        type: "file",
        text: "  ✓ Created: tests/test_user_service.py",
        delay: 400,
        class: "success",
    },
    { type: "output", text: "", delay: 300 },
    {
        type: "output",
        text: "Running step: replace",
        delay: 400,
        class: "info",
    },
    { type: "output", text: "  Updating configuration files...", delay: 600 },
    {
        type: "file",
        text: "  ✓ Updated: config/services.yml",
        delay: 400,
        class: "success",
    },
    { type: "output", text: "", delay: 500 },
    {
        type: "output",
        text: "✨ Build completed successfully!",
        delay: 800,
        class: "success",
    },
    { type: "output", text: "", delay: 300 },
    { type: "tree", delay: 600 },
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

function createFileTree() {
    return `<div class="file-tree">
<span class="output">Project structure:</span>
<span class="tree-item">my-project/</span>
<span class="tree-item">├── src/</span>
<span class="tree-item">│   ├── services/</span>
<span class="tree-item tree-new">│   │   ├── user_service.py (created)</span>
<span class="tree-item tree-new">│   │   └── __init__.py (created)</span>
<span class="tree-item">├── tests/</span>
<span class="tree-item tree-new">│   └── test_user_service.py (created)</span>
<span class="tree-item">├── config/</span>
<span class="tree-item tree-new">│   └── services.yml (updated)</span>
<span class="tree-item">└── .pyportion.yml</span>
</div>`;
}

async function runAnimation() {
    terminal.innerHTML = "";
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
            } else if (step.type === "tree") {
                const treeDiv = document.createElement("div");
                treeDiv.className = "terminal-line";
                treeDiv.innerHTML = createFileTree();
                terminal.appendChild(treeDiv);
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
