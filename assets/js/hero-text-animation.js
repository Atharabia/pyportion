const dynamicWordElement = document.getElementById("dynamic-word");

const words = [
    "Faster",
    "Smarter",
    "Easier",
    "Cleaner",
    "Stronger",
    "Sleeker",
    "Better",
    "Polished",
    "Effortless",
    "Consistent",
    "Reliable",
    "Organized",
    "Reusable",
    "Customizable",
    "Professional",
    "Optimized",
    "Elegant",
    "Efficient",
    "Stable",
    "Structured",
    "Scalable",
    "Streamlined",
    "Flexible",
    "Powerful",
    "Minimal",
    "Modular",
    "Lean",
    "Rapid",
    "Innovative",
    "Predictable",
    "High-quality",
    "Clean-Cut",
    "Future-proof",
    "Refined",
    "Balanced",
    "Perfect",
    "Ready-to-go",
    "Next-level",
    "Top-notch",
];

let lastWordIndex = -1;

const TYPING_SPEED = 100;
const DELETING_SPEED = 80;
const PAUSE_BEFORE_DELETE = 800;
const PAUSE_BEFORE_TYPE = 500;

function getRandomWordIndex() {
    let randomIndex;
    do {
        randomIndex = Math.floor(Math.random() * words.length);
    } while (randomIndex === lastWordIndex && words.length > 1);
    return randomIndex;
}

async function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

async function deleteWord() {
    const currentText = dynamicWordElement.textContent;

    for (let i = currentText.length; i >= 0; i--) {
        dynamicWordElement.textContent = currentText.substring(0, i);
        await sleep(DELETING_SPEED);
    }
}

async function typeWord(word) {
    for (let i = 0; i <= word.length; i++) {
        dynamicWordElement.textContent = word.substring(0, i) + "_";
        await sleep(TYPING_SPEED);
    }
}

async function animateWords() {
    while (true) {
        await sleep(PAUSE_BEFORE_DELETE);
        await deleteWord();
        await sleep(PAUSE_BEFORE_TYPE);
        lastWordIndex = getRandomWordIndex();
        await typeWord(words[lastWordIndex]);
    }
}

// Start the animation when the page loads
window.addEventListener("DOMContentLoaded", () => {
    // Add a small delay before starting the animation
    setTimeout(() => {
        animateWords();
    }, 1000);
});
