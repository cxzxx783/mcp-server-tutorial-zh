# 03 - 核心概念

MCP Server 有三大能力：**Tool、Resource、Prompt**。新手先掌握 Tool 就够了（90% 场景用 Tool），另两个懂概念就行。

---

## 🛠️ Tool（工具）—— 重点掌握

**Tool 就是 AI 能调用的函数。** 你写好，AI 觉得需要时自己决定调不调。

```python
@mcp.tool()
def search_news(keyword: str, top_k: int = 5) -> str:
    \"\"\"搜索最新新闻，keyword=关键词，top_k=返回条数\"\"\"
    # 函数体：查数据库/调API/读文件……
    return result
```

**要点：**
- 函数名 = 工具名（AI 通过名字决定调哪个）
- 参数要有**类型注解**（`str`、`int`、`list` 等），AI 靠它知道传什么
- 函数文档字符串（`"""..."""`）就是 AI 看到的**工具描述**——写清什么时候用、参数含义
- 返回值必须是字符串（AI 能读的格式）

> 💡 **命名技巧**：函数名写清楚用途，比如 `search_news` 而不是 `sn`——AI 猜名字的能力没那么强。

---

## 📄 Resource（资源）—— 了解即可

**Resource 让 AI 能读取数据**（文件、配置、日志等），类似 REST 里的 GET 请求。

```python
@mcp.resource(\"config://app/settings\")
def get_settings() -> str:
    \"\"\"读取应用配置\"\"\"
    with open(\"config.json\", encoding=\"utf-8\") as f:
        return f.read()
```

Resource 用 URI 寻址（`file://`、`db://`、`config://` 等），适合让 AI 主动读取信息。

---

## 💬 Prompt（提示模板）—— 了解即可

**Prompt 是预设指令**，让 AI 快速进入特定工作模式。

```python
@mcp.prompt()
def review_code() -> str:
    return \"请审查以下代码：格式规范、性能问题、安全隐患，逐条列出。\"
```

适合：代码审查、文档翻译、日志分析等固定场景。

---

## 怎么选？

| 场景 | 用哪个 |
|------|--------|
| AI 需要主动执行操作 | **Tool** ✅ |
| AI 需要读取固定数据 | Resource |
| 用户需要一个固定对话模板 | Prompt |
| 不确定 | **Tool** ✅（最通用） |

---

## 关键原则

1. **一个 Server 只做一件事**，做精不做杂
2. 每个 Tool 的**描述要写清楚**——AI 不会猜，全靠描述决定调不调
3. 参数**宁少勿多**，3-4 个以内最好（AI 容易搞混太多参数）
4. 返回**纯文本 + 换行排版**，不要 JSON（AI 读纯文本最舒服）