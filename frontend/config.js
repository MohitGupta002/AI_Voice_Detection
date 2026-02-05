

// Configuration file for API settings
const CONFIG = {
  API_URL: "http://localhost:5000/predict", // change if needed
  USE_MOCK: false, // true => demo mode (no backend needed)
};

// Optional export (if you ever use Node)
if (typeof module !== "undefined" && module.exports) {
  module.exports = CONFIG;
}
