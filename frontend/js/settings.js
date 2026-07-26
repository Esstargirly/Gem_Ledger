requireAuth();

const businessNameEl = document.getElementById("settings-business-name");
if (businessNameEl) {
  businessNameEl.innerText = getBusinessName();
}

const emailEl = document.getElementById("settings-email");
if (emailEl) {
  emailEl.innerText = getEmail() || "No email on file";
}

const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    if (confirm("Are you sure you want to log out?")) {
      logout();
    }
  });
}