

// Mock response for demo purposes
const mockResponse = {
  prediction: "Human",
  confidence: 95,
  explanation: "The audio shows natural human speech patterns.",
};

// DOM elements
const fileInput = document.getElementById("audio-file");
const predictBtn = document.getElementById("predict-btn");
const loadingDiv = document.getElementById("loading");
const resultDiv = document.getElementById("result");
const errorDiv = document.getElementById("error");

const predictionSpan = document.getElementById("prediction");
const explanationSpan = document.getElementById("explanation");

const confidenceFill = document.getElementById("confidence-fill");
const confidenceText = document.getElementById("confidence-text");

const fileNameEl = document.getElementById("fileName");
const badgeEl = document.getElementById("badge");

// Enable/disable predict button based on file selection
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];

  // show file name on UI
  fileNameEl.textContent = file ? file.name : "No file selected";

  if (!file) {
    predictBtn.disabled = true;
    hideError();
    return;
  }

  // accept MP3 + WAV (since UI shows both)
  const isMP3 = file.type === "audio/mpeg" || file.name.toLowerCase().endsWith(".mp3");
  const isWAV = file.type === "audio/wav" || file.name.toLowerCase().endsWith(".wav");

  if (isMP3 || isWAV) {
    predictBtn.disabled = false;
    hideError();
  } else {
    predictBtn.disabled = true;
    showError("Only MP3/WAV files are supported. Please select a valid audio file.");
  }
});

// Handle predict button click
predictBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];
  if (!file) {
    showError("No file selected.");
    return;
  }

  // UI states
  showLoading(true);
  hideResult();
  hideError();

  try {
    let data;

    if (CONFIG.USE_MOCK) {
      await new Promise((r) => setTimeout(r, 800));
      data = mockResponse;
    } else {
      // Convert file to Base64
      const base64Audio = await fileToBase64(file);

      // Send POST request
      const response = await fetch(CONFIG.API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ audio: base64Audio }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      data = await response.json();
    }

    displayResult(data);
  } catch (err) {
    console.error("Error:", err);
    displayResult(mockResponse);
    showError("API unavailable. Showing mock result.");
  } finally {
    showLoading(false);
  }
});

// Utility: file -> base64 (without prefix)
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result.split(",")[1]);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function showLoading(show) {
  loadingDiv.classList.toggle("hidden", !show);
}

function hideResult() {
  resultDiv.classList.add("hidden");
}

function hideError() {
  errorDiv.classList.add("hidden");
  errorDiv.textContent = "";
}

function showError(message) {
  errorDiv.textContent = message;
  errorDiv.classList.remove("hidden");
}

function setBadge(prediction) {
  const p = (prediction || "").toLowerCase();

  if (p.includes("human")) {
    badgeEl.textContent = "Human";
    badgeEl.className = "badge ok";
  } else if (p.includes("ai")) {
    badgeEl.textContent = "AI";
    badgeEl.className = "badge bad";
  } else {
    badgeEl.textContent = prediction || "—";
    badgeEl.className = "badge neutral";
  }
}

function displayResult(data) {
  predictionSpan.textContent = data.prediction ?? "—";
  explanationSpan.textContent = data.explanation ?? "—";

  const conf = Number(data.confidence ?? 0);
  confidenceFill.style.width = `${Math.max(0, Math.min(100, conf))}%`;
  confidenceText.textContent = `${Math.max(0, Math.min(100, conf))}%`;

  setBadge(data.prediction);
  resultDiv.classList.remove("hidden");
}
