# 05 - 注册与配置

> Server 写好了，怎么让 AI 用上它？本章讲**各种客户端怎么接 MCP Server**。

---

## 🔧 通用流程

所有客户端配置 MCP 的流程都一样：

1. 写好 Server 脚本（`server.py`）
2. 告诉客户端：启动这个 Server 的**命令**是什么
3. 重启客户端 → 就能用了

命令格式一般长这样：

```json
{
  "python": "D:/路径/python.exe",
  "args": ["D:/路径/server.py"]
}
```

---

## 🖥️ Cherry Studio（推荐）

Cherry Studio 对 MCP 支持最好，配置方式：

### 方法一：界面配置 ✅ 推荐

1. 设置 → MCP 服务 → 添加
2. 名称：随便写（如"文件读取器"）
3. 类型：stdio
4. 命令：`D:/你的Python路径/python.exe`
5. 参数：`["D:/你的项目路径/server.py"]`
6. 保存 → 重启 Cherry Studio

### 方法二：`.mcp.json` 配置文件

项目根目录放 `.mcp.json`：

```json
{
  "mcpServers": {
    "文件读取器": {
      "command": "D:/你的Python路径/python.exe",
      "args": ["D:/你的项目路径/server.py"]
    }
  }
}
```

### ⚠️ Windows 路径注意

**一定要用正斜杠 `/`**！反斜杠 `\` 在 JSON 里是转义字符，会写坏配置文件：

```json
// ✅ 正确
"command": "D:/Python313/python.exe"

// ❌ 错误——Cherry Studio 启动会崩溃
"command": "D:\\Python313\\python.exe"
```

---

## 🌀 Claude Desktop

Claude Desktop 的配置文件在：

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "文件读取器": {
      "command": "D:/Python313/python.exe",
      "args": ["D:/projects/file-reader/server.py"]
    }
  }
}
```

---

## ⚙️ VS Code + Copilot

VS Code 的 MCP 配置在项目根目录的 `.vscode/mcp.json`：

```json
{
  "servers": {
    "文件读取器": {
      "type": "stdio",
      "command": "D:/Python313/python.exe",
      "args": ["D:/projects/file-reader/server.py"]
    }
  }
}
```

---

## 🐍 自己写代码调用

想在自己的 Python 程序里用 MCP Server？

```python
from mcp import ClientSession, StdioServerParameters

# 启动 Server 进程
params = StdioServerParameters(
    command="D:/Python313/python.exe",
    args=["D:/projects/file-reader/server.py"]
)

# 创建会话
async with ClientSession(params) as session:
    # 列出可用的工具
    tools = await session.list_tools()
    for tool in tools:
        print(f"  🛠️ {tool.name}: {tool.description}")

    # 调用工具
    result = await session.call_tool("read_text_file", {
        "file_path": "D:/test.txt"
    })
    print(result.content[0].text)
```

---

## 📝 注册信息存放位置（进阶）

如果你用的是 Cherry Studio V2，MCP 配置存在**数据库**里，不是纯配置文件：

- 数据库：`Data/cherrystudio.sqlite`
- 表名：`mcp_server`
- 字段：`id` / `name` / `type` / `command` / `args`（JSON 字符串）/ `is_active`

改配置推荐用界面操作，不推荐直接改数据库。