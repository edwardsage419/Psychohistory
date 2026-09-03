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

## 当前状态：V0.1

这是项目的第一个版本，只完成了页面结构和视觉框架。

**⚠️ 页面上的所有数据目前都是 Mock Data（占位数据），不代表任何真实观测结果。** 数据来源、趋势、预测和历史记录均为示例，用于验证 Dashboard 的布局和显示是否正常。

### 文件结构

```
index.html   页面结构
style.css    样式（深色数据仪表盘风格）
app.js       Mock 数据 + 渲染逻辑
README.md    本文件
```

### 页面模块

- **Global State** — 七个核心社会指标（Global Risk / Economic Pressure / Geopolitical Risk / Technology Momentum / Market Stress / Energy Stress / Social Attention）
- **Today's Trends** — 当天趋势变化
- **Predictions** — 当前有效的概率预测
- **Prediction History** — 历史预测与验证结果
- **Model Performance** — 模型评分（Accuracy / Brier Score / Calibration / Log Loss）
- **Data Sources** — 数据来源清单及接入状态

### 技术说明

- 纯 HTML + CSS + JavaScript，无任何外部依赖、无框架、无构建步骤。
- 不接入任何 API，不使用任何 API Key。
- 通过 GitHub Pages 直接部署。

## 后续规划（尚未开始）

- V0.2：接入 GDELT 真实新闻数据
- V0.3：建立社会趋势指数
- V0.4：加入 AI 分析
- V0.5：建立预测数据库
- V0.6 及以后：自动验证、历史回测、多模型比较

每个版本都会在通过验收后才进入下一阶段。

## 免责声明

本项目所有预测均为概率估计，不构成投资、政治或其他任何决策建议。历史预测记录一旦生成不会被事后修改。
