# CJYSA Codex Free Marketplace

CJYSA 面向 Codex 用户提供的免费插件市场。

## 安装

在 Codex 中添加以下市场来源：

```text
https://git.cjysa.top/CJYSA/codex-free-market.git
```

Git 引用填写 `main`，稀疏路径留空。添加后按需安装插件。

## 当前插件

### cjysa-relay-basic

提供基础的 Codex 中转连接与兼容性诊断，包括：

- 模型列表与认证检查
- Responses API 检查
- SSE 流式输出检查
- 首字延迟分层诊断
- Web Search、图片生成和函数调用能力检查

### git-tools

提供原创的 Git、Gitea 和 GitHub 仓库管理工作流，包括：

- 仓库状态与远程连接诊断
- 安全提交、推送和发布
- Gitea 主仓库与 GitHub 镜像同步
- SSH、HTTPS 和权限故障排查
- 凭据脱敏与本地修改保护

### cjysa-documents

原创中文 Word 工作流，支持：

- DOCX 创建、读取、局部编辑和结构检查
- 标题、段落、表格、分节和图片关系概览
- 简单文本生成 DOCX 和安全替换
- 可用时执行逐页渲染检查

### cjysa-pdf

原创中文 PDF 工作流，支持：

- PDF 信息与文本提取
- 合并、拆分、旋转和基础文本 PDF 生成
- Poppler 页面渲染与视觉检查
- 加密文件和扫描件的安全边界

### cjysa-spreadsheets

原创中文表格工作流，支持：

- XLSX、CSV、TSV 创建、读取和编辑
- CSV/TSV 转带基础格式的 XLSX
- 工作表结构、公式数量和常见错误扫描
- 使用可审计公式并保留现有格式

### cjysa-presentations

原创中文演示文稿工作流，支持：

- PPTX 创建、读取、编辑和模板跟随
- 幻灯片结构、标题、图片和文字概览
- 空白页、越界对象和过小字号检查
- 逐页预览、叙事和版式交付检查

## 安全

本仓库不包含任何客户 API Key、服务器密码或中转上游凭据。提交问题或诊断日志前，请先删除授权头、令牌、Cookie 和签名链接。

## 许可证

Apache-2.0
