document.addEventListener("DOMContentLoaded", () => {

  async function fetchAndUpdate(endpoint, interval, targetId) {
    const target = document.getElementById(targetId);
    if (!target) return;

    // Exibe indicador de carregamento
    const originalContent = target.innerHTML;
    target.innerHTML = '<div class="d-flex justify-content-center"><div class="spinner-grow text-primary" role="status"><span class="sr-only">Loading...</span></div></div>';

    try {
      const response = await fetch(`${endpoint}?interval=${interval}`);
      if (!response.ok) {
        throw new Error(`Erro na requisição AJAX: ${response.status}`);
      }

      const data = await response.json();

      if (data.html && data.html !== originalContent) {
        target.innerHTML = data.html;
      } else {
        target.innerHTML = "<p>Sem dados para exibir.</p>";
      }

    } catch (error) {
      console.error("Erro na requisição:", error);
      target.innerHTML = "<p>Erro ao carregar os dados.</p>";
    }
  }

  function setupIntervalSelect(selectId, endpoint, targetId) {
    const select = document.getElementById(selectId);
    if (!select) return;

    let lastValue = null;

    select.addEventListener("change", function () {
      const interval = this.value;
      if (interval === lastValue) return;
      lastValue = interval;

      fetchAndUpdate(endpoint, interval, targetId);
    });
  }

  // Inicialização dos seletores
  setupIntervalSelect("upcoming-interval-select", "/dashboard/upcoming-bookings/", "upcoming-bookings-table");
  setupIntervalSelect("general-count-interval-select", "/dashboard/general_count/", "general-count-monitor");

});
