"use strict";

$(document).ready(function () {
  // Area chart

  if ($("#apexcharts-area").length > 0) {
    var options = {
      chart: {
        height: 350,
        type: "area",
        toolbar: {
          show: true,
        },
      },
      dataLabels: {
        enabled: true,
      },
      stroke: {
        curve: "smooth",
      },
      series: [
        {
          name: "Reservado",
          color: "#2196F3",
          data: [15, 20, 5, 7, 12, 16, 6, 8, 10, 11, 13, 9],
        },
        {
          name: "Cancelado",
          color: "#F44336",
          data: [4, 0, 2, 3, 1, 0, 2, 1, 3, 4, 2, 1],
        },
      ],
      xaxis: {
        categories: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
      },
    };
    var chart = new ApexCharts(
      document.querySelector("#apexcharts-area"),
      options
    );
    chart.render();
  }

  // Bar chart

  if ($("#bar").length > 0) {
    var optionsBar = {
      chart: {
        type: "bar",
        height: 350,
        width: "100%",
        stacked: true,
        toolbar: {
          show: true,
        },
      },
      dataLabels: {
        enabled: true,
      },
      plotOptions: {
        bar: {
          columnWidth: "65%",
        },
      },
      series: [
        {
          name: "Faturado",
          color: "#4CAF50",
          data: [
            420, 532, 516, 575, 519, 517, 454, 392, 262, 383, 446, 551, 563, 421, 563, 254, 452,
          ],
        },
        {
          name: "Parceiros",
          color: "#9C27B0",
          data: [
            336, 612, 344, 647, 345, 563, 256, 344, 323, 300, 455, 456, 526, 652, 325, 425, 436,
          ],
        },
      ],
      labels: [
        'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez',
      ],
      xaxis: {
        labels: {
          show: false,
        },
        axisBorder: {
          show: false,
        },
        axisTicks: {
          show: false,
        },
      },
      yaxis: {
        axisBorder: {
          show: false,
        },
        axisTicks: {
          show: false,
        },
        labels: {
          show: true,
          formatter: function (val) {
            return "$ " + val;
          },
          style: {
            colors: "#777",
          },
        },
      },
      title: {
        text: "",
        align: "left",
        style: {
          fontSize: "18px",
        },
      },
    };

    var chartBar = new ApexCharts(document.querySelector("#bar"), optionsBar);
    chartBar.render();
  }
});
