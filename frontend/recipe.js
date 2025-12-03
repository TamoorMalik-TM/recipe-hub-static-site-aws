
async function loadRecipe() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");
  const container = document.getElementById("recipe-detail");
  const title = document.getElementById("recipe-title");

  if (!id) {
    container.innerHTML = "<p>Missing recipe id.</p>";
    return;
  }

  container.innerHTML = "<p>Loading...</p>";

  const res = await fetch(API_BASE_URL + "/recipes/" + id);
  if (!res.ok) {
    container.innerHTML = "<p>Failed to load recipe.</p>";
    return;
  }

  const r = await res.json();
  title.textContent = r.title;

  container.innerHTML = `
    ${r.image_url ? `<img src="${r.image_url}" alt="${r.title}" style="max-width:100%; border-radius:4px;">` : ""}
    <p><strong>Author:</strong> ${r.author}</p>
    <p><strong>Difficulty:</strong> ${r.difficulty}</p>
    <p><strong>Time:</strong> Prep ${r.prep_time} min, Cook ${r.cook_time} min</p>
    <p><strong>Servings:</strong> ${r.servings}</p>
    <p><strong>Rating:</strong> ${r.avg_rating.toFixed(1)} (${r.votes} votes)</p>
    <h3>Ingredients</h3>
    <pre>${r.ingredients}</pre>
    <h3>Steps</h3>
    <pre>${r.steps}</pre>
  `;
}

async function submitRating() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");
  const rating = document.getElementById("rating-select").value;
  const msg = document.getElementById("rate-message");
  const token = getToken();

  if (!token) {
    msg.textContent = "You must be logged in to rate.";
    return;
  }
  if (!rating) {
    msg.textContent = "Select a rating.";
    return;
  }

  try {
    const res = await fetch(API_BASE_URL + "/recipes/" + id + "/rate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify({ rating: parseInt(rating) })
    });

    if (!res.ok) {
      msg.textContent = "Failed to submit rating.";
      return;
    }

    msg.textContent = "Rating submitted!";
    loadRecipe();
  } catch (err) {
    msg.textContent = "Error connecting to server.";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadRecipe();
  document.getElementById("rate-btn").addEventListener("click", submitRating);
});
