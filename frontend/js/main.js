/**
 * LUXURY HOTEL ROOM BOOKING SYSTEM - CLIENT SCRIPT
 * Handles API integration, local state management, dynamic DOM rendering,
 * and graceful fallback data.
 */

const API_BASE_URL = window.location.origin.includes("5000")
  ? window.location.origin + "/api"
  : "http://127.0.0.1:5000/api";

// Local Storage Keys
const TOKEN_KEY = "luxe_jwt_token";
const USER_KEY = "luxe_user_profile";
const THEME_KEY = "aura_luxury_theme";

// Immediate execution to prevent theme flash
(function () {
  try {
    const saved = localStorage.getItem(THEME_KEY) || "dark";
    document.documentElement.setAttribute("data-theme", saved);
  } catch (e) {}
})();

// ==========================================
// THEME MANAGER (PROFESSIONAL LIGHT / LUXURY DARK)
// ==========================================
const Theme = {
  getTheme() {
    return localStorage.getItem(THEME_KEY) || "dark";
  },
  setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
    this.updateToggleIcon();
  },
  toggle() {
    const next = this.getTheme() === "light" ? "dark" : "light";
    this.setTheme(next);
    showToast(`Switched to ${next === "light" ? "Professional Light" : "Luxury Dark"} Theme`, "info");
  },
  init() {
    const current = this.getTheme();
    document.documentElement.setAttribute("data-theme", current);
    this.injectToggleBtn();
  },
  injectToggleBtn() {
    const authContainer = document.getElementById("nav-auth-container");
    if (!authContainer) return;

    let btn = document.getElementById("theme-toggle-btn");
    if (!btn) {
      btn = document.createElement("button");
      btn.id = "theme-toggle-btn";
      btn.className = "theme-toggle-btn";
      btn.type = "button";
      btn.setAttribute("aria-label", "Toggle Dark/Light Mode");
      btn.onclick = () => Theme.toggle();
      authContainer.prepend(btn);
    }
    this.updateToggleIcon();
  },
  updateToggleIcon() {
    const btn = document.getElementById("theme-toggle-btn");
    if (!btn) return;
    const isLight = this.getTheme() === "light";
    btn.innerHTML = `<i class="fa-solid ${isLight ? 'fa-moon' : 'fa-sun'}"></i>`;
    btn.setAttribute("title", isLight ? "Switch to Luxury Dark Mode" : "Switch to Professional Light Mode");
  }
};

// ==========================================
// AUTHENTICATION STATE
// ==========================================
const Auth = {
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },
  getUser() {
    try {
      return JSON.parse(localStorage.getItem(USER_KEY));
    } catch {
      return null;
    }
  },
  setAuth(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    this.updateNav();
  },
  logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    showToast("You have been signed out.", "info");
    setTimeout(() => {
      window.location.href = "login.html";
    }, 500);
  },
  isLoggedIn() {
    return !!this.getToken();
  },
  updateNav() {
    const authContainer = document.getElementById("nav-auth-container");
    if (!authContainer) return;

    const user = this.getUser();
    if (user && this.isLoggedIn()) {
      authContainer.innerHTML = `
        <div class="user-profile-badge">
          <i class="fa-solid fa-crown"></i>
          <span>${user.name}</span>
          ${user.role === 'admin' ? '<span class="tag" style="color:var(--accent-gold);margin-left:4px;">Admin</span>' : ''}
        </div>
        ${user.role === 'admin' ? `
          <a href="admin.html" class="btn btn-gold btn-sm" style="box-shadow: 0 0 12px rgba(212,175,55,0.35);">
            <i class="fa-solid fa-gauge-high"></i> Admin Portal
          </a>
        ` : ''}
        ${user.role !== 'admin' ? `
          <a href="my_bookings.html" class="btn btn-outline btn-sm">
            <i class="fa-solid fa-suitcase"></i> My Trips
          </a>
        ` : ''}
        <button onclick="Auth.logout()" class="btn btn-danger btn-sm" title="Sign Out">
          <i class="fa-solid fa-arrow-right-from-bracket"></i>
        </button>
      `;
    } else {
      authContainer.innerHTML = `
        <a href="login.html" class="btn btn-outline btn-sm">Sign In</a>
        <a href="register.html" class="btn btn-gold btn-sm">Join Club</a>
      `;
    }

    // Dynamic Admin link & Navigation customization
    const navLinks = document.querySelector(".nav-links");
    if (navLinks) {
      // For Admin accounts: remove "My Reservations" tab from the top navbar
      if (user && user.role === 'admin') {
        const reservationLinks = Array.from(navLinks.querySelectorAll("li")).filter(li => {
          const a = li.querySelector("a");
          return a && (a.getAttribute("href")?.includes("my_bookings.html") || a.textContent.toLowerCase().includes("reservation"));
        });
        reservationLinks.forEach(li => li.remove());
      }

      const existingAdmin = document.getElementById("nav-admin-link") || navLinks.querySelector('a[href="admin.html"]')?.closest("li");
      if (user && user.role === 'admin') {
        if (!existingAdmin) {
          const adminLi = document.createElement("li");
          adminLi.id = "nav-admin-link";
          adminLi.className = "nav-item";
          adminLi.innerHTML = `<a href="admin.html" style="color:var(--accent-gold);font-weight:600;"><i class="fa-solid fa-shield-halved"></i> Admin Portal</a>`;
          navLinks.appendChild(adminLi);
        }
      } else if (existingAdmin) {
        existingAdmin.remove();
      }

      // Ensure no duplicate Admin Portal links exist
      const allAdminItems = Array.from(navLinks.querySelectorAll('a[href="admin.html"]'));
      if (allAdminItems.length > 1) {
        for (let i = 1; i < allAdminItems.length; i++) {
          allAdminItems[i].closest("li")?.remove();
        }
      }
    }

    // Ensure theme toggle is always available in navbar
    Theme.injectToggleBtn();
  }
};

