redirectIfNotAuthenticated();

const transactionsMessage = document.getElementById("transactionsMessage");
const refreshTransactionsButton = document.getElementById("refreshTransactionsButton");

const totalTransactions = document.getElementById("totalTransactions");
const salesTransactions = document.getElementById("salesTransactions");
const purchaseTransactions = document.getElementById("purchaseTransactions");

const salesList = document.getElementById("salesList");
const purchasesList = document.getElementById("purchasesList");

function showTransactionsMessage(message, type = "success") {
    if (!transactionsMessage) return;

    transactionsMessage.textContent = message;
    transactionsMessage.className = `message ${type}`;
}

function setText(element, value) {
    if (element) {
        element.textContent = value;
    }
}

function formatDate(dateString) {
    if (!dateString) return "Data não informada";

    const date = new Date(dateString);

    return date.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}

function renderEmptyState(container, title, description) {
    container.innerHTML = `
        <article class="card" style="box-shadow: none;">
            <h3>${title}</h3>
            <p style="color: var(--muted); margin-top: 8px;">
                ${description}
            </p>
        </article>
    `;
}

function renderTransactionCard(transaction, type) {
    const residue = transaction.residue;
    const seller = transaction.seller_company;
    const buyer = transaction.buyer_company;

    const mainCompany = type === "sale" ? buyer : seller;
    const companyLabel = type === "sale" ? "Comprador" : "Vendedor";

    const card = document.createElement("article");
    card.className = "card residue-card";
    card.style.boxShadow = "none";

    card.innerHTML = `
        <h3>${residue?.title || "Resíduo não informado"}</h3>

        <p>
            <strong>${companyLabel}:</strong> ${mainCompany?.company_name || "Empresa não informada"}<br />
            <strong>E-mail:</strong> ${mainCompany?.email || "Não informado"}<br />
            <strong>Setor:</strong> ${mainCompany?.industry || "Não informado"}
        </p>

        <div class="meta">
            <span class="pill">${transaction.material_type}</span>
            <span class="pill">${transaction.quantity} ${transaction.unit}</span>
            <span class="pill">${transaction.status}</span>
        </div>

        <p>
            <strong>Finalizada em:</strong><br />
            ${formatDate(transaction.completed_at)}
        </p>

        <p>
            <strong>Observações:</strong><br />
            ${transaction.final_notes || "Sem observações finais."}
        </p>
    `;

    return card;
}

function renderTransactions(sales, purchases) {
    salesList.innerHTML = "";
    purchasesList.innerHTML = "";

    setText(totalTransactions, sales.length + purchases.length);
    setText(salesTransactions, sales.length);
    setText(purchaseTransactions, purchases.length);

    if (!sales.length) {
        renderEmptyState(
            salesList,
            "Nenhuma venda concluída",
            "Quando sua empresa finalizar uma negociação como dona do resíduo, ela aparecerá aqui."
        );
    } else {
        sales.forEach((transaction) => {
            salesList.appendChild(renderTransactionCard(transaction, "sale"));
        });
    }

    if (!purchases.length) {
        renderEmptyState(
            purchasesList,
            "Nenhuma compra concluída",
            "Quando sua empresa concluir uma negociação como interessada, ela aparecerá aqui."
        );
    } else {
        purchases.forEach((transaction) => {
            purchasesList.appendChild(renderTransactionCard(transaction, "purchase"));
        });
    }
}

async function loadTransactions() {
    try {
        showTransactionsMessage("Carregando transações...");

        const [sales, purchases] = await Promise.all([
            apiRequest("/transactions/sales"),
            apiRequest("/transactions/purchases")
        ]);

        renderTransactions(sales, purchases);

        showTransactionsMessage(
            `Transações carregadas. Vendas: ${sales.length} | Compras: ${purchases.length}`,
            "success"
        );
    } catch (error) {
        showTransactionsMessage(error.message, "error");

        if (error.message.includes("Could not validate credentials")) {
            removeToken();
            window.location.href = "./login.html";
        }
    }
}

if (refreshTransactionsButton) {
    refreshTransactionsButton.addEventListener("click", loadTransactions);
}

loadTransactions();