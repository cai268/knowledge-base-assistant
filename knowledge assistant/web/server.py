# -*- coding: utf-8 -*-
"""网页版学习知识助手服务端。

仅使用 Python 标准库，复用 src/agent 中已构建好的 agent：
- GET  /api/health      健康检查
- POST /api/chat        发送消息，body: {"message": "...", "thread_id": "..."}
- POST /api/reset       清空指定会话记忆，body: {"thread_id": "..."}
其余路径从 web/static/ 返回静态文件。
"""

import contextlib
import io
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# config.py 导入时会打印 DEEPSEEK_API_KEY，屏蔽该输出避免密钥泄漏到日志
with contextlib.redirect_stdout(io.StringIO()):
    from src.agent import agent  # noqa: F401  构建好的 agent

from src.memory import clean_thread  # 复用 CLI 版会话清理函数
from langchain.messages import HumanMessage

STATIC_DIR = Path(__file__).resolve().parent / "static"

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
}


def run_agent(message: str, thread_id: str) -> str:
    """调用 langgraph agent；thread_id 让每个网页会话拥有独立记忆。"""
    response = agent.invoke(
        {"messages": [HumanMessage(message)]},
        {"configurable": {"thread_id": thread_id}},
    )
    return response["messages"][-1].content


class Handler(BaseHTTPRequestHandler):
    server_version = "KnowledgeAssistantWeb/1.0"
    protocol_version = "HTTP/1.1"

    # ---------- 工具方法 ----------

    def _send(self, status: int, body: bytes, content_type: str):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8")

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length else b""
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def _get_thread_id(self, data: dict) -> str:
        tid = str(data.get("thread_id") or "web_default")
        # 只保留常规字符，避免 thread_id 干扰 SQL 清理逻辑
        safe = "".join(ch for ch in tid if ch.isalnum() or ch in "-_")
        return (safe or "web_default")[:64]

    # ---------- HTTP 请求 ----------

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            self._send_json(200, {"status": "ok"})
            return
        self._serve_static(path)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            data = self._read_json()
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "请求体不是合法的 JSON"})
            return

        if path == "/api/chat":
            message = str(data.get("message", "")).strip()
            if not message:
                self._send_json(400, {"error": "消息不能为空"})
                return
            thread_id = self._get_thread_id(data)
            try:
                reply = run_agent(message, thread_id)
            except Exception as exc:  # noqa: BLE001 错误详情返回给前端展示
                self._send_json(500, {"error": f"AI 回复失败：{exc}"})
                return
            self._send_json(200, {"reply": reply})
            return

        if path == "/api/reset":
            thread_id = self._get_thread_id(data)
            try:
                clean_thread(thread_id)
            except Exception as exc:  # noqa: BLE001
                self._send_json(500, {"error": f"清理会话失败：{exc}"})
                return
            self._send_json(200, {"ok": True, "thread_id": thread_id})
            return

        self._send_json(404, {"error": "接口不存在"})

    # ---------- 静态文件 ----------

    def _serve_static(self, url_path: str):
        rel = "index.html" if url_path in ("", "/") else url_path.lstrip("/")
        target = (STATIC_DIR / rel).resolve()
        try:
            is_inside = target.is_relative_to(STATIC_DIR.resolve())
        except ValueError:
            is_inside = False
        if not is_inside or not target.is_file():
            self._send(404, b"404 Not Found", "text/plain; charset=utf-8")
            return
        ext = target.suffix.lower()
        content_type = MIME_TYPES.get(ext, "application/octet-stream")
        body = target.read_bytes()
        if ext in (".html", ".css", ".js"):
            cache = "no-store"  # 开发期方便刷新
        else:
            cache = "public, max-age=3600"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def log_message(self, fmt, *args):  # 精简控制台日志
        sys.stdout.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


def main():
    host = os.environ.get("WEB_HOST", "127.0.0.1")
    port = int(os.environ.get("WEB_PORT", "8000"))
    try:
        server = ThreadingHTTPServer((host, port), Handler)
    except OSError as exc:
        print(f"启动失败，端口 {port} 可能被占用：{exc}")
        raise SystemExit(1)
    server.daemon_threads = True
    print(f"学习知识助手网页版已启动：http://{host}:{port}")
    print("按 Ctrl+C 停止服务")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")


if __name__ == "__main__":
    main()