// ==========================================
// TOAST NOTIFICATIONS
// ==========================================
function showToast(message, type = "info") {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  const icon = type === "success" ? "fa-circle-check" : type === "error" ? "fa-circle-xmark" : "fa-bell";

  toast.innerHTML = `
    <i class="fa-solid ${icon}" style="font-size:1.1rem;color:${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#d4af37'}"></i>
    <div style="flex:1;">${message}</div>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// ==========================================
// API CLIENT
// ==========================================
async function apiRequest(endpoint, method = "GET", body = null, requireAuth = false) {
  const headers = { "Content-Type": "application/json" };
  if (requireAuth) {
    const token = Auth.getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message || `HTTP error ${res.status}`);
    }
    return data;
  } catch (err) {
    console.warn(`API call failed for ${endpoint}:`, err.message);
    throw err;
  }
}

// Fallback Mock Datastore for Standalone / Offline Previews
const FALLBACK_HOTELS = [
  {
    id: "htl_001",
    name: "The Grand Coromandel Bay Luxury Palace & Spa",
    city: "Chennai",
    state: "Tamil Nadu",
    country: "India",
    star_rating: 4.9,
    description: "Commanding breathtaking vistas of the Bay of Bengal along East Coast Road with infinity pools, private beaches, and Chettinad fine dining.",
    images: ["https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80"],
    amenities: ["Oceanfront Pool", "Private Beach", "Ayurvedic Spa", "Chettinad Dining"],
    starting_price: 320
  },
  {
    id: "htl_002",
    name: "The Savoy Nilgiri Mist Heritage Retreat",
    city: "Ooty",
    state: "Tamil Nadu",
    country: "India",
    star_rating: 4.8,
    description: "Colonial-era heritage estate nestled in eucalyptus hills featuring stone fireplaces, rose gardens, and English high tea.",
    images: ["https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80"],
    amenities: ["Rose Gardens", "Tea Estate Trails", "Fireplace Lounge", "Nilgiri Spa"],
    starting_price: 280
  },
  {
    id: "htl_003",
    name: "Tamara Pine & Mist Lake Sanctuary",
    city: "Kodaikanal",
    state: "Tamil Nadu",
    country: "India",
    star_rating: 4.9,
    description: "Eco-luxury valley retreat overlooking tranquil lakes and pine forests with cantilevered decks and stargazing domes.",
    images: ["https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=1200&q=80"],
    amenities: ["Cliffside Heated Pool", "Lakeview Lounge", "Nature Trails", "Organic Bistro"],
    starting_price: 310
  },
  {
    id: "htl_004",
    name: "The Heritage Madurai Royal Sanctuary & Gardens",
    city: "Madurai",
    state: "Tamil Nadu",
    country: "India",
    star_rating: 4.8,
    description: "Geoffrey Bawa designed 17-acre sanctuary celebrating Pandyan architectural heritage with banyan courtyards and temple-tank pool.",
    images: ["https://images.unsplash.com/photo-1502784444187-359ac186c5bb?auto=format&fit=crop&w=1200&q=80"],
    amenities: ["Temple Tank Pool", "Pandyan Architecture", "Ayurvedic Spa", "Cultural Tours"],
    starting_price: 340
  },
  {
    id: "htl_005",
    name: "Shore Temple Bayview Heritage Eco-Resort",
    city: "Mahabalipuram",
    state: "Tamil Nadu",
    country: "India",
    star_rating: 4.9,
    description: "Overlooking UNESCO shore temples and golden beaches, offering thatched beachside villas, sea breeze cabanas, and fresh seafood barbecue.",
    images: ["https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=80"],
    amenities: ["Private Beach Frontage", "Shore Temple Walk", "Catamaran Sailing", "Surf Club"],
    starting_price: 360
  }
];

const FALLBACK_ROOMS = [
  {
    id: "rm_101",
    hotel_id: "htl_001",
    hotel_name: "The Grand Coromandel Bay Luxury Palace & Spa",
    room_number: "Coromandel-101",
    room_type: "Deluxe Coromandel Ocean Suite",
    price_per_night: 320,
    capacity: 2,
    bed_type: "King Size Bed",
    images: ["https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=1000&q=80"],
    features: ["Private Sea Balcony", "Italian Marble Bathroom", "Rain Shower", "Filter Coffee Bar"]
  },
  {
    id: "rm_102",
    hotel_id: "htl_001",
    hotel_name: "The Grand Coromandel Bay Luxury Palace & Spa",
    room_number: "Coromandel-Penthouse",
    room_type: "Presidential Bayview Penthouse",
    price_per_night: 750,
    capacity: 4,
    bed_type: "2 King Beds + Lounge",
    images: ["https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=1000&q=80"],
    features: ["Private Rooftop Jacuzzi", "Panoramic 360 Bay View", "Dedicated Butler", "Dravidian Teak Carvings"]
  },
  {
    id: "rm_201",
    hotel_id: "htl_002",
    hotel_name: "The Savoy Nilgiri Mist Heritage Retreat",
    room_number: "Nilgiri-201",
    room_type: "Colonial Heritage Fireplace Suite",
    price_per_night: 280,
    capacity: 2,
    bed_type: "Four-Poster Royal King Bed",
    images: ["https://images.unsplash.com/photo-1591088398332-8a7791972843?auto=format&fit=crop&w=1000&q=80"],
    features: ["Original Stone Fireplace", "Tea Garden Verandah", "Clawfoot Soaking Tub", "Organic Nilgiri Tea"]
  },
  {
    id: "rm_301",
    hotel_id: "htl_003",
    hotel_name: "Tamara Pine & Mist Lake Sanctuary",
    room_number: "Tamara-301",
    room_type: "Pine Valley Panoramic Suite",
    price_per_night: 310,
    capacity: 2,
    bed_type: "Custom Ergonomic King",
    images: ["https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=1000&q=80"],
    features: ["Floor-to-Ceiling Valley Windows", "Private Pine Deck", "Smart Climate Automation"]
  },
  {
    id: "rm_401",
    hotel_id: "htl_004",
    hotel_name: "The Heritage Madurai Royal Sanctuary & Gardens",
    room_number: "Pandyan-401",
    room_type: "Pandyan Royal Courtyard Villa",
    price_per_night: 340,
    capacity: 3,
    bed_type: "1 King Bed + 1 Daybed",
    images: ["https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=1000&q=80"],
    features: ["Private Plunge Pool", "Open Sky Shower & Courtyard", "Brass Artifacts & Teak Columns"]
  },
  {
    id: "rm_501",
    hotel_id: "htl_005",
    hotel_name: "Shore Temple Bayview Heritage Eco-Resort",
    room_number: "Shore-501",
    room_type: "Coromandel Shore Villa",
    price_per_night: 360,
    capacity: 2,
    bed_type: "Handcrafted Teak King Bed",
    images: ["https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1000&q=80"],
    features: ["Direct Beach Access", "Private Sun Deck", "Outdoor Rain Bath", "Catamaran Sailing"]
  }
];

// Initialize on document ready
document.addEventListener("DOMContentLoaded", () => {
  Theme.init();
  Auth.updateNav();
});
