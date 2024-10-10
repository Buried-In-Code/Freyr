function toggleChartLoading(id) {
  const progress = document.getElementById(`${id}-loading`).parentElement;
  const chart = document.getElementById(id).parentElement;
  progress.hidden = !progress.hidden;
  chart.hidden = !chart.hidden;
}

function createDataset(index, data, label, type, yAxisID = "y") {
  const colours = [
    "rgba(255,0,0,0.5)",
    "rgba(255,215,0,0.5)",
    "rgba(0,128,0,0.5)",
    "rgba(0,191,255,0.5)",
    "rgba(128,0,128,0.5)",
    "rgba(128,128,128,0.5)",
    "rgba(160,82,45,0.5)"
  ];
  const borderColour = colours[index];
  const backgroundColour = `${borderColour.slice(0, -2)}1)`;

  return {
    backgroundColor: backgroundColour,
    borderColor: borderColour,
    borderWidth: 2,
    borderSkipped: false,
    data,
    label,
    type,
    yAxisID,
  };
}

function createScaleConfig(title, position) {
  return {
    title: {
      display: true,
      text: title
    },
    position,
    beginAtZero: false,
  };
}

function createGraph(elementId, labels, datasets, yTitle) {
  const config = {
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      interaction: {
        intersect: false,
        mode: "nearest",
      },
      plugins: {
        legend: {
          display: datasets.length > 1
        },
      },
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: "Timestamp",
          },
          position: "bottom",
        },
        y: {
          title: {
            display: true,
            text: yTitle
          },
          position: "left",
          beginAtZero: false,
        }
      }
    }
  };

  new Chart(document.getElementById(elementId), config);
}
