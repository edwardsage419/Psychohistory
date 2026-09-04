# Psychohistory

个人心理史学系统：基于公开数据、新闻事件与 AI 分析的社会趋势观测与概率预测系统。

## 项目目标

长期回答四个问题：世界现在发生什么；哪些趋势正在增强或减弱；未来可能发生什么；过去预测是否有效。

系统不声称能够真正预测历史。所有预测均为概率判断，并持续与真实结果对照验证。

## 当前开发阶段

```text
V0.2      GDELT DOC 真实数据
V0.2.1-A  GKG 2.1 数据源验证
V0.2.1-B  GKG Theme Mapping
V0.2.1-C  多日稳定性采集与生产准入检查  ← 当前
V0.3      社会趋势指数
V0.4      AI 分析
V0.5      预测数据库
V0.6+     自动验证、历史回测、多模型比较
```

当前原则：先验证数据地基、主题定义和长期稳定性。稳定性不足时不进入生产指数，不提前加入 AI 预测。

## V0.2.1-A：GKG 数据源验证

验证 GDELT GKG 2.1 批量文件的可获取性和格式，不修改 `data/gdelt.json`。

- `scripts/validate_gkg.py`：发现最新 GKG、下载、ZIP 完整性、流式解析、字段数、日期、V1THEMES 和 SHA-256 检查。
- `scripts/test_validate_gkg.py`：离线测试。
- `.github/workflows/validate-gkg.yml`：定时和手动验证。

GitHub Actions 已真实验证 GKG 2.1 文件可以下载并解析。

## V0.2.1-B：GKG Theme Mapping

`V1THEMES` 位于 GKG 第 8 个字段，是分号分隔的 Theme code。当前建立七个 provisional 研究主题：

Economic / Geopolitics / Technology / Energy / War & Conflict / Inflation / AI

每个主题区分 `primary`、`secondary` 和 `excluded`。

映射依据 GDELT 官方 Theme lookup、Codebook 和实际 GKG 批次频次。官方 lookup 的第二列是历史文档频次，不是自然语言 description，程序不会把该数字误标成描述。

AI 当前为 `proxy_only_not_for_production`。后续需要独立的 lexical / entity / enhanced-theme 层后才能进入生产。

### 计数规则

同一篇 GKG 文档中的同一个 Theme 只计一次。

一个文档在某个 Psychohistory 主题中只计一次：只要至少命中该主题的一个 primary 或 secondary Theme，就计入该主题的 `all_union_documents`。这样可以避免一篇文章包含多个 Theme 时被重复放大。

## V0.2.1-C：多日稳定性管线

当前已经进入自动采集。所有数据均为 `analysis_only`，不会修改 `data/gdelt.json`。

核心文件：

- `scripts/collect_gkg_stability.py`
- `scripts/evaluate_gkg_stability.py`
- `scripts/test_collect_gkg_stability.py`
- `scripts/test_evaluate_gkg_stability.py`
- `scripts/gkg_stability_history/`
- `scripts/gkg_stability_report.json`
- `.github/workflows/collect-gkg-stability.yml`

### GKG 发布延迟保护

`lastupdate.txt` 可能先出现最新时间戳，而对应 ZIP 暂时返回 HTTP 404。采集器会尝试最新批次以及之前的多个 15 分钟批次，并兼容 HTTP/HTTPS，避免短暂发布延迟导致当天采集失败。

### 稳定性窗口

稳定性窗口按不同 UTC 自然日计算，不按原始批次数量计算。

一天内如果手动运行多次，只选择当天最新的有效批次参与日级统计。因此重复运行不会错误地提前满足 7 天或 14 天门槛。

当前门槛：

- 少于 7 个不同 UTC 日期：`collecting`
- 达到 7 个不同 UTC 日期：`minimum_window_reached`，第一次人工检查
- 达到 14 个不同 UTC 日期：`target_reached`，正式人工生产准入评估

任何门槛都不会自动把 Theme 或主题指数提升到生产状态。

### 稳定性统计

对每个主题使用按 1000 个有效 GKG 文档归一化的 `all_union_documents`，并计算：

- mean
- sample standard deviation
- coefficient of variation (CV)
- minimum / maximum
- primary / secondary 平均覆盖率

CV 仅用于描述稳定程度，不作为自动生产准入条件。

## 当前真实状态

2026-09-04 已成功采集真实 GKG 批次，最新成功批次包含 1025 条有效记录、0 条异常记录。当前稳定性状态为 `collecting`，有效日样本为 1。

下一阶段主要观察：

1. GKG 是否持续可获取。
2. 是否持续保持 0 个异常行。
3. 每批文档量是否出现异常跳变。
4. 各主题 normalized rate 是否稳定。
5. Theme overlap 是否造成重复计量或高度相关。
6. 泛化 Theme 是否长期主导信号。
7. AI proxy 是否过于宽泛。

## V0.2：DOC 数据层

V0.2 已把 Monitoring Topics 从 Mock Data 换成真实 GDELT DOC 数据。Today's Trends、Predictions、Prediction History、Model Performance 仍为占位数据。

DOC API 在 GitHub Actions 共享环境中实测大量出现 HTTP 429，偶尔出现 SSL 问题。退避策略调整后成功率仍只有约 15-30%，因此不再把 DOC 查询 API 作为长期核心数据管线。GKG 批量文件成为后续主题分析的主要数据基础。

## 生产准入原则

V0.2.1-C 完成前：

- 不把 GKG Theme 写入 `data/gdelt.json`。
- 不把单日结果当作长期趋势。
- 不根据 CV 自动判断可靠性。
- 不把 AI proxy 当作 AI 指数。
- 不跳过人工 Theme mapping 审查。

达到至少 14 个不同 UTC 日期后，综合数据质量、稳定性、Theme overlap、语义合理性和异常情况，决定哪些信号进入 V0.3。

## 文件结构

```text
index.html
style.css
app.js
data/gdelt.json
scripts/update_gdelt.py
scripts/validate_gkg.py
scripts/test_validate_gkg.py
scripts/gkg_theme_mapping.json
scripts/analyze_gkg_themes.py
scripts/test_analyze_gkg_themes.py
scripts/collect_gkg_stability.py
scripts/test_collect_gkg_stability.py
scripts/evaluate_gkg_stability.py
scripts/test_evaluate_gkg_stability.py
scripts/gkg_stability_history/
scripts/gkg_stability_report.json
.github/workflows/update-gdelt.yml
.github/workflows/validate-gkg.yml
.github/workflows/analyze-gkg-themes.yml
.github/workflows/collect-gkg-stability.yml
```

## 免责声明

本项目所有预测均为概率估计，不构成投资、政治或其他任何决策建议。历史预测记录一旦生成不会被事后修改。
