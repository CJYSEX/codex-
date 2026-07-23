---
name: create-edit-documents
description: 创建、读取、编辑、审阅和验证 DOCX/Word 文档。用户要求制作报告、方案、备忘录、合同草稿、修改已有 Word 文件、提取文档结构、检查排版或保留模板格式时使用。
---

# CJYSA 文档

## 工作原则

- 先判断任务是只读、创建还是编辑；只读任务不要改写文件。
- 创建新文档时优先使用 Codex 工作区依赖加载器返回的 Python 和 `python-docx`。
- 编辑已有文档时保留原文件，输出新副本；除非用户明确要求重排，只做局部修改。
- 任何交付都先做结构检查；具备 DOCX 渲染能力时，再逐页检查预览。
- 不复制或依赖 OpenAI 官方 Documents 插件中的脚本、模板或素材。

## 标准流程

1. 调用工作区依赖加载器，使用其返回的 Python 路径，不猜测运行时位置。
2. 对输入文档运行：

```powershell
& "<bundled-python>" "<skill-dir>\scripts\docx_tool.py" inspect "<input.docx>"
```

3. 创建文档时，先确定页面尺寸、边距、标题层级、字体、段落间距和表格样式，再编写任务专用 builder。简单文本可直接使用：

```powershell
& "<bundled-python>" "<skill-dir>\scripts\docx_tool.py" create `
  --input "<content.txt>" --output "<output.docx>" --title "标题"
```

4. 简单文字替换可使用 `replace`；涉及跨段、批注、修订、目录、页眉页脚或复杂表格时，编写任务专用 OOXML/python-docx 脚本并保留备份。
5. 再次运行 `inspect`，确认文档可打开、段落和表格数量合理、无意外空白内容。
6. 若环境提供 Word、WPS、LibreOffice 或其他可靠渲染方式，导出 PDF/PNG 并逐页查看；不可渲染时明确说明只完成了结构验证。

## 编辑约束

- 不覆盖用户原文件，除非用户明确授权。
- 尽量保留段落样式、分节、页眉页脚、图片关系和表格宽度。
- 不把所有内容重新写成一个段落来完成局部修改。
- 涉及敏感信息时，不在日志中输出全文；只输出统计或脱敏摘要。
- 交付前按 [quality-checks.md](references/quality-checks.md) 检查。

## 输出

最终只链接用户要求的 DOCX，不主动附带内部检查日志或预览文件。
