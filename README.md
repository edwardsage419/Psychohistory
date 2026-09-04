# Psychohistory

个人心理史学系统 — 基于公开数据、新闻事件与 AI 分析的社会趋势观测与概率预测系统。

灵感来源：Isaac Asimov《银河帝国》中的"心理史学"概念。

## 项目目标

本系统尝试长期、系统性地回答：

- 世界现在正在发生什么？
- 哪些趋势正在增强或减弱？
- 根据当前数据，未来可能发生什么，概率是多少？
- 过去的预测准不准？哪个模型表现最好？

系统**不**声称能够真正预测历史。所有预测都是概率判断，会被持续记录并与真实结果对照验证。


### V0.2.1-A：GKG 数据源验证（当前阶段）

V0.2.1-A 只验证 GDELT GKG 2.1 批量文件的可获取性和格式，不修改 `data/gdelt.json`，也不把任何 GKG 数据写入生产数据。GDELT 官方说明 GKG 2.1 每条记录使用制表符分隔，并包含固定字段，其中 `V1THEMES` 位于第 8 个字段；GKG 2.1 是按文档逐条记录的格式。

新增：
- `scripts/validate_gkg.py`：发现最新 GKG 文件、下载、ZIP 完整性检查、流式解析、字段数检查、日期检查、`V1THEMES` 统计和 SHA-256 记录。
- `scripts/test_validate_gkg.py`：离线合成数据测试，不依赖网络。
- `.github/workflows/validate-gkg.yml`：在 GitHub Actions 中定时验证最新线上 GKG 文件，每小时运行一次，也支持手动运行。该工作流只生成 Artifact，不提交生产数据。

当前阶段的验收标准：
1. GitHub Actions 能从 `lastupdate.txt` 找到最新 `.gkg.csv.zip`。
2. ZIP 可以完整读取且包含单一 GKG 数据文件。
3. 每条记录至少包含 GKG 2.1 的前 8 个字段。
4. 第 8 个字段可以稳定解析为分号分隔的主题列表。
5. 不修改现有 DOC API 数据。

通过 V0.2.1-A 后，下一阶段才建立 7 个 Psychohistory 主题的 GKG Theme Mapping。主题映射会先依据 GDELT 官方主题列表和实际频次验证，再进入生产聚合。

## 当前状态：V0.2

V0.2 把 **Monitoring Topics** 板块从 Mock Data 换成了真实的 GDELT 数据，并建立了每日自动更新机制。其余板块（Today's Trends / Predictions / Prediction History / Model Performance）仍是 V0.1 的占位数据，尚未接入真实数据源，会在后续版本中逐步替换。

### 文件结构

```
index.html                          页面结构
style.css                           样式（深色数据仪表盘风格）
app.js                              读取 data/gdelt.json + 渲染逻辑
data/gdelt.json                     GDELT 数据存储（metadata / current / history）
scripts/update_gdelt.py             每日拉取 GDELT 数据的 Python 脚本
.github/workflows/update-gdelt.yml  每日自动运行 + 手动运行的 GitHub Actions 配置
README.md                           本文件
```

### 数据架构

```
GDELT DOC 2.0 API (timelinevol)
        ↓
GitHub Actions（每日一次，也可手动运行）
        ↓
scripts/update_gdelt.py（拉取 → 校验 → 聚合 → 保存）
        ↓
data/gdelt.json（metadata + current + history，逐日累积）
        ↓
GitHub Pages（浏览器只读取这个 JSON 文件，不直接访问 GDELT）
        ↓
Dashboard
```

**浏览器不直接调用 GDELT。** 这样即使 GDELT 当天访问不了，Dashboard 依然能正常打开并显示上一次成功的数据。

### `value` 到底是什么

Monitoring Topics 里的 `value` 是 **GDELT 匹配到的新闻，占 GDELT 监测的全球新闻总量的百分比**，也就是「媒体报道量占比」。

它反映的是**媒体对某个话题的关注程度**，**不代表**：
- 该事件真实发生的严重程度
- 经济 / 地缘政治 / 军事等风险的真实水平

页面上会明确标注这一点，避免把「报道量」误读成「真实情况」。

### 七个监测主题

Economic / Geopolitics / Technology / Energy / War & Conflict / Inflation / AI

每个主题保存：`current`（最新一天数值）、`7_day_average`（过去 7 个自然日的平均值）、`change_percent`（相对 7 日均值的变化）、`trend`（`rising` / `falling` / `stable`，阈值 ±10 个百分点，见 `scripts/update_gdelt.py` 中的 `TREND_THRESHOLD`）。

