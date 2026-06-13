const askForm = document.querySelector("#ask-form");
const saveContextForm = document.querySelector("#save-context-form");
const answerOutput = document.querySelector("#answer-output");
const contextList = document.querySelector("#context-list");
const contextUsedBanner = document.querySelector("#context-used-banner");
const contextUsedKeys = document.querySelector("#context-used-keys");

const API_BASE_URL = "http://127.0.0.1:8000";

function getCurrentUserId() {
  return document.querySelector("#user-id").value.trim() || "demo_user";
}

askForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const userId = getCurrentUserId();
  const question = document.querySelector("#question").value.trim();

  answerOutput.textContent = "Consultando...";
  contextUsedBanner.classList.add("hidden");

  try {
    const response = await fetch(`${API_BASE_URL}/api/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, question }),
    });
    const result = await response.json();

    answerOutput.textContent = result.answer ?? JSON.stringify(result, null, 2);
    showContextUsedBanner(result.context_used ?? []);
    await loadContext(userId);
  } catch (error) {
    answerOutput.textContent = `No se pudo conectar con el backend: ${error.message}`;
  }
});

saveContextForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const userId = getCurrentUserId();
  const key = document.querySelector("#ctx-key").value.trim();
  const value = document.querySelector("#ctx-value").value.trim();

  if (!key || !value) return;

  const btn = saveContextForm.querySelector("button");
  btn.textContent = "Guardando...";
  btn.disabled = true;

  try {
    await saveContext(userId, key, value);
    saveContextForm.reset();
    await loadContext(userId);
  } finally {
    btn.textContent = "Guardar Contexto";
    btn.disabled = false;
  }
});

async function saveContext(userId, key, value) {
  const response = await fetch(`${API_BASE_URL}/api/context`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, key, value }),
  });
  return response.json();
}

async function loadContext(userId) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/context?user_id=${encodeURIComponent(userId)}`
    );
    const result = await response.json();
    renderContextList(result.context ?? []);
  } catch {
    contextList.innerHTML = '<p class="context-empty">El modulo CAG aun no esta disponible.</p>';
  }
}

function renderContextList(items) {
  if (items.length === 0) {
    contextList.innerHTML = '<p class="context-empty">Sin contexto guardado para este usuario.</p>';
    return;
  }

  contextList.innerHTML = items
    .map(
      (item) =>
        `<div class="context-item">
          <span class="context-item-key">${escapeHtml(item.key)}</span>
          <span class="context-item-value">${escapeHtml(item.value)}</span>
        </div>`
    )
    .join("");
}

function showContextUsedBanner(usedKeys) {
  if (!usedKeys || usedKeys.length === 0) {
    contextUsedBanner.classList.add("hidden");
    return;
  }

  contextUsedKeys.innerHTML = usedKeys
    .map((k) => `<span class="key-tag">${escapeHtml(k)}</span>`)
    .join("");
  contextUsedBanner.classList.remove("hidden");
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

loadContext(getCurrentUserId());
