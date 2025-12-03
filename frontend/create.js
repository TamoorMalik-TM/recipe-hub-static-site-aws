
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("create-btn");
  const msg = document.getElementById("create-message");

  btn.addEventListener("click", async () => {
    const token = getToken();
    if (!token) {
      msg.textContent = "You must be logged in to create recipes.";
      return;
    }

    const payload = {
      title: document.getElementById("title").value.trim(),
      description: document.getElementById("description").value.trim(),
      ingredients: document.getElementById("ingredients").value.trim(),
      steps: document.getElementById("steps").value.trim(),
      tags: document.getElementById("tags").value.trim(),
      difficulty: document.getElementById("difficulty").value,
      prep_time: parseInt(document.getElementById("prep_time").value || "0"),
      cook_time: parseInt(document.getElementById("cook_time").value || "0"),
      servings: parseInt(document.getElementById("servings").value || "1"),
      image_url: document.getElementById("image_url").value.trim(),
    };

    if (!payload.title || !payload.description || !payload.ingredients || !payload.steps) {
      msg.textContent = "Fill in required fields.";
      return;
    }

    try {
      const res = await fetch(API_BASE_URL + "/recipes", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        msg.textContent = "Failed to create recipe.";
        return;
      }

      const data = await res.json();
      msg.textContent = "Recipe created! Redirecting...";
      setTimeout(() => {
        window.location.href = "recipe.html?id=" + data.id;
      }, 800);
    } catch (err) {
      msg.textContent = "Error connecting to server.";
    }
  });
});
