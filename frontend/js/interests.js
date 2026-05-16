redirectIfNotAuthenticated();

const interestsMessage = document.getElementById("interestsMessage");
const receivedInterestsList = document.getElementById("receivedInterestsList");
const sentInterestsList = document.getElementById("sentInterestsList");
const refreshInterestsButton = document.getElementById("refreshInterestsButton");

function showInterestsMessage(message, type = "success") {
    if (!interestsMessage) return;

    interestsMessage.textContent = message;
    interestsMessage.className = `message ${type}`;
}

function getStatusLabel(status) {
    const labels = {
        pending: "Pendente",
        accepted: "Aceito",
        rejected: "Rejeitado",
        cancelled: "Cancelado",
        completed: "Concluído"
    };

    return labels[status] || status;
}

function getResidueInfo(interest) {
    if (!interest.residue) {
        return {
            title: "Resíduo não informado",
            material: "-",
            quantity: "-",
            location: "-"
        };
    }

    return {
        title: interest.residue.title,
        material: interest.residue.material_type,
        quantity: `${interest.residue.quantity} ${interest.residue.unit}`,
        location: `${interest.residue.city} - ${interest.residue.state}`,
        status: interest.residue.status
    };
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

function renderReceivedInterests(interests) {
    receivedInterestsList.innerHTML = "";

    if (!interests.length) {
        renderEmptyState(
            receivedInterestsList,
            "Nenhum interesse recebido",
            "Quando outra empresa demonstrar interesse em seus resíduos, aparecerá aqui."
        );
        return;
    }

    interests.forEach((interest) => {
        const residue = getResidueInfo(interest);
        const company = interest.interested_company;

        const card = document.createElement("article");
        card.className = "card residue-card";
        card.style.boxShadow = "none";

        const canAcceptOrReject = interest.status === "pending";
        const canComplete = interest.status === "accepted";

        card.innerHTML = `
            <h3>${residue.title}</h3>

            <p>
                <strong>Empresa interessada:</strong> ${company?.company_name || "Não informada"}<br />
                <strong>E-mail:</strong> ${company?.email || "Não informado"}<br />
                <strong>Setor:</strong> ${company?.industry || "Não informado"}
            </p>

            <div class="meta">
                <span class="pill">${residue.material}</span>
                <span class="pill">${residue.quantity}</span>
                <span class="pill">${residue.location}</span>
                <span class="pill">${getStatusLabel(interest.status)}</span>
            </div>

            <p>
                <strong>Mensagem:</strong><br />
                ${interest.message || "Sem mensagem enviada."}
            </p>

            <div class="actions">
                ${
                    canAcceptOrReject
                        ? `
                            <button class="btn btn-primary" onclick="updateInterestStatus(${interest.id}, 'accepted')">
                                Aceitar
                            </button>

                            <button class="btn btn-secondary" onclick="updateInterestStatus(${interest.id}, 'rejected')">
                                Rejeitar
                            </button>
                        `
                        : ""
                }

                ${
                    canComplete
                        ? `
                            <button class="btn btn-primary" onclick="completeInterest(${interest.id})">
                                Finalizar negociação
                            </button>
                        `
                        : ""
                }
            </div>
        `;

        receivedInterestsList.appendChild(card);
    });
}

function renderSentInterests(interests) {
    sentInterestsList.innerHTML = "";

    if (!interests.length) {
        renderEmptyState(
            sentInterestsList,
            "Nenhum interesse enviado",
            "Quando você demonstrar interesse em resíduos do marketplace, aparecerá aqui."
        );
        return;
    }

    interests.forEach((interest) => {
        const residue = getResidueInfo(interest);
        const company = interest.owner_company;

        const card = document.createElement("article");
        card.className = "card residue-card";
        card.style.boxShadow = "none";

        const canCancel = interest.status === "pending";

        card.innerHTML = `
            <h3>${residue.title}</h3>

            <p>
                <strong>Empresa dona:</strong> ${company?.company_name || "Não informada"}<br />
                <strong>E-mail:</strong> ${company?.email || "Não informado"}<br />
                <strong>Setor:</strong> ${company?.industry || "Não informado"}
            </p>

            <div class="meta">
                <span class="pill">${residue.material}</span>
                <span class="pill">${residue.quantity}</span>
                <span class="pill">${residue.location}</span>
                <span class="pill">${getStatusLabel(interest.status)}</span>
            </div>

            <p>
                <strong>Sua mensagem:</strong><br />
                ${interest.message || "Sem mensagem enviada."}
            </p>

            <div class="actions">
                ${
                    canCancel
                        ? `
                            <button class="btn btn-secondary" onclick="updateInterestStatus(${interest.id}, 'cancelled')">
                                Cancelar interesse
                            </button>
                        `
                        : ""
                }
            </div>
        `;

        sentInterestsList.appendChild(card);
    });
}

async function loadInterests() {
    try {
        showInterestsMessage("Carregando interesses...");

        const [receivedInterests, sentInterests] = await Promise.all([
            apiRequest("/interests/received"),
            apiRequest("/interests/sent")
        ]);

        renderReceivedInterests(receivedInterests);
        renderSentInterests(sentInterests);

        showInterestsMessage("Interesses carregados com sucesso.");
    } catch (error) {
        showInterestsMessage(error.message, "error");

        if (error.message.includes("Could not validate credentials")) {
            removeToken();
            window.location.href = "./login.html";
        }
    }
}

async function updateInterestStatus(interestId, status) {
    const confirmationMessages = {
        accepted: "Tem certeza que deseja aceitar este interesse? O resíduo será reservado.",
        rejected: "Tem certeza que deseja rejeitar este interesse?",
        cancelled: "Tem certeza que deseja cancelar este interesse?"
    };

    const shouldContinue = confirm(confirmationMessages[status] || "Confirmar ação?");

    if (!shouldContinue) return;

    try {
        showInterestsMessage("Atualizando interesse...");

        await apiRequest(`/interests/${interestId}/status`, {
            method: "PATCH",
            body: JSON.stringify({
                status
            })
        });

        showInterestsMessage("Interesse atualizado com sucesso.");
        await loadInterests();
    } catch (error) {
        showInterestsMessage(error.message, "error");
    }
}

async function completeInterest(interestId) {
    const finalNotes = prompt("Observações finais da negociação:");

    if (finalNotes === null) {
        return;
    }

    try {
        showInterestsMessage("Finalizando negociação...");

        await apiRequest(`/interests/${interestId}/complete`, {
            method: "PATCH",
            body: JSON.stringify({
                final_notes: finalNotes.trim() || "Negotiation completed successfully."
            })
        });

        showInterestsMessage("Negociação finalizada com sucesso.");
        await loadInterests();
    } catch (error) {
        showInterestsMessage(error.message, "error");
    }
}

if (refreshInterestsButton) {
    refreshInterestsButton.addEventListener("click", loadInterests);
}

loadInterests();