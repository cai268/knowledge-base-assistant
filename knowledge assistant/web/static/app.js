(function () {
  "use strict";

  const threadId = new URLSearchParams(location.search).get("tid") ||
    (localStorage.getItem("chatThreadId") || defaultThread());

  function defaultThread() {
    return "web_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  }

  const els = {
    input: document.getElementById("input"),
    send: document.getElementById("send"),
    messages: document.getElementById("messages"),
    welcome: document.getElementById("welcome"),
    chatArea: document.getElementById("chat-area"),
    history: document.getElementById("history"),
    newChat: document.getElementById("new-chat"),
    statusDot: document.getElementById("status-dot"),
    toast: document.getElementById("toast"),
  };

  let busy = false;
  let historyCount = 0;
  localStorage.setItem("chatThreadId", threadId);

  // ---------- 工具函数 ----------

  function showToast(text, isError) {
    els.toast.textContent = text;
    els.toast.classList.toggle("error", !!isError);
    els.toast.hidden = false;
    clearTimeout(showToast.timer);
    showToast.timer = setTimeout(() => { els.toast.hidden = true; }, 2600);
  }

  async function post(url, body) {
    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) throw new Error(data.error || ("请求失败：" + resp.status));
    return data;
  }

  function addMessage(role, text) {
    els.welcome.style.display = "none";
    const msg = document.createElement("div");
    msg.className = "msg " + role;
    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = role === "user" ? "我" : "AI";
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;
    msg.appendChild(avatar);
    msg.appendChild(bubble);
    els.messages.appendChild(msg);
    els.chatArea.scrollTop = els.chatArea.scrollHeight;
    return msg;
  }

  function addTyping() {
    els.welcome.style.display = "none";
    const msg = document.createElement("div");
    msg.className = "msg ai thinking";
    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = "AI";
    const bubble = document.createElement("div");
    bubble.className = "bubble typing";
    for (let i = 0; i < 3; i++) {
      const dot = document.createElement("span");
      dot.className = "dot";
      bubble.appendChild(dot);
    }
    msg.appendChild(avatar);
    msg.appendChild(bubble);
    els.messages.appendChild(msg);
    els.chatArea.scrollTop = els.chatArea.scrollHeight;
    return msg;
  }

  function setStatus(kind) {
    els.statusDot.className = "status-dot" + (kind ? " " + kind : "");
    els.statusDot.title =
      kind === "ok" ? "服务正常" : kind === "err" ? "服务异常" : "服务状态未知";
  }

  function refreshHistoryTitle() {
    const item = document.querySelector(".history-item.active");
    if (item && !item.dataset.pinned) {
      const first = els.messages.querySelector(".msg.user .bubble");
      if (first) item.textContent = (first.textContent || "新对话").slice(0, 18);
    }
  }

  // ---------- 核心逻辑 ----------

  async function sendMessage(text) {
    if (!text.trim() || busy) return;
    busy = true;
    els.send.disabled = true;
    els.send.textContent = "…";
    addMessage("user", text.trim());

    const typing = addTyping();
    try {
      const data = await post("/api/chat", { message: text.trim(), thread_id: threadId });
      typing.remove();
      addMessage("ai", data.reply);
      historyCount++;
      if (historyCount === 1) refreshHistoryTitle();
      setStatus("ok");
    } catch (err) {
      typing.remove();
      addMessage("ai", "请求出错了：" + err.message);
      setStatus("err");
    } finally {
      busy = false;
      els.send.disabled = false;
      els.send.textContent = "➤";
      els.input.focus();
    }
  }

  async function newChat() {
    if (busy) return;
    try {
      await post("/api/reset", { thread_id: threadId });
    } catch (err) {
      showToast("清理旧会话失败：" + err.message, true);
      return;
    }
    location.href = location.pathname + "?tid=" + threadId;
  }

  // ---------- 事件绑定 ----------

  function sendFromInput() {
    const text = els.input.value;
    els.input.value = "";
    els.input.style.height = "auto";
    sendMessage(text);
  }

  els.send.addEventListener("click", sendFromInput);

  els.input.addEventListener("keydown", function (ev) {
    if (ev.key === "Enter" && !ev.shiftKey && !ev.isComposing) {
      ev.preventDefault();
      sendFromInput();
    }
  });

  els.input.addEventListener("input", function () {
    els.input.style.height = "auto";
    els.input.style.height = Math.min(els.input.scrollHeight, 160) + "px";
  });

  els.newChat.addEventListener("click", newChat);

  document.querySelectorAll(".hint-chip").forEach(function (chip) {
    chip.addEventListener("click", function () {
      els.input.value = chip.dataset.q;
      els.input.focus();
    });
  });

  document.addEventListener("click", function (ev) {
    const item = ev.target.closest(".history-item");
    if (!item || item.classList.contains("active")) return;
    window.location.href = location.pathname + "?tid=" + item.dataset.tid;
  });

  // 首次进入：历史列表中加入当前会话
  const firstItem = document.createElement("button");
  firstItem.type = "button";
  firstItem.className = "history-item active";
  firstItem.dataset.tid = threadId;
  firstItem.dataset.pinned = "1";
  firstItem.textContent = "新对话";
  els.history.appendChild(firstItem);

  // 服务健康检查
  fetch("/api/health")
    .then(function (resp) {
      setStatus(resp.ok ? "ok" : "err");
    })
    .catch(function () {
      setStatus("err");
    });

  els.input.focus();
})();