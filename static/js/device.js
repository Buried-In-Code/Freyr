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

function createGraph(elementId, labels, datasets) {
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
        yTem: createScaleConfig("Temperature (°C)", "left"),
        yHum: createScaleConfig("Humidity (%)", "right"),
      }
    }
  };

  new Chart(document.getElementById(elementId), config);
}

async function loadReadings(device_id, timeframe, timeFormat, params = {}) {
  const response = await submitRequest(`/api/devices/${device_id}/readings/${timeframe}?${new URLSearchParams(params)}`, "GET");
  if (!response)
    return;

  addLoading(`${timeframe}-stats`);
  const labels = [];
  const datasets = [];

  const tempRange = [];
  const tempAverage = [];
  const humidRange = [];
  const humidAverage = [];

  for (const [index, high] of response.highs.entries()) {
    const avg = response.averages[index];
    const low = response.lows[index];

    labels.push(moment(high.timestamp).format(timeFormat));
    tempRange.push([high.temperature, low.temperature]);
    tempAverage.push(avg.temperature);
    humidRange.push([high.humidity, low.humidity]);
    humidAverage.push(avg.humidity);
  }

  datasets.push(createDataset(0, tempRange, "Temperature (High/Low)", "bar", "yTem"));
  datasets.push(createDataset(1, tempAverage, "Temperature (Avg)", "line", "yTem"));
  datasets.push(createDataset(2, humidRange, "Humidity (High/Low)", "bar", "yHum"));
  datasets.push(createDataset(3, humidAverage, "Humidity (Avg)", "line", "yHum"));

  createGraph(`${timeframe}-stats`, labels, datasets);
  removeLoading(`${timeframe}-stats`);
}

function loadYearlyReadings(device_id) {
  loadReadings(device_id, "yearly", "YYYY");
  toggleChartLoading("yearly-stats");
}

function loadMonthlyReadings(device_id) {
  const currentParams = new URLSearchParams(window.location.search);
  const params = {
    year: currentParams.get("year") || 0,
  };
  loadReadings(device_id, "monthly", "MMM", params);
  toggleChartLoading("monthly-stats");
}

function loadDailyReadings(device_id) {
  const currentParams = new URLSearchParams(window.location.search);
  const params = {
    year: currentParams.get("year") || 0,
    month: currentParams.get("month") || 0,
  };
  loadReadings(device_id, "daily", "Do", params);
  toggleChartLoading("daily-stats");
}

function loadHourlyReadings(device_id) {
  const currentParams = new URLSearchParams(window.location.search);
  const params = {
    year: currentParams.get("year") || 0,
    month: currentParams.get("month") || 0,
    day: currentParams.get("day") || 0,
  };
  loadReadings(device_id, "hourly", "hhA", params);
  toggleChartLoading("hourly-stats");
}
