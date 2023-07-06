const unique = (arr) => [...new Set(arr)];
const headers = {
  "Accept": "application/json; charset=UTF-8",
  "Content-Type": "application/json; charset=UTF-8",
};

function ready(fn) {
  if (document.readyState !== 'loading') {
    fn();
    return;
  }
  document.addEventListener('DOMContentLoaded', fn);
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function addLoading(caller){
  let element = document.getElementById(caller);
  element.classList.add("is-loading");
}

function removeLoading(caller){
  let element = document.getElementById(caller);
  element.classList.remove("is-loading");
}

function setTheme(){
  let darkCss = document.getElementById("dark-theme");
  let lightCss = document.getElementById("light-theme");
  let theme = getCookie("theme");
  if (theme == "light"){
    darkCss.disabled = true;
    lightCss.disabled = false;
  } else {
    darkCss.disabled = false;
    lightCss.disabled = true;
  }
}

function changeTheme(){
  let currentTheme = getCookie("theme");
  let newTheme = "dark";
  if (currentTheme == "dark")
    newTheme = "light";

  document.cookie = `theme=${newTheme};path=/;max-age=${60*60*24*30};SameSite=Strict`;
  setTheme();
}

function createGraph(elementId, data) {
  val tData = [];
  val hData = [];
  data.forEach((entry) => {
    tData.push({
      x: entry.timestamp,
      y: entry.temperature,
    });
    hData.push({
      x: entry.timestamp,
      y: entry.humidity,
    });
  });

  var config = {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "Temperature",
          backgroundColor: "#F00",
          borderColor: "#F00",
          data: tData,
          fill: false,
          yAxisID: "yTem"
        },
        {
          label: "Humidity",
          backgroundColor: "#00F",
          borderColor: "#00F",
          data: hData,
          fill: false,
          yAxisID: "yHum"
        }
      ]
    },
    options: {
      animation: false,
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          type: "time",
          position: "bottom"
        },
        yTem: {
          type: "linear",
          display: true,
          position: "left",
          id: "temperature-y-axis",
          scaleLabel: {
            display: true,
            labelString: "Temperature",
          },
          ticks: {
            callback: function (value, index, values) {
              return value + "°C"
            }
          }
        },
        yHum: {
          type: "linear",
          display: true,
          position: "right",
          id: "humidity-y-axis",
          grid: {
            display: false,
          },
          scaleLabel: {
            display: true,
            labelString: "Humidity",
          },
          ticks: {
            callback: function (value, index, values) {
              return value + "%"
            }
          }
        }
      }
    }
  }
  let ctx = document.getElementById(elementId);
  new Chart(ctx, config);
}

function updateCharts(){
  console.log("Updating")
  fetch("/api/stats", {
    method: "GET",
    headers: headers
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((data) => {
      createGraph("device-1", data[0].entries);
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`)
  }));
}
