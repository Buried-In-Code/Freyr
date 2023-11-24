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
          display: true
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

function getBackgroundColour(index) {
  const colours = [
    "rgba(255,0,0,0.5)",
    "rgba(255,215,0,0.5)",
    "rgba(0,128,0,0.5)",
    "rgba(0,191,255,0.5)",
    "rgba(128,0,128,0.5)",
    "rgba(128,128,128,0.5)",
    "rgba(160,82,45,0.5)"
  ];
  while (index >= colours.length) {
    index = index - colours.length;
  }
  return colours[index];
}

function getBorderColour(index) {
  const colours = [
    "rgba(255,0,0,1)",
    "rgba(255,215,0,1)",
    "rgba(0,128,0,1)",
    "rgba(0,191,255,1)",
    "rgba(128,0,128,1)",
    "rgba(128,128,128,1)",
    "rgba(160,82,45,1)"
  ];
  while (index >= colours.length) {
    index = index - colours.length;
  }
  return colours[index];
}

function createDataset(index, data, label, type, yAxisID) {
  return {
    backgroundColor: getBackgroundColour(index),
    borderColor: getBorderColour(index),
    borderWidth: 2,
    borderSkipped: false,
    data: data,
    label: label,
    type: type,
    yAxisID: yAxisID,
  };
}

function createScaleConfig(title, position) {
  return {
    title: {
      display: true,
      text: title
    },
    position: position,
    beginAtZero: false,
  };
}

async function loadReadings(timeframe, timeFormat, params = {}) {
  const response = await submitRequest(`/api/readings/${timeframe}?${new URLSearchParams(params)}`, "GET");
  if (response !== null) {
    response.forEach((device) => {
      addLoading(`${device.name}-${timeframe}-stats`);
      const labels = [];
      const datasets = [];
      const temperatureHLData = [];
      const temperatureAvgData = [];
      const humidityHLData = [];
      const humidityAvgData = [];
      device.highs.forEach((high, index) => {
        const avg = device.averages[index];
        const low = device.lows[index];
        labels.push(moment(high.timestamp).format(timeFormat));
        temperatureHLData.push([high.temperature, low.temperature]);
        temperatureAvgData.push(avg.temperature);
        humidityHLData.push([high.humidity, low.humidity]);
        humidityAvgData.push(avg.humidity);
      });
      datasets.push(createDataset(datasets.length, temperatureHLData, "Temperature (High/Low)", "bar", "yTem"))
      datasets.push(createDataset(datasets.length, temperatureAvgData, "Temperature (Avg)", "line", "yTem"))
      datasets.push(createDataset(datasets.length, humidityHLData, "Humidity (High/Low)", "bar", "yHum"))
      datasets.push(createDataset(datasets.length, humidityAvgData, "Humidity (Avg)", "line", "yHum"))
      createGraph(`${device.name}-${timeframe}-stats`, labels, datasets);
      removeLoading(`${device.name}-${timeframe}-stats`);
    });
  }
}

function loadYearlyReadings() {
  loadReadings("yearly", "YYYY");
}

function loadMonthlyReadings() {
  const params = {
    year: new URLSearchParams(window.location.search).get("year") || 0,
  };
  loadReadings("monthly", "MMM", params);
}

function loadDailyReadings() {
  const params = {
    year: new URLSearchParams(window.location.search).get("year") || 0,
    month: new URLSearchParams(window.location.search).get("month") || 0,
  };
  loadReadings("daily", "Do", params);
}

function loadHourlyReadings() {
  const params = {
    year: new URLSearchParams(window.location.search).get("year") || 0,
    month: new URLSearchParams(window.location.search).get("month") || 0,
    day: new URLSearchParams(window.location.search).get("day") || 0,
  };
  loadReadings("hourly", "hhA", params);
}
