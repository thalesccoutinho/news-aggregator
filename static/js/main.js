// ── Category filter ──────────────────────────────────────────────────────────
document.querySelectorAll(".filter-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");

    const category = btn.dataset.category;
    document.querySelectorAll(".card").forEach((card) => {
      if (!category || card.dataset.category === category) {
        card.classList.remove("hidden");
      } else {
        card.classList.add("hidden");
      }
    });
  });
});

// ── AI summarize ─────────────────────────────────────────────────────────────
document.querySelectorAll(".btn-ai").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const id = btn.dataset.id;
    const box = document.getElementById(`ai-${id}`);

    btn.disabled = true;
    btn.textContent = "⏳ Gerando resumo…";

    try {
      const res = await fetch(`/api/summarize/${id}`, { method: "POST" });
      const data = await res.json();

      if (data.summary) {
        box.textContent = data.summary;
        box.style.display = "block";
        btn.textContent = "✅ Resumo gerado";
      } else {
        btn.textContent = "⚠️ Erro ao resumir";
        btn.disabled = false;
      }
    } catch (err) {
      btn.textContent = "⚠️ Erro ao resumir";
      btn.disabled = false;
    }
  });
});

// ── Manual refresh ────────────────────────────────────────────────────────────
document.getElementById("btn-refresh").addEventListener("click", async () => {
  const btn = document.getElementById("btn-refresh");
  btn.textContent = "⏳ Atualizando…";
  btn.disabled = true;
  try {
    await fetch("/api/refresh", { method: "POST" });
  } finally {
    window.location.reload();
  }
});

// ── Auto-refresh countdown (30 min) ──────────────────────────────────────────
let secondsLeft = 30 * 60;
const countdownEl = document.getElementById("countdown");

const tick = () => {
  secondsLeft--;
  if (secondsLeft <= 0) {
    window.location.reload();
    return;
  }
  const m = String(Math.floor(secondsLeft / 60)).padStart(2, "0");
  const s = String(secondsLeft % 60).padStart(2, "0");
  countdownEl.textContent = `${m}:${s}`;
};

setInterval(tick, 1000);
