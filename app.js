/* ===========================================================
   Psychohistory — V0.2
   "Monitoring Topics" 板块读取 data/gdelt.json（真实 GDELT 数据）。
   浏览器不直接访问 GDELT，只读取本仓库内的静态 JSON 文件，
   该文件由 GitHub Actions（scripts/update_gdelt.py）每日更新。

   Today's Trends / Predictions / Prediction History / Model
   Performance 仍是 V0.1 遗留的 MOCK DATA，尚未接入真实数据源，
   将在后续版本（V0.4 起）逐步替换。
   =========================================================== */

const GDELT_DATA_URL = "data/gdelt.json";

const MOCK = {

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
    { label: "Accuracy",   value: "0.71" },
    { label: "Brier Score",value: "0.19" },
    { label: "Calibration",value: "0.86" },
    { label: "Log Loss",   value: "0.52" },
    { label: "预测总数",   value: "12" },
    { label: "已验证预测", value: "9" }
  ],

  sources: [
    { name: "GDELT DOC 2.0 API", desc: "全球新闻媒体报道量（timelinevol）— 已接入", status: "live" },
    { name: "World Bank",        desc: "宏观经济指标", status: "planned" },
    { name: "FRED",               desc: "美国经济数据", status: "planned" },
    { name: "Mock Generator",     desc: "Predictions / History 板块占位数据生成器", status: "mock" }
  ]
};

/* ---------- Generic helpers ---------- */

function dirClass(dir) {
  if (dir === "up" || dir === "rising")  return "dir-up";
  if (dir === "down" || dir === "falling") return "dir-down";
  return "dir-flat";
}

function dirArrow(dir) {
  if (dir === "up" || dir === "rising")  return "▲";
  if (dir === "down" || dir === "falling") return "▼";
  return "▬";
}

function fmtPct(v) {
  if (v === null || v === undefined || Number.isNaN(v)) return "—";
  return `${v.toFixed(3)}%`;
}

