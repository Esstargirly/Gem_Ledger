
requireAuth();

// Greet the user with their business name
const greetingEl = document.getElementById("greeting");
if (greetingEl) {
  greetingEl.innerText = `Hi, ${getBusinessName()} 👋`;
}

const journalEntry = document.getElementById("journal-entry");
const addEntryBtn = document.getElementById("add-entry-btn");
const insightCard = document.getElementById("insight-text");
const recentList = document.getElementById("recent-records-list");
const micBtn = document.getElementById("mic-btn");

// ---- ADD ENTRY (calls Gemma via backend) ----
async function submitEntry() {
  const text = journalEntry.value.trim();
  if (!text) return;

  const originalText = addEntryBtn.innerText;
  addEntryBtn.disabled = true;
  addEntryBtn.innerText = "Thinking...";

  try {
    const data = await apiFetch("/analyze", {
      method: "POST",
      body: JSON.stringify({ text }),
    });

    if (data.summary && insightCard) {
      insightCard.innerText = data.summary;
    }

    if (data.transactions && Array.isArray(data.transactions)) {
      data.transactions.forEach((tx) => prependRecentRecord(tx));
    }

    journalEntry.value = "";
    journalEntry.style.height = "auto";
  } catch (err) {
    if (insightCard) {
      insightCard.innerText = `Something went wrong: ${err.message}`;
    }
  } finally {
    addEntryBtn.disabled = false;
    addEntryBtn.innerText = originalText;
  }
}

if (addEntryBtn) {
  addEntryBtn.addEventListener("click", submitEntry);
}

// ---- Render a new record row at the top of "Recent Records" ----
function prependRecentRecord(tx) {
  if (!recentList) return;

  const isIncome = tx.type === "income";
  const amountColor = isIncome ? "text-primary" : "text-error";
  const amountPrefix = isIncome ? "+" : "-";
  const iconBg = isIncome ? "bg-secondary-container/20 text-secondary" : "bg-primary-fixed/20 text-primary";
  const icon = isIncome ? "sell" : "shopping_basket";

  const row = document.createElement("div");
  row.className = "bg-surface-container-low rounded-xl p-4 flex items-center justify-between hover:bg-white transition-colors cursor-pointer";
  row.innerHTML = `
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl ${iconBg} flex items-center justify-center">
        <span class="material-symbols-outlined">${icon}</span>
      </div>
      <div>
        <p class="font-body-md text-on-surface font-medium">${tx.description || tx.category || "Entry"}</p>
        <p class="font-label-sm text-label-sm text-outline">Just now</p>
      </div>
    </div>
    <span class="font-headline-sm text-headline-sm ${amountColor}">${amountPrefix} ₦${Number(tx.amount).toLocaleString()}</span>
  `;

  recentList.prepend(row);
}

// ---- Load recent records on page load ----
async function loadRecentRecords() {
  if (!recentList) return;
  try {
    const data = await apiFetch("/transactions?limit=5", { method: "GET" });
    if (data.transactions && Array.isArray(data.transactions)) {
      recentList.innerHTML = "";
      data.transactions.forEach((tx) => prependRecentRecord(tx));
    }
  } catch (err) {
    // Silently ignore on the home screen — records.html is the source of truth
    console.warn("Could not load recent records:", err.message);
  }
}

loadRecentRecords();

// ---- Voice input (Web Speech API) ----
let isListening = false;
let recognition = null;

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition && micBtn) {
  console.log("Voice input: SpeechRecognition is supported, mic button wired up.");
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    journalEntry.value = journalEntry.value
      ? `${journalEntry.value} ${transcript}`
      : transcript;
    journalEntry.dispatchEvent(new Event("input"));
  };

  recognition.onend = () => {
    console.log("Speech recognition ended.");
    setMicListeningState(false);
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    if (event.error === "not-allowed" || event.error === "service-not-allowed") {
      alert("Microphone access was denied. Please allow microphone permission in your browser settings and try again.");
    } else if (event.error === "no-speech") {
      console.log("No speech detected — try speaking right after clicking the mic.");
    }
    setMicListeningState(false);
  };

  micBtn.addEventListener("click", () => {
    console.log("Mic button clicked. isListening =", isListening);
    try {
      if (!isListening) {
        recognition.start();
        setMicListeningState(true);
      } else {
        recognition.stop();
        setMicListeningState(false);
      }
    } catch (err) {
      console.error("Error starting/stopping recognition:", err);
      setMicListeningState(false);
    }
  });
} else if (micBtn) {
  // Browser doesn't support voice input (e.g. Safari) — hide the mic button gracefully
  micBtn.title = "Voice input isn't supported in this browser. Try Chrome.";
  micBtn.addEventListener("click", () => {
    alert("Voice input works best in Chrome. Please type your entry instead.");
  });
}

function setMicListeningState(listening) {
  isListening = listening;
  const ring = micBtn.querySelector(".mic-pulse");
  const icon = micBtn.querySelector(".material-symbols-outlined");

  if (listening) {
    ring.classList.replace("bg-secondary-container", "bg-error");
    icon.innerText = "graphic_eq";
    icon.style.color = "#fff";
    micBtn.classList.replace("bg-secondary-container", "bg-error");
  } else {
    ring.classList.replace("bg-error", "bg-secondary-container");
    icon.innerText = "mic";
    icon.style.color = "";
    micBtn.classList.replace("bg-error", "bg-secondary-container");
  }
}

// ---- Textarea auto-expand ----
if (journalEntry) {
  journalEntry.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = this.scrollHeight + "px";
  });
}
