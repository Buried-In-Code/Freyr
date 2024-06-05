var DateTime = luxon.DateTime;

async function appendToContent(content) {
  document.getElementById("content").insertAdjacentHTML("beforeend", content);
}

function createNoContent() {
  appendToContent(`
    <div class="column is-7">
      <div class="box has-text-centered" id="no-content">
        <h3 class="subtitle has-text-danger">No Devices</h3>
      </div>
    </div>
  `);
}

function statEntry(id, value) {
  return `<h4 class="title is-4 has-text-centered has-text-info metric" id="${id}">${value}</h4>`;
}

function createColumn(name) {
  appendToContent(`
    <div class="column is-7">
      <div class="box has-text-centered" id="${name}">
        <div class="columns is-mobile is-multiline">
          <div class="column is-half">
            <h3 class="subtitle is-3 is-pulled-left">${name}</h3>
          </div>
          <div class="column is-half">
            <p class="has-text-centered is-pulled-right" id="${name}-time">{time}</p>
          </div>
          <div class="column is-one-third">${statEntry(`${name}-temperature`, "{temperature}")}</div>
          <div class="column is-one-third">${statEntry(`${name}-humidity`, "{humidity}")}</div>
          <div class="column is-one-third">${statEntry(`${name}-feels`, "{feels}")}</div>
        </div>
      </div>
    </div>
  `);
}

function calculateFeelsLike(temperature, humidity) {
  const temp = parseFloat(temperature);
  const hum = parseFloat(humidity) / 100;
  const pressure = hum * 6.105 * Math.exp((17.27 * temp) / (237.7 + temp));
  return (temp + 0.33 * pressure - 4.00);
}

function updateColumn(name, reading) {
  const timeLabel = document.getElementById(`${name}-time`);
  const temperatureLabel = document.getElementById(`${name}-temperature`);
  const humidityLabel = document.getElementById(`${name}-humidity`);
  const feelsLabel = document.getElementById(`${name}-feels`);

  const time = (reading === null || reading.timestamp === null) ? "null" : DateTime.fromISO(reading.timestamp).toRelative();
  const temperature = (reading === null || reading.temperature === null) ? "null" : parseFloat(reading.temperature).toFixed(2);
  const humidity = (reading === null || reading.humidity === null) ? "null" : parseFloat(reading.humidity).toFixed(2);
  const feelsLike = (reading === null || reading.temperature === null || reading.humidity === null) ? "null" : calculateFeelsLike(reading.temperature, reading.humidity).toFixed(2);

  timeLabel.textContent = time;
  temperatureLabel.textContent = `${temperature}°C`;
  humidityLabel.textContent = `${humidity}%`;
  feelsLabel.textContent = `${feelsLike}°C`;
}

async function getCurrentReadings() {
  const response = await submitRequest("/api/devices", "GET");
  if (!response || response.length === 0) {
    createNoContent();
    return;
  }

  const noContent = document.getElementById("no-content");
  if (noContent)
    noContent.remove();

  for (const device of response) {
    const readings = await submitRequest(`/api/devices/${device.id}/readings?limit=1`, "GET");
    const reading = readings ? readings[0] || null : null;

    if (!document.getElementById(device.name))
      createColumn(device.name);
    updateColumn(device.name, reading);
  }
}

ready(getCurrentReadings);
setInterval(getCurrentReadings, 1000 * 30); // Wait 30s
