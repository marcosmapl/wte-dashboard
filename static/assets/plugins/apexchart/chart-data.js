"use strict";

$(document).ready(function () {
  // Area chart

  if ($("#apexcharts-area").length > 0) {
    var options = {
      chart: {
        height: 350,
        type: "area",
        toolbar: {
          show: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        curve: "smooth",
      },
      series: [
        {
          name: "Reservado",
          color: "#27AE60",
          data: [15, 20, 5, 7, 12, 16, 6, 8, 10, 11, 13, 9],
        },
        {
          name: "Cancelado",
          color: "#C0392B",
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
          show: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
      plotOptions: {
        bar: {
          columnWidth: "45%",
        },
      },
      series: [
        {
          name: "Faturado",
          color: "#fdbb38",
          data: [
            420, 532, 516, 575, 519, 517, 454, 392, 262, 383, 446, 551, 563,
            421, 563, 254, 452,
          ],
        },
        {
          name: "Parceiros",
          color: "#19affb",
          data: [
            336, 612, 344, 647, 345, 563, 256, 344, 323, 300, 455, 456, 526,
            652, 325, 425, 436,
          ],
        },
      ],
      labels: [
        2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020,
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
