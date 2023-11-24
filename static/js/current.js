function statEntry(id, value) {
  return `<h1 class="title is-1 has-text-centered has-text-info metric" id="${id}">${value}</h4>`;
}

function createColumn(device) {
  const timeEntry = `<p class="has-text-centered is-pulled-right" id="${device}-time">{time}</p>`;
  const tempEntry = statEntry(`${device}-temp`, "{temp}");
  const humidEntry = statEntry(`${device}-humid`, "{humid}");
  const newColumn = `<div class="column is-7"><div class="box has-text-centered" id="${device}"><div class="columns is-mobile is-multiline"><div class="column is-half"><h3 class="subtitle is-3 is-pulled-left">${device}</h2></div><div class="column is-half">${timeEntry}</div><div class="column is-half">${tempEntry}</div><div class="column is-half">${humidEntry}</div></div></div></div>`;
  document.getElementById("content").insertAdjacentHTML("beforeend", newColumn);
}

function createNoContent() {
  const noContent = `<div class="column is-7"><div class="box has-text-centered" id="no-content"><h3 class="subtitle has-text-danger">No devices</h3></div></div>`;
  document.getElementById("content").insertAdjacentHTML("beforeend", noContent);
}

async function getCurrentReadings() {
  const response = await submitRequest("/api/readings/current", "GET");
  if (response !== null) {
    const noContent = document.getElementById("no-content");
    if (response.length > 0) {
      if (noContent != null)
        noContent.remove();
      response.forEach((device) => {
        if (document.getElementById(device.name) == null)
          createColumn(device.name);
        if (device.readings.length > 0)
          updateColumn(device.name, device.readings[0]);
      });
    } else if (noContent == null) {
      createNoContent();
    }
  }
}

function updateColumn(device, reading) {
  const timeLabel = document.getElementById(`${device}-time`);
  timeLabel.textContent = moment(reading.timestamp, "YYYY-MM-DD[T]hh:mm:ss").fromNow();
  const tempLabel = document.getElementById(`${device}-temp`);
  tempLabel.textContent = `${reading.temperature}°C`;
  const humidLabel = document.getElementById(`${device}-humid`);
  humidLabel.textContent = `${reading.humidity}%`;
}
