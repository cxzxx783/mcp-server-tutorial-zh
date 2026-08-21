# 📂 文件读取器

让 AI **读取你电脑上的本地文件**——看日志、读配置、查笔记，AI 像你一样能翻文件。

## 功能

- `read_text_file` — 读取文件内容（自动尝试 UTF-8 → GBK 解码）
- `list_files` — 列出目录下可读的文件

## 快速跑

```bash
pip install mcp
python server.py
```

## 安全限制

- 只支持纯文本格式（txt/csv/md/json/xml/yaml/log/ini/cfg）
- 最大只读 1MB，防止 AI 读大文件烧 token
- 不能改文件、不能删文件——只读

## 在你自己的 Server 里怎么用？

这段**编码自动尝试逻辑**是所有 Windows MCP Server 必备的：

```python
for enc in ["utf-8", "gbk", "gb2312"]:
    try:
        with open(file_path, "r", encoding=enc) as f:
            content = f.read()
        break
    except UnicodeDecodeError:
        continue
```

Windows 中文文件很可能是 GBK 编码，直接 UTF-8 读会乱码，这段代码帮你兜底。