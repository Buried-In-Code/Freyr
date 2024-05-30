function appendToContent(content) {
  document.getElementById("content").insertAdjacentHTML("beforeend", content);
}

function createNoContent() {
  const noContent = `
    <div class="column is-7">
      <div class="box has-text-centered" id="no-content">
        <h3 class="subtitle has-text-danger">No Devices</h3>
      </div>
    </div>`;
  appendToContent(noContent);
}

function statEntry(id, value) {
  return `<h4 class="title is-4 has-text-centered has-text-info metric" id="${id}">${value}</h4>`;
}

function createColumn(name) {
  const timeEntry = `<p class="has-text-centered is-pulled-right" id="${name}-time">{time}</p>`;
  const tempEntry = statEntry(`${name}-temp`, "{temp}");
  const humidEntry = statEntry(`${name}-humid`, "{humid}");

  const newColumn = `
    <div class="column is-7">
      <div class="box has-text-centered" id="${name}">
        <div class="columns is-mobile is-multiline">
          <div class="column is-half">
            <h3 class="subtitle is-3 is-pulled-left">${name}</h3>
          </div>
          <div class="column is-half">${timeEntry}</div>
          <div class="column is-half">${tempEntry}</div>
          <div class="column is-half">${humidEntry}</div>
        </div>
      </div>
    </div>`;
  appendToContent(newColumn);
}

function updateColumn(name, reading) {
  const timeLabel = document.getElementById(`${name}-time`);
  timeLabel.textContent = moment(reading.timestamp, "YYYY-MM-DD[T]hh:mm:ss").fromNow();

  const tempLabel = document.getElementById(`${name}-temp`);
  tempLabel.textContent = `${reading.temperature}°C`;

  const humidLabel = document.getElementById(`${name}-humid`);
  humidLabel.textContent = `${reading.humidity}%`;
}

async function getCurrentReadings() {
  let response = await submitRequest("/api/devices", "GET");
  if (!response || response.length === 0) {
    createNoContent();
    return;
  }

  const noContent = document.getElementById("no-content");
  if (noContent != null)
    noContent.remove();

  for (const device of response) {
    let reading = await submitRequest(`/api/devices/${device.id}/readings?limit=1`, "GET");
    reading = reading ? reading[0] || null : null;

    if (reading !== null) {
      if (document.getElementById(device.name) == null)
        createColumn(device.name);
      updateColumn(device.name, reading);
    } else
      createNoContent();
  }
}
