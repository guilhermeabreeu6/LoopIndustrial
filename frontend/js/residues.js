redirectIfNotAuthenticated();

const residueForm = document.getElementById("residueForm");
const residueFormMessage = document.getElementById("residueFormMessage");
const myResiduesMessage = document.getElementById("myResiduesMessage");
const myResiduesList = document.getElementById("myResiduesList");
const refreshResiduesButton = document.getElementById("refreshResiduesButton");

const myResiduesCount = document.getElementById("myResiduesCount");
const availableCount = document.getElementById("availableCount");
const closedCount = document.getElementById("closedCount");

function showResidueFormMessage(message, type = "success") {
    if (!residueFormMessage) return;

    residueFormMessage.textContent = message;
    residueFormMessage.className = `message ${type}`;
}

function showMyResiduesMessage(message, type = "success") {
    if (!myResiduesMessage) return;

    myResiduesMessage.textContent = message;
    myResiduesMessage.className = `message ${type}`;
}

function setText(element, value) {
    if (element) {
        element.textContent = value;
    }
}

function updateResidueCounters(residues) {
    const available = residues.filter((residue) => residue.status === "available").length;
    const closed = residues.filter((residue) => {
        return residue.status === "reserved" || residue.status === "sold";
    }).length;

    setText(myResiduesCount, residues.length);
    setText(availableCount, available);
    setText(closedCount, closed);
}

function getStatusLabel(status) {
    const labels = {
        available: "Disponível",
        reserved: "Reservado",
        sold: "Vendido",
        inactive: "Inativo"
    };

    return labels[status] || status;
}

function renderMyResidues(residues) {
    myResiduesList.innerHTML = "";

    updateResidueCounters(residues);

    if (!residues.length) {
        myResiduesList.innerHTML = `
            <article class="card">
                <h3>Nenhum resíduo cadastrado</h3>
                <p style="color: var(--muted); margin-top: 8px;">
                    Cadastre seu primeiro material para aparecer no marketplace.
                </p>
            </article>
        `;
        return;
    }

    residues.forEach((residue) => {
        const card = document.createElement("article");
        card.className = "card residue-card";

        card.innerHTML = `
            <h3>${residue.title}</h3>

            <p>${residue.description || "Sem descrição informada."}</p>

            <div class="meta">
                <span class="pill">${residue.material_type}</span>
                <span class="pill">${residue.quantity} ${residue.unit}</span>
                <span class="pill">${residue.city} - ${residue.state}</span>
                <span class="pill">${getStatusLabel(residue.status)}</span>
            </div>

            <p>
                <strong>ID:</strong> ${residue.id}<br />
                <strong>Publicado por:</strong> ${residue.company?.company_name || "Sua empresa"}
            </p>
        `;

        myResiduesList.appendChild(card);
    });
}

async function loadMyResidues() {
    try {
        showMyResiduesMessage("Carregando seus resíduos...");

        const residues = await apiRequest("/residues/my-residues");

        renderMyResidues(residues);
        showMyResiduesMessage(`${residues.length} resíduo(s) cadastrado(s).`);
    } catch (error) {
        showMyResiduesMessage(error.message, "error");

        if (error.message.includes("Could not validate credentials")) {
            removeToken();
            window.location.href = "./login.html";
        }
    }
}

async function createResidue(event) {
    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const materialType = document.getElementById("materialType").value.trim();
    const quantity = Number(document.getElementById("quantity").value);
    const unit = document.getElementById("unit").value.trim();
    const city = document.getElementById("city").value.trim();
    const state = document.getElementById("state").value.trim().toUpperCase();

    showResidueFormMessage("Cadastrando resíduo...");

    try {
        await apiRequest("/residues", {
            method: "POST",
            body: JSON.stringify({
                title,
                description: description || null,
                material_type: materialType,
                quantity,
                unit,
                city,
                state
            })
        });

        showResidueFormMessage("Resíduo cadastrado com sucesso.", "success");

        residueForm.reset();

        await loadMyResidues();
    } catch (error) {
        showResidueFormMessage(error.message, "error");
    }
}

if (residueForm) {
    residueForm.addEventListener("submit", createResidue);
}

if (refreshResiduesButton) {
    refreshResiduesButton.addEventListener("click", loadMyResidues);
}

loadMyResidues();