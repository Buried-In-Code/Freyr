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
  return (temp + 0.33 * pressure - 4.00).toFixed(2);
}

function updateColumn(name, reading) {
  const timeLabel = document.getElementById(`${name}-time`);
  const temperatureLabel = document.getElementById(`${name}-temperature`);
  const humidityLabel = document.getElementById(`${name}-humidity`);
  const feelsLabel = document.getElementById(`${name}-feels`);


  const temperature = reading.temperature !== null ? parseFloat(reading.temperature).toFixed(2) : "null";
  const humidity = reading.humidity !== null ? parseFloat(reading.humidity).toFixed(2) : "null";
  const feelsLike = (reading.temperature !== null && reading.humidity !== null) ? calculateFeelsLike(reading.temperature, reading.humidity) : "null";

  timeLabel.textContent = moment(reading.timestamp, "YYYY-MM-DD[T]hh:mm:ss").fromNow();
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

    if (reading) {
      if (!document.getElementById(device.name))
        createColumn(device.name);
      updateColumn(device.name, reading);
    } else
      createNoContent();
  }
}
