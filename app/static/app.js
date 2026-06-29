const form = document.querySelector("#uploadForm");
const input = document.querySelector("#imageInput");
const statusBox = document.querySelector("#status");
const emptyState = document.querySelector("#emptyState");
const resultView = document.querySelector("#resultView");
const historyList = document.querySelector("#historyList");

const fileName = document.querySelector("#fileName");
const modelName = document.querySelector("#modelName");
const latency = document.querySelector("#latency");
const objectCount = document.querySelector("#objectCount");
const predictionRows = document.querySelector("#predictionRows");

function setStatus(message, type = "idle") {
  statusBox.textContent = message;
  statusBox.className = `status ${type}`;
}

function formatDate(value) {
  return new Intl.DateTimeFormat("ko-KR", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function renderAnalysis(analysis) {
  emptyState.classList.add("hidden");
  resultView.classList.remove("hidden");

  fileName.textContent = analysis.original_filename;
  modelName.textContent = analysis.model_name;
  latency.textContent = `${analysis.inference_ms} ms`;
  objectCount.textContent = analysis.predictions.length;

  if (analysis.predictions.length === 0) {
    predictionRows.innerHTML =
      '<tr><td colspan="3">No objects detected above the configured threshold.</td></tr>';
    return;
  }

  predictionRows.innerHTML = analysis.predictions
    .map((item) => {
      const box = item.bbox;
      const bbox = `${box.x1.toFixed(1)}, ${box.y1.toFixed(1)}, ${box.x2.toFixed(1)}, ${box.y2.toFixed(1)}`;
      return `
        <tr>
          <td><strong>${item.class_name}</strong><br><span class="label">class_id ${item.class_id}</span></td>
          <td><span class="confidence">${(item.confidence * 100).toFixed(1)}%</span></td>
          <td>${bbox}</td>
        </tr>
      `;
    })
    .join("");
}

async function loadHistory() {
  const response = await fetch("/api/v1/analyses");
  if (!response.ok) throw new Error("Failed to load analysis history.");

  const analyses = await response.json();
  if (analyses.length === 0) {
    historyList.innerHTML = '<div class="empty-state">No saved analysis yet.</div>';
    return;
  }

  historyList.innerHTML = analyses
    .map(
      (item) => `
        <button class="history-item" type="button" data-id="${item.id}">
          <strong>${item.original_filename}</strong>
          <span>${item.prediction_count} objects · ${item.model_name} · ${formatDate(item.created_at)}</span>
        </button>
      `,
    )
    .join("");
}

historyList.addEventListener("click", async (event) => {
  const item = event.target.closest(".history-item");
  if (!item) return;

  setStatus("Loading saved analysis...", "idle");
  const response = await fetch(`/api/v1/analyses/${item.dataset.id}`);
  if (!response.ok) {
    setStatus("Could not load the selected analysis.", "error");
    return;
  }
  renderAnalysis(await response.json());
  setStatus("Saved analysis loaded.", "success");
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const file = input.files[0];
  if (!file) {
    setStatus("Choose an image before running inference.", "error");
    return;
  }

  const submitButton = form.querySelector("button");
  submitButton.disabled = true;
  setStatus("Running YOLO inference. This can take a moment on small EC2 instances...", "idle");

  const body = new FormData();
  body.append("file", file);

  try {
    const response = await fetch("/api/v1/analyses", {
      method: "POST",
      body,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Image analysis failed.");
    }

    const analysis = await response.json();
    renderAnalysis(analysis);
    await loadHistory();
    setStatus("Analysis completed and stored.", "success");
  } catch (error) {
    setStatus(error.message, "error");
  } finally {
    submitButton.disabled = false;
  }
});

loadHistory().catch(() => {
  historyList.innerHTML = '<div class="empty-state">History is not available.</div>';
});
