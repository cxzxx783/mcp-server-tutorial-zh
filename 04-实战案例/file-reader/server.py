# -*- coding: utf-8 -*-
"""文件读取 MCP Server：让 AI 读取本地文件内容（TXT/CSV/MD 等纯文本格式）"""
import sys
import os
from mcp.server.fastmcp import FastMCP

if sys.platform == "win32":
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

mcp = FastMCP("文件读取器")

# 限制读取范围，防止 AI 乱翻系统文件
ALLOWED_EXTENSIONS = {".txt", ".csv", ".md", ".json", ".xml", ".yaml", ".yml", ".log", ".ini", ".cfg"}
MAX_FILE_SIZE = 1024 * 1024  # 1MB


@mcp.tool()
def read_text_file(file_path: str) -> str:
    """读取本地文本文件的内容。支持格式: txt/csv/md/json/xml/yaml/log/ini/cfg。文件大小限制 1MB。
    file_path=文件的完整路径(如 D:/projects/data.txt 或 C:/Users/name/note.md)"""
    # 统一用正斜杠，避免 Windows 反斜杠问题
    file_path = file_path.replace("\\", "/")

    if not os.path.exists(file_path):
        return f"文件不存在: {file_path}"

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return f"不支持的文件格式: {ext}（支持 {', '.join(sorted(ALLOWED_EXTENSIONS))}）"

    size = os.path.getsize(file_path)
    if size > MAX_FILE_SIZE:
        return f"文件过大 ({size / 1024 / 1024:.1f}MB)，超过 1MB 限制"

    try:
        # 先试 UTF-8，不行就 GBK
        for enc in ["utf-8", "gbk", "gb2312"]:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        else:
            return f"文件无法用 UTF-8/GBK 解码，请确认编码"

        # 超长时截断，避免 AI 处理不了
        if len(content) > 20000:
            content = content[:20000] + f"\n\n...（文件过长，仅显示前 20000 字符，共 {len(content)} 字符）"
        return content
    except PermissionError:
        return f"无权限读取文件: {file_path}"
    except Exception as e:
        return f"读取失败: {e}"


@mcp.tool()
def list_files(directory: str, pattern: str = "") -> str:
    """列出目录下的文本文件。directory=目录路径; pattern=可选筛选关键词(如 \"log\" 只显示含 log 的文件)"""
    directory = directory.replace("\\", "/")

    if not os.path.isdir(directory):
        return f"目录不存在: {directory}"

    try:
        files = []
        for f in os.listdir(directory):
            fpath = os.path.join(directory, f)
            if os.path.isfile(fpath):
                ext = os.path.splitext(f)[1].lower()
                if ext in ALLOWED_EXTENSIONS:
                    if pattern and pattern.lower() not in f.lower():
                        continue
                    size = os.path.getsize(fpath)
                    files.append(f"{f}  ({size / 1024:.1f}KB)")

        if not files:
            return f"目录下没有可读的文本文件（支持：{', '.join(sorted(ALLOWED_EXTENSIONS))}）"
        return "可读取的文件：\n" + "\n".join(sorted(files))
    except PermissionError:
        return f"无权限访问目录: {directory}"


if __name__ == "__main__":
    mcp.run(transport="stdio")