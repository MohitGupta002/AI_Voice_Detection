// Configuration file for API settings
const CONFIG = {
    API_URL: 'http://localhost:5000/predict', // Change this to your backend URL
    USE_MOCK: false // Set to true to use mock API for demo purposes
};

// Export for use in script.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
