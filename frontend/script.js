const APIS = {
    setup: '/api/setup',
    assessment: '/api/assessment',
    problem: '/api/problem',
    run: '/api/run',
    progress: '/api/progress',
    skip: '/api/skip'
};

const ALL_TOPICS = [
    "Arrays", "Strings", "Linked Lists", "Stacks & Queues",
    "Trees", "Graphs", "Dynamic Programming", "Recursion", "Greedy"
];

const DEFAULT_TEMPLATES = {
    "python": "def solve():\n    # Write your code here\n    pass",
    "cpp": "#include <iostream>\nusing namespace std;\n\nint main() {\n    // Write your code here\n    return 0;\n}",
    "java": "public class Solution {\n    public static void main(String[] args) {\n        // Write your code here\n    }\n}",
    "javascript": "function solve() {\n    // Write your code here\n}"
};

let progressChart = null;
let cooldownActive = false;  // Global cooldown flag

// ── DOM references ────────────────────────────────────────────────
const pages = {
    loading:    document.getElementById('loading'),
    topics:     document.getElementById('page-topics'),
    assessment: document.getElementById('page-assessment'),
    playground: document.getElementById('page-playground')
};

function showPage(id) {
    Object.values(pages).forEach(p => p.classList.add('hidden'));
    pages[id].classList.remove('hidden');
}

// ── Init ──────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initTopicsGrid();
    showPage('topics');

    document.getElementById('btn-start-assessment').addEventListener('click', handleTopicsSubmit);
    document.getElementById('btn-submit-assessment').addEventListener('click', handleAssessmentSubmit);
    document.getElementById('btn-submit-code').addEventListener('click', handleCodeSubmit);
    document.getElementById('btn-next-prob').addEventListener('click', handleSkipProblem);
    document.getElementById('lang-select').addEventListener('change', handleLanguageChange);

    // Modal buttons
    document.getElementById('modal-btn-retry').addEventListener('click', handleModalRetry);
    document.getElementById('modal-btn-next').addEventListener('click', handleModalNext);
});

// ── Topics ────────────────────────────────────────────────────────
function initTopicsGrid() {
    const grid = document.getElementById('topics-grid');
    ALL_TOPICS.forEach(topic => {
        const label = document.createElement('label');
        label.className = 'checkbox-group';
        label.innerHTML = `<input type="checkbox" value="${topic}"> ${topic}`;
        grid.appendChild(label);
    });
}

async function handleTopicsSubmit() {
    const selected = Array.from(document.querySelectorAll('#topics-grid input:checked'))
        .map(cb => cb.value);
    if (selected.length === 0) {
        alert("Please select at least one topic.");
        return;
    }
    try {
        await fetch(APIS.setup, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topics: selected })
        });
        showPage('assessment');
    } catch (err) {
        console.error("Setup error:", err);
    }
}

// ── Assessment ────────────────────────────────────────────────────
async function handleAssessmentSubmit() {
    const q1 = document.querySelector('input[name="q1"]:checked')?.value || 0;
    const q2 = document.querySelector('input[name="q2"]:checked')?.value || 0;
    const totalScore = (parseInt(q1) + parseInt(q2)) / 2;

    try {
        await fetch(APIS.assessment, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ score: totalScore })
        });
        await loadProblem();
        initChart();
        showPage('playground');
    } catch (err) {
        console.error("Assessment error:", err);
    }
}

// ── Problem Loading ───────────────────────────────────────────────
async function loadProblem() {
    try {
        const res = await fetch(APIS.problem);
        const data = await res.json();
        renderProblem(data.problem, data.level);
    } catch (err) {
        console.error("Error loading problem:", err);
    }
}

function renderProblem(problem, level) {
    document.getElementById('prob-title').innerText = problem.title;
    document.getElementById('prob-desc').innerText = problem.description;
    document.getElementById('prob-hint').innerText = problem.expected_complexity || "O(?)";

    const badge = document.getElementById('prob-difficulty');
    badge.className = 'difficulty-badge';

    if (level === 2) {
        badge.innerText = 'HARD';
        badge.classList.add('diff-hard');
    } else if (level === 1) {
        badge.innerText = 'MEDIUM';
        badge.classList.add('diff-medium');
    } else {
        badge.innerText = 'EASY';
        badge.classList.add('diff-easy');
    }

    document.getElementById('feedback-panel').classList.add('hidden');
}

