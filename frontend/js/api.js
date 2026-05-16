const API_BASE_URL = "http://127.0.0.1:8000";

function getToken() {
    return localStorage.getItem("techbridge_token");
}

function setToken(token) {
    localStorage.setItem("techbridge_token", token);
}

function removeToken() {
    localStorage.removeItem("techbridge_token");
}

function isAuthenticated() {
    return !!getToken();
}

function getAuthHeaders() {
    const token = getToken();

    return {
        "Content-Type": "application/json",
        ...(token && { "Authorization": `Bearer ${token}` })
    };
}

async function apiRequest(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            ...getAuthHeaders(),
            ...(options.headers || {})
        }
    });

    let data = null;

    try {
        data = await response.json();
    } catch (error) {
        data = null;
    }

    if (!response.ok) {
        const message = data?.detail || "Unexpected API error.";
        throw new Error(message);
    }

    return data;
}

function redirectIfNotAuthenticated() {
    if (!isAuthenticated()) {
        window.location.href = "./login.html";
    }
}

function logout() {
    removeToken();
    window.location.href = "./login.html";
}