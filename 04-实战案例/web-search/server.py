# -*- coding: utf-8 -*-
"""百度搜索 MCP Server：让 AI 实时搜索中文网页（国内直连，免代理）"""
import sys
import json
import urllib.request
from mcp.server.fastmcp import FastMCP

if sys.platform == "win32":
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ---------- 配置 ----------
# ⚠️ 你需要去百度千帆平台申请自己的 API key
# 申请地址：https://console.bce.baidu.com/qianfan/ais/console/onlineService
# 方式1：设置环境变量 BAIDU_API_KEY
# 方式2：直接修改下面的 API_KEY
API_URL = "https://qianfan.baidubce.com/v2/ai_search/web_search"
API_KEY = __import__("os").environ.get("BAIDU_API_KEY", "你的百度千帆 API Key")

# 时间过滤参数映射
_RECENCY_MAP = {
    "week": "now-1w/d",
    "month": "now-1M/d",
    "semiyear": "now-6M/d",
    "year": "now-1y/d",
}

mcp = FastMCP("百度搜索")


def _search(query, top_k=10, site="", recency=""):
    """调用百度千帆 ai_search API"""
    body = {
        "messages": [{"content": query, "role": "user"}],
        "search_source": "baidu_search_v2",
        "resource_type_filter": [{"type": "web", "top_k": top_k}],
    }
    # 过滤条件
    filt = {}
    if site:
        filt["match"] = {"site": [site]}
    if recency in _RECENCY_MAP:
        filt["page_time"] = {"gte": _RECENCY_MAP[recency]}
    if filt:
        body["search_filter"] = filt

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode("utf-8", errors="replace"))
    return data.get("references", []) or []


@mcp.tool()
def baidu_web_search(query: str, top_k: int = 10, site: str = "", recency: str = "") -> str:
    """搜索中文网页（百度搜索引擎，国内直连）。
    query=搜索关键词;
    top_k=返回结果数(1-50，默认10);
    site=限定站点(如 baike.baidu.com，空=不限);
    recency=时间范围(week/week/month/semiyear/year，空=不限)"""
    try:
        refs = _search(query, max(1, min(top_k, 50)), site, recency)
        if not refs:
            return "暂无搜索结果"

        out = []
        for r in refs:
            title = r.get("title", "无标题")
            url = r.get("url", "")
            date = r.get("date", "")[:10]
            snippet = (r.get("snippet") or "").strip()
            line = f"【{title}】"
            if date:
                line += f" [{date}]"
            line += f"\n  {url}"
            if snippet:
                line += f"\n  {snippet}"
            out.append(line)
        return "\n\n".join(out)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return "API Key 无效或未设置，请到百度千帆平台申请"
        return f"搜索 API 请求失败 (HTTP {e.code})"
    except Exception as e:
        return f"搜索失败: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")