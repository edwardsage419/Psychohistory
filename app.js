/* ===========================================================
   Psychohistory — V0.1
   本文件所有数据均为 MOCK DATA（占位数据），用于验证页面结构。
   V0.2 起将逐步替换为 GDELT 等真实数据源。
   =========================================================== */

const MOCK = {

  meta: {
    updatedAt: "2026-09-03 08:00 (Mock)",
    sourceCount: 0,
    modelVersion: "V0.1-mock"
  },

  // Global State: 0-100，deltas 为百分点变化
  indicators: [
    { name: "Global Risk",          value: 58, d7: +3, d30: +7,  dir: "up"   },
    { name: "Economic Pressure",    value: 47, d7: +1, d30: -2,  dir: "flat" },
    { name: "Geopolitical Risk",    value: 63, d7: +5, d30: +11, dir: "up"   },
    { name: "Technology Momentum",  value: 71, d7: +2, d30: +9,  dir: "up"   },
    { name: "Market Stress",        value: 39, d7: -4, d30: -6,  dir: "down" },
    { name: "Energy Stress",        value: 44, d7: 0,  d30: +3,  dir: "flat" },
    { name: "Social Attention",     value: 52, d7: +6, d30: +2,  dir: "up"   }
  ],

  trends: [
    {
      title: "全球关于「供应链」的新闻提及量上升",
      dir: "up",
      change: "+40%（30天）",
      tags: ["经济", "供应链"],
      basis: "新闻数量统计（Mock）",
      updated: "2小时前"
    },
    {
      title: "能源相关负面情绪指数下降",
      dir: "down",
      change: "-12%（7天）",
      tags: ["能源", "情绪分析"],
      basis: "新闻情绪评分（Mock）",
      updated: "5小时前"
    },
    {
      title: "科技领域政策相关报道显著增加",
      dir: "up",
      change: "+28%（14天）",
      tags: ["科技", "政策"],
      basis: "新闻分类统计（Mock）",
      updated: "1天前"
    }
  ],

  predictions: [
    {
      event: "未来12个月美国经济进入衰退",
      probability: 35,
      confidence: "Medium",
      created: "2026-09-02",
      evidenceCount: 4
    },
    {
      event: "未来6个月全球能源价格显著上升（>15%）",
      probability: 28,
      confidence: "Low",
      created: "2026-08-29",
      evidenceCount: 3
    },
    {
      event: "未来3个月主要科技监管政策出台",
      probability: 54,
      confidence: "Medium",
      created: "2026-08-20",
      evidenceCount: 6
    }
  ],

  history: [
    { event: "未来6个月全球贸易紧张局势升级",  probability: 62, created: "2026-02-10", target: "2026-08-10", result: "correct" },
    { event: "未来3个月主要央行下调利率",       probability: 45, created: "2026-03-01", target: "2026-06-01", result: "incorrect" },
    { event: "未来12个月全球通胀率下降至3%以下", probability: 40, created: "2025-12-15", target: "2026-12-15", result: "pending" },
    { event: "未来6个月科技行业重大并购增加",    probability: 58, created: "2026-01-20", target: "2026-07-20", result: "correct" }
  ],

  metrics: [
    { label: "Accuracy",              value: "0.71" },
    { label: "Brier Score",           value: "0.19" },
    { label: "Calibration",           value: "0.86" },
    { label: "Log Loss",              value: "0.52" },
    { label: "预测总数",              value: "12" },
    { label: "已验证预测",            value: "9" }
  ],

  sources: [
    { name: "GDELT",        desc: "全球新闻事件数据库", status: "planned" },
    { name: "World Bank",   desc: "宏观经济指标",       status: "planned" },
    { name: "FRED",         desc: "美国经济数据",       status: "planned" },
    { name: "Mock Generator", desc: "V0.1 占位数据生成器", status: "mock" }
  ]
};

/* ---------- Helpers ---------- */

function dirArrow(dir) {
  if (dir === "up") return "▲";
  if (dir === "down") return "▼";
  return "▬";
}

function dirClass(dir) {
  if (dir === "up") return "dir-up";
  if (dir === "down") return "dir-down";
  return "dir-flat";
}

function fmtDelta(n) {
  if (n > 0) return `+${n}`;
  return `${n}`;
}

/* ---------- Render: Header meta ---------- */

