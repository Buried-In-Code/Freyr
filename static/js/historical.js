function resetForm(page) {
  window.location = page;
}

function createGraph(elementId, labelList, temperatureData, humidityData) {
  var config = {
    type: "line",
    data: {
      labels: labelList,
      datasets: [
        {
          label: "Temperature",
          fill: false,
          backgroundColor: "#F00",
          borderColor: "#F00",
          data: temperatureData,
          steppedLine: false,
          yAxisID: "yTem",
        }, {
          label: "Humidity",
          fill: false,
          backgroundColor: "#00F",
          borderColor: "#00F",
          data: humidityData,
          steppedLine: false,
          yAxisID: "yHum"
        }
      ]
    },
    options: {
      plugins: {
        legend: {
          display: true
        }
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
        yTem: {
          title: {
            display: true,
            text: "Temperature (°C)"
          },
          position: "left",
        },
        yHum: {
          title: {
            display: true,
            text: "Humidity (%)"
          },
          position: "right",
        }
      }
    }
  }
  let ctx = document.getElementById(elementId);
  new Chart(ctx, config);
}

function loadYearlyReadings() {
  fetch("/api/readings/yearly", {
    method: "GET",
    headers: headers,
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((devices) => {
      devices.forEach((device) => {
        let labelList = [];
        let temperatureData = [];
        let humidityData = [];
        device.readings.forEach((reading) => {
          labelList.push(moment(reading.timestamp).format("YYYY"));
          temperatureData.push(reading.temperature);
          humidityData.push(reading.humidity);
        });
        createGraph(`${device.name}-yearly-stats`, labelList, temperatureData, humidityData);
      });
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`);
  }));
}

function loadMonthlyReadings() {
  let params = new URLSearchParams(window.location.search);
  fetch("/api/readings/monthly?" + new URLSearchParams({
    year: params.get("year") || 0,
  }), {
    method: "GET",
    headers: headers,
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((devices) => {
      devices.forEach((device) => {
        let labelList = [];
        let temperatureData = [];
        let humidityData = [];
        device.readings.forEach((reading) => {
          labelList.push(moment(reading.timestamp).format("MMM"));
          temperatureData.push(reading.temperature);
          humidityData.push(reading.humidity);
        });
        createGraph(`${device.name}-monthly-stats`, labelList, temperatureData, humidityData);
      });
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`);
  }));
}

function loadDailyReadings() {
  let params = new URLSearchParams(window.location.search);
  fetch("/api/readings/daily?" + new URLSearchParams({
    year: params.get("year") || 0,
    month: params.get("month") || 0,
  }), {
    method: "GET",
    headers: headers,
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((devices) => {
      devices.forEach((device) => {
        let labelList = [];
        let temperatureData = [];
        let humidityData = [];
        device.readings.forEach((reading) => {
          labelList.push(moment(reading.timestamp).format("Do"));
          temperatureData.push(reading.temperature);
          humidityData.push(reading.humidity);
        });
        createGraph(`${device.name}-daily-stats`, labelList, temperatureData, humidityData);
      });
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`);
  }));
}

function loadHourlyReadings() {
  let params = new URLSearchParams(window.location.search);
  fetch("/api/readings/hourly?" + new URLSearchParams({
    year: params.get("year") || 0,
    month: params.get("month") || 0,
    day: params.get("day") || 0,
  }), {
    method: "GET",
    headers: headers,
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((devices) => {
      devices.forEach((device) => {
        let labelList = [];
        let temperatureData = [];
        let humidityData = [];
        device.readings.forEach((reading) => {
          labelList.push(moment(reading.timestamp).format("hhA"));
          temperatureData.push(reading.temperature);
          humidityData.push(reading.humidity);
        });
        createGraph(`${device.name}-hourly-stats`, labelList, temperatureData, humidityData);
      });
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`);
  }));
}