// ── Language Change ───────────────────────────────────────────────
function handleLanguageChange(e) {
    const lang = e.target.value;
    document.getElementById('code-editor').value =
        DEFAULT_TEMPLATES[lang] || DEFAULT_TEMPLATES["python"];
}

// ── Skip Problem ──────────────────────────────────────────────────
async function handleSkipProblem() {
    if (cooldownActive) return;

    const btn = document.getElementById('btn-next-prob');
    btn.disabled = true;
    btn.innerText = "Loading...";

    try {
        const res = await fetch(APIS.skip, { method: 'POST' });
        const data = await res.json();

        renderProblem(data.problem, data.level);
        if (data.state) updateStats(data.state);
        if (data.observation && data.reward) renderFeedback(data.observation, data.reward);
        refreshChart();

        // Reset editor to clean template
        const lang = document.getElementById('lang-select').value;
        document.getElementById('code-editor').value =
            DEFAULT_TEMPLATES[lang] || DEFAULT_TEMPLATES["python"];
    } catch (err) {
        console.error("Skip error:", err);
    } finally {
        if (!cooldownActive) {
            btn.disabled = false;
            btn.innerText = "Change Problem";
        }
    }
}

// ── Submit Code ───────────────────────────────────────────────────
let lastSubmitData = null;  // Store response so modal buttons can use it

async function handleCodeSubmit() {
    if (cooldownActive) return;

    const code = document.getElementById('code-editor').value;
    const language = document.getElementById('lang-select').value;

    // Block empty / unedited template
    if (code.trim() === "" || code === DEFAULT_TEMPLATES[language]) {
        renderFeedback(
            { feedback_summary: "Please write some code before submitting!" },
            { value: 0.0 }
        );
        return;
    }

    const btn = document.getElementById('btn-submit-code');
    btn.disabled = true;
    btn.innerText = "Evaluating...";

    try {
        const res = await fetch(APIS.run, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                code: code,
                problem: document.getElementById('prob-title').innerText,
                language: language
            })
        });
        const data = await res.json();
        lastSubmitData = data;

        // Update stats & chart
        updateStats(data.state);
        renderFeedback(data.observation, data.reward);
        refreshChart();

        // If rate-limited, start cooldown (no modal)
        if (data.info && data.info.retry_after) {
            startCooldown(data.info.retry_after);
            return;
        }

        // Show the result modal
        showSubmitModal(data);

    } catch (err) {
        console.error("Submit error:", err);
    } finally {
        if (!cooldownActive) {
            btn.disabled = false;
            btn.innerText = "Submit Solution";
        }
    }
}

// ── Post-Submission Modal ────────────────────────────────────────
function showSubmitModal(data) {
    const modal = document.getElementById('submit-modal');
    const icon = document.getElementById('modal-icon');
    const title = document.getElementById('modal-title');
    const feedback = document.getElementById('modal-feedback');
    const scoreFill = document.getElementById('modal-score-fill');
    const scoreLabel = document.getElementById('modal-score-label');

    const score = data.reward?.value || 0;
    const feedbackText = data.observation?.feedback_summary || "No feedback.";

    // Set icon and title based on score
    if (score >= 0.7) {
        icon.textContent = "🎉";
        title.textContent = "Excellent!";
        title.style.color = "var(--success)";
    } else if (score >= 0.4) {
        icon.textContent = "✅";
        title.textContent = "Good Attempt!";
        title.style.color = "var(--accent-primary)";
    } else {
        icon.textContent = "💡";
        title.textContent = "Keep Trying!";
        title.style.color = "var(--error)";
    }

    feedback.textContent = feedbackText;
    scoreLabel.textContent = `Score: ${score.toFixed(2)}`;

    // Animate score bar
    scoreFill.style.width = "0%";
    setTimeout(() => {
        scoreFill.style.width = `${Math.round(score * 100)}%`;
        // Color the bar based on score
        if (score >= 0.7) {
            scoreFill.style.background = "linear-gradient(90deg, #10b981, #34d399)";
        } else if (score >= 0.4) {
            scoreFill.style.background = "var(--accent-gradient)";
        } else {
            scoreFill.style.background = "linear-gradient(90deg, #ef4444, #f97316)";
        }
    }, 100);

    // Show mastery message if done
    if (data.done) {
        feedback.textContent += " 🏆 You've mastered all levels!";
    }

    // Show modal
    modal.classList.remove('hidden');
}

