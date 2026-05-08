/* -------------------------------------------------------------
   Greenleaf — chatbot.js
   Floating plant-care assistant. Talks to Flask /api/chat endpoint.
------------------------------------------------------------- */

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("chatToggle");
  const panel = document.getElementById("chatPanel");
  const closeBtn = document.getElementById("chatClose");
  const form = document.getElementById("chatForm");
  const input = document.getElementById("chatInput");
  const messages = document.getElementById("chatMessages");

  if (!toggle || !panel || !form) return;

  // Open / close panel
  toggle.addEventListener("click", () => {
    panel.classList.toggle("open");
    if (panel.classList.contains("open")) input.focus();
  });
  closeBtn.addEventListener("click", () => { panel.classList.remove("open"); });

  // Append a message bubble
  function appendMessage(text, role) {
    const div = document.createElement("div");
    div.className = `chat-msg ${role}`;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  // Submit a question to the backend
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    appendMessage(text, "user");
    input.value = "";

    const typing = document.createElement("div");
    typing.className = "chat-msg bot";
    typing.textContent = "Thinking...";
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      typing.remove();
      appendMessage(data.reply || "I didn't catch that. Try again?", "bot");
    } catch (err) {
      typing.remove();
      appendMessage("Sorry — I'm having trouble connecting right now.", "bot");
    }
  });
});