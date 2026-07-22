# CJYSA Codex Free Marketplace

CJYSA 面向 Codex 用户提供的免费插件市场。

## 安装

在 Codex 中添加以下市场来源：

```text
CJYSEX/codex-
```

添加后安装 `cjysa-relay-basic`。

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

## 安全

本仓库不包含任何客户 API Key、服务器密码或中转上游凭据。提交问题或诊断日志前，请先删除授权头、令牌、Cookie 和签名链接。

## 许可证

Apache-2.0
