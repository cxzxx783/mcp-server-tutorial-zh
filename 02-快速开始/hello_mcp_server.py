# -*- coding: utf-8 -*-
"""第一个 MCP Server —— 你好世界！"""
import sys
from mcp.server.fastmcp import FastMCP

# Windows 下确保 stdio 用 UTF-8，不乱码
if sys.platform == "win32":
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 创建 MCP Server（名字会显示在 AI 客户端的工具列表里）
mcp = FastMCP("你好世界")


@mcp.tool()
def hello(name: str) -> str:
    """跟用户打个招呼"""
    return f"你好, {name}! 欢迎来到 MCP 世界 🎉"


@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个数的和"""
    return a + b


@mcp.tool()
def get_weather(city: str) -> str:
    """查询指定城市的天气（示例，返回模拟数据）"""
    data = {
        "北京": "晴, 28°C",
        "上海": "多云, 32°C",
        "广州": "雷阵雨, 30°C",
        "深圳": "阴, 29°C",
        "苏州": "晴转多云, 26°C",
    }
    return data.get(city, f"暂无 {city} 的天气数据")


if __name__ == "__main__":
    mcp.run(transport="stdio")