function fmtChange(v) {
  if (v === null || v === undefined || Number.isNaN(v)) return "—";
  const sign = v > 0 ? "+" : "";
  return `${sign}${v.toFixed(1)}%`;
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

/* ---------- Load GDELT data ---------- */

async function loadGdeltData() {
  try {
    const res = await fetch(GDELT_DATA_URL, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (!data || typeof data !== "object") throw new Error("Invalid JSON shape");
    return data;
  } catch (err) {
    console.error("Failed to load data/gdelt.json:", err);
    return null;
  }
}

/* ---------- Render: Header meta + GDELT status ---------- */

function renderHeaderMeta(gdelt) {
  const meta = gdelt && gdelt.metadata ? gdelt.metadata : null;
  document.getElementById("meta-updated").textContent = meta && meta.updated_at ? meta.updated_at : "—";
  document.getElementById("meta-sources").textContent = meta && meta.source ? meta.source : "—";
  document.getElementById("meta-topics").textContent = meta && meta.topics ? `${meta.topics.length}` : "—";
  document.getElementById("meta-model").textContent = meta && meta.system_version ? meta.system_version : "V0.2";
}

function renderGdeltStatus(gdelt) {
  const bar = document.getElementById("gdelt-status");
  const meta = gdelt && gdelt.metadata ? gdelt.metadata : null;

  if (!gdelt || !meta || !meta.updated_at) {
    bar.innerHTML = `
      <div class="status-row status-bad">
        <span class="status-dot"></span>
        GDELT Data Unavailable — 尚未成功运行过数据抓取
      </div>`;
    return;
  }

  const ok = meta.last_run_status === "ok";
  bar.innerHTML = `
    <div class="status-row ${ok ? "" : "status-warn"}">
      <span class="status-dot"></span>
      ${ok ? "GDELT Data Updated" : "GDELT Update Issue — 显示最后一次成功数据"}
    </div>
    <dl class="status-meta">
      <div><dt>Data Updated</dt><dd>${escapeHtml(meta.updated_at)}</dd></div>
      <div><dt>Data Source</dt><dd>${escapeHtml(meta.source || "—")}</dd></div>
      <div><dt>Monitoring Topics</dt><dd>${(meta.topics || []).length}</dd></div>
      <div><dt>System Version</dt><dd>${escapeHtml(meta.system_version || "—")}</dd></div>
    </dl>`;
}

/* ---------- Render: Monitoring Topics (real GDELT data) ---------- */

function buildSparkline(history, name) {
  if (!Array.isArray(history) || history.length === 0) return "";

  const points = history
    .slice(-7)
    .map(row => (row.topics && row.topics[name] ? row.topics[name].value : null))
    .filter(v => v !== null && v !== undefined && !Number.isNaN(v));

  if (points.length < 2) return "";

  const max = Math.max(...points);
  const min = Math.min(...points);
  const range = max - min || 1;
  const w = 100, h = 28;
  const step = w / (points.length - 1);

  const coords = points
    .map((v, i) => {
      const x = i * step;
      const y = h - ((v - min) / range) * h;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  return `<svg class="sparkline" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
    <polyline points="${coords}" />
  </svg>`;
}

function renderTopics(gdelt) {
  const grid = document.getElementById("topic-grid");
  const defEl = document.getElementById("topic-value-def");

  const meta = gdelt && gdelt.metadata ? gdelt.metadata : null;
  const current = gdelt && gdelt.current ? gdelt.current : {};
  const history = gdelt && gdelt.history ? gdelt.history : [];
  const topicNames = meta && Array.isArray(meta.topics) && meta.topics.length
    ? meta.topics
    : ["Economic", "Geopolitics", "Technology", "Energy", "War & Conflict", "Inflation", "AI"];

  defEl.textContent = meta && meta.value_definition
    ? meta.value_definition
    : "value 表示该主题相关新闻占 GDELT 监测的全球新闻总量的百分比（媒体报道量占比），不代表真实世界风险或事件发生程度。";

  grid.innerHTML = topicNames.map(name => {
    const t = current[name];

    if (!t || t.value === null || t.value === undefined) {
      return `
        <div class="topic-card topic-card-empty">
          <div class="topic-top">
            <span class="topic-name">${escapeHtml(name)}</span>
          </div>
          <div class="empty-state">Data Unavailable</div>
        </div>`;
    }

    const trend = t.trend || "stable";
    const spark = buildSparkline(history, name);
    const staleNote = t.status === "failed"
      ? `<div class="topic-stale-note">最近一次抓取失败（${escapeHtml(t.error || "unknown error")}），显示为最后一次成功数据${t.last_success_at ? `（${escapeHtml(t.last_success_at)}）` : ""}</div>`
      : "";

    return `
      <div class="topic-card">
        <div class="topic-top">
          <span class="topic-name">${escapeHtml(name)}</span>
          <span class="topic-trend ${dirClass(trend)}">${dirArrow(trend)} ${trend.toUpperCase()}</span>
        </div>
        <div class="topic-stats">
          <div>
            <div class="topic-stat-label">CURRENT</div>
            <div class="topic-stat-value">${fmtPct(t.value)}</div>
          </div>
          <div>
            <div class="topic-stat-label">7D AVG</div>
            <div class="topic-stat-value">${fmtPct(t["7_day_average"])}</div>
          </div>
          <div>
            <div class="topic-stat-label">CHANGE</div>
            <div class="topic-stat-value">${fmtChange(t.change_percent)}</div>
          </div>
        </div>
        ${spark}
        ${staleNote}
      </div>`;
  }).join("");
}

/* ---------- Render: Today's Trends (mock) ---------- */

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

/* ---------- Render: Predictions (mock) ---------- */

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
        <span>Model: V0.1-mock</span>
      </div>
    </div>
  `).join("");
}

/* ---------- Render: Prediction History (mock) ---------- */

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

/* ---------- Render: Model Performance (mock) ---------- */

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
  const statusLabel = { live: "LIVE", planned: "PLANNED", mock: "MOCK" };
  list.innerHTML = MOCK.sources.map(s => `
    <div class="source-item">
      <div>
        <span class="source-name">${s.name}</span>
        <span class="source-desc">${s.desc}</span>
      </div>
      <span class="source-status status-${s.status}">${statusLabel[s.status] || s.status.toUpperCase()}</span>
    </div>
  `).join("");
}

/* ---------- Init ---------- */

async function init() {
  const gdelt = await loadGdeltData();

  renderHeaderMeta(gdelt);
  renderGdeltStatus(gdelt);
  renderTopics(gdelt);

  renderTrends();
  renderPredictions();
  renderHistory();
  renderMetrics();
  renderSources();
}

document.addEventListener("DOMContentLoaded", init);
