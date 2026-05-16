redirectIfNotAuthenticated();

const companyName = document.getElementById("companyName");
const companyInfo = document.getElementById("companyInfo");
const dashboardMessage = document.getElementById("dashboardMessage");

const totalResidues = document.getElementById("totalResidues");
const availableResidues = document.getElementById("availableResidues");
const reservedResidues = document.getElementById("reservedResidues");
const soldResidues = document.getElementById("soldResidues");
const receivedInterests = document.getElementById("receivedInterests");
const sentInterests = document.getElementById("sentInterests");
const completedSales = document.getElementById("completedSales");
const completedPurchases = document.getElementById("completedPurchases");

const completedTransactions = document.getElementById("completedTransactions");
const co2Saved = document.getElementById("co2Saved");

function setText(element, value) {
    if (element) {
        element.textContent = value;
    }
}

function showDashboardMessage(message, type = "success") {
    if (!dashboardMessage) return;

    dashboardMessage.textContent = message;
    dashboardMessage.className = `message ${type}`;
}

async function loadCompanyData() {
    const company = await apiRequest("/companies/me");

    setText(companyName, company.company_name);
    setText(
        companyInfo,
        `${company.industry} • ${company.city} - ${company.state} • ${company.email}`
    );
}

async function loadDashboardSummary() {
    const summary = await apiRequest("/dashboard/summary");

    setText(totalResidues, summary.total_residues);
    setText(availableResidues, summary.available_residues);
    setText(reservedResidues, summary.reserved_residues);
    setText(soldResidues, summary.sold_residues);
    setText(receivedInterests, summary.received_interests);
    setText(sentInterests, summary.sent_interests);
    setText(completedSales, summary.completed_sales);
    setText(completedPurchases, summary.completed_purchases);
}

async function loadImpactSummary() {
    const impact = await apiRequest("/impact/summary");

    setText(completedTransactions, impact.completed_transactions);
    setText(co2Saved, impact.estimated_co2_saved_kg);
}

async function initializeDashboard() {
    try {
        showDashboardMessage("Carregando dados do painel...");

        await Promise.all([
            loadCompanyData(),
            loadDashboardSummary(),
            loadImpactSummary()
        ]);

        showDashboardMessage("Dashboard atualizado com sucesso.");
    } catch (error) {
        showDashboardMessage(error.message, "error");

        if (error.message.includes("Could not validate credentials")) {
            removeToken();
            window.location.href = "./login.html";
        }
    }
}

initializeDashboard();