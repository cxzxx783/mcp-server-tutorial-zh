# 06 - 常见坑与技巧

> 实战中踩过的坑，写在这里让你绕过去。

---

## 🪟 Windows 路径坑

**现象**：配置文件里的 `D:\Python313\python.exe` 导致客户端启动失败

**原因**：反斜杠 `\` 在 JSON 里是转义字符——`\P` → 转义成 `P`（碰巧能用），但 `\m`、`\s` 等直接炸

**解决**：**永远用正斜杠** `/`

```json
// ✅ 正确
"command": "D:/Python313/python.exe"

// ❌ 错误
"command": "D:\\Python313\\python.exe"
```

---

## 🌐 控制台输出乱码

**现象**：MCP Server 返回的中文是乱码

**原因**：Windows 控制台默认 GBK 编码，Python 默认 UTF-8，不统一就乱

**解决**：每个 Server 开头加这段代码：

```python
import sys
if sys.platform == "win32":
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
```

---

## 📂 读本地文件编码问题

**现象**：AI 读中文 .txt 文件时出现乱码

**原因**：Windows 中文文件常用 GBK/GB2312 编码，直接 UTF-8 读会乱

**解决**：尝试多种编码

```python
for enc in ["utf-8", "gbk", "gb2312"]:
    try:
        with open(path, "r", encoding=enc) as f:
            return f.read()
    except UnicodeDecodeError:
        continue
return "无法解码文件"
```

---

## 🐌 Server 启动慢 / AI 响应卡

**原因**：每次调用都要启动 Python 进程，如果依赖多（PIL/numpy 等）启动就慢

**解决**：
- 用轻量依赖：能用 `urllib` 就别装 `requests`
- 把能复用的对象（如 API 客户端）放在模块级别，别放函数里
- 如果 Server 需要重依赖，接受第一次调用会慢的事实（约 2-5 秒）

---

## 🔍 调试技巧

### 1. 用 MCP Inspector

最好用的调试工具，能直接看到 Server 暴露了什么、调用结果、错误：

```bash
mcp dev your_server.py
```

### 2. 模拟调用

```
{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "hello", "arguments": {"name": "测试"}}, "id": 1}
```

### 3. 测试 Server 是否活着

```python
# test_server.py
import subprocess, json

proc = subprocess.Popen(
    ["python", "your_server.py"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
)
req = json.dumps({"jsonrpc": "2.0", "method": "tools/list", "id": 1})
out, _ = proc.communicate(input=req.encode(), timeout=10)
print(json.loads(out))
```

---

## 💡 开发习惯

| 习惯 | 原因 |
|------|------|
| **一个 Server 只做一件事** | AI 容易理解，调试简单，复用性强 |
| **参数名用英文** | MCP 协议对中文参数名支持不稳定 |
| **返回值简洁 + 换行排版** | AI 读纯文本段落的准确率最高 |
| **工具描述写清楚** | AI 靠描述决定调不调——别偷懒 |
| **每次改完重启客户端** | MCP Server 配置只在启动时读取一次 |
| **先加 `--help` 注释** | 以后自己回来看也能秒懂 |

---

## ❓ 常见报错

| 错误 | 原因 | 修复 |
|------|------|------|
| `ModuleNotFoundError: No module named 'mcp'` | 没装 MCP SDK | `pip install mcp` |
| `Connection refused` | SSE 模式端口被占用 | 换端口或检查是否已有实例在跑 |
| `Tool not found` | 调了不存在的工具名 | 检查 `@mcp.tool()` 函数名是否写对了 |
| `Invalid params` | 传了不支持的参数 | 检查类型注解和参数名是否匹配 |
| `[MCP] Error: -32000` | Server 内部报错 | 看控制台输出定位具体异常 |