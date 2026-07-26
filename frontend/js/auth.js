
function showError(elementId, message) {
const el = document.getElementById(elementId);
if (!el) return;
el.textContent = message;
el.classList.remove("hidden");
}

function hideError(elementId) {
const el = document.getElementById(elementId);
if (!el) return;
el.classList.add("hidden");
}

function setButtonLoading(buttonId, textId, isLoading, loadingText, defaultText) {
const button = document.getElementById(buttonId);
const text = document.getElementById(textId);
if (!button || !text) return;
button.disabled = isLoading;
text.innerText = isLoading ? loadingText : defaultText;
button.classList.toggle("opacity-70", isLoading);
}

// –– SIGN UP ––
const signupForm = document.getElementById("signup-form");
if (signupForm) {
signupForm.addEventListener("submit", async (e) => {
e.preventDefault();
hideError("signup-error");

const business_name = document.getElementById("business_name").value.trim();
const email = document.getElementById("email").value.trim();
const password = document.getElementById("password").value;

if (!business_name || !email || !password) {
  showError("signup-error", "Please fill in all fields.");
  return;
}

if (password.length < 8) {
  showError("signup-error", "Password must be at least 8 characters.");
  return;
}

setButtonLoading("signup-submit", "signup-submit-text", true, "Creating account...", "Create Account");

try {
  const data = await apiFetch("/auth/signup", {
    method: "POST",
    body: JSON.stringify({ business_name, email, password }),
  });

  saveToken(data.token);
  saveBusinessName(data.business_name || business_name);
  window.location.href = "home.html";
} catch (err) {
  showError("signup-error", err.message);
  setButtonLoading("signup-submit", "signup-submit-text", false, "Creating account...", "Create Account");
}

});
}

// –– LOG IN ––
const loginForm = document.getElementById("login-form");
if (loginForm) {
loginForm.addEventListener("submit", async (e) => {
e.preventDefault();
hideError("login-error");

const email = document.getElementById("email").value.trim();
const password = document.getElementById("password").value;

if (!email || !password) {
  showError("login-error", "Please enter your email and password.");
  return;
}

setButtonLoading("login-submit", "login-submit-text", true, "Logging in...", "Log In");

try {
  const data = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  saveToken(data.token);
  saveBusinessName(data.business_name || "");
  window.location.href = "home.html";
} catch (err) {
  showError("login-error", err.message);
  setButtonLoading("login-submit", "login-submit-text", false, "Logging in...", "Log In");
}
});
}