const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

const loginMessage = document.getElementById("loginMessage");
const registerMessage = document.getElementById("registerMessage");

function showMessage(element, message, type = "success") {
    if (!element) return;

    element.textContent = message;
    element.className = `message ${type}`;
}

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        showMessage(loginMessage, "Entrando...", "success");

        try {
            const data = await apiRequest("/companies/login", {
                method: "POST",
                body: JSON.stringify({
                    email,
                    password
                })
            });

            setToken(data.access_token);

            showMessage(loginMessage, "Login realizado com sucesso.", "success");

            setTimeout(() => {
                window.location.href = "./dashboard.html";
            }, 600);
        } catch (error) {
            showMessage(loginMessage, error.message, "error");
        }
    });
}

if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const companyName = document.getElementById("companyName").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();
        const city = document.getElementById("city").value.trim();
        const state = document.getElementById("state").value.trim().toUpperCase();
        const industry = document.getElementById("industry").value.trim();

        showMessage(registerMessage, "Criando conta...", "success");

        try {
            await apiRequest("/companies/register", {
                method: "POST",
                body: JSON.stringify({
                    company_name: companyName,
                    email,
                    password,
                    city,
                    state,
                    industry
                })
            });

            showMessage(registerMessage, "Conta criada com sucesso. Redirecionando para login...", "success");

            setTimeout(() => {
                window.location.href = "./login.html";
            }, 900);
        } catch (error) {
            showMessage(registerMessage, error.message, "error");
        }
    });
}