function renderMeta() {
  document.getElementById("meta-updated").textContent = MOCK.meta.updatedAt;
  document.getElementById("meta-sources").textContent = `${MOCK.sources.length} 个（规划中）`;
  document.getElementById("meta-predictions").textContent = `${MOCK.predictions.length} 条`;
  document.getElementById("meta-model").textContent = MOCK.meta.modelVersion;
}

/* ---------- Render: Global State ---------- */

function renderIndicators() {
  const grid = document.getElementById("indicator-grid");
  grid.innerHTML = MOCK.indicators.map(ind => `
    <div class="indicator-card">
      <div class="indicator-name">${ind.name}</div>
      <div class="indicator-value-row">
        <span class="indicator-value">${ind.value}</span>
        <span class="indicator-dir ${dirClass(ind.dir)}">${dirArrow(ind.dir)}</span>
      </div>
      <div class="indicator-bar">
        <div class="indicator-bar-fill" style="width:${ind.value}%"></div>
      </div>
      <div class="indicator-deltas">
        <span>7天 ${fmtDelta(ind.d7)}</span>
        <span>30天 ${fmtDelta(ind.d30)}</span>
      </div>
    </div>
  `).join("");
}

/* ---------- Render: Today's Trends ---------- */

function renderTrends() {
  const list = document.getElementById("trend-list");
  list.innerHTML = MOCK.trends.map(t => `
    <div class="trend-item trend-${t.dir}">
      <div class="trend-top">
        <span class="trend-title">${t.title}</span>
        <span class="trend-change ${dirClass(t.dir)}">${dirArrow(t.dir)} ${t.change}</span>
      </div>
      <div class="trend-meta">
        ${t.tags.map(tag => `<span class="trend-tag">${tag}</span>`).join("")}
        <span>依据：${t.basis}</span>
        <span>更新：${t.updated}</span>
      </div>
    </div>
  `).join("");
}

/* ---------- Render: Predictions ---------- */

function renderPredictions() {
  const grid = document.getElementById("prediction-grid");
  grid.innerHTML = MOCK.predictions.map(p => `
    <div class="prediction-card">
      <div class="prediction-event">${p.event}</div>
      <div class="prediction-stats">
        <div>
          <div class="prediction-stat-label">PROBABILITY</div>
          <div class="prediction-stat-value prob-value">${p.probability}%</div>
        </div>
        <div>
          <div class="prediction-stat-label">CONFIDENCE</div>
          <div class="prediction-stat-value">${p.confidence}</div>
        </div>
        <div>
          <div class="prediction-stat-label">EVIDENCE</div>
          <div class="prediction-stat-value">${p.evidenceCount}</div>
        </div>
      </div>
      <div class="prediction-foot">
        <span>Created: ${p.created}</span>
        <span>Model: ${MOCK.meta.modelVersion}</span>
      </div>
    </div>
  `).join("");
}

/* ---------- Render: Prediction History ---------- */

function resultBadge(result) {
  if (result === "correct")   return `<span class="result-badge result-correct">Correct</span>`;
  if (result === "incorrect") return `<span class="result-badge result-incorrect">Incorrect</span>`;
  return `<span class="result-badge result-pending">Pending</span>`;
}

function renderHistory() {
  const body = document.getElementById("history-body");
  body.innerHTML = MOCK.history.map(h => `
    <tr>
      <td>${h.event}</td>
      <td>${h.probability}%</td>
      <td>${h.created}</td>
      <td>${h.target}</td>
      <td>${resultBadge(h.result)}</td>
    </tr>
  `).join("");
}

/* ---------- Render: Model Performance ---------- */

function renderMetrics() {
  const grid = document.getElementById("metric-grid");
  grid.innerHTML = MOCK.metrics.map(m => `
    <div class="metric-card">
      <div class="metric-value">${m.value}</div>
      <div class="metric-label">${m.label}</div>
    </div>
  `).join("");
}

/* ---------- Render: Data Sources ---------- */

function renderSources() {
  const list = document.getElementById("source-list");
  list.innerHTML = MOCK.sources.map(s => `
    <div class="source-item">
      <div>
        <span class="source-name">${s.name}</span>
        <span class="source-desc">${s.desc}</span>
      </div>
      <span class="source-status status-${s.status}">${s.status === "mock" ? "MOCK" : "PLANNED"}</span>
    </div>
  `).join("");
}

/* ---------- Init ---------- */

function init() {
  renderMeta();
  renderIndicators();
  renderTrends();
  renderPredictions();
  renderHistory();
  renderMetrics();
  renderSources();
}

document.addEventListener("DOMContentLoaded", init);
