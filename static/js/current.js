function statEntry(id, value) {
  return `<h4 class="has-text-centered has-text-info metric" id="${id}">${value}</h4>`
}

function createColumn(device) {
  let timeEntry = `<p class="has-text-centered is-pulled-right" id="${device}-time">{time}</p>`;
  let tempEntry = statEntry(`${device}-temp`, "{temp}")
  let humidEntry = statEntry(`${device}-humid`, "{humid}")
  let newColumn = `<div class="column is-7"><div class="box has-text-centered" id="${device}"><div class="columns is-mobile is-multiline"><div class="column is-half"><h2 class="subtitle is-pulled-left">${device}</h2></div><div class="column is-half">${timeEntry}</div><div class="column is-half">${tempEntry}</div><div class="column is-half">${humidEntry}</div></div></div></div>`;
  let columnsRoot = document.getElementById("content");
  columnsRoot.insertAdjacentHTML("beforeend", newColumn);
}

function createNoContent() {
  let noContent = `<div class="column is-7"><div class="box has-text-centered" id="no-content"><h3 class="subtitle has-text-danger">No devices</h3></div></div>`
  let columnsRoot = document.getElementById("content");
  columnsRoot.insertAdjacentHTML("beforeend", noContent);
}

function getCurrentReadings() {
  fetch("/api/readings/current", {
    method: "GET",
    headers: headers,
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((devices) => {
      let noContent = document.getElementById("no-content");
      if (devices.length > 0) {
        if (noContent != null)
          noContent.parentNode.removeChild(noContent);
        devices.forEach((device) => {
          let column = document.getElementById(device.name);
          if (column == null)
            createColumn(device.name);
          if (device.reading != null)
            updateColumn(device.name, device.reading);
        });
      } else if (noContent == null)
        createNoContent()
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`)
  }));
}

function updateColumn(device, reading){
  let timeLabel = document.getElementById(`${device}-time`);
  timeLabel.textContent = moment(reading.timestamp, "YYYY-MM-DD[T]hh:mm:ss").fromNow();
  let tempLabel = document.getElementById(`${device}-temp`);
  tempLabel.textContent = `${reading.temperature}°C`;
  let humidLabel = document.getElementById(`${device}-humid`);
  humidLabel.textContent = `${reading.humidity}%`;
}