function closeModal() {
    document.getElementById('submit-modal').classList.add('hidden');
}

// Modal button handlers (attached in DOMContentLoaded)
function handleModalRetry() {
    closeModal();
    // User stays on same problem, code is preserved
}

async function handleModalNext() {
    closeModal();
    const language = document.getElementById('lang-select').value;

    // If server already loaded a new problem, use it
    if (lastSubmitData && lastSubmitData.info && lastSubmitData.info.new_problem) {
        renderProblem(lastSubmitData.info.new_problem, lastSubmitData.state.user_level);
        document.getElementById('code-editor').value =
            DEFAULT_TEMPLATES[language] || DEFAULT_TEMPLATES["python"];
        return;
    }

    // Otherwise, explicitly skip to next problem
    try {
        const res = await fetch(APIS.skip, { method: 'POST' });
        const data = await res.json();
        renderProblem(data.problem, data.level);
        if (data.state) updateStats(data.state);
        refreshChart();
        document.getElementById('code-editor').value =
            DEFAULT_TEMPLATES[language] || DEFAULT_TEMPLATES["python"];
    } catch (err) {
        console.error("Skip error:", err);
    }
}

// ── Rate-Limit Cooldown ──────────────────────────────────────────
function startCooldown(seconds) {
    cooldownActive = true;
    const btnSubmit = document.getElementById('btn-submit-code');
    const btnSkip = document.getElementById('btn-next-prob');

    btnSubmit.disabled = true;
    btnSkip.disabled = true;

    let remaining = seconds;
    const interval = setInterval(() => {
        if (remaining <= 0) {
            clearInterval(interval);
            cooldownActive = false;
            btnSubmit.disabled = false;
            btnSkip.disabled = false;
            btnSubmit.innerText = "Submit Solution";
            btnSkip.innerText = "Change Problem";
        } else {
            const text = `⏳ Wait ${remaining}s`;
            btnSubmit.innerText = text;
            btnSkip.innerText = text;
            remaining--;
        }
    }, 1000);
}

// ── Feedback Panel ────────────────────────────────────────────────
function renderFeedback(obs, reward) {
    const panel = document.getElementById('feedback-panel');
    const title = document.getElementById('feedback-title');
    const text = document.getElementById('feedback-text');

    panel.classList.remove('hidden', 'error');

    if (reward.value < 0.4) {
        panel.classList.add('error');
        title.style.color = 'var(--error)';
        title.innerText = `Needs Improvement (Score: ${reward.value})`;
    } else {
        title.style.color = 'var(--success)';
        title.innerText = `Great Job! (Score: ${reward.value})`;
    }

    // Format Markdown-like syntax to basic HTML for the UI
    let formatted = (obs.feedback_summary || "No feedback.")
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
    
    text.innerHTML = formatted;
}

// ── Stats Bar ─────────────────────────────────────────────────────
function updateStats(state) {
    const levels = ["Beginner", "Intermediate", "Advanced"];
    document.getElementById('ui-level').innerText = levels[state.user_level] || "Beginner";
    document.getElementById('ui-score').innerText = state.success_rate.toFixed(2);
    document.getElementById('ui-streak').innerText = state.streak;
}

// ── Chart ─────────────────────────────────────────────────────────
function initChart() {
    const ctx = document.getElementById('progressChart').getContext('2d');
    if (progressChart) progressChart.destroy();

    progressChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Task Scores',
                data: [],
                borderColor: '#8b5cf6',
                backgroundColor: 'rgba(139, 92, 246, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1.0,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            },
            plugins: {
                legend: { labels: { color: '#e2e8f0' } }
            }
        }
    });
}

async function refreshChart() {
    if (!progressChart) return;
    try {
        const res = await fetch(APIS.progress);
        const data = await res.json();
        progressChart.data.labels = data.attempts;
        progressChart.data.datasets[0].data = data.scores;
        progressChart.update();
    } catch (err) {
        console.error("Chart error:", err);
    }
}
