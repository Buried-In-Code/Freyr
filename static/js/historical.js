function resetForm(page) {
  window.location = page;
}

function createGraph(elementId, labelList, temperatureData, humidityData) {
  var config = {
    type: "bar",
    data: {
      labels: labelList,
      datasets: [
        {
          label: "Temperature",
          backgroundColor: "rgba(255,76,76,0.2)",
          borderColor: "rgba(255,76,76,1)",
          borderWidth: 2,
          borderSkipped: false,
          data: temperatureData,
          yAxisID: "yTem",
        }, {
          label: "Humidity",
          backgroundColor: "rgba(76,76,255,0.2)",
          borderColor: "rgba(76,76,255,1)",
          borderWidth: 2,
          borderSkipped: false,
          data: humidityData,
          yAxisID: "yHum",
        }
      ]
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
        device.highs.forEach((high, index) => {
          let low = device.lows[index];
          labelList.push(moment(high.timestamp).format("YYYY"));
          temperatureData.push([high.temperature, low.temperature]);
          humidityData.push([high.humidity, low.humidity]);
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
        device.highs.forEach((high, index) => {
          let low = device.lows[index];
          labelList.push(moment(high.timestamp).format("MMM"));
          temperatureData.push([high.temperature, low.temperature]);
          humidityData.push([high.humidity, low.humidity]);
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
        device.highs.forEach((high, index) => {
          let low = device.lows[index];
          labelList.push(moment(high.timestamp).format("Do"));
          temperatureData.push([high.temperature, low.temperature]);
          humidityData.push([high.humidity, low.humidity]);
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
        device.highs.forEach((high, index) => {
          let low = device.lows[index];
          labelList.push(moment(high.timestamp).format("hhA"));
          temperatureData.push([high.temperature, low.temperature]);
          humidityData.push([high.humidity, low.humidity]);
        });
        createGraph(`${device.name}-hourly-stats`, labelList, temperatureData, humidityData);
      });
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`);
  }));
}
