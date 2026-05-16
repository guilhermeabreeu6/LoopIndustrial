const residuesList = document.getElementById("residuesList");
const marketplaceMessage = document.getElementById("marketplaceMessage");
const filterForm = document.getElementById("filterForm");
const clearFiltersButton = document.getElementById("clearFiltersButton");

function showMarketplaceMessage(message, type = "success") {
    if (!marketplaceMessage) return;

    marketplaceMessage.textContent = message;
    marketplaceMessage.className = `message ${type}`;
}

function buildQueryParams() {
    const search = document.getElementById("search").value.trim();
    const materialType = document.getElementById("materialType").value.trim();
    const city = document.getElementById("city").value.trim();
    const state = document.getElementById("state").value.trim().toUpperCase();
    const minQuantity = document.getElementById("minQuantity").value;

    const params = new URLSearchParams();

    if (search) params.append("search", search);
    if (materialType) params.append("material_type", materialType);
    if (city) params.append("city", city);
    if (state) params.append("state", state);
    if (minQuantity) params.append("min_quantity", minQuantity);

    return params.toString();
}

function renderResidues(residues) {
    residuesList.innerHTML = "";

    if (!residues.length) {
        residuesList.innerHTML = `
            <article class="card">
                <h3>Nenhum resíduo encontrado</h3>
                <p style="color: var(--muted); margin-top: 8px;">
                    Tente ajustar os filtros ou buscar por outro material.
                </p>
            </article>
        `;
        return;
    }

    residues.forEach((residue) => {
        const companyName = residue.company?.company_name || "Empresa não informada";
        const companyIndustry = residue.company?.industry || "Setor não informado";

        const card = document.createElement("article");
        card.className = "card residue-card";

        card.innerHTML = `
            <h3>${residue.title}</h3>

            <p>${residue.description || "Sem descrição informada."}</p>

            <div class="meta">
                <span class="pill">${residue.material_type}</span>
                <span class="pill">${residue.quantity} ${residue.unit}</span>
                <span class="pill">${residue.city} - ${residue.state}</span>
                <span class="pill">${residue.status}</span>
            </div>

            <p>
                <strong>Empresa:</strong> ${companyName}<br />
                <strong>Setor:</strong> ${companyIndustry}
            </p>

            <div class="actions">
                <button class="btn btn-primary" onclick="createInterest(${residue.id})">
                    Tenho interesse
                </button>
            </div>
        `;

        residuesList.appendChild(card);
    });
}

async function loadResidues() {
    try {
        showMarketplaceMessage("Carregando resíduos disponíveis...");

        const queryParams = buildQueryParams();
        const endpoint = queryParams ? `/residues?${queryParams}` : "/residues";

        const residues = await apiRequest(endpoint);

        renderResidues(residues);
        showMarketplaceMessage(`${residues.length} resíduo(s) encontrado(s).`);
    } catch (error) {
        showMarketplaceMessage(error.message, "error");
    }
}

async function createInterest(residueId) {
    if (!isAuthenticated()) {
        window.location.href = "./login.html";
        return;
    }

    const message = prompt("Digite uma mensagem para a empresa dona do resíduo:");

    if (message === null) {
        return;
    }

    try {
        await apiRequest(`/interests/residues/${residueId}`, {
            method: "POST",
            body: JSON.stringify({
                message: message.trim() || "We are interested in this residue."
            })
        });

        showMarketplaceMessage("Interesse enviado com sucesso.", "success");
    } catch (error) {
        showMarketplaceMessage(error.message, "error");
    }
}

if (filterForm) {
    filterForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await loadResidues();
    });
}

if (clearFiltersButton) {
    clearFiltersButton.addEventListener("click", async () => {
        document.getElementById("search").value = "";
        document.getElementById("materialType").value = "";
        document.getElementById("city").value = "";
        document.getElementById("state").value = "";
        document.getElementById("minQuantity").value = "";

        await loadResidues();
    });
}

loadResidues();