### 失败处理

任何一个主题当天抓取失败，不会影响其它主题，也不会用假数据覆盖历史：
- 该主题会保留**上一次成功的数值**，并标记 `"status": "failed"` 和具体错误信息
- Dashboard 会在对应卡片上显示"最近一次抓取失败，显示为最后一次成功数据"
- 如果七个主题当天全部失败，`data/gdelt.json` 完全不变，工作流日志里会有明确的 `[ERROR]` 记录

同一个 UTC 自然日内重复运行（无论是定时触发还是手动 `workflow_dispatch`），只会更新当天这一行历史记录，不会产生重复行。

### 为什么选 GDELT DOC 2.0 API 而不是之前的方案

之前直接在网页端或 GitHub Actions 里高频调用 GDELT DOC API（文章列表模式）出现了 429 / timeout / SSL / JSON 解析失败等问题。这一版做了三处根本性调整，而不是单纯增加重试次数：

1. **换成 `timelinevol` 模式**：只返回一个很小的时间序列 JSON，而不是完整文章列表，请求本身更轻。
2. **补上浏览器 User-Agent**：有实际证据表明 GDELT 现在会拒绝没有 User-Agent 的请求（即使请求频率很低）。
3. **把请求量降到每天 7 次**（每个主题一次），并在主题之间间隔 15 秒，这和之前触发限流的高频调用模式完全不同。

同时，脚本对 GDELT「返回 HTTP 200 但内容是纯文本错误提示」这种已知的怪异行为做了防御性处理：任何非预期的响应格式都会被当作失败处理，而不会让整个工作流崩溃或产生假数据。这部分逻辑已经用本地模拟的 HTTP 响应测试过（成功 / 纯文本报错 / 单主题失败三种情况）。

**已知局限**：这次开发环境本身无法访问外网，所以这个脚本从未真正打到 GDELT 的服务器——已验证的是 JSON 解析、聚合计算、趋势判断、失败保护、历史去重这些逻辑本身没问题，但**没有验证 GitHub Actions 实际运行时能否连上 GDELT**。请在推送后手动运行一次 workflow（见下方验证步骤），如果仍然频繁失败，下一步会迁移到 GDELT 的批量数据文件（GKG）而不是继续调整这个 API 方案。

## 已知问题（实测结果，2026-09-04）

部署到 GitHub Actions 后跑了两次真实的数据抓取，结果：

| 次数 | 退避策略 | 成功 / 总数 | 耗时 |
|---|---|---|---|
| 第 1 次 | 15 秒间隔，1 次重试 | 1 / 7 | 7 秒（脚本几乎没跑，另有上传不完整的问题，已修复） |
| 第 2 次 | 45 秒+抖动间隔，最多 3 次尝试，按 429 的 `Retry-After` 智能退避 | 2 / 7 | 24 分 26 秒 |

失败原因几乎全是 `HTTP 429: Too Many Requests`，偶尔混一个 SSL 握手超时。**结论：GDELT DOC 2.0 API 在 GitHub Actions 的共享 IP 环境下不适合长期稳定使用**，退避策略已经调得比较讲道理了，成功率依然只有 15-30%，这不是"重试次数不够"能解决的。

**下一步方向（尚未实施）**：迁移到 GDELT 的批量数据文件（GKG，Global Knowledge Graph），这是静态文件下载（每 15 分钟发布一次），不经过会被限流的查询接口。已确认的技术细节：
- GKG 2.1 格式，`V1THEMES` 字段固定在每行第 8 列（已核实官方 Codebook：http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf）
- 已核实"通胀"对应真实存在的主题代码 `ECON_INFLATION`
- 其余 6 个主题（Economic / Geopolitics / Technology / Energy / War & Conflict / AI）对应的官方主题代码**还没有逐一核实**，在核实完之前不会写死猜测的代码，避免用错误代码产出「看起来正常但其实是错的」数据

在决定继续深入做 GKG 迁移、还是先用"每天轮换只抓 2-3 个主题"的折中方案降低失败率之前，`scripts/update_gdelt.py` 暂时保持当前这版（45 秒间隔 + 429 感知退避）。

## 后续规划（尚未开始）

- V0.3：建立社会趋势指数
- V0.4：加入 AI 分析
- V0.5：建立预测数据库
- V0.6 及以后：自动验证、历史回测、多模型比较

每个版本都会在通过验收后才进入下一阶段。

## 免责声明

本项目所有预测均为概率估计，不构成投资、政治或其他任何决策建议。历史预测记录一旦生成不会被事后修改。
