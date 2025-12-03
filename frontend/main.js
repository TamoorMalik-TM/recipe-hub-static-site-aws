
function renderUserInfo() {
  const token = getToken();
  const userInfo = document.getElementById("user-info");
  const loginLink = document.getElementById("login-link");
  if (!userInfo || !loginLink) return;

  if (token) {
    userInfo.innerHTML = '<span>Logged in</span> <button id="logout-btn">Logout</button>';
    loginLink.style.display = "none";
    document.getElementById("logout-btn").addEventListener("click", () => {
      clearToken();
      window.location.reload();
    });
  } else {
    userInfo.textContent = "";
    loginLink.style.display = "inline";
  }
}

async function loadRecipes(search = "") {
  const container = document.getElementById("recipes-container");
  container.innerHTML = "<p>Loading...</p>";

  const url = new URL(API_BASE_URL + "/recipes");
  if (search) {
    url.searchParams.append("search", search);
  }

  const res = await fetch(url);
  if (!res.ok) {
    container.innerHTML = "<p>Failed to load recipes</p>";
    return;
  }

  const recipes = await res.json();
  if (recipes.length === 0) {
    container.innerHTML = "<p>No recipes found.</p>";
    return;
  }

  container.innerHTML = "";
  recipes.forEach(r => {
    const card = document.createElement("article");
    card.className = "card recipe-card";
    card.innerHTML = `
      ${r.image_url ? `<img src="${r.image_url}" alt="${r.title}">` : ""}
      <h2>${r.title}</h2>
      <p>${r.description || ""}</p>
      <p class="recipe-meta">
        By ${r.author} • ${r.difficulty || "medium"} • Prep: ${r.prep_time || 0} min • Cook: ${r.cook_time || 0} min
      </p>
      <a href="recipe.html?id=${r.id}">View recipe</a>
    `;
    container.appendChild(card);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("recipes-container")) {
    loadRecipes();

    const searchBtn = document.getElementById("search-btn");
    const searchInput = document.getElementById("search-input");
    if (searchBtn && searchInput) {
      searchBtn.addEventListener("click", () => {
        loadRecipes(searchInput.value);
      });
    }
  }

  renderUserInfo();
});
