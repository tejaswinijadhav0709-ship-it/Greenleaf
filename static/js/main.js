/* -------------------------------------------------------------
   Greenleaf — main.js
   Handles: mobile nav toggle, add-to-cart AJAX, toast feedback
------------------------------------------------------------- */

// Mobile navigation toggle
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");
  if (toggle && links) {
    toggle.addEventListener("click", () => {
      links.classList.toggle("open");
    });
  }

  // Auto-dismiss flash messages after 4 seconds
  document.querySelectorAll(".flash").forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity .35s, transform .35s";
      el.style.opacity = "0";
      el.style.transform = "translateY(-6px)";
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });

  // Wire up "Add to cart" buttons (AJAX so the page doesn't reload)
  document.querySelectorAll(".add-to-cart-btn").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const plantId = btn.dataset.plantId;
      btn.disabled = true;
      btn.textContent = "Adding...";

      try {
        const res = await fetch(`/cart/add/${plantId}`, { method: "POST" });
        const data = await res.json();

        if (data.ok) {
          // Update cart badge
          const badge = document.getElementById("cartBadge");
          if (badge) badge.textContent = data.cart_count;
          showToast(data.message);
          btn.textContent = "Added ✓";
          setTimeout(() => {
            btn.textContent = "Add to cart";
            btn.disabled = false;
          }, 1200);
        } else {
          showToast(data.message || "Could not add to cart");
          btn.textContent = "Add to cart";
          btn.disabled = false;
        }
      } catch (err) {
        showToast("Network error — please try again");
        btn.textContent = "Add to cart";
        btn.disabled = false;
      }
    });
  });
});

// Lightweight toast popup
function showToast(message) {
  const existing = document.querySelector(".toast");
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = "opacity .3s, transform .3s";
    toast.style.opacity = "0";
    toast.style.transform = "translateY(-8px)";
    setTimeout(() => toast.remove(), 320);
  }, 2400);
}


// Wait until page fully loads
document.addEventListener("DOMContentLoaded", function () {

  // Attach click event to button
  const button = document.getElementById("suggestBtn");

  if (button) {
    button.addEventListener("click", findPlant);
  }

});



function findPlant() {
  const sunlight = document.getElementById("sunlight").value;
  const care = document.getElementById("care").value;
  const purpose = document.getElementById("purpose").value;

  let result = "";

  if (sunlight === "low" && care === "low") {
    result = "🌿 Snake Plant – Perfect for low light & low maintenance!";
  } 
  else if (purpose === "air") {
    result = "🌱 Aloe Vera – Great for air purification!";
  } 
  else if (purpose === "medicinal") {
    result = "🌿 Tulsi – Best medicinal plant for your home!";
  } 
  else if (sunlight === "high" && care === "high") {
    result = "🌸 Rose Plant – Needs sunlight & care!";
  } 
  else {
    result = "🌿 Money Plant – Easy & perfect for any home!";
  }

  document.getElementById("result").innerText = result;
}