// settings.js — handles the settings page
// Expects api.js to be loaded first (uses requireAuth, getBusinessName, logout)

requireAuth();

const businessNameEl = document.getElementById("settings-business-name");
if (businessNameEl) {
  businessNameEl.innerText = getBusinessName();
}

const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    if (confirm("Are you sure you want to log out?")) {
      logout();
    }
  });
}