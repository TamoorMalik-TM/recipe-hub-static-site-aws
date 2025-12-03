
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("login-btn");
  const msg = document.getElementById("login-message");

  btn.addEventListener("click", async () => {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
      msg.textContent = "Enter username and password.";
      return;
    }

    try {
      const res = await fetch(API_BASE_URL + "/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });

      if (!res.ok) {
        msg.textContent = "Login failed.";
        return;
      }

      const data = await res.json();
      setToken(data.token);
      msg.textContent = "Login successful. Redirecting...";
      setTimeout(() => {
        window.location.href = "index.html";
      }, 800);
    } catch (err) {
      msg.textContent = "Error connecting to server.";
    }
  });
});
