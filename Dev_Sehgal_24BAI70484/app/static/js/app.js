// AzureCloudHub Frontend Interactive Engine
let currentTab = 'ai-studio';
let quizQuestions = [];
let userAnswers = {};
let currentQuestionIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
    initSharedResponsibility();
    calculateTCO();
    runSlaCalculation();
    calculateStorageCost();
    loadQuizQuestions();
    loadErrorLog();
    fetchTelemetry();
    setInterval(fetchTelemetry, 3000);
});

// Tab Switching Logic
function switchTab(tabId) {
    const tabs = ['ai-studio', 'architecture', 'tco-calculator', 'governance', 'exam-prep', 'telemetry'];
    tabs.forEach(t => {
        const tabEl = document.getElementById(`tab-${t}`);
        const btnEl = document.getElementById(`tab-btn-${t}`);
        if (t === tabId) {
            tabEl.classList.remove('hidden');
            btnEl.classList.add('nav-tab-active');
            btnEl.classList.remove('text-slate-400');
        } else {
            tabEl.classList.add('hidden');
            btnEl.classList.remove('nav-tab-active');
            btnEl.classList.add('text-slate-400');
        }
    });
    currentTab = tabId;
}

// ----------------------------------------------------------------------
// 1. AI Model Serving Studio
// ----------------------------------------------------------------------
const SAMPLE_TEXTS = {
    positive: "Azure Kubernetes Service auto-scaling worked flawlessly during our product launch with sub-20ms latency!",
    query: "How do I configure zone-redundant storage for our secondary disaster recovery region in Central India?",
    incident: "Virtual machine instance terminated unexpectedly in East US with error code 500 and network latency spike."
};

function loadSampleText(type) {
    const txtArea = document.getElementById('ai-input-text');
    if (SAMPLE_TEXTS[type]) {
        txtArea.value = SAMPLE_TEXTS[type];
    }
}

async function runInference() {
    const text = document.getElementById('ai-input-text').value.trim();
    if (!text) {
        alert("Please enter input text for AI inference.");
        return;
    }

    try {
        const res = await fetch('/api/ml/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        
        document.getElementById('ai-result-card').classList.remove('hidden');
        document.getElementById('ai-latency-badge').innerText = `Latency: ${data.latency_ms.toFixed(1)} ms`;
        
        const sentEl = document.getElementById('ai-sentiment-val');
        sentEl.innerText = data.sentiment;
        if (data.sentiment === 'Positive') {
            sentEl.className = 'text-lg font-bold text-emerald-400';
        } else if (data.sentiment === 'Negative') {
            sentEl.className = 'text-lg font-bold text-rose-400';
        } else {
            sentEl.className = 'text-lg font-bold text-blue-400';
        }

        document.getElementById('ai-sentiment-conf').innerText = `${(data.sentiment_confidence * 100).toFixed(1)}% Conf`;
        document.getElementById('ai-category-val').innerText = data.category;
        document.getElementById('ai-category-conf').innerText = `${(data.category_confidence * 100).toFixed(1)}% Conf`;

        // Probability bars
        const posP = (data.probabilities.Positive || 0) * 100;
        const neuP = (data.probabilities.Neutral || 0) * 100;
        const negP = (data.probabilities.Negative || 0) * 100;

        document.getElementById('prob-pos').innerText = `${posP.toFixed(1)}%`;
        document.getElementById('bar-pos').style.width = `${posP}%`;
        
        document.getElementById('prob-neu').innerText = `${neuP.toFixed(1)}%`;
        document.getElementById('bar-neu').style.width = `${neuP}%`;

        document.getElementById('prob-neg').innerText = `${negP.toFixed(1)}%`;
        document.getElementById('bar-neg').style.width = `${negP}%`;

        fetchTelemetry();
    } catch (err) {
        console.error("Inference failed:", err);
        alert("Inference request failed. Check server connection.");
    }
}

async function runBatchSimulation() {
    const samples = [
        "The migration from on-prem to Azure Blob storage was smooth and cut costs significantly",
        "Cost management budget alerts saved us from an accidental overspend last week",
        "Microservice container crashed with out of memory error during peak traffic load",
        "What is the pricing difference between Azure SQL General Purpose and Business Critical?",
        "Azure App Service responding in under 15ms with 100% uptime"
    ];

    try {
        const res = await fetch('/api/ml/batch-predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ items: samples })
        });
        const data = await res.json();
        alert(`Simulated batch execution of ${data.total_processed} items!\nAverage latency per item: ${data.avg_latency_ms.toFixed(1)} ms.\nLogged to Application Insights.`);
        fetchTelemetry();
    } catch (e) {
        console.error(e);
    }
}

// ----------------------------------------------------------------------
// 2. Shared Responsibility Model Explorer
// ----------------------------------------------------------------------
const SR_DATA = {
    onprem: {
        customer: ["Data & Information", "Identity & Directory Infrastructure", "Applications", "Runtime & Middleware", "Operating System", "Network Controls", "Hypervisor / Virtualization", "Physical Datacenter & Servers"],
        microsoft: []
    },
    iaas: {
        customer: ["Data & Information", "Identity & Directory Infrastructure", "Applications", "Runtime & Middleware", "Operating System (Patching & Config)", "Network Controls (NSGs, Routing)"],
        microsoft: ["Physical Datacenter & Building Security", "Physical Servers & Blades", "Physical Network Cabling", "Hypervisor & Host Virtualization"]
    },
    paas: {
        customer: ["Data & Information", "Identity & Access Management (Entra ID)", "Applications & Source Code"],
        microsoft: ["Runtime & Framework", "Operating System Patching", "Hypervisor", "Network Security Appliances", "Physical Datacenter & Servers"]
    },
    saas: {
        customer: ["Data & Information (Data Governance)", "Identity & Access Management (User Accounts)"],
        microsoft: ["Application Code & Features", "Runtime & Framework", "Operating System", "Network Controls", "Physical Datacenter & Servers"]
    }
};

function initSharedResponsibility() {
    setSharedRespModel('paas');
}

function setSharedRespModel(model) {
    const btns = ['onprem', 'iaas', 'paas', 'saas'];
    btns.forEach(b => {
        const btn = document.getElementById(`btn-sr-${b}`);
        if (b === model) {
            btn.className = 'px-3 py-1.5 rounded bg-blue-600 text-white font-bold';
        } else {
            btn.className = 'px-3 py-1.5 rounded text-slate-300';
        }
    });

    const data = SR_DATA[model];
    const container = document.getElementById('sr-matrix-container');
    
    container.innerHTML = `
        <div class="p-4 bg-slate-900 rounded-lg border border-blue-500/30">
            <div class="flex items-center space-x-2 mb-3">
                <i class="fa-solid fa-user-shield text-blue-400"></i>
                <h4 class="font-bold text-slate-200 text-sm">Customer Responsibility (${data.customer.length} layers)</h4>
            </div>
            <ul class="space-y-1.5 text-xs text-slate-300">
                ${data.customer.map(item => `
                    <li class="flex items-center space-x-2">
                        <i class="fa-solid fa-check text-blue-400 text-xs"></i>
                        <span>${item}</span>
                    </li>
                `).join('')}
            </ul>
        </div>
        <div class="p-4 bg-slate-900 rounded-lg border border-cyan-500/30">
            <div class="flex items-center space-x-2 mb-3">
                <i class="fa-brands fa-microsoft text-cyan-400"></i>
                <h4 class="font-bold text-slate-200 text-sm">Microsoft Azure Responsibility (${data.microsoft.length} layers)</h4>
            </div>
            <ul class="space-y-1.5 text-xs text-slate-300">
                ${data.microsoft.length === 0 ? '<li class="text-slate-500 italic">None (Customer manages 100% of the datacenter stack on-premises)</li>' : 
                data.microsoft.map(item => `
                    <li class="flex items-center space-x-2">
                        <i class="fa-solid fa-shield text-cyan-400 text-xs"></i>
                        <span>${item}</span>
                    </li>
                `).join('')}
            </ul>
        </div>
    `;
}

// ----------------------------------------------------------------------
// 3. Storage Redundancy & Lifecycle Simulator
// ----------------------------------------------------------------------
async function calculateStorageCost() {
    const gb = parseFloat(document.getElementById('storage-sim-gb').value) || 1000;
    const red = document.getElementById('storage-sim-red').value;
    const tier = document.getElementById('storage-sim-tier').value;
    const ret = parseFloat(document.getElementById('storage-sim-retrieval').value) || 200;

    try {
        const res = await fetch('/api/calculator/storage', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                data_size_gb: gb,
                redundancy_type: red,
                tier: tier,
                monthly_read_gb: ret
            })
        });
        const d = await res.json();
        
        document.getElementById('storage-sim-output').classList.remove('hidden');
        document.getElementById('sim-cost-val').innerText = `$${d.total_monthly_cost_usd.toFixed(2)}`;
        document.getElementById('sim-cost-breakdown').innerText = `Storage: $${d.monthly_storage_cost_usd.toFixed(2)} | Retrieval: $${d.monthly_retrieval_cost_usd.toFixed(2)}`;
        document.getElementById('sim-durability-val').innerText = d.durability;
        document.getElementById('sim-scope-val').innerText = d.replication_scope;
        document.getElementById('sim-rehydrate-val').innerText = d.rehydration_latency;
        document.getElementById('sim-usecase-val').innerText = d.ideal_use_case;
    } catch (e) {
        console.error(e);
    }
}

// ----------------------------------------------------------------------
// 4. Cloud Economics & TCO Simulator
// ----------------------------------------------------------------------
function updateTCOSliders() {
    document.getElementById('lbl-tco-servers').innerText = `${document.getElementById('tco-servers').value} servers`;
    document.getElementById('lbl-tco-cores').innerText = `${document.getElementById('tco-cores').value} cores`;
    document.getElementById('lbl-tco-ram').innerText = `${document.getElementById('tco-ram').value} GB`;
    document.getElementById('lbl-tco-storage').innerText = `${document.getElementById('tco-storage').value} TB`;
}

async function calculateTCO() {
    const servers = parseInt(document.getElementById('tco-servers').value);
    const cores = parseInt(document.getElementById('tco-cores').value);
    const ram = parseInt(document.getElementById('tco-ram').value);
    const storage = parseFloat(document.getElementById('tco-storage').value);
    const years = parseInt(document.getElementById('tco-years').value);
    const model = document.getElementById('tco-model').value;
    const ahb = document.getElementById('tco-ahb').checked;

    try {
        const res = await fetch('/api/calculator/tco', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                num_servers: servers,
                cpu_cores_per_server: cores,
                ram_gb_per_server: ram,
                storage_tb: storage,
                years: years,
                purchase_model: model,
                use_azure_hybrid_benefit: ahb
            })
        });
        const d = await res.json();

        document.getElementById('tco-res-onprem').innerText = `$${d.on_premises_total_usd.toLocaleString()}`;
        document.getElementById('tco-res-azure').innerText = `$${d.azure_total_usd.toLocaleString()}`;
        document.getElementById('tco-res-savings').innerText = `$${d.cost_savings_usd.toLocaleString()}`;
        document.getElementById('tco-res-pct').innerText = `${d.cost_savings_percentage}% Cost Reduction`;

        document.getElementById('tco-summary-text').innerText = d.capex_vs_opex_summary;

        // Populate itemized breakdown
        const onpremList = document.getElementById('tco-list-onprem');
        onpremList.innerHTML = d.on_premises_breakdown.map(i => `
            <li class="flex justify-between items-center py-1 border-b border-slate-800">
                <span>${i.name}</span>
                <span class="font-mono text-rose-300 font-semibold">$${i.cost_usd.toLocaleString()}</span>
            </li>
        `).join('');

        const azureList = document.getElementById('tco-list-azure');
        azureList.innerHTML = d.azure_breakdown.map(i => `
            <li class="flex justify-between items-center py-1 border-b border-slate-800">
                <span>${i.name}</span>
                <span class="font-mono text-cyan-300 font-semibold">$${i.cost_usd.toLocaleString()}</span>
            </li>
        `).join('');

    } catch (e) {
        console.error("TCO Calculation Error:", e);
    }
}

// ----------------------------------------------------------------------
// 5. Governance & Policy Engine + Composite SLA
// ----------------------------------------------------------------------
async function evaluateGovernance() {
    const resName = document.getElementById('gov-res-name').value.trim();
    const resType = document.getElementById('gov-res-type').value;
    const region = document.getElementById('gov-res-region').value;
    const lock = document.getElementById('gov-res-lock').value;
    let tags = {};
    try {
        tags = JSON.parse(document.getElementById('gov-res-tags').value);
    } catch (err) {
        alert("Tags must be valid JSON format!");
        return;
    }

    try {
        const res = await fetch('/api/governance/check', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                resource_name: resName,
                resource_type: resType,
                region: region,
                tags: tags,
                lock_type: lock
            })
        });
        const d = await res.json();

        const outEl = document.getElementById('gov-eval-output');
        outEl.classList.remove('hidden');

        const badge = document.getElementById('gov-badge-status');
        if (d.is_compliant) {
            badge.className = 'badge-success px-2 py-0.5 rounded font-bold';
            badge.innerText = `Score: ${d.compliance_score}/100 (Compliant)`;
        } else {
            badge.className = 'badge-danger px-2 py-0.5 rounded font-bold';
            badge.innerText = `Score: ${d.compliance_score}/100 (Non-Compliant)`;
        }

        const rulesList = document.getElementById('gov-rules-list');
        rulesList.innerHTML = d.rule_results.map(r => `
            <div class="flex items-start space-x-2 py-1">
                <i class="fa-solid ${r.passed ? 'fa-circle-check text-emerald-400' : 'fa-circle-xmark text-rose-400'} mt-0.5"></i>
                <div>
                    <span class="font-semibold text-slate-200">${r.rule_name}:</span>
                    <span class="text-slate-400">${r.details}</span>
                </div>
            </div>
        `).join('') + `
            <div class="mt-2 pt-2 border-t border-slate-800 text-slate-300">
                <strong>Lock Protection:</strong> ${d.lock_status}
            </div>
        `;
    } catch (e) {
        console.error(e);
    }
}

async function runSlaCalculation() {
    const mode = document.getElementById('sla-deploy-mode').value;
    const components = [
        { name: "Azure App Service", sla_percentage: 99.95, tier: "Premium" },
        { name: "Azure SQL Database", sla_percentage: 99.99, tier: "General Purpose" },
        { name: "Azure Blob Storage", sla_percentage: 99.90, tier: "Hot" }
    ];

    try {
        const res = await fetch('/api/calculator/sla', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                architecture_name: "Web API + SQL + Blob Architecture",
                components: components,
                deployment_mode: mode
            })
        });
        const d = await res.json();

        document.getElementById('sla-val').innerText = `${d.composite_sla_percentage}%`;
        document.getElementById('sla-downtime-year').innerText = `${d.max_downtime_per_year_hours} hrs/yr`;

        const recEl = document.getElementById('sla-recommendations');
        recEl.innerHTML = `
            <span class="font-bold text-slate-200 block mb-1">Architecture Guidance:</span>
            ${d.recommendations.map(r => `<p class="flex items-center gap-1.5"><i class="fa-solid fa-lightbulb text-amber-400 text-xs"></i> ${r}</p>`).join('')}
        `;
    } catch (e) {
        console.error(e);
    }
}

// ----------------------------------------------------------------------
// 6. AZ-900 Exam Simulator & Error Log
// ----------------------------------------------------------------------
async function loadQuizQuestions() {
    try {
        const res = await fetch('/api/quiz/questions');
        const data = await res.json();
        quizQuestions = data.questions;
        userAnswers = {};
        currentQuestionIndex = 0;
        renderCurrentQuestion();
    } catch (e) {
        console.error("Failed to load questions:", e);
    }
}

function renderCurrentQuestion() {
    if (!quizQuestions.length) return;
    const q = quizQuestions[currentQuestionIndex];
    document.getElementById('quiz-progress').innerText = `Question ${currentQuestionIndex + 1} of ${quizQuestions.length}`;

    const container = document.getElementById('quiz-question-container');
    const selectedAns = userAnswers[q.id];

    container.innerHTML = `
        <div class="space-y-3">
            <div class="flex items-center space-x-2">
                <span class="badge-azure text-xs px-2 py-0.5 rounded">${q.domain}</span>
                <span class="text-xs text-slate-400 font-medium">Weight: ${q.domain_weight} • ${q.subtopic}</span>
            </div>
            <h4 class="text-base font-bold text-white">${q.question}</h4>

            <div class="space-y-2 pt-2">
                ${q.options.map((opt, idx) => `
                    <div onclick="selectAnswer('${q.id}', ${idx})" class="p-3 rounded-lg border text-xs cursor-pointer transition flex items-center space-x-3 ${selectedAns === idx ? 'bg-blue-600/30 border-blue-500 text-white font-semibold' : 'bg-slate-900 border-slate-800 text-slate-300 hover:border-slate-600'}">
                        <span class="w-6 h-6 rounded-full flex items-center justify-center font-bold ${selectedAns === idx ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-400'}">${String.fromCharCode(65 + idx)}</span>
                        <span>${opt}</span>
                    </div>
                `).join('')}
            </div>

            <div class="flex justify-between items-center pt-4 border-t border-slate-800">
                <button onclick="prevQuestion()" ${currentQuestionIndex === 0 ? 'disabled' : ''} class="px-3 py-1.5 rounded bg-slate-800 text-slate-300 text-xs hover:bg-slate-700 disabled:opacity-40">Previous</button>
                <div class="flex space-x-2">
                    ${currentQuestionIndex < quizQuestions.length - 1 ? 
                        `<button onclick="nextQuestion()" class="px-4 py-1.5 rounded bg-blue-600 text-white text-xs font-semibold hover:bg-blue-500">Next Question</button>` : 
                        `<button onclick="submitQuiz()" class="px-5 py-1.5 rounded bg-emerald-600 text-white text-xs font-bold hover:bg-emerald-500 shadow-lg shadow-emerald-600/30">Submit Exam for Scoring</button>`
                    }
                </div>
            </div>
        </div>
    `;
}

function selectAnswer(qid, ansIdx) {
    userAnswers[qid] = ansIdx;
    renderCurrentQuestion();
}

function nextQuestion() {
    if (currentQuestionIndex < quizQuestions.length - 1) {
        currentQuestionIndex++;
        renderCurrentQuestion();
    }
}

function prevQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        renderCurrentQuestion();
    }
}

async function submitQuiz() {
    try {
        const res = await fetch('/api/quiz/submit', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ answers: userAnswers })
        });
        const d = await res.json();

        const banner = document.getElementById('quiz-result-banner');
        banner.classList.remove('hidden');

        if (d.passed) {
            banner.className = 'p-5 rounded-xl border border-emerald-500/30 bg-emerald-950/20 space-y-4';
        } else {
            banner.className = 'p-5 rounded-xl border border-rose-500/30 bg-rose-950/20 space-y-4';
        }

        banner.innerHTML = `
            <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-3">
                <div>
                    <span class="text-xs font-bold uppercase tracking-wider ${d.passed ? 'text-emerald-400' : 'text-rose-400'}">${d.passed ? 'Examination Passed' : 'Needs Revision'}</span>
                    <h3 class="text-2xl font-black text-white">Score: ${d.candidate_score} / 1000</h3>
                    <p class="text-xs text-slate-300 mt-1">${d.performance_analysis}</p>
                </div>
                <div class="text-right">
                    <span class="text-xs text-slate-400 block">Dev Sehgal's Actual Score</span>
                    <span class="text-xl font-bold text-cyan-400">971 / 1000</span>
                    <span class="text-xs text-slate-500 block">Certiport Oct 2026</span>
                </div>
            </div>

            <!-- Domain-wise bars -->
            <div class="space-y-2 pt-2 border-t border-slate-800 text-xs">
                <span class="font-bold text-slate-200">Domain-Wise Breakdown:</span>
                ${d.domain_scores.map(s => `
                    <div>
                        <div class="flex justify-between text-slate-300 mb-1">
                            <span>${s.domain_name} (${s.weight})</span>
                            <span class="font-mono font-bold">${s.percentage}% (${s.correct}/${s.total})</span>
                        </div>
                        <div class="w-full bg-slate-900 h-2 rounded-full overflow-hidden">
                            <div class="h-full bg-blue-500" style="width: ${s.percentage}%"></div>
                        </div>
                    </div>
                `).join('')}
            </div>

            ${d.incorrect_questions.length > 0 ? `
                <div class="pt-3 border-t border-slate-800 space-y-2 text-xs">
                    <span class="font-bold text-rose-400">Review Incorrect Items:</span>
                    <div class="space-y-2 max-h-48 overflow-y-auto">
                        ${d.incorrect_questions.map(iq => `
                            <div class="p-2.5 bg-slate-900 rounded border border-slate-800">
                                <p class="font-semibold text-slate-200">${iq.question}</p>
                                <p class="text-emerald-400 mt-1"><strong>Correct:</strong> ${iq.correct_answer}</p>
                                <p class="text-slate-400 mt-0.5"><em>${iq.explanation}</em></p>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : '<div class="text-xs text-emerald-400 font-semibold"><i class="fa-solid fa-star"></i> Perfect score! 100% correct answers.</div>'}
        `;

        banner.scrollIntoView({ behavior: 'smooth' });
    } catch (e) {
        console.error("Submission failed:", e);
    }
}

function resetQuiz() {
    userAnswers = {};
    currentQuestionIndex = 0;
    document.getElementById('quiz-result-banner').classList.add('hidden');
    renderCurrentQuestion();
}

function toggleErrorLog() {
    const el = document.getElementById('error-log-container');
    const icon = document.getElementById('error-log-toggle-icon');
    if (el.classList.contains('hidden')) {
        el.classList.remove('hidden');
        icon.innerHTML = '<i class="fa-solid fa-chevron-up"></i> Click to collapse';
    } else {
        el.classList.add('hidden');
        icon.innerHTML = '<i class="fa-solid fa-chevron-down"></i> Click to expand';
    }
}

async function loadErrorLog() {
    try {
        const res = await fetch('/api/quiz/error-log');
        const data = await res.json();
        const container = document.getElementById('error-log-container');
        container.innerHTML = data.error_log_entries.map(err => `
            <div class="p-3 bg-slate-900 rounded-lg border border-slate-800 space-y-1">
                <div class="flex justify-between items-center">
                    <span class="font-bold text-cyan-400">${err.distinction}</span>
                    <span class="text-xs badge-azure px-1.5 py-0.5 rounded">${err.topic}</span>
                </div>
                <p class="text-rose-300"><strong>Trap:</strong> ${err.error_trap}</p>
                <p class="text-emerald-300"><strong>Rule:</strong> ${err.one_line_rule}</p>
            </div>
        `).join('');
    } catch (e) {
        console.error(e);
    }
}

// ----------------------------------------------------------------------
// 7. Azure Monitor & Telemetry Stream
// ----------------------------------------------------------------------
async function fetchTelemetry() {
    try {
        const res = await fetch('/api/telemetry/metrics');
        const d = await res.json();

        document.getElementById('telem-req-count').innerText = d.total_requests;
        document.getElementById('telem-avg-lat').innerText = `${d.avg_latency_ms.toFixed(1)} ms`;
        document.getElementById('telem-uptime').innerText = d.uptime_human;
        document.getElementById('telem-budget-pct').innerText = `${d.cost_management.spend_percentage}%`;
        document.getElementById('telem-budget-status').innerText = `$${d.cost_management.current_spend_usd.toFixed(2)} of $${d.cost_management.budget_limit_usd.toFixed(2)}`;
        document.getElementById('status-budget').innerText = `$${d.cost_management.current_spend_usd.toFixed(2)} / $${d.cost_management.budget_limit_usd.toFixed(2)}`;

        // Logs
        const logStream = document.getElementById('live-log-stream');
        if (d.recent_logs && d.recent_logs.length > 0) {
            logStream.innerHTML = d.recent_logs.map(log => {
                let color = "text-slate-300";
                if (log.level === "ERROR") color = "text-rose-400 font-bold";
                else if (log.level === "WARN") color = "text-amber-400 font-bold";
                else if (log.level === "INFO") color = "text-emerald-400";
                return `<div><span class="text-slate-500">[${log.timestamp}]</span> <span class="${color}">[${log.level}]</span> ${log.message}</div>`;
            }).join('');
        }
    } catch (e) {
        // Silently catch polling errors if server rebooting
    }
}

async function simulateSpendSpike() {
    await fetch('/api/telemetry/simulate-spend-spike', { method: 'POST' });
    fetchTelemetry();
    alert("Simulated budget consumption spike to $135.00! Azure Cost Management alert threshold (80%) triggered.");
}

async function resetSpend() {
    await fetch('/api/telemetry/reset-budget-alert', { method: 'POST' });
    fetchTelemetry();
}
