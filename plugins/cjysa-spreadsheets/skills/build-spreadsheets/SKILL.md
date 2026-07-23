---
name: build-spreadsheets
description: 创建、读取、编辑、分析和验证 XLSX、CSV、TSV 表格文件。用户要求制作 Excel、整理 CSV、加入公式和图表、分析工作簿、修复公式或保留模板格式时使用；不用于控制正在 Excel 中打开的实时工作簿。
---

# CJYSA 表格

## 路由

- 对 CSV/TSV 做纯数据清洗时可直接用 Python。
- 对 XLSX 创建和编辑，优先使用工作区依赖加载器提供的 `@oai/artifact-tool`；不可用时使用其 Python 和 `openpyxl`。
- 用户要求控制当前打开的 Excel 窗口时，不使用本技能；需要 Excel/WPS 实时控制能力。

## 标准流程

1. 先运行结构检查：

```powershell
& "<bundled-python>" "<skill-dir>\scripts\xlsx_tool.py" inspect "<input.xlsx>"
```

2. 编辑已有工作簿前检查相关单元格的值、公式、数字格式、合并区域、冻结窗格、条件格式和图表。
3. 创建工作簿时把输入、计算和输出分区；派生数据使用可审计公式，不把结果硬编码。
4. 简单 CSV 转 XLSX 可运行：

```powershell
& "<bundled-python>" "<skill-dir>\scripts\xlsx_tool.py" csv-to-xlsx `
  "<input.csv>" --output "<output.xlsx>"
```

5. 运行 `formula-scan` 检查明显错误，再读取关键范围核对结果。
6. 使用 artifact-tool、Excel、WPS 或可靠渲染器查看所有工作表；不可渲染时明确只完成结构和公式检查。

## 表格规则

- 数字、日期、百分比和货币使用真实类型，不写成带符号的文本。
- 公式引用保持一致，跨表引用对含空格的工作表名加单引号。
- 编辑已有表格时做最小改动，不对整张表盲目自动宽度或重设样式。
- 重要假设集中放置并标注；复杂公式拆成辅助行/列。
- 不复制 OpenAI 官方 Spreadsheets 插件、内部 API 文档或 App 集成。
- 交付前按 [quality-checks.md](references/quality-checks.md) 检查。

## 输出

最终只链接用户要求的 XLSX/CSV/TSV，不主动附带 builder、预览图或检查日志。
