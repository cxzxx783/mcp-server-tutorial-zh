# 🌐 百度搜索 MCP Server

让 AI **实时搜索中文网页**，国内直连，不需要代理。

## 前置条件

去[百度千帆平台](https://console.bce.baidu.com/qianfan/ais/console/onlineService)申请 API Key（免费额度 1500 次/月）。

申请后将 `server.py` 里的 `API_KEY` 替换成你自己的。

## 功能

- `baidu_web_search` — 搜索中文网页
  - 支持限定站点（如只搜百度百科）
  - 支持按时间过滤（周/月/半年/年）
  - 返回标题+链接+摘要+日期

## 快速跑

```bash
pip install mcp
# 先改 server.py 里的 API_KEY
python server.py
```

## 设计要点

这个 Server 展示了几个 MCP 开发技巧：

1. **参数校验**：`max(1, min(top_k, 50))` 防止 AI 传离谱值
2. **友好的错误提示**：API Key 无效时直接告诉用户去申请，而不是抛一堆技术错误
3. **结构化输出**：返回纯文本+换行排版，AI 读起来舒服
4. **时间过滤**：用人类可读的 `week/month` 而不是时间戳——AI 更容易理解