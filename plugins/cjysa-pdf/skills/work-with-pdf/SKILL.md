---
name: work-with-pdf
description: 读取、提取、生成、合并、拆分、旋转和验证 PDF 文件。用户要求总结 PDF、提取页面文本、重排页面、制作 PDF 报告或检查 PDF 排版时使用。
---

# CJYSA PDF

## 标准流程

1. 调用工作区依赖加载器，优先使用返回的 Python、Poppler 和相关包。
2. 先运行 `info` 获取页数、页面尺寸、元数据和加密状态。
3. 读取内容时使用 `extract`；遇到扫描件且无文本层时，再选择 OCR 工具，不把空文本误判为无内容。
4. 修改文件时输出新副本，使用 `merge`、`split` 或 `rotate`。
5. 创建 PDF 时优先使用任务专用 ReportLab builder；简单纯文本可用 `create-text`。
6. 用 `pdftoppm` 或等价工具渲染所有页面并逐页检查；至少确认无裁切、重叠、黑块、乱码和空白页。

## 命令

```powershell
& "<bundled-python>" "<skill-dir>\scripts\pdf_tool.py" info "<input.pdf>"
& "<bundled-python>" "<skill-dir>\scripts\pdf_tool.py" extract "<input.pdf>" --output "<text.txt>"
& "<bundled-python>" "<skill-dir>\scripts\pdf_tool.py" merge "<a.pdf>" "<b.pdf>" --output "<merged.pdf>"
& "<bundled-python>" "<skill-dir>\scripts\pdf_tool.py" split "<input.pdf>" --pages "1-3,7" --output "<part.pdf>"
& "<bundled-python>" "<skill-dir>\scripts\pdf_tool.py" rotate "<input.pdf>" --degrees 90 --output "<rotated.pdf>"
```

## 约束

- 不覆盖原文件，除非用户明确授权。
- 对加密 PDF 不尝试绕过密码。
- 文本提取不能替代视觉检查；表格、图形和阅读顺序必须结合页面图像判断。
- 不复制或依赖 OpenAI 官方 PDF 插件中的素材或实现。
- 交付前按 [quality-checks.md](references/quality-checks.md) 检查。

## 输出

最终只链接用户要求的 PDF；除非用户要求，不提供中间拆分页、渲染图和日志。
