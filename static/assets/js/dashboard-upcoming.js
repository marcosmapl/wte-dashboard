console.log("Script carregado corretamente.");

document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("interval-select");

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  if (select) {
    select.addEventListener("change", function () {
      const days = this.value;
      console.log("Intervalo selecionado:", days);

      fetch(`/dashboard/upcoming-bookings/?interval=${days}`, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrftoken,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Erro na requisição AJAX: " + response.status);
          }
          return response.json();
        })
        .then((data) => {
          const tbody = document.getElementById("upcoming-bookings-table");
          if (tbody) {
            console.log("Atualizando tabela:");
            tbody.innerHTML = data.html;
          }
        })
        .catch((error) => {
          console.error("Erro na requisição:", error);
        });
    });
  }
});
