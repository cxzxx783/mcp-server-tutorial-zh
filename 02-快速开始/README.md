# 02 - 快速开始

> 从装环境到跑通第一个 MCP Server，**5 分钟搞定**。

---

## 1️⃣ 安装 Python 和依赖

```bash
# 需要 Python 3.10+（推荐 3.12/3.13）
python --version

# 装 MCP SDK
pip install "mcp[cli]"
```

验证安装：`mcp --version`

## 2️⃣ 写第一个 Server

创建 `hello_mcp_server.py`：

```python
# hello_mcp_server.py
from mcp.server.fastmcp import FastMCP

# 创建 MCP Server，起个名
mcp = FastMCP("你好世界")

@mcp.tool()
def hello(name: str) -> str:
    """跟用户打个招呼"""
    return f"你好, {name}! 欢迎来到 MCP 世界 🎉"

@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个数的和"""
    return a + b

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## 3️⃣ 用 Inspector 调试（推荐）

MCP SDK 自带图形化调试工具：

```bash
mcp dev hello_mcp_server.py
```

浏览器会自动打开一个调试面板，你可以：
- 看到 Server 暴露了哪些 Tool
- 手动调用 Tool 看返回结果
- 检查有没有报错

## 4️⃣ 用命令行调试

不想开浏览器？直接用 mcp CLI 调用：

```bash
# 列出所有工具
mcp run hello_mcp_server.py --list-tools

# 测一个工具
echo '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "hello", "arguments": {"name": "小明"}}, "id": 1}' | mcp run hello_mcp_server.py
```

## 5️⃣ 配到客户端

跑通后就能接到 AI 客户端里用了——详见 [05 - 注册与配置](../05-注册与配置/README.md)。

## 代码文件

- [`hello_mcp_server.py`](./hello_mcp_server.py) — 完整可运行的示例
- [`requirements.txt`](./requirements.txt) — 依赖列表

## 排错

| 问题 | 解决办法 |
|------|----------|
| `ModuleNotFoundError: No module named 'mcp'` | `pip install "mcp[cli]"` |
| Windows 控制台乱码 | 在代码开头加 `sys.stdin.reconfigure(encoding="utf-8")` |
| `mcp` 命令找不到 | 检查 Python Scripts 目录是否在 PATH 里 |