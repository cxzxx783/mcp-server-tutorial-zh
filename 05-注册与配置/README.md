# 05 - 注册与配置

> Server 写好了，怎么让 AI 用上它？本章讲**主流客户端怎么接 MCP Server**。

---

## 🔧 通用流程

所有客户端配置 MCP 的流程都一样：

1. 写好 Server 脚本（`server.py`）
2. 告诉客户端：启动这个 Server 的**命令**是什么
3. 重启客户端 → 就能用了

配置本质就两样东西：

| 字段 | 含义 | 示例 |
|------|------|------|
| `command` | 启动 Server 的可执行文件 | `D:/Python313/python.exe` |
| `args` | 传给可执行文件的参数 | `["D:/projects/server.py"]` |

---

## 🌀 Claude Desktop

**配置文件位置：**
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

配置完**重启 Claude Desktop**，对话中 AI 就会自动调用你的 Server。

---

## 💻 VS Code + Copilot / Cline

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

适合在 VS Code 里用 **Cline** 或 **Copilot Agent Mode** 时调用自定义工具。

---

## ✨ Cursor

Cursor 支持 MCP，配置在项目根目录的 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "文件读取器": {
      "type": "stdio",
      "command": "D:/Python313/python.exe",
      "args": ["D:/projects/file-reader/server.py"]
    }
  }
}
```

添加后重启 Cursor，在 Composer / Chat 中按 `@MCP` 就能看到你的工具。

---

## 🌊 Windsurf

Windsurf 同样支持 MCP，配置在项目根目录的 `.windsurf/mcp_config.json`：

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

## 🖥️ Cherry Studio（额外参考）

Cherry Studio 是国内一款支持多模型的 AI 桌面客户端，对 MCP 的支持比较完善。

### 方法一：界面配置

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

---

## ⚠️ Windows 路径坑（所有客户端通用）

**永远用正斜杠 `/`，不要用反斜杠 `\`！**

反斜杠在 JSON 里是转义字符——`\P` 碰巧能用，但 `\m`、`\s` 等直接炸。

```json
// ✅ 正确（所有客户端通用）
"command": "D:/Python313/python.exe"

// ❌ 错误
"command": "D:\\Python313\\python.exe"
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

需要 `pip install mcp`。

---

## 🤔 不知道选哪个？

| 如果你用 | 推荐方式 |
|----------|----------|
| Claude Desktop | 改 `claude_desktop_config.json` |
| VS Code + Cline/Copilot | 项目下 `.vscode/mcp.json` |
| Cursor | 项目下 `.cursor/mcp.json` |
| Windsurf | 项目下 `.windsurf/mcp_config.json` |
| Cherry Studio | 设置界面添加 |
| 自己写 Python 程序 | ClientSession API |
| 不确定 | 先用 `mcp dev your_server.py` 调试 |