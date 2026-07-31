document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchForm = document.getElementById("search-form");
    const taskList = document.getElementById("task-list");
    const filterButtons = document.querySelectorAll(".filter");
    const countAll = document.getElementById("count-all");
    const countTodo = document.getElementById("count-todo");
    const countCompleted = document.getElementById("count-completed");

    if (!searchInput || !taskList) {
        return; // on n'est pas sur la page task_list, rien à faire
    }

    let debounceTimer;
    let currentStatus = "";

    /**
     * Demande à Django la liste des tâches à jour (recherche + filtre),
     * puis remplace le contenu de #task-list sans recharger la page.
     * Appelée par : la recherche, les clics sur les filtres, et après
     * chaque bascule de case à cocher.
     *
     * @param {string} query  - texte tapé dans la barre de recherche
     * @param {string} status - filtre actif ("", "todo" ou "completed")
     * @returns {void} - ne renvoie rien, mais met à jour l'affichage
     */
    function lancerRecherche(query, status) {
        const url = new URL(window.location.href);
        url.searchParams.set("search", query);

        if (status) {
            url.searchParams.set("status", status);
        } else {
            url.searchParams.delete("status");
        }

        fetch(url, {
            headers: { "X-Requested-With": "XMLHttpRequest" },
        })
            .then((response) => response.json())
            .then((data) => {
                taskList.innerHTML = data.html;
                if (countAll) countAll.textContent = data.all_count;
                if (countTodo) countTodo.textContent = data.todo_count;
                if (countCompleted) countCompleted.textContent = data.completed_count;
                window.history.replaceState({}, "", url);

                // Important : on vient de réinjecter du HTML dans #task-list,
                // donc les checkbox sont de nouveaux éléments DOM.
                // Il faut réattacher les écouteurs dessus.
                attacherCheckboxes();
            })
            .catch((error) => {
                console.error("Erreur lors de la recherche :", error);
            });
    }

    // Recherche à chaque frappe, avec un léger délai (debounce)
    searchInput.addEventListener("input", function () {
        clearTimeout(debounceTimer);
        const query = this.value;
        debounceTimer = setTimeout(() => lancerRecherche(query, currentStatus), 300);
    });

    // Empêche le rechargement de page si l'utilisateur appuie sur Entrée
    if (searchForm) {
        searchForm.addEventListener("submit", function (e) {
            e.preventDefault();
            clearTimeout(debounceTimer);
            lancerRecherche(searchInput.value, currentStatus);
        });
    }

    // Clic sur un des 3 boutons de filtre
    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            currentStatus = this.dataset.status; // "", "todo" ou "completed"

            filterButtons.forEach(function (b) {
                b.classList.remove("active");
            });
            this.classList.add("active");

            lancerRecherche(searchInput.value, currentStatus);
        });
    });

    // ---------------------------------------------------------
    // Gestion du (dé)cochage d'une tâche
    // ---------------------------------------------------------

    /**
     * Lit le jeton CSRF caché dans la page (généré par {% csrf_token %}),
     * nécessaire pour que Django accepte une requête POST.
     *
     * @param {} aucun paramètre
     * @returns {string|null} - le jeton CSRF, ou null s'il est introuvable
     */
    function getCsrfToken() {
        const input = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return input ? input.value : null;
    }

    /**
     * Envoie à Django la demande de bascule (coché <-> décoché) pour une
     * tâche précise, puis rafraîchit la liste si ça a réussi, ou annule
     * visuellement le clic si ça a échoué.
     *
     * @param {string} taskId - identifiant de la tâche concernée
     * @param {HTMLElement} checkboxEl - la case à cocher cliquée
     * @returns {void} - ne renvoie rien, mais déclenche un rafraîchissement de l'affichage
     */
    function basculerTache(taskId, checkboxEl) {
        const csrfToken = getCsrfToken();
        const toggleUrl = checkboxEl.dataset.toggleUrl;

        fetch(toggleUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    lancerRecherche(searchInput.value, currentStatus);
                } else {
                    checkboxEl.checked = !checkboxEl.checked;
                }
            })
            .catch((error) => {
                console.error("Erreur lors du changement de statut :", error);
                checkboxEl.checked = !checkboxEl.checked;
            });
    }

    /**
     * Pose un écouteur "change" sur chaque case à cocher présente dans
     * la page à cet instant, pour déclencher basculerTache() dès qu'une
     * case est cochée ou décochée. À rappeler après chaque réécriture
     * du HTML de #task-list, sinon les nouvelles cases ne sont pas surveillées.
     *
     * @param {} aucun paramètre
     * @returns {void} - ne renvoie rien, attache seulement les écouteurs
     */
    function attacherCheckboxes() {
        document.querySelectorAll(".task-checkbox input[type='checkbox']").forEach((checkbox) => {
            checkbox.addEventListener("change", function () {
                const taskId = this.dataset.taskId;
                basculerTache(taskId, this);
            });
        });
    }

    // Premier attachement au chargement initial de la page
    attacherCheckboxes();
});