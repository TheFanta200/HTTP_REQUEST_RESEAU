document.addEventListener('DOMContentLoaded', () => {
    // Fonction pour mettre à jour le sommaire
    const updateSummary = () => {
        const resultsContainer = document.querySelector('.results-container');
        const summaryContainer = document.getElementById('summary-container');

        if (resultsContainer && summaryContainer) {
            let errorCount = 0; // Compteur d'erreurs
            let errorDevices = []; // Liste des IP des équipements en erreur

            // Parcourir toutes les cartes pour vérifier les erreurs
            resultsContainer.querySelectorAll('.device-card').forEach(card => {
                const preContent = card.querySelector('pre').innerText.trim();
                const deviceIP = card.querySelector('.device-header h2').innerText.trim();

                // Vérifie si le contenu contient des mots-clés d'erreur
                if (preContent.match(/ERROR|Error|Erreur:|Invalid|Bad command|Échec connexion|% Incomplete command|% Invalid input/)) { 
                    card.classList.add('error');
                    card.classList.remove('success');
                    errorCount++;
                    errorDevices.push(deviceIP);
                } else {
                    card.classList.add('success');
                    card.classList.remove('error');
                }
            });

            // Mise à jour du sommaire en fonction des erreurs détectées
            if (errorCount > 0) {
                summaryContainer.innerHTML = `
                    <p><strong>Sommaire :</strong></p>
                    <p>${errorCount} commande(s) échouée(s).</p>
                    <p>Équipements concernés :</p>
                    <ul>
                        ${errorDevices.map(ip => `<li>${ip}</li>`).join('')}
                    </ul>
                `;
            } else {
                summaryContainer.innerHTML = `
                    <p><strong>Sommaire :</strong></p>
                    <p>Toutes les commandes ont réussi.</p>
                `;
            }
        }
    };

    // Mise à jour initiale du sommaire
    updateSummary();

    // Gestion de la copie des résultats par carte
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const content = btn.closest('.device-card').querySelector('pre').innerText.trim();

            navigator.clipboard.writeText(content)
                .then(() => {
                    btn.textContent = '✅';
                    setTimeout(() => btn.textContent = '📋', 2000);
                })
                .catch(err => console.error('Erreur copie:', err));
        });
    });

    // Gestion de la copie globale des résultats
    const copyAllBtn = document.getElementById('copy-all-btn');
    copyAllBtn?.addEventListener('click', () => {
        let allText = '';

        document.querySelectorAll('.device-card pre').forEach(pre => {
            allText += pre.innerText.trim() + '\n\n';
        });

        navigator.clipboard.writeText(allText.trim())
            .then(() => {
                copyAllBtn.textContent = '✅ Copié !';
                setTimeout(() => copyAllBtn.textContent = 'Copier Tous les Résultats', 2000);
            })
            .catch(err => console.error('Erreur lors de la copie globale:', err));
    });

    // Observation des changements dynamiques dans les résultats
    const resultsContainer = document.querySelector('.results-container');
    if (resultsContainer) {
        const observer = new MutationObserver(() => updateSummary());
        observer.observe(resultsContainer, { childList: true, subtree: true });
    